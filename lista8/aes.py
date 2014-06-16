# -*- coding: utf-8 -*-
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Hash import SHA512
import base64
import os



class AESCipher:
	def __init__( self, key ):
		self.BS = 16
		self.pad = lambda s: s + (self.BS - len(s) % self.BS) * chr(self.BS - len(s) % self.BS) 
		self.unpad = lambda s : s[0:-ord(s[-1])]

		h = SHA512.new()
		h.update(str(key))
		self.key = h.hexdigest()[:16]

	def encrypt( self, raw ):
		raw = self.pad(raw)
		iv = Random.new().read( AES.block_size )
		cipher = AES.new( self.key, AES.MODE_CBC, iv )
		return base64.b64encode( iv + cipher.encrypt( raw ) ) 

	def decrypt( self, enc ):
		enc = base64.b64decode(enc)
		iv = enc[:16]
		cipher = AES.new(self.key, AES.MODE_CBC, iv )
		return self.unpad(cipher.decrypt( enc[16:] ))