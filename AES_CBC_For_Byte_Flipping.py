#!/usr/bin/python3
"""
Script written by Martin Carlisle on his YT channel :
https://www.youtube.com/watch?v=Fs3EbH-Wdhc
This script get's to Flip mode bit for a CTF challenge that 
encrpyt's client side cookes using Hompophonic Encryption.
Searching the cookie on the endpoint won't give a clue to find
the flag. The only way to decrpyt the data is by actually finding
and algorith that can decipher the language used in AES Algorithm
"""
import requests
import base64

s = requests.Session()
s.get("http://mercury.picoctf.net:25992/")
cookie = s.cookies["auth_name"]
print(cookie)
unb64 = base64.b64decode(cookie)
print(unb64)
unb64b = base64.b64decode(unb64)
for i in range(0, 128):
    pos = i // 8
    guessdec = unb64b[0:pos] + chr(ord(unb64b[pos]) ^ (1 << (i % 8))) + unb64b[pos + 1:]
    guessenc1 = base64.b64encode(guessdec)
    guess = base64.b64encode(base64.b64encode(guessdec)).decode()
    r = requests.get("http://mercury.picoctf.net:25992/", cookies={"auth_name": guess})
    if "pico" in r.text:
        print(r.text)
