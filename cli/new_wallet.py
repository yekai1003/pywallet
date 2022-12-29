import click
import getpass
import sys
sys.path.append("..") 
from Wallet import ( Wallet )

from configuration import (Configuration,)

@click.command()
def new_wallet():
    """Creates new wallet and store encrypted keystore file."""
    # 提示用户输入密钥库文件的密码
    password = getpass.getpass('Passphrase from keystore: ')

    configuration = Configuration().load_configuration()

    wallet = Wallet(configuration).create(password)
    wallet.save_keystore(password)

    click.echo('Account address: %s' % str(wallet.get_address()))
    click.echo('Account pub key: %s' % str(wallet.get_public_key()))
    click.echo('Keystore path: %s' % configuration.keystore_location + configuration.keystore_filename)
    click.echo('Remember these words to restore eth-wallet: %s' % wallet.get_mnemonic())

if __name__ == '__main__':
    new_wallet()