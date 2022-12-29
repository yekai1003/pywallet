import click
import sys 
sys.path.append("..") 

from contract import ( Contract, )
# from infura import ( Infura, )
from configuration import ( Configuration, )
from web3 import Web3
import asyncio
# from brownie import  Contract
import os

# Create Infura Connection
# define "INFURA_PROVIDER" in your .env file
web3 = Web3(Web3.HTTPProvider(os.getenv("INFURA_PROVIDER")))

# contract Address
contractAddress = '0x0845d45E1D8b2e4c7583623Bed34b6D59Da0fBA3'

# Connect to rinkeby network
# doing this step just to read the Contract abi
# file but you can read the abi file manually with web3. py as well


# token = Contract(contractAddress)

# contract = web3.eth.contract(address=contractAddress, abi=token.abi)

# define function to handle events and print to the console
# You can also setup any action after listening to the event
def handle_event(event):
    print('event', event)
    print('dir(event)', dir(event))
    # print('toText',Web3.toText(event))
    # print('toHex',Web3.toHex(event))
    # print('toWei',Web3.toWei(event))
    # print('toInt',Web3.toInt(event))


# asynchronous defined function to loop
# this loop sets up an event filter and is looking for new entires for the "PairCreated" event
# this loop runs on a poll interval
async def log_loop(event_filter, poll_interval):
    while True:
        for PairCreated in event_filter.get_new_entries():
            handle_event(PairCreated)
        await asyncio.sleep(poll_interval)


# when main is called
# create a filter for the latest block and look for the "PairCreated" event for the uniswap factory contract
# run an async loop
# try to run the log_loop function above every 2 seconds

@click.command()
@click.option('-c', '--contract_address', default='', prompt='Contract address',
              help='Contract address.')
def event_listener(contract_address):
    """List all added tokens."""
    configuration = Configuration().load_configuration()
    contract_address = Web3.toChecksumAddress(contract_address)
    contract = Contract(configuration, contract_address)
    # print('contract.contract', contract.contract)
    # 监听合约里的 mint 函数里 emit 的 Transfer event：
    event_filter = contract.contract.events.Transfer.createFilter(fromBlock='latest')
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                log_loop(event_filter, 2)))
    finally:
        # close loop to free up system resources
        loop.close()



if __name__ == "__main__":
    event_listener()