import click
import sys 
sys.path.append("..") 
from Wallet import Wallet
from contract import Contract
from configuration import Configuration
from web3.exceptions import *
from exceptions import *


@click.command()
@click.option('-t', '--token', default=None,
              help='Token symbol.')
def get_balance(token):
    """获取账户余额."""
    configuration = Configuration().load_configuration()
    wallet_address = Wallet(configuration).get_address()
    try:
        if token is None:
            eth_balance = Wallet(configuration).get_balance(wallet_address)
            click.echo('Balance on address %s is: %sETH' % (wallet_address, eth_balance))

        if token is not None:
            try:  # check if token is added to the wallet
                contract_address = configuration.contracts[token]
            except KeyError:
                raise ERC20NotExistsException()
            contract = Contract(configuration, contract_address)
            token_balance = contract.get_balance(wallet_address)

            # token_balance, address = get_balance(configuration, token)
            click.echo('Balance on address %s is: %s%s' % (wallet_address, token_balance, token))
    except InvalidAddress:
        click.echo('Invalid address or wallet does not exist!')
    except InfuraErrorException:
        click.echo('Wallet is not connected to Ethereum network!')
    except ERC20NotExistsException:
        click.echo('This token is not added to the wallet!')

if __name__ == '__main__':
    get_balance()