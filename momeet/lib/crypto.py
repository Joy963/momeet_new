#!/usr/bin/env python
#-*- coding: utf-8 -*-
import struct
from Crypto.Cipher import ARC4


class IdCipher(object):
    MAX = 4294967295

    def __init__(self, secret_key):
        self.secret_key = secret_key

    def encrypt(self, id):
        obj = ARC4.new(self.secret_key)
        ciph = obj.encrypt(struct.pack('I', id))
        return struct.unpack('I', ciph)[0]

    def decrypt(self, ciph):
        obj = ARC4.new(self.secret_key)
        id = obj.decrypt(struct.pack('I', ciph))
        return struct.unpack('I', id)[0]

rhct_crypto_key = 'Momeet^!'  # 加密key
id_cipher = IdCipher(rhct_crypto_key)
id_encrypt = id_cipher.encrypt
id_decrypt = id_cipher.decrypt
