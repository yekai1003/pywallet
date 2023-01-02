from web3 import Web3
import time
from Wallet import ( Wallet )
from transaction import ( Transaction, )
from infura import ( Infura, )
from exceptions import (
    InsufficientFundsException,
    InvalidValueException,
    InsufficientERC20FundsException,
    ERC20NotExistsException,
)
from contract import ( Contract, )
from web3.exceptions import (
    InvalidAddress,
)
from decimal import (
    Decimal,
)


class WalletAPI:

    @staticmethod
    def get_network(configuration):
        """
        Returns connected network (Mainnet, Ropsten )
        :param configuration: loaded configuration file instance
        :return: network number defined in EIP155
        """
        return configuration.network

    @staticmethod
    def get_private_key(configuration, keystore_password):
        """
        Get account private key from default keystore location
        :param configuration: loaded configuration file instance
        :param keystore_password: user password from keystore
        :return: account object
        """
        wallet = Wallet(configuration).load_keystore(keystore_password)

        return wallet

    @staticmethod
    def get_wallet(configuration):
        """
        Get account address and private key from default keystore location
        :param configuration: loaded configuration file instance
        :return: account object
        """
        address = Wallet(configuration).get_address()
        pub_key = Wallet(configuration).get_public_key()

        return address, pub_key


    @staticmethod
    def add_contract(configuration, contract_symbol, contract_address):
        """
        Adds new contract ERC20 token into config file with symbol and address
        :param configuration: configuration file
        :param contract_symbol: contract symbol
        :param contract_address: contract address
        :return:
        """
        contract = Contract(configuration, contract_address)
        contract.add_new_contract(contract_symbol, contract_address)
