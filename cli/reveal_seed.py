import click
import sys 
sys.path.append("..") 
import getpass
from Wallet import Wallet
from configuration import ( Configuration, )
from exceptions import ( InvalidPasswordException, )


@click.command()
def reveal_seed():
    """显示私钥 Reveals private key from encrypted keystore."""
    password = getpass.getpass('Password from keystore: ')  # Prompt the user for a password of keystore file
    configuration = Configuration().load_configuration()

    try:
        address = Wallet(configuration).get_address()
        pub_key = Wallet(configuration).get_public_key()
        wallet = Wallet(configuration).load_keystore(password)

        click.echo('Account prv key: %s' % str(wallet.get_private_key().hex()))
        click.echo('Account pub_key: %s' % str(pub_key))
        click.echo('Account address: %s' % str(address))

    except InvalidPasswordException:
        click.echo('Incorrect password!')

if __name__ == '__main__':
    reveal_seed()