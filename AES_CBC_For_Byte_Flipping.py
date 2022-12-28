# Script written by Mike on Tech on YT: /
# https://youtu.be/i9KiOjeE-VY/
# This script gets to decrypt by flipping the mode bit/
# for a CTF challenge that ecnrpyt's client side cookies using Homomophonic/
# Encryption. Searching the cookie on the endpoint won't give a/
# to find the flag. The only way to decrypt the data is by actually/
# finding alogrithm that can decipher the language used in AES/
# Algorithm.

from base64 import b64decode
from base64 import b64encode
import requests

#https://play.picoctf.org/practice/challenge/124?category=1&page=1&search=

original_cookie = b64decode("UHJQRkdWTyswVFhhMHFrRktmNnQ3WmhuWUtVc09sTHB4VFgzSllIQUJYRXNBWkY4Q1RLMmVGZENCVld6MVhhbS8xWk5vKzBIQmd0SmVaRzJzUklkTE81dFFOb1FBMnNjMk1kK3VDeXEzUVk1K3JHTnYzMmVlNHRyVmsvdllITDI=")
original_cookie = bytearray(original_cookie)

def bitFlip(cookie_char_pos:int, bit_pos:int) -> str:
    altered_cookie = bytearray(original_cookie)

    flipped = altered_cookie[cookie_char_pos]^bit_pos

    altered_cookie[cookie_char_pos] = flipped

    altered_cookie_b64 = b64encode(bytes(altered_cookie))

    return altered_cookie_b64.decode("utf-8")

for cookie_char_pos in range(len(original_cookie)):
  print(f"Checking cookie position: {cookie_char_pos} ")
  for bit_pos in range(128): # [1,2,4,8,16,32,64,128]: #byte stream - 8 bit range affords 128 possiblities
    altered_cookie = bitFlip(cookie_char_pos, bit_pos)
    cookies = {'auth_name': altered_cookie}
    r = requests.get('http://mercury.picoctf.net:21553/', cookies=cookies)
    t = r.text.lower()
    if "picoCTF{".lower() in t or "picoCTF {".lower() in t:
      print(r.text)
      break
