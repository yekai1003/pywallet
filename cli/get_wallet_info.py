import click
import sys
sys.path.append("..") 
from configuration import Configuration
from Wallet import Wallet

@click.command()
def get_wallet_info():
    """Get wallet account from encrypted keystore."""
    configuration = Configuration().load_configuration()

    address = Wallet(configuration).get_address()
    pub_key = Wallet(configuration).get_public_key()

    click.echo('Account address: %s' % str(address))
    click.echo('Account pub key: %s' % str(pub_key))

if __name__ == '__main__':
    get_wallet_info()