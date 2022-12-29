import json
import pprint
from eth_account import ( Account, )
from eth_keys import ( keys, )
from utils import ( create_directory, )
from infura import ( Infura, )
from exceptions import ( InvalidPasswordException,)
from mnemonic import ( Mnemonic )


class Wallet(object):
    def __init__(self, configuration):
        self.conf = configuration
        self.account = None
        self.w3 = None
        self.mnemonic_sentence = None

    def create(self, password='', restore_sentence=None):
        """
        create 函数可以创建新钱包，
        :param password: 作为存储在 configuration 中的的钱包密码和随机的噪声
           （钱包软件在创建私钥 Private Key 时，有必要引入随机性来保证密码学上的私钥安全）
        :param restore_sentence: 用于从助记词恢复钱包
        :return: 带有私钥的对象
        """
        extra_entropy = password
        
        # 助记词对象 
        mnemonic = Mnemonic("english")
        if restore_sentence is None:
            # 生成助记词
            self.mnemonic_sentence = mnemonic.generate(strength=128)
        else:
            self.mnemonic_sentence = restore_sentence

        # 1. 通过助记词和随机噪声生成种子seed
        ## 如果用户输入了助记词和 password，那么 seed 就是之前生成过的确定值，从而私钥和 address 也是确定的
        seed = mnemonic.to_seed(self.mnemonic_sentence, extra_entropy)
        # 2. 获取 seed中的masterPrivateKey
        master_private_key = seed[32:]
        # 3. 借助 eth_account 库的 Account 对象利用 masterPrivateKey 生成一个账户对象 account
        self.account = Account.privateKeyToAccount(master_private_key)

        # update config address
        self.conf.update_eth_address(self.account.address)
        # convert 类似 b'\xfe1h\xc5B\x14tV\xbe\xfe.. to 0xfe3168c54..
        priv_key = keys.PrivateKey(self.account.privateKey)  
        # update config public key
        pub_key = priv_key.public_key
        self.conf.update_public_key(pub_key.to_hex())

        self.w3 = Infura().get_web3()
        return self

    def restore(self, mnemonic_sentence, password):
        """
        Recreates wallet from mnemonic sentence
        :param mnemonic_sentence: remembered user mnemonic sentence
        :type mnemonic_sentence: str
        :param password: password from keystore which is used as entropy too
        :return: wallet
        """
        return self.create(password, mnemonic_sentence)

    def get_account(self):
        """
        Returns account
        :return: account object
        """
        return self.account

    def set_account(self, private_key):
        """
        Creates new account from private key with appropriate address
        :param private_key: in format hex str/bytes/int/eth_keys.datatypes.PrivateKey
        :return: currently created account
        """
        self.account = Account.privateKeyToAccount(private_key)
        return self.account

    def save_keystore(self, password):
        """
        将[私钥+passphrase] 通过 Account.encrypt 加密成 keystore JSON 文件
          保存在本地目录中。
        :param password: 用户输入的 passphrase
        :return: 存储路径
        """
        create_directory(self.conf.keystore_location)
        keystore_path = self.conf.keystore_location + self.conf.keystore_filename
        encrypted_private_key = Account.encrypt(self.account.privateKey, password)
        with open(keystore_path, 'w+') as outfile:
            json.dump(encrypted_private_key, outfile, ensure_ascii=False)
        return keystore_path

    def load_keystore(self, password):
        """
        从解密的 keystore 中加载钱包帐户（私钥）
        :param password: 用户输入的 passphrase
        :return:  account 钱包账户实例
        """
        keystore_path = self.conf.keystore_location + self.conf.keystore_filename
        with open(keystore_path) as keystore:
            keyfile_json = json.load(keystore)

        try:
            private_key = Account.decrypt(keyfile_json, password)
        except ValueError:
            raise InvalidPasswordException()

        self.set_account(private_key)
        return self

    def get_mnemonic(self):
        """
        Returns BIP39 mnemonic sentence
        :return: mnemonic words
        """
        return self.mnemonic_sentence

    def get_private_key(self):
        """
        Returns wallet private key
        :return: private key
        """
        return self.account.privateKey  # to print private key in hex use account.privateKey.hex() function

    def get_public_key(self):
        """
        Returns wallet public key
        :return: public key
        """
        return self.conf.public_key

    def get_address(self):
        """
        Returns wallet address
        :return: address
        """
        return self.conf.eth_address

    def get_balance(self, address):
        """
        Read balance from the Ethereum network in ether
        :return: number of ether on users account
        """
        self.w3 = Infura().get_web3()
        eth_balance = self.w3.fromWei(self.w3.eth.getBalance(address), 'ether')
        return eth_balance


if __name__ == '__main__':
    pass