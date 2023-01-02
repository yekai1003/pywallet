import click
import sys
sys.path.append("..") 
import getpass
from Wallet import Wallet
from configuration import ( Configuration, )

@click.command()
@click.option(
    '-m', '--mnemonic-sentence', default='',
    prompt='Mnemonic sentence',
    help='Remembered mnemonic sentence to restore wallet.')
def restore_wallet(mnemonic_sentence):
    """
    从助记词和 passphrase 恢复钱包，存储加密的 keystore
    :param mnemonic_sentence: 使用助记词恢复钱包
    """
    # passphrase: 解密 keystore 的密码
    passphrase = getpass.getpass('Passphrase: ')
    # configuration: 从本地加载配置文件实例
    configuration = Configuration().load_configuration()

    wallet = Wallet(configuration)   \
              .restore(mnemonic_sentence, passphrase)
    wallet.save_keystore(passphrase)

    click.echo('Account address: %s' % str(wallet.get_address()))
    click.echo('Account pub key: %s' % str(wallet.get_public_key()))

if __name__ == '__main__':
    restore_wallet()