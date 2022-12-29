import click
import sys
sys.path.append("..") 
import getpass
from Wallet import Wallet
from utils_cli import ( get_api, )
from configuration import ( Configuration, )


@click.command()
@click.option('-m', '--mnemonic-sentence', default='', prompt='Mnemonic sentence',
              help='Remembered mnemonic sentence to restore wallet.')
def restore_wallet(mnemonic_sentence):
    """Creates new wallet and store encrypted keystore file."""
    """
    Create new wallet account and save encrypted keystore
    :param configuration: loaded configuration file instance
    :param mnemonic_sentence: user's mnemonic sentence to restore wallet
    :param password: set password from keystore and used also as entropy for CSPRNG
    :return: restored wallet object and saved keystore path
    """
    passphrase = getpass.getpass('Passphrase: ')  # Prompt the user for a password of keystore file

    configuration = Configuration().load_configuration()

    wallet = Wallet(configuration).restore(mnemonic_sentence, passphrase)
    wallet.save_keystore(passphrase)

    click.echo('Account address: %s' % str(wallet.get_address()))
    click.echo('Account pub key: %s' % str(wallet.get_public_key()))
    click.echo('Keystore path: %s' % configuration.keystore_location + configuration.keystore_filename)
    click.echo('Remember these words to restore eth-wallet: %s' % wallet.get_mnemonic())

if __name__ == '__main__':
    restore_wallet()