#!/usr/bin/env python3

import binascii
import hmac
import sys
from base64 import b32decode
from getpass import getpass
from hashlib import sha1
from time import time

import keyring
from keyring.backends import libsecret


SERVICE_NAME = "sshautopass"
keyring.set_keyring(libsecret.Keyring())


def compute_ga_code(secret):
    GOOGLE_AUTHENTICATOR_STEP = 30

    while True:
        try:
            secret = b32decode(secret)
        except binascii.Error:
            secret += "="
        else:
            break

    value = int(time()) // GOOGLE_AUTHENTICATOR_STEP
    val = value.to_bytes(8, byteorder="big")
    hmac_hash = hmac.new(secret, val, sha1).digest()
    offset = hmac_hash[-1] & 0x0F
    code = hmac_hash[offset : offset + 4]
    code = int.from_bytes(code, byteorder="big") & 0x7FFFFFFF
    return code % 1000000


if __name__ == "__main__":
    prompt = sys.argv[1]

    cred = keyring.get_password(SERVICE_NAME, prompt)
    if not cred:
        cred = getpass(prompt.strip() + " ")
        keyring.set_password(SERVICE_NAME, prompt, cred.strip())
        cred = keyring.get_password(SERVICE_NAME, prompt)

    if "password" in prompt.lower():
        print(cred)
    elif "verification code" in prompt.lower():
        print(compute_ga_code(cred))
