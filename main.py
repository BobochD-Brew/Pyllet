#----X  ___                                                 ___                         
#      /\  \                                               /\__\                        
#     /::\  \       ___                                   /:/ _/_         ___           
#    /:/\:\__\     /|  |                                 /:/ /\__\       /\__\          
#   /:/ /:/  /    |:|  |    ___     ___   ___     ___   /:/ /:/ _/_     /:/  /          
#  /:/_/:/  /     |:|  |   /\  \   /\__\ /\  \   /\__\ /:/_/:/ /\__\   /:/__/           
#  \:\/:/  /    __|:|__|   \:\  \ /:/  / \:\  \ /:/  / \:\/:/ /:/  /  /::\  \           
#   \::/__/    /::::\  \    \:\  /:/  /   \:\  /:/  /   \::/_/:/  /  /:/\:\  \          
#    \:\  \    ~~~~\:\  \    \:\/:/  /     \:\/:/  /     \:\/:/  /   \/__\:\  \         
#     \:\__\        \:\__\    \::/  /       \::/  /       \::/  /         \:\__\        
#      \/__/         \/__/     \/__/         \/__/         \/__/           \/__/   
#        
#----X Pyllet : Bitcon python wallet

#----------------------------X
#          Imports           |
#----------------------------X

import hashlib
import hmac
from ecdsa import SigningKey, SECP256k1
from base58 import b58encode, b58encode_check
from secrets import token_bytes
from os import path,system
import qrcode
import sys

#----------------------------X
#        Setup data          |
#----------------------------X

walletData = {}
selectedWalletData = {}
bip39Dic = []

#----------------------------X
#    ECDSA Transformation    |
#----------------------------X

def keyToWalletData(Pkey):
    signingKey = SigningKey.from_string(Pkey, curve = SECP256k1)
    verifyingKey = signingKey.get_verifying_key()
    publicKey = b'\x04'+verifyingKey.to_string()
    if (publicKey[-1] % 2 == 0):
        publicKeyCompressedPrefix = b'\x02'
    else:
        publicKeyCompressedPrefix = b'\x03'
    publicKeyCompressed = publicKeyCompressedPrefix + publicKey[1:33]
    hashedPublicKeySha256 = hashlib.sha256(publicKeyCompressed).digest()
    hashedPublicKeyRipemd160 = hashlib.new("ripemd160")
    hashedPublicKeyRipemd160.update(hashedPublicKeySha256)
    hashedPublicKey = bytes.fromhex("00") + hashedPublicKeyRipemd160.digest()
    checksum = hashlib.sha256(hashlib.sha256(hashedPublicKey).digest()).digest()[:4]
    publicAddress = b58encode(hashedPublicKey + checksum)
    return {
        "privateKey": Pkey,
        "encodedPrivateKey":  b58encode_check(b'\x80' +Pkey+hashlib.sha256(Pkey).digest()[:1]),
        "signingKey":  signingKey,
        "verifyingKey":  verifyingKey,
        "publicKey":  publicKey,
        "publicCompressedKey":  publicKeyCompressed,
        "publicAddress":  publicAddress,
        "fingerprint": hashedPublicKeyRipemd160.digest()[:4]
    }

#----------------------------X
#    Misc Utils Functions    |
#----------------------------X

def toCleanInt(x):
    return int.from_bytes(x,"big")

def toEcdsaRange(x):
    return x%115792089237316195423570985008687907852837564279074904382605163141518161494337

#----------------------------X
#        BIP32 - CKD         |
#----------------------------X

def keysToNormalChildByIndex(privateKey,publicKey,chaincode,childIndex):
    hashedResult = hmac.new(chaincode,publicKey+childIndex.to_bytes(4, 'big'),hashlib.sha512).digest()
    newPrivateKey = (toEcdsaRange(toCleanInt(hashedResult[:32])+toCleanInt(privateKey))).to_bytes(32, 'big')
    newWallet = keyToWalletData(newPrivateKey)
    newWallet["chaincode"] = hashedResult[32:]
    return newWallet

def keysToHardenedChildByIndex(privateKey,publicKey,chaincode,childIndex):
    hashedResult = hmac.new(chaincode,b'\x00'+privateKey+(2**31+childIndex).to_bytes(4, 'big'),hashlib.sha512).digest()
    newPrivateKey = (toEcdsaRange(toCleanInt(hashedResult[:32])+toCleanInt(privateKey))).to_bytes(32, 'big')
    newWallet = keyToWalletData(newPrivateKey)
    newWallet["chaincode"] = hashedResult[32:]
    return newWallet

def masterToChildByPath(path):
    splitedPath = path.split("/")
    lastPath = splitedPath.pop()
    if lastPath == "m":
        masterWallet = keyToWalletData(walletData["masterPrivateKey"])
        masterWallet["chaincode"] = walletData["chaincode"]
        return masterWallet
    if lastPath[-1] == "'":
        newSource = masterToChildByPath('/'.join(splitedPath))
        newChild = keysToHardenedChildByIndex(newSource["privateKey"],newSource["publicCompressedKey"],newSource["chaincode"],int(lastPath[0]))
        newChild["parentFingerprint"] = newSource["fingerprint"]
        return newChild
    else:
        newSource = masterToChildByPath('/'.join(splitedPath))
        newChild = keysToNormalChildByIndex(newSource["privateKey"],newSource["publicCompressedKey"],newSource["chaincode"],int(lastPath[0]))
        newChild["parentFingerprint"] = newSource["fingerprint"]
        return newChild

def walletToExtendedPrivateKey(wallet):
    depth = (len(wallet["path"].split("/"))-1).to_bytes(1,"big")
    pathSplited = wallet["path"].split("/").pop()
    index = 0
    if pathSplited[-1] == "'":
        index = 2**31+int(pathSplited[-2])
    elif pathSplited != "m":
        index = int(pathSplited)
    return str(b58encode_check(bytes.fromhex("0488ade4")+depth+wallet["parentFingerprint"]+index.to_bytes(4,"big")+wallet["chaincode"]+b'\x00'+wallet["privateKey"]))[1:].replace("'","")

def walletToExtendedPublicKey(wallet):
    depth = (len(wallet["path"].split("/"))-1).to_bytes(1,"big")
    pathSplited = wallet["path"].split("/").pop()
    index = 0
    if pathSplited[-1] == "'":
        index = 2**31+int(pathSplited[-2])
    elif pathSplited != "m":
        index = int(pathSplited)
    return str(b58encode_check(bytes.fromhex("0488b21e")+depth+wallet["parentFingerprint"]+index.to_bytes(4,"big")+wallet["chaincode"]+wallet["publicCompressedKey"]))[1:].replace("'","")

#----------------------------X
#     BIP39 - Seed utils     |
#----------------------------X

def seedToKey(seed):
    wordsIndexs = list(map(lambda x: bip39Dic.index(x), seed))
    binString = "".join( map(lambda x: "".join(["0"]*(264//24 - len(bin(x)[2:]))) +bin(x)[2:],wordsIndexs))
    hexString = ""+hex(int(binString,base=2))[2:].upper().strip()+""
    return bytes.fromhex(hexString)

def keyToSeed(PKey):
    binString = bin(int(PKey.hex().upper(),base=16))[2:]
    binStringClean = "".join(["0"]*(264-len(binString))) + binString
    bitsLength = len(binStringClean)//24
    binSplited = [binString[i:i+bitsLength] for i in range(0, len(binString), bitsLength)]
    seed = list(map(lambda x: bip39Dic[int(x, base=2)], binSplited))
    return seed

def seedToRootSeed(seed, passphrase = "mnemonic", repetitions = 2048):
    return hashlib.pbkdf2_hmac('sha512'," ".join(seed).encode(),passphrase.encode('utf-8'),repetitions,None)

#----------------------------X
#     Save & Load utils      |
#----------------------------X

def loadSeedFile(file = ".mySeed1.env"):
    global walletData
    global selectedWalletData
    with open(file) as f:
        seed = f.readlines()[0].strip().split(" ")
        privateKeyFromFile = seedToKey(seed)
        BIP39seed = seedToRootSeed(seed)
        hashedSeed = hmac.new(b'Bitcoin seed', BIP39seed,hashlib.sha512).digest()
        walletData["entropy"] = privateKeyFromFile
        walletData["rootSeed"] = BIP39seed
        walletData["masterPrivateKey"] = hashedSeed[:32]
        walletData["masterWalletData"] = keyToWalletData(hashedSeed[:32])
        walletData["masterPublicKey"] = walletData["masterWalletData"]["publicKey"]
        walletData["chaincode"] = hashedSeed[32:]
        walletData["masterWalletData"]["chaincode"] = walletData["chaincode"]
        walletData["masterWalletData"]["path"] = "m"
        walletData["masterWalletData"]["parentFingerprint"] = (0).to_bytes(4,"big")
        selectedWalletData = walletData["masterWalletData"].copy()


def generateSeedFile(file = ".mySeed1.env"):
    with open(file,"w") as f:
        securedRandomBytes = token_bytes(32)
        securedRandomBytesChecksum = hashlib.sha256(securedRandomBytes).digest()[:1]
        seed = keyToSeed(securedRandomBytes+securedRandomBytesChecksum)
        f.write(" ".join(seed))

#----------------------------X
#   Display Part & Routine   |
#----------------------------X

windowLength = 95

class bc:
    HEADER = '\u001b[30;1m'
    OKBLUE = '\u001b[36;1m\033[1m'
    OKCYAN = '\u001b[35;1m\033[1m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    WAB = '\033[93m\033[1m'

system('color')

horizontalBar = bc.WAB+"X---------------------------------------------------------------------------------------------X"+bc.ENDC

def startMenu():
    print(horizontalBar)
    print(bc.WAB+"|"+bc.ENDC+bc.OKCYAN+"             ___                                                 ___                         "+bc.WAB+"|"+bc.ENDC)
    print(bc.WAB+"|"+bc.ENDC+bc.OKCYAN+"            /\  \                                               /\__\                        "+bc.WAB+"|"+bc.ENDC)
    print(bc.WAB+"|"+bc.ENDC+bc.OKCYAN+"           /::\  \       ___                                   /:/ _/_         ___           "+bc.WAB+"|"+bc.ENDC)
    print(bc.WAB+"|"+bc.ENDC+bc.OKCYAN+"          /:/\:\__\     /|  |                                 /:/ /\__\       /\__\          "+bc.WAB+"|"+bc.ENDC)
    print(bc.WAB+"|"+bc.ENDC+bc.OKCYAN+"         /:/ /:/  /    |:|  |    ___     ___   ___     ___   /:/ /:/ _/_     /:/  /          "+bc.WAB+"|"+bc.ENDC)
    print(bc.WAB+"|"+bc.ENDC+bc.OKCYAN+"        /:/_/:/  /     |:|  |   /\  \   /\__\ /\  \   /\__\ /:/_/:/ /\__\   /:/__/           "+bc.WAB+"|"+bc.ENDC)
    print(bc.WAB+"|"+bc.ENDC+bc.OKCYAN+"        \:\/:/  /    __|:|__|   \:\  \ /:/  / \:\  \ /:/  / \:\/:/ /:/  /  /::\  \           "+bc.WAB+"|"+bc.ENDC)
    print(bc.WAB+"|"+bc.ENDC+bc.OKCYAN+"         \::/__/    /::::\  \    \:\  /:/  /   \:\  /:/  /   \::/_/:/  /  /:/\:\  \          "+bc.WAB+"|"+bc.ENDC)
    print(bc.WAB+"|"+bc.ENDC+bc.OKCYAN+"          \:\  \    ~~~~\:\  \    \:\/:/  /     \:\/:/  /     \:\/:/  /   \/__\:\  \         "+bc.WAB+"|"+bc.ENDC)
    print(bc.WAB+"|"+bc.ENDC+bc.OKCYAN+"           \:\__\        \:\__\    \::/  /       \::/  /       \::/  /         \:\__\        "+bc.WAB+"|"+bc.ENDC)
    print(bc.WAB+"|"+bc.ENDC+bc.OKCYAN+"            \/__/         \/__/     \/__/         \/__/         \/__/           \/__/        "+bc.WAB+"|"+bc.ENDC)
    print(bc.WAB+"|"+bc.ENDC+bc.OKCYAN+"                                                                                             "+bc.WAB+"|"+bc.ENDC)
    print(horizontalBar)
    print(bc.WAB+"|"+bc.ENDC+bc.HEADER+" https://github.com/BobochD-Brew/BtcPyllet                                 https://boboch.tk "+bc.WAB+"|"+bc.ENDC)
    print(horizontalBar)
    if(not path.exists(".mySeed1.env")):
        generateSeedFile()
        loadSeedFile()
        print(bc.WAB+"|"+bc.ENDC+bc.FAIL+"-> Counldn't find a seed file, {.mySeed1.env} has been generated.                            "+bc.WAB+"|"+bc.ENDC)
    else:
        loadSeedFile()
        print(bc.WAB+"|"+bc.ENDC+bc.OKGREEN+"-> Loaded seed phrase from {.mySeed1.env}.                                                   "+bc.WAB+"|"+bc.ENDC)

def showData(dataName,dataContent):
    printPrefix = bc.WAB+"|"+bc.ENDC+" "+bc.BOLD+dataName+" : "+bc.ENDC
    firstLineContent = dataContent[:(windowLength-len(printPrefix)-2+len(bc.WAB+bc.ENDC+bc.BOLD+bc.ENDC))]
    restContent = dataContent[(windowLength-len(printPrefix)-2+len(bc.WAB+bc.ENDC+bc.BOLD+bc.ENDC)):]
    splitedContent = [restContent[i:i+(windowLength-4)] for i in range(0, len(restContent), (windowLength-4))]
    print(printPrefix+bc.HEADER+firstLineContent+''.join([" "]*((windowLength-len(printPrefix)-2) - len(firstLineContent)+len(bc.WAB+bc.ENDC+bc.BOLD+bc.ENDC)))+" "+bc.WAB+"|"+bc.ENDC)
    for k in splitedContent:
        print(bc.WAB+"|"+bc.ENDC+bc.HEADER+" "+k+''.join([" "]*((windowLength-4)-len(k)))+" "+bc.WAB+"|"+bc.ENDC)
    
def mainMenu():
    print(horizontalBar)
    showData("Selected Wallet","MASTER" if selectedWalletData["publicKey"] == walletData["masterPublicKey"] else selectedWalletData["path"])
    showData("Address",str(selectedWalletData["publicAddress"])[1:].replace("'",""))
    subMenu()

def subMenu():
    global selectedWalletData
    print(horizontalBar)
    print(bc.WAB+"|"+bc.ENDC+"  "+bc.OKBLUE+" 1->"+bc.ENDC+" Show public keys            "+bc.OKBLUE+"2->"+bc.ENDC+" Generate new seed          "+bc.OKBLUE+"3->"+bc.ENDC+" Load seed file         "+bc.WAB+"|"+bc.ENDC)
    print(bc.WAB+"|"+bc.ENDC+"  "+bc.OKBLUE+" 4->"+bc.ENDC+" Select child                "+bc.OKBLUE+"5->"+bc.ENDC+" Select master wallet       "+bc.OKBLUE+"6->"+bc.ENDC+" Show private keys      "+bc.WAB+"|"+bc.ENDC)
    print(bc.WAB+"|"+bc.ENDC+"  "+bc.OKBLUE+" 7->"+bc.ENDC+" Show master private Key     "+bc.OKBLUE+"8->"+bc.ENDC+" Show master public Key     "+bc.OKBLUE+"9->"+bc.ENDC+" Show master chaincode  "+bc.WAB+"|"+bc.ENDC)
    print(bc.WAB+"|"+bc.ENDC+"  "+bc.OKBLUE+"10->"+bc.ENDC+" Show addess QR Code         "+bc.OKBLUE+"   "+bc.ENDC+"                            "+bc.OKBLUE+"   "+bc.ENDC+"                        "+bc.WAB+"|"+bc.ENDC)
    print(horizontalBar)

    option = input(bc.WAB+"|"+bc.ENDC+"-> Select action: ")
    print("\033[A                             \033[A")
    option = int(option) if option.isdecimal() else None
    if(option == None or option > 10 or option <1):
        print(bc.WAB+"|"+bc.ENDC+"-> Please enter a valid option !                                                             "+bc.WAB+"|"+bc.ENDC)
        return subMenu()
    elif option == 1:
        showData("Compressed Public key",selectedWalletData["publicCompressedKey"].hex())
        showData("Signing key",selectedWalletData["signingKey"].to_string().hex())
        showData("Verifying Key",selectedWalletData["verifyingKey"].to_string().hex())
        showData("Extended Public Key",walletToExtendedPublicKey(selectedWalletData))
        showData("Address",str(selectedWalletData["publicAddress"])[1:].replace("'",""))
        return subMenu()
    elif option == 2:
        print(bc.WAB+"|"+bc.ENDC+"-> Entering a used filename will overwrite it !                                              "+bc.WAB+"|"+bc.ENDC)
        filename = input(bc.WAB+"|"+bc.ENDC+"-> Enter a filename : ")
        print("\033[A                             \033[A")
        if "." not in filename:
            filename = "."+filename+".env"
        generateSeedFile(filename)
        loadSeedFile(filename)
        showData("New seed phrase at","{"+filename+"}")
        return mainMenu()
    elif option == 3:
        filename = input(bc.WAB+"|"+bc.ENDC+"-> Enter a filename : ")
        print("\033[A                             \033[A")
        if "." not in filename:
            filename = "."+filename+".env"
        if(not path.exists(filename)):
            print(bc.WAB+"|"+bc.ENDC+"-> Please enter a valid filename !                                                           "+bc.WAB+"|"+bc.ENDC)
            return subMenu()
        loadSeedFile(filename)
        showData("Loaded seed phrase from","{"+filename+"}")
        return mainMenu()
    elif option == 4:
        print(bc.WAB+"|"+bc.ENDC+"-> Enter a BIP32 wallet path. ex: m/0 or m/0'/5h/2 ...                                       "+bc.WAB+"|"+bc.ENDC)
        path = input(bc.WAB+"|"+bc.ENDC+"-> path: ")
        print("\033[A                             \033[A")
        path = path.replace("h","'")
        wrongPath = not set(path).issubset(set("m/0123456789'")) or path[0].lower() != 'm' or 'm' in path[1:].lower()
        for p in path.split("/"):
            wrongPath = wrongPath or p[0] == "'" or p == "" or "'" in p[:-1]
        if wrongPath:
            print(bc.WAB+"|"+bc.ENDC+"-> Please enter a valid path !                                                               "+bc.WAB+"|"+bc.ENDC)
            return subMenu()
        selectedWalletData = masterToChildByPath(path)
        selectedWalletData["path"] = path
        return mainMenu()
    elif option == 5:
        selectedWalletData = walletData["masterWalletData"]
        print("\033[A                             \033[A")
        return mainMenu()
    elif option == 6:
        showData("WIF Private key",str(selectedWalletData["encodedPrivateKey"])[1:].replace("'",""))
        showData("Hex Private key",selectedWalletData["privateKey"][1:].hex())
        showData("Extended Private key",walletToExtendedPrivateKey(selectedWalletData))
        if( selectedWalletData["publicKey"] == walletData["masterPublicKey"]):
            showData("BIP39 Seed"," ".join(keyToSeed(walletData["entropy"])))
            showData("Entropy",walletData["entropy"].hex())

        return subMenu()
    elif option == 7:
        showData("Master Private Key",walletData["masterPrivateKey"].hex())
        subMenu()
    elif option == 8:
        showData("Master Public Key",walletData["masterWalletData"]["publicCompressedKey"].hex())
        return subMenu()
    elif option == 9:
        showData("Master Chain Code",walletData["chaincode"].hex())
        return subMenu()
    elif option == 10:
        qr = qrcode.QRCode(version=1,error_correction=qrcode.constants.ERROR_CORRECT_L,box_size=10,border=1,)
        qr.add_data(str(selectedWalletData["publicAddress"])[1:].replace("'",""))
        qr.make(fit=True)
        drawQRCodeInside(qr)
        return subMenu()


#Custom QRCode.print_ascii()
def drawQRCodeInside(self):
    out = sys.stdout
    if self.data_cache is None:
        self.make()
    modcount = self.modules_count
    codes = [bytes((code,)).decode('cp437') for code in (255, 223, 220, 219)]
    def get_module(x, y):
        if min(x, y) < 0 or max(x, y) >= modcount:
            return 0
        return self.modules[x][y]
    for r in range(-self.border, modcount+self.border, 2):
        out.write(bc.WAB+"|"+bc.ENDC+'                              ')
        for c in range(-self.border, modcount+self.border):
            pos = get_module(r, c) + (get_module(r+1, c) << 1)
            out.write(codes[pos])
        out.write(''.join([" "]*(windowLength-2-61))+bc.WAB+"|"+bc.ENDC)
        out.write('\n')
    out.flush()

#In order to keep everything in 1 file
bip39Dic = "abandon ability able about above absent absorb abstract absurd abuse access accident account accuse achieve acid acoustic acquire across act action actor actress actual adapt add addict address adjust admit adult advance advice aerobic affair afford afraid again age agent agree ahead aim air airport aisle alarm album alcohol alert alien all alley allow almost alone alpha already also alter always amateur amazing among amount amused analyst anchor ancient anger angle angry animal ankle announce annual another answer antenna antique anxiety any apart apology appear apple approve april arch arctic area arena argue arm armed armor army around arrange arrest arrive arrow art artefact artist artwork ask aspect assault asset assist assume asthma athlete atom attack attend attitude attract auction audit august aunt author auto autumn average avocado avoid awake aware away awesome awful awkward axis baby bachelor bacon badge bag balance balcony ball bamboo banana banner bar barely bargain barrel base basic basket battle beach bean beauty because become beef before begin behave behind believe below belt bench benefit best betray better between beyond bicycle bid bike bind biology bird birth bitter black blade blame blanket blast bleak bless blind blood blossom blouse blue blur blush board boat body boil bomb bone bonus book boost border boring borrow boss bottom bounce box boy bracket brain brand brass brave bread breeze brick bridge brief bright bring brisk broccoli broken bronze broom brother brown brush bubble buddy budget buffalo build bulb bulk bullet bundle bunker burden burger burst bus business busy butter buyer buzz cabbage cabin cable cactus cage cake call calm camera camp can canal cancel candy cannon canoe canvas canyon capable capital captain car carbon card cargo carpet carry cart case cash casino castle casual cat catalog catch category cattle caught cause caution cave ceiling celery cement census century cereal certain chair chalk champion change chaos chapter charge chase chat cheap check cheese chef cherry chest chicken chief child chimney choice choose chronic chuckle chunk churn cigar cinnamon circle citizen city civil claim clap clarify claw clay clean clerk clever click client cliff climb clinic clip clock clog close cloth cloud clown club clump cluster clutch coach coast coconut code coffee coil coin collect color column combine come comfort comic common company concert conduct confirm congress connect consider control convince cook cool copper copy coral core corn correct cost cotton couch country couple course cousin cover coyote crack cradle craft cram crane crash crater crawl crazy cream credit creek crew cricket crime crisp critic crop cross crouch crowd crucial cruel cruise crumble crunch crush cry crystal cube culture cup cupboard curious current curtain curve cushion custom cute cycle dad damage damp dance danger daring dash daughter dawn day deal debate debris decade december decide decline decorate decrease deer defense define defy degree delay deliver demand demise denial dentist deny depart depend deposit depth deputy derive describe desert design desk despair destroy detail detect develop device devote diagram dial diamond diary dice diesel diet differ digital dignity dilemma dinner dinosaur direct dirt disagree discover disease dish dismiss disorder display distance divert divide divorce dizzy doctor document dog doll dolphin domain donate donkey donor door dose double dove draft dragon drama drastic draw dream dress drift drill drink drip drive drop drum dry duck dumb dune during dust dutch duty dwarf dynamic eager eagle early earn earth easily east easy echo ecology economy edge edit educate effort egg eight either elbow elder electric elegant element elephant elevator elite else embark embody embrace emerge emotion employ empower empty enable enact end endless endorse enemy energy enforce engage engine enhance enjoy enlist enough enrich enroll ensure enter entire entry envelope episode equal equip era erase erode erosion error erupt escape essay essence estate eternal ethics evidence evil evoke evolve exact example excess exchange excite exclude excuse execute exercise exhaust exhibit exile exist exit exotic expand expect expire explain expose express extend extra eye eyebrow fabric face faculty fade faint faith fall false fame family famous fan fancy fantasy farm fashion fat fatal father fatigue fault favorite feature february federal fee feed feel female fence festival fetch fever few fiber fiction field figure file film filter final find fine finger finish fire firm first fiscal fish fit fitness fix flag flame flash flat flavor flee flight flip float flock floor flower fluid flush fly foam focus fog foil fold follow food foot force forest forget fork fortune forum forward fossil foster found fox fragile frame frequent fresh friend fringe frog front frost frown frozen fruit fuel fun funny furnace fury future gadget gain galaxy gallery game gap garage garbage garden garlic garment gas gasp gate gather gauge gaze general genius genre gentle genuine gesture ghost giant gift giggle ginger giraffe girl give glad glance glare glass glide glimpse globe gloom glory glove glow glue goat goddess gold good goose gorilla gospel gossip govern gown grab grace grain grant grape grass gravity great green grid grief grit grocery group grow grunt guard guess guide guilt guitar gun gym habit hair half hammer hamster hand happy harbor hard harsh harvest hat have hawk hazard head health heart heavy hedgehog height hello helmet help hen hero hidden high hill hint hip hire history hobby hockey hold hole holiday hollow home honey hood hope horn horror horse hospital host hotel hour hover hub huge human humble humor hundred hungry hunt hurdle hurry hurt husband hybrid ice icon idea identify idle ignore ill illegal illness image imitate immense immune impact impose improve impulse inch include income increase index indicate indoor industry infant inflict inform inhale inherit initial inject injury inmate inner innocent input inquiry insane insect inside inspire install intact interest into invest invite involve iron island isolate issue item ivory jacket jaguar jar jazz jealous jeans jelly jewel job join joke journey joy judge juice jump jungle junior junk just kangaroo keen keep ketchup key kick kid kidney kind kingdom kiss kit kitchen kite kitten kiwi knee knife knock know lab label labor ladder lady lake lamp language laptop large later latin laugh laundry lava law lawn lawsuit layer lazy leader leaf learn leave lecture left leg legal legend leisure lemon lend length lens leopard lesson letter level liar liberty library license life lift light like limb limit link lion liquid list little live lizard load loan lobster local lock logic lonely long loop lottery loud lounge love loyal lucky luggage lumber lunar lunch luxury lyrics machine mad magic magnet maid mail main major make mammal man manage mandate mango mansion manual maple marble march margin marine market marriage mask mass master match material math matrix matter maximum maze meadow mean measure meat mechanic medal media melody melt member memory mention menu mercy merge merit merry mesh message metal method middle midnight milk million mimic mind minimum minor minute miracle mirror misery miss mistake mix mixed mixture mobile model modify mom moment monitor monkey monster month moon moral more morning mosquito mother motion motor mountain mouse move movie much muffin mule multiply muscle museum mushroom music must mutual myself mystery myth naive name napkin narrow nasty nation nature near neck need negative neglect neither nephew nerve nest net network neutral never news next nice night noble noise nominee noodle normal north nose notable note nothing notice novel now nuclear number nurse nut oak obey object oblige obscure observe obtain obvious occur ocean october odor off offer office often oil okay old olive olympic omit once one onion online only open opera opinion oppose option orange orbit orchard order ordinary organ orient original orphan ostrich other outdoor outer output outside oval oven over own owner oxygen oyster ozone pact paddle page pair palace palm panda panel panic panther paper parade parent park parrot party pass patch path patient patrol pattern pause pave payment peace peanut pear peasant pelican pen penalty pencil people pepper perfect permit person pet phone photo phrase physical piano picnic picture piece pig pigeon pill pilot pink pioneer pipe pistol pitch pizza place planet plastic plate play please pledge pluck plug plunge poem poet point polar pole police pond pony pool popular portion position possible post potato pottery poverty powder power practice praise predict prefer prepare present pretty prevent price pride primary print priority prison private prize problem process produce profit program project promote proof property prosper protect proud provide public pudding pull pulp pulse pumpkin punch pupil puppy purchase purity purpose purse push put puzzle pyramid quality quantum quarter question quick quit quiz quote rabbit raccoon race rack radar radio rail rain raise rally ramp ranch random range rapid rare rate rather raven raw razor ready real reason rebel rebuild recall receive recipe record recycle reduce reflect reform refuse region regret regular reject relax release relief rely remain remember remind remove render renew rent reopen repair repeat replace report require rescue resemble resist resource response result retire retreat return reunion reveal review reward rhythm rib ribbon rice rich ride ridge rifle right rigid ring riot ripple risk ritual rival river road roast robot robust rocket romance roof rookie room rose rotate rough round route royal rubber rude rug rule run runway rural sad saddle sadness safe sail salad salmon salon salt salute same sample sand satisfy satoshi sauce sausage save say scale scan scare scatter scene scheme school science scissors scorpion scout scrap screen script scrub sea search season seat second secret section security seed seek segment select sell seminar senior sense sentence series service session settle setup seven shadow shaft shallow share shed shell sheriff shield shift shine ship shiver shock shoe shoot shop short shoulder shove shrimp shrug shuffle shy sibling sick side siege sight sign silent silk silly silver similar simple since sing siren sister situate six size skate sketch ski skill skin skirt skull slab slam sleep slender slice slide slight slim slogan slot slow slush small smart smile smoke smooth snack snake snap sniff snow soap soccer social sock soda soft solar soldier solid solution solve someone song soon sorry sort soul sound soup source south space spare spatial spawn speak special speed spell spend sphere spice spider spike spin spirit split spoil sponsor spoon sport spot spray spread spring spy square squeeze squirrel stable stadium staff stage stairs stamp stand start state stay steak steel stem step stereo stick still sting stock stomach stone stool story stove strategy street strike strong struggle student stuff stumble style subject submit subway success such sudden suffer sugar suggest suit summer sun sunny sunset super supply supreme sure surface surge surprise surround survey suspect sustain swallow swamp swap swarm swear sweet swift swim swing switch sword symbol symptom syrup system table tackle tag tail talent talk tank tape target task taste tattoo taxi teach team tell ten tenant tennis tent term test text thank that theme then theory there they thing this thought three thrive throw thumb thunder ticket tide tiger tilt timber time tiny tip tired tissue title toast tobacco today toddler toe together toilet token tomato tomorrow tone tongue tonight tool tooth top topic topple torch tornado tortoise toss total tourist toward tower town toy track trade traffic tragic train transfer trap trash travel tray treat tree trend trial tribe trick trigger trim trip trophy trouble truck true truly trumpet trust truth try tube tuition tumble tuna tunnel turkey turn turtle twelve twenty twice twin twist two type typical ugly umbrella unable unaware uncle uncover under undo unfair unfold unhappy uniform unique unit universe unknown unlock until unusual unveil update upgrade uphold upon upper upset urban urge usage use used useful useless usual utility vacant vacuum vague valid valley valve van vanish vapor various vast vault vehicle velvet vendor venture venue verb verify version very vessel veteran viable vibrant vicious victory video view village vintage violin virtual virus visa visit visual vital vivid vocal voice void volcano volume vote voyage wage wagon wait walk wall walnut want warfare warm warrior wash wasp waste water wave way wealth weapon wear weasel weather web wedding weekend weird welcome west wet whale what wheat wheel when where whip whisper wide width wife wild will win window wine wing wink winner winter wire wisdom wise wish witness wolf woman wonder wood wool word work world worry worth wrap wreck wrestle wrist write wrong yard year yellow you young youth zebra zero zone zoo".split(" ")

startMenu()
mainMenu()
print(horizontalBar)
