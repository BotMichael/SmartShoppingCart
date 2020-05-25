# generate_key.py

import rsa

import os
import sys

sys.path.append(os.getcwd())
import Global_Var


# Only run once to generate the key
def generate_rsa_key():
    (pubkey, privkey) = rsa.newkeys(1024)

    pub = pubkey.save_pkcs1()
    pubfile = open(Global_Var.pubkey_file,'wb+')
    pubfile.write(pub)
    pubfile.close()

    pri = privkey.save_pkcs1()
    prifile = open(Global_Var.privkey_file,'wb+')
    prifile.write(pri)
    prifile.close()


if __name__ == "__main__":
    generate_rsa_key()