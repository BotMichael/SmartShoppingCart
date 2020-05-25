
import rsa
def rsa_encrypt(d_str):
    # 生成公钥和私钥
    pubkey, privkey = rsa.newkeys(1024)
    # 将字符串进行编码
    content = d_str.encode('utf-8')
    # 公钥加密
    crypto = rsa.encrypt(content, pubkey)
    print ('加密后', crypto)
    return crypto, privkey
 
def rsa_decrypt(crypto, privkey):
    # 解密
    content = rsa.decrypt(crypto, privkey)
    # 解码
    content = content.decode('utf-8')
    print ('解密结果', content)

if __name__ == '__main__':
    crypto, privkey = rsa_encrypt('hello word')
    print(crypto)
    c = str(crypto)
    d = eval(c)
    rsa_decrypt(d, privkey)