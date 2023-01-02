from infura import ( Infura, )
from utils import ( get_abi_json,)

class Contract:
    """ERC20 代币的 Abstraction"""

    def __init__(self, configuration, address):
        self.conf = configuration
        self.address = address
        self.w3 = Infura().get_web3()
        # 获取指定合约地址上的合约对象
        self.contract = self.w3.eth.contract(address=address, abi=get_abi_json())
        self.contract_decimals = self.contract.functions.decimals().call()

    def add_new_contract(self, contract_symbol, contract_address):
        """Add ERC20 token to the wallet"""
        self.conf.add_contract_token(contract_symbol, contract_address)

    def get_balance(self, wallet_address):
        """Get wallet's ballance of self.contract"""
        return self.contract.functions.balanceOf(wallet_address).call() / (10 ** self.contract_decimals)

    def get_decimals(self):
        """返回“小数”位数"""
        return self.contract_decimals

    def get_erc20_contract(self):
        """
        Returns w3.eth.contract instance
        :return:
        """
        return self.contract
