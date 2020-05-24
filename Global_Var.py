# Global Variable

import rsa

CLOUD_PORT = 5557
CLOUD_IP = "localhost"
FOG_PORT = 5556
FOG_IP = "localhost"

pubkey, privkey = rsa.newkeys(1024)
