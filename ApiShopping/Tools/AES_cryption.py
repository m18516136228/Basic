#!/usr/bin/env python
# encoding: utf-8
'''
@author: duanqiyang
@project: ApiShopping
@file: AES_cryption.py
@time: 2019-12-17 09:47:22
@desc:
'''
from Crypto.Cipher import AES
import base64
from Tools.base64_en import ba64decode_u
from Tools.url_code import urldecode
import os
from Crypto import Random


class Aes_ECB(object):
    def __init__(self,key):
        self.key = key
        self.MODE = AES.MODE_ECB
        self.BS = AES.block_size
        self.pad = lambda s: s + (self.BS - len(s) % self.BS) * chr(self.BS - len(s) % self.BS)
        self.unpad = lambda s: s[0:-ord(s[-1])]

    # str不是16的倍数那就补足为16的倍数
    def add_to_16(value):
        while len(value) % 16 != 0:
            value += '\0'
        return str.encode(value)  # 返回bytes


    def AES_encrypt(self, text):
        aes = AES.new(Aes_ECB.add_to_16(self.key), self.MODE)  # 初始化加密器
        encrypted_text = str(base64.encodebytes(aes.encrypt(Aes_ECB.add_to_16(self.pad(text)))), encoding='utf-8').replace('\n', '')     #这个replace大家可以先不用，然后在调试出来的结果中看是否有'\n'换行符
        # 执行加密并转码返回bytes
        return encrypted_text

    # 解密
    def AES_decrypt(self, text):
        # 初始化加密器
        aes = AES.new(Aes_ECB.add_to_16(self.key), self.MODE)
        # 优先逆向解密base64成bytes
        base64_decrypted = base64.decodebytes(text.encode(encoding='utf-8'))
        decrypted_text = self.unpad(aes.decrypt(base64_decrypted).decode('utf-8'))
        decrypted_code = decrypted_text.rstrip('\0')
        return decrypted_code

class Aes_CBC:

    def add_to_16(self, value):
        while len(value) % 16 != 0:
            value += '\0'
        return str.encode(value)  # 返回bytes

    # 加密方法
    def encrypt_oracle(self, key, text):
        # iv=self.add_to_16(key)   #多了个iv
        # 偏移量 16个0
        iv = "0000000000000000"
        # 初始化加密器
        aes = AES.new(self.add_to_16(key), AES.MODE_CBC, self.add_to_16(iv))
        bs = AES.block_size
        pad2 = lambda s: s + (bs - len(s) % bs) * chr(bs - len(s) % bs)  # PKS7

        encrypt_aes = aes.encrypt(str.encode(pad2(text)))

        # 用base64转成字符串形式
        # 执行加密并转码返回bytes
        encrypted_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8')
        print(encrypted_text)
        # 和js的 结果相同 http://tool.chacuo.net/cryptaes
        return encrypted_text

    # 解密方法
    def decrypt_oralce(self, key, text):
        # 初始化加密器
        # 偏移量 16个0
        iv = "0000000000000000"
        aes = AES.new(self.add_to_16(key), AES.MODE_CBC, self.add_to_16(iv))
        # 优先逆向解密base64成bytes
        base64_decrypted = base64.decodebytes(text.encode(encoding='utf-8'))
        #
        decrypted_text = str(aes.decrypt(base64_decrypted), encoding='utf-8')  # 执行解密密并转码返回str
        unpad = lambda s: s[0:-ord(s[-1])]
        # PADDING = '\0'
        # print decrypted_text.rstrip(PADDING)  #zeropadding只见诶去掉结尾\0
        # print(unpad(decrypted_text))
        return unpad(decrypted_text)

if __name__ == '__main__':
    # ECB加密
    # en_text = Aes_ECB('18de677b90fcadbe').AES_encrypt('CCYQ|3paQlVuN2lWdkVFRHFMYjBSV|9999999999999')
    #
    # print('加密:',en_text)
    # print('解密:',Aes_ECB('18de677b90fcadbe').AES_decrypt(en_text))
    #
    # aa='Ym4yS2h5UWhYMkY1SVglMkJyWkxqQUF5cVBPbGolMkZiOVpMRHZDcjl5RUNHaFpHciUyQkNhJTJCajZOS21nOExtckV4OE5k'
    # kk=ba64decode_u(aa)
    # print(kk)
    # xx=urldecode(kk)
    # print(xx)
    # print('解密:', Aes_ECB('18de677b90fcadbe').AES_decrypt(str(xx)))

    #CBC加密
    aes = Aes_CBC()
    # 加密
    key = "12345678"
    enc_text = aes.encrypt_oracle(key, "wwww.baidu.com")

    # 解密
    dec_text = aes.decrypt_oralce(key, enc_text)
    print(key)
    print(enc_text)
    print(dec_text)