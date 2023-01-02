import click
import sys 
sys.path.append("..") 
from contract import ( Contract, )
from configuration import ( Configuration, )
from web3.exceptions import ( InvalidAddress, )
from exceptions import ( InfuraErrorException, )


@click.command()
@click.option('-c', '--contract_address', default='', prompt='Contract address',
              help='Contract address.')
@click.option('-s', '--symbol', default='', prompt='Token symbol',
              help='Token symbol.')

def add_token(contract_address, symbol):
    """Add new ERC20 contract.
       Adds new contract ERC20 token into config file with symbol and address
    """

    configuration = Configuration().load_configuration()

    try:
        contract = Contract(configuration, contract_address)
        contract.add_new_contract(symbol, contract_address)
        click.echo('New coin was added! %s %s' % (symbol, contract_address))
    except InvalidAddress:
        click.echo('Invalid address or wallet does not exist!')
    except InfuraErrorException:
        click.echo('Wallet is not connected to Ethereum network!')

if __name__ == '__main__':
    add_token()