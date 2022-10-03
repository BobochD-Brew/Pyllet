```diff
@@             ___                                                 ___                         @@
@@            /\  \                                               /\__\                        @@
@@           /::\  \       ___                                   /:/ _/_         ___           @@
@@          /:/\:\__\     /|  |                                 /:/ /\__\       /\__\          @@
@@         /:/ /:/  /    |:|  |    ___     ___   ___     ___   /:/ /:/ _/_     /:/  /          @@
@@        /:/_/:/  /     |:|  |   /\  \   /\__\ /\  \   /\__\ /:/_/:/ /\__\   /:/__/           @@
@@        \:\/:/  /    __|:|__|   \:\  \ /:/  / \:\  \ /:/  / \:\/:/ /:/  /  /::\  \           @@
@@         \::/__/    /::::\  \    \:\  /:/  /   \:\  /:/  /   \::/_/:/  /  /:/\:\  \          @@
@@          \:\  \    ~~~~\:\  \    \:\/:/  /     \:\/:/  /     \:\/:/  /   \/__\:\  \         @@
@@           \:\__\        \:\__\    \::/  /       \::/  /       \::/  /         \:\__\        @@
@@            \/__/         \/__/     \/__/         \/__/         \/__/           \/__/        @@
```
A simple python bitcoin wallet manager implementing BIP39 & BIP32.

### EXE packed with PyInstaller

Download the packed .exe file here [main.exe](dist/main.exe)

### One file python script

Or download [main.py](main.py) and run it with:

```console
foo@bar:~$ python3 -m pip install ecdsa base58 qrcode
foo@bar:~$ python3 main.py
```

A file named ```.mySeed1.env``` will be created with a new seed, you can edit it and enter you BIP39 seed phrase or generate a new one. 

### Example

```console
X---------------------------------------------------------------------------------------------X
|             ___                                                 ___                         |
|            /\  \                                               /\__\                        |
|           /::\  \       ___                                   /:/ _/_         ___           |
|          /:/\:\__\     /|  |                                 /:/ /\__\       /\__\          |
|         /:/ /:/  /    |:|  |    ___     ___   ___     ___   /:/ /:/ _/_     /:/  /          |
|        /:/_/:/  /     |:|  |   /\  \   /\__\ /\  \   /\__\ /:/_/:/ /\__\   /:/__/           |
|        \:\/:/  /    __|:|__|   \:\  \ /:/  / \:\  \ /:/  / \:\/:/ /:/  /  /::\  \           |
|         \::/__/    /::::\  \    \:\  /:/  /   \:\  /:/  /   \::/_/:/  /  /:/\:\  \          |
|          \:\  \    ~~~~\:\  \    \:\/:/  /     \:\/:/  /     \:\/:/  /   \/__\:\  \         |
|           \:\__\        \:\__\    \::/  /       \::/  /       \::/  /         \:\__\        |
|            \/__/         \/__/     \/__/         \/__/         \/__/           \/__/        |
|                                                                                             |
X---------------------------------------------------------------------------------------------X
|-> Counldn't find a seed file, {.mySeed1.env} has been generated.                            |
X---------------------------------------------------------------------------------------------X
| Selected Wallet : MASTER                                                                    |
| Address : 1JsbYFtNhxfGjFa2D2xRiUcUqpP1Y64Bpk                                                |
X---------------------------------------------------------------------------------------------X
|   1-> Show public keys            2-> Generate new seed          3-> Load seed file         |
|   4-> Select child                5-> Select master wallet       6-> Show private keys      |
|   7-> Show master private Key     8-> Show master public Key     9-> Show master chaincode  |
|  10-> Show addess QR Code                                                                   |
X---------------------------------------------------------------------------------------------X
| Compressed Public key : 020e9fea1d0c91e4f0602db114dfdb1529426fe97dd2aaadd072e76e643b4be9d7  |
| Signing key : 21c52bf45e23545baeb0331609a5679145742354737694ad20b1227b29515e31              |
| Verifying Key : 0e9fea1d0c91e4f0602db114dfdb1529426fe97dd2aaadd072e76e643b4be9d74e5a655e289 |
| 8f84ea3825a146f97e628729d26ed914789a71214b705ffb8afde                                       |
| Extended Public Key : xpub661MyMwAqRbcFb5t6KoSZF6tnj9s3FC9PjaCnAJM7gDaRFoap6ioxFqsKEteVEMds |
| EWyTkCyFNx8JsySdKpUhswkm2MqifUfxxwtXRGv8oa                                                  |
| Address : 1JsbYFtNhxfGjFa2D2xRiUcUqpP1Y64Bpk                                                |
X---------------------------------------------------------------------------------------------X
|   1-> Show public keys            2-> Generate new seed          3-> Load seed file         |
|   4-> Select child                5-> Select master wallet       6-> Show private keys      |
|   7-> Show master private Key     8-> Show master public Key     9-> Show master chaincode  |
|  10-> Show addess QR Code                                                                   |
X---------------------------------------------------------------------------------------------X
|                               ▄▄▄▄▄▄▄   ▄ ▄▄▄▄  ▄▄▄ ▄▄▄▄▄▄▄                                 |
|                               █ ▄▄▄ █ ▀ ▀ ▄█▀█▀▀▀ █ █ ▄▄▄ █                                 |
|                               █ ███ █ ▀█▀ ▀ ▀█▄   █ █ ███ █                                 |
|                               █▄▄▄▄▄█ █▀▄▀█ ▄ ▄ ▄ █ █▄▄▄▄▄█                                 |
|                               ▄▄▄▄▄ ▄▄▄█▀█  ▀ ▀▄ ▄ ▄ ▄ ▄ ▄                                  |
|                               ▀▀▀▀██▄█▀ █ ▀███▄ ▄▀▀███▀ ▄▀▀                                 |
|                               ▄▄▀▄▄ ▄▄ ▄▄ █▀▄  ▄ ▀▄▀▀▀██ ▄▀                                 |
|                               ▀█▀▀▀▀▄█▀▀ ▄▄  ▄▀ ▄ ▀▀ ▀▀▄▀ ▀                                 |
|                               ▄█ ▄▀▀▄  ▄ █  ▀█▄ ▀▄▄▀▀▀▀▀ ██                                 |
|                               █▀▄▄ ▀▄ ▄▄  ▀██▄▀ ▄▀▀█▀▀█▀▄▀                                  |
|                               █ ▄ █▄▄ █ █ █▀▄▄ ▄█▀▄▄▄▄▄█▄▄                                  |
|                               ▄▄▄▄▄▄▄ █▄ ▄▄  █▀ ▄██ ▄ █▀ ▄▀                                 |
|                               █ ▄▄▄ █ ▄▀██  ▀██   █▄▄▄█▀ █▀                                 |
|                               █ ███ █ ██  ▀██▄ ▀▄▄ ▀▄█▄▀██▀                                 |
|                               █▄▄▄▄▄█ █▄▀ █▀▄▄█▄▄▄ █▄ ▀▀▄▀                                  |
|                                                                                             |
X---------------------------------------------------------------------------------------------X
|   1-> Show public keys            2-> Generate new seed          3-> Load seed file         |
|   4-> Select child                5-> Select master wallet       6-> Show private keys      |
|   7-> Show master private Key     8-> Show master public Key     9-> Show master chaincode  |
|  10-> Show addess QR Code                                                                   |
X---------------------------------------------------------------------------------------------X
| WIF Private key : KxMMaxz97MQt8cLiiS3C9p6i1dayfR3dAQeJA9PBGjvkvbp8sBCT                      |
| Hex Private key : 21c52bf45e23545baeb0331609a5679145742354737694ad20b1227b29515e31          |
| Extended Private key : xprv9s21ZrQH143K371QzJGSC7AAEhKNdnUJ2WebymtjZLgbYTUSGZQZQTXPTz1K6KUt |
| PCFmtq5AyG4NGS4uKkEoZS7EgNpfLFTzRDg5qiXbNAt                                                 |
| BIP39 Seed : october now number holiday suffer unique enable taste race donkey olive chat b |
| asket school never trend fatigue roast great cluster install family race glance             |
| Entropy : 9912e65db66d8bdb1256f1b068266893613381a5474053d76198963756a52c1b15                |
X---------------------------------------------------------------------------------------------X
|   1-> Show public keys            2-> Generate new seed          3-> Load seed file         |
|   4-> Select child                5-> Select master wallet       6-> Show private keys      |
|   7-> Show master private Key     8-> Show master public Key     9-> Show master chaincode  |
|  10-> Show addess QR Code                                                                   |
X---------------------------------------------------------------------------------------------X
|-> Enter a BIP32 wallet path. ex: m/0 or m/0'/5h/2 ...                                       |
X---------------------------------------------------------------------------------------------X
| Selected Wallet : m/44'/0'/0'/0                                                             |
| Address : 19QwAsJ3KUAeFvY6t9FmGht9A8AeVmVzjv                                                |
X---------------------------------------------------------------------------------------------X
|   1-> Show public keys            2-> Generate new seed          3-> Load seed file         |
|   4-> Select child                5-> Select master wallet       6-> Show private keys      |
|   7-> Show master private Key     8-> Show master public Key     9-> Show master chaincode  |
|  10-> Show addess QR Code                                                                   |
X---------------------------------------------------------------------------------------------X
|-> Enter a BIP32 wallet path. ex: m/0 or m/0'/5h/2 ...                                       |
X---------------------------------------------------------------------------------------------X
| Selected Wallet : m/555'/0/0/0/0/0/0                                                        |
| Address : 1MNJhPWQj7uzJsZwUzrUKijTowZ3TJidt                                                 |
X---------------------------------------------------------------------------------------------X
|   1-> Show public keys            2-> Generate new seed          3-> Load seed file         |
|   4-> Select child                5-> Select master wallet       6-> Show private keys      |
|   7-> Show master private Key     8-> Show master public Key     9-> Show master chaincode  |
|  10-> Show addess QR Code                                                                   |
X---------------------------------------------------------------------------------------------X
| Master Private Key : 21c52bf45e23545baeb0331609a5679145742354737694ad20b1227b29515e31       |
X---------------------------------------------------------------------------------------------X
|   1-> Show public keys            2-> Generate new seed          3-> Load seed file         |
|   4-> Select child                5-> Select master wallet       6-> Show private keys      |
|   7-> Show master private Key     8-> Show master public Key     9-> Show master chaincode  |
|  10-> Show addess QR Code                                                                   |
X---------------------------------------------------------------------------------------------X
| Master Public Key : 020e9fea1d0c91e4f0602db114dfdb1529426fe97dd2aaadd072e76e643b4be9d7      |
X---------------------------------------------------------------------------------------------X
|   1-> Show public keys            2-> Generate new seed          3-> Load seed file         |
|   4-> Select child                5-> Select master wallet       6-> Show private keys      |
|   7-> Show master private Key     8-> Show master public Key     9-> Show master chaincode  |
|  10-> Show addess QR Code                                                                   |
X---------------------------------------------------------------------------------------------X
| Master Chain Code : 6908371f914416a4cccc8003faf79a97e03828f7043acc6ff7eca6ce36b9d108        |
X---------------------------------------------------------------------------------------------X
|   1-> Show public keys            2-> Generate new seed          3-> Load seed file         |
|   4-> Select child                5-> Select master wallet       6-> Show private keys      |
|   7-> Show master private Key     8-> Show master public Key     9-> Show master chaincode  |
|  10-> Show addess QR Code                                                                   |
X---------------------------------------------------------------------------------------------X
```
