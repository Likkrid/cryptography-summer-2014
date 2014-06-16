# rpyc client
import rpyc
import ec
import random
import hashfun
import sys
from aes import AESCipher


def diffie_hellman():
	#BOB#
	domain, bob_pub_key, bob_priv_key = ec.get_keypair()

	conn = rpyc.connect("localhost", 18861, config = {"allow_public_attrs" : True})
	c = conn.root

	#Agree upon a public key
	c.send_pub_key(bob_pub_key)
	alice_pub_key = c.get_pub_key()
	print "Alice:\n", alice_pub_key

	secret_bob = bob_priv_key.a * alice_pub_key.Q

	print "Sharing secret..."
	secret_alice = c.share_secret(secret_bob)

	print "Secrets:\nAlice: %s\nBob %s\n" % (secret_alice, secret_bob)

	print "Encoding AES message [Sample message]..."
	ac = AESCipher(secret_bob.x)
	enc = ac.encrypt('Sample message')

	print "Sending encrypted message [%s]..." % enc
	c.decrypt(enc)

def naxos():
	#Keypair generation
	#BOB#
	domain, bob_pub_key, bob_priv_key = ec.get_keypair()

	#connecting to a server
	conn = rpyc.connect("localhost", 18861, config = {"allow_all_attrs" : True})
	c = conn.root

	alice_pub_key = c.exchange_pubkey(bob_pub_key)
	print 'Alice pub key', alice_pub_key

	bob_esk = random.getrandbits(32) #32 bitowy ciag losowy
	G = domain.P #nasz publiczny punkt na krzywej

	#exch_bob H1(esk_B, sk_B)
	exch_bob = hashfun.sha(hashfun.concat(bob_esk, bob_priv_key.a))
	exch_alice = c.exchange(G * exch_bob)

	S0 = alice_pub_key.Q * exch_bob #punkt
	S1 = (exch_alice) * bob_priv_key.a #punkt
	S2 = (exch_alice) * exch_bob

	session_key = hashfun.sha(hashfun.concat(S0.x.n, S1.x.n, S2.x.n))
        
	print 'Session key:', session_key
	
	#AES PART
	print "Encoding AES message [Sample message]..."
	ac = AESCipher(session_key)
	enc = ac.encrypt('Sample message')

	print "Sending encrypted message [%s]..." % enc
	c.decrypt(enc)


if __name__ == '__main__':
	#diffie_hellman()
	naxos()



