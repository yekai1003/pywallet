import click
from utils_cli import (
    get_api,
)
from configuration import (
    Configuration,
)


@click.command()
def get_wallet_info():
    """Get wallet account from encrypted keystore."""
    configuration = Configuration().load_configuration()
    api = get_api()

    address, pub_key = api.get_wallet(configuration)

    click.echo('Account address: %s' % str(address))
    click.echo('Account pub key: %s' % str(pub_key))

if __name__ == '__main__':
    get_wallet_info()