# generate_key.py

import rsa

# Only run once to generate the key
def generate_rsa_key(pubkey_file, privkey_file):
    (pubkey, privkey) = rsa.newkeys(1024)

    pub = pubkey.save_pkcs1()
    pubfile = open(pubkey_file,'wb+')
    pubfile.write(pub)
    pubfile.close()

    pri = privkey.save_pkcs1()
    prifile = open(privkey_file,'wb+')
    prifile.write(pri)
    prifile.close()


if __name__ == "__main__":
    generate_rsa_key("public.pem", "private.pem")