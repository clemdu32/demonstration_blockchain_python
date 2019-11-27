from collections import OrderedDict
import binascii
import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
import requests
from pprint import pprint


class Transaction:

    def __init__(self, sender_address, sender_private_key, recipient_address, value):
        self.sender_address = sender_address
        self.sender_private_key = sender_private_key
        self.recipient_address = recipient_address
        self.value = value

    def __getattr__(self, attr):
        return self.data[attr]

    def to_dict(self):
        return OrderedDict({'sender_address': self.sender_address,
                            'recipient_address': self.recipient_address,
                            'value': self.value})

    def sign_transaction(self):
        """
        Sign transaction with private key
        """
        private_key = RSA.importKey(binascii.unhexlify(self.sender_private_key))
        signer = PKCS1_v1_5.new(private_key)
        h = SHA.new(str(self.to_dict()).encode('ascii'))
        return binascii.hexlify(signer.sign(h)).decode('ascii')


def new_wallet():
    random_gen = Crypto.Random.new().read
    private_key = RSA.generate(1024, random_gen)
    public_key = private_key.publickey()
    response = {
        'private_key': binascii.hexlify(private_key.exportKey(format='DER')).decode('ascii'),
        'public_key': binascii.hexlify(public_key.exportKey(format='DER')).decode('ascii')
    }

    return response


if __name__ == '__main__':
    node_address = input("Enter the IPv4:port of the node that you want to use to deal with the blockchain \n >")
    is_running = True
    while is_running:
        command = input('>')
        if command == "new-transaction":
            sender_address = input('Enter your public key : \n >')
            sender_private_key = input('Enter your private key : \n >')
            recipient_address = input("Recipients's public key : \n >")
            amount = input("Amount of the transaction : \n >")
            new_transaction = Transaction(sender_address, sender_private_key, recipient_address, amount)
            validated = input("Do you want to continue? (y or n) \n >")
            if validated == 'y':
                print("Transaction sending...")
                response = requests.post('http://' + node_address + '/transactions/new',
                                         {'sender_address': sender_address,
                                          'recipient_address': recipient_address,
                                          'amount': amount,
                                          'signature': new_transaction.sign_transaction()})
                print(response.json())
                del validated
            else:
                print("An error has been encountered!")
        elif command == "generate-wallet":
            wallet = new_wallet()
            print('Public Key : ' + wallet['public_key'] + '\n')
            print('Private Key : ' + wallet['private_key'] + '\n')
            print('Save them safely!')
        elif command == 'chain':
            response = requests.get('http://' + node_address + '/chain')
            if response.status_code == 200:
                pprint(response.json())
        elif command == 'exit':
            is_running = False
        else:
            print("Invalid command")
