import rpyc
import ec
from aes import AESCipher
import base64
import random
import hashfun

#ALICE#
class MyService(rpyc.Service):
    def on_connect(self):
        
        #Diffie Hellman
        self.domain, self.alice_pub_key, self.alice_priv_key = ec.get_keypair()
        self.bob_pub_key = None

        #Naxos

        self.alice_esk = random.getrandbits(32)
        G = self.domain.P #nasz publiczny punkt na krzywej
        self.exch_alice = hashfun.sha(hashfun.concat(self.alice_esk, self.alice_priv_key.a))


    def on_disconnect(self):
        # code that runs when the connection has already closed
        # (to finalize the service, if needed)
        pass

    def exposed_exchange_pubkey(self, bob_pub_key):
        self.bob_pub_key = bob_pub_key
        return self.alice_pub_key

    def exposed_send_pub_key(self, bob_pub_key):
        self.bob_pub_key = bob_pub_key
        print "Receiving public key..."
        print "Bob: ", bob_pub_key

    def exposed_get_pub_key(self):
        print "Sending public key..."
        return self.alice_pub_key

    def exposed_share_secret(self, secret_bob):
        print "Sharing secret..."
        self.secret_bob = secret_bob
        self.secret_alice = self.alice_priv_key.a * self.bob_pub_key.Q

        print "Secrets:\nAlice: %s\nBob %s\n" % (self.secret_alice, secret_bob)

        return self.secret_alice

    def exposed_decrypt(self, msg):
        print 'Received hash. Printing message...'
        print msg
        ac = AESCipher(self.session_key)#secret_alice.x)
        dec = ac.decrypt(msg)
        print dec
        
    def exposed_domain(self):
        print self.domain.P

    def exposed_exchange(self, exch_bob):
        print "Exchanging ephemeral secret keys... "
        self.exch_bob = exch_bob

        G = self.domain.P

        S0 = (self.exch_bob) * self.alice_priv_key.a # PUNKT
        S1 = self.bob_pub_key.Q * self.exch_alice #Punkt
        S2 = (self.exch_bob) * self.exch_alice

        self.session_key = hashfun.sha(hashfun.concat(S0.x.n, S1.x.n, S2.x.n))
        print 'Session key', self.session_key
        return G * self.exch_alice

if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(MyService, port = 18861, protocol_config= {"allow_all_attrs":True})
    t.start()