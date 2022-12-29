import sys 
sys.path.append("..") 

from api import ( WalletAPI, )


def get_api():
    api = WalletAPI()
    return api