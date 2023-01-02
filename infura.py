from web3 import ( Web3, )
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")
infura_url = "https://goerli.infura.io/v3/"+API_KEY

class Infura:
    def __init__(self):
        self.web3 = Web3(Web3.HTTPProvider(infura_url))

    def get_web3(self):
        return self.web3