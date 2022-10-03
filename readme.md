```diff
@@        ___                                                 ___                    @@
@@       /\  \                                               /\__\                   @@
@@      /::\  \       ___                                   /:/ _/_         ___      @@
@@     /:/\:\__\     /|  |                                 /:/ /\__\       /\__\     @@
@@    /:/ /:/  /    |:|  |    ___     ___   ___     ___   /:/ /:/ _/_     /:/  /     @@
@@   /:/_/:/  /     |:|  |   /\  \   /\__\ /\  \   /\__\ /:/_/:/ /\__\   /:/__/      @@
@@   \:\/:/  /    __|:|__|   \:\  \ /:/  / \:\  \ /:/  / \:\/:/ /:/  /  /::\  \      @@
@@    \::/__/    /::::\  \    \:\  /:/  /   \:\  /:/  /   \::/_/:/  /  /:/\:\  \     @@
@@     \:\  \    ~~~~\:\  \    \:\/:/  /     \:\/:/  /     \:\/:/  /   \/__\:\  \    @@
@@      \:\__\        \:\__\    \::/  /       \::/  /       \::/  /         \:\__\   @@
@@       \/__/         \/__/     \/__/         \/__/         \/__/           \/__/   @@
```
A simple python bitcoin wallet manager implementing BIP39 & BIP32.

### EXE packed with PyInstaller

You can download the packed .exe file here [main.exe](dist/main.exe)

### One file python script

Or download [main.py](main.py) and run it with:

```console
foo@bar:~$ python3 -m pip install ecdsa base58 qrcode
foo@bar:~$ python3 main.py
```

A file named ".mySeed1.env" will be created with a new seed you can edit it and enter you BIP39 seed phrase or generate a new one 

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
|-> Loaded seed phrase from {.mySeed1.env}.                                                   |
X---------------------------------------------------------------------------------------------X
| Selected Wallet : MASTER                                                                    |
| Address : 1KMvrZc5VA683PHBcRdgFDSyKgMDBXMqGN                                                |
X---------------------------------------------------------------------------------------------X
|   1-> Show public keys            2-> Generate new seed          3-> Load seed file         |
|   4-> Select child                5-> Select master wallet       6-> Show private keys      |
|   7-> Show master private Key     8-> Show master public Key     9-> Show master chaincode  |
|  10-> Show addess QR Code                                                                   |
X---------------------------------------------------------------------------------------------X
| Compressed Public key : 027592fd32f4c2a10372ce041e4c66185734cd85531e54ea810cb4f2444c857a80  |
| Signing key : 9b13cb232f414ff27126ff4dc25b7fecf51a4a175be1d4bf7fbc880408bf7758              |
| Verifying Key : 7592fd32f4c2a10372ce041e4c66185734cd85531e54ea810cb4f2444c857a8081acd5c960f |
| 22a1564e7972e1bdd3c629772522d053d964cb56128936b8a6e54                                       |
| Extended Public Key : xpub661MyMwAqRbcGhQeubTB8J4n5vtZBTLo85FWDGqAT8r8HGkwCUTVhM2XUGdLscJZs |
| k4mJu9reoSSgsMrZpnVrgt8qxjojGzHfBJdKPiqAa6                                                  |
| Address : 1KMvrZc5VA683PHBcRdgFDSyKgMDBXMqGN                                                |
X---------------------------------------------------------------------------------------------X
|   1-> Show public keys            2-> Generate new seed          3-> Load seed file         |
|   4-> Select child                5-> Select master wallet       6-> Show private keys      |
|   7-> Show master private Key     8-> Show master public Key     9-> Show master chaincode  |
|  10-> Show addess QR Code                                                                   |
X---------------------------------------------------------------------------------------------X
|                               ▄▄▄▄▄▄▄   ▄ ▄▄▄▄    ▄ ▄▄▄▄▄▄▄                                 |
|                               █ ▄▄▄ █ ▀ ▀ ▄█▀█▀▀▀ ▄ █ ▄▄▄ █                                 |
|                               █ ███ █ ▀█▀ ▀ ▀█▄█  ▄ █ ███ █                                 |
|                               █▄▄▄▄▄█ █▀▄▀█ ▄ ▄ █ ▄ █▄▄▄▄▄█                                 |
|                               ▄▄▄▄▄ ▄▄▄█▀█  ▀ ▀  ▀▀▄ ▄ ▄ ▄                                  |
|                               ▄▀▀▄█ ▄ █ █ ▀███ ██ █▄▀ █▀▄ ▀                                 |
|                               ▀▀▄ ▄▄▄▄ ▄▄ █▀▄ ▀▄ ▀▀ ▀▄ █▄ ▄                                 |
|                               ▄▀█  ▄▄▄▄  ▄▄  ██▄▀▀▀▄  ▀ ▄▀                                  |
|                               ▄  ▄█▄▄▀ ▀▀█  ▀▄▀   ▀▀ █▀█ ▄█                                 |
|                               █▀▀▀▀▄▄█▄▄  ▀████▀▀▀▀█▄▄█ █▀                                  |
|                               █ ▀▄▀▄▄▀▀▄▀ █▀▄█▄  ▀▄█▄▄█▀▄▄                                  |
|                               ▄▄▄▄▄▄▄ █▀ ▄▄  ▄█ ▀▀█ ▄ █▄▄▄▀                                 |
|                               █ ▄▄▄ █ ▄▀▄█  ▀▀▀ ▀▀█▄▄▄█▄▄█▀                                 |
|                               █ ███ █ █▄  ▀███▀▄█▀▀▄ ▄██ █▀                                 |
|                               █▄▄▄▄▄█ █▄  █▀▄▀▄ ▀▄▀█▄▄▄█ ▀                                  |
|                                                                                             |
X---------------------------------------------------------------------------------------------X
|   1-> Show public keys            2-> Generate new seed          3-> Load seed file         |
|   4-> Select child                5-> Select master wallet       6-> Show private keys      |
|   7-> Show master private Key     8-> Show master public Key     9-> Show master chaincode  |
|  10-> Show addess QR Code                                                                   |
X---------------------------------------------------------------------------------------------X
|-> Enter a BIP32 wallet path. ex: m/0 or m/0'/5h/2 ...                                       |
X---------------------------------------------------------------------------------------------X
| Selected Wallet : m/14/1'/5/9'/26'/5358/97                                                  |
| Address : 1B8JsKs4CfhRgNswbrPjVvC3EntFESCySw                                                |
X---------------------------------------------------------------------------------------------X
|   1-> Show public keys            2-> Generate new seed          3-> Load seed file         |
|   4-> Select child                5-> Select master wallet       6-> Show private keys      |
|   7-> Show master private Key     8-> Show master public Key     9-> Show master chaincode  |
|  10-> Show addess QR Code                                                                   |
X---------------------------------------------------------------------------------------------X
| WIF Private key : KyrmX1wftXAq8T4ELPUg3h7RrADgLK1fjV9jFjDpDQ3phS2C5eri                      |
| Hex Private key : bd12840f2caae2f18f81d4032cffdc9dae157c91b26ba5d87ac3265ce5d4db            |
| Extended Private key : xprvA6KkzCb2bPoUq59Ykvq3JeSKeuEws4WPYkBAdS6Dd5yj971VYsM4rD7WrLhMbhYk |
| L4sazrW4pw3gGZbp8Z9EHW7zpLqZS6hKUHVaxKLQnxB                                                 |
X---------------------------------------------------------------------------------------------X
|   1-> Show public keys            2-> Generate new seed          3-> Load seed file         |
|   4-> Select child                5-> Select master wallet       6-> Show private keys      |
|   7-> Show master private Key     8-> Show master public Key     9-> Show master chaincode  |
|  10-> Show addess QR Code                                                                   |
X---------------------------------------------------------------------------------------------X
| Master Chain Code : d86cbc21977eade2dd72950949d7141a8f9aac389d59c7186173ee283c53cf03        |
X---------------------------------------------------------------------------------------------X
|   1-> Show public keys            2-> Generate new seed          3-> Load seed file         |
|   4-> Select child                5-> Select master wallet       6-> Show private keys      |
|   7-> Show master private Key     8-> Show master public Key     9-> Show master chaincode  |
|  10-> Show addess QR Code                                                                   |
X---------------------------------------------------------------------------------------------X
| Master Public Key : 027592fd32f4c2a10372ce041e4c66185734cd85531e54ea810cb4f2444c857a80      |
X---------------------------------------------------------------------------------------------X
|   1-> Show public keys            2-> Generate new seed          3-> Load seed file         |
|   4-> Select child                5-> Select master wallet       6-> Show private keys      |
|   7-> Show master private Key     8-> Show master public Key     9-> Show master chaincode  |
|  10-> Show addess QR Code                                                                   |
X---------------------------------------------------------------------------------------------X
| Selected Wallet : MASTER                                                                    |
| Address : 1KMvrZc5VA683PHBcRdgFDSyKgMDBXMqGN                                                |
X---------------------------------------------------------------------------------------------X
|   1-> Show public keys            2-> Generate new seed          3-> Load seed file         |
|   4-> Select child                5-> Select master wallet       6-> Show private keys      |
|   7-> Show master private Key     8-> Show master public Key     9-> Show master chaincode  |
|  10-> Show addess QR Code                                                                   |
X---------------------------------------------------------------------------------------------X
|-> Select action:
```