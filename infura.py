from web3 import ( Web3, )
from exceptions import ( InfuraErrorException )
from dotenv import load_dotenv
import os

load_dotenv()
PRIVATEKEY = os.getenv("PRIVATEKEY")
infura_url = "https://goerli.infura.io/v3/"+PRIVATEKEY
# print(infura_url)

class Infura:
    def __init__(self):
        self.web3 = Web3(Web3.HTTPProvider(infura_url))

    def get_web3(self):
        return self.web3