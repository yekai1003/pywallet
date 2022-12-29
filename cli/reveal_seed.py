import click
import sys 
sys.path.append("..") 
import getpass
from utils_cli import ( get_api, )
from configuration import ( Configuration, )
from exceptions import ( InvalidPasswordException, )


@click.command()
def reveal_seed():
    """Reveals private key from encrypted keystore."""
    password = getpass.getpass('Password from keystore: ')  # Prompt the user for a password of keystore file

    configuration = Configuration().load_configuration()
    api = get_api()

    try:
        wallet = api.get_private_key(configuration, password)
        address, pub_key = api.get_wallet(configuration)
        click.echo('Account prv key: %s' % str(wallet.get_private_key().hex()))
        click.echo('Account pub_key: %s' % str(pub_key))
        click.echo('Account address: %s' % str(address))

    except InvalidPasswordException:
        click.echo('Incorrect password!')


if __name__ == '__main__':
    reveal_seed()