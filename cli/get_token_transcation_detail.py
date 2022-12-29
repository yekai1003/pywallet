import sys 
sys.path.append("..") 
import pickle
from infura import ( Infura, )
import click
from utils_cli import (
    get_api,
)
from configuration import (
    Configuration,
)

@click.command()
def get_token_transcation_detail():
    """List all added tokens."""
    w3 = Infura().get_web3()
    """
    # 交易 hash 可以查
    print(w3.eth.getTransaction("0xd6b622f07a29e5cec855745d26dd87c699be99c17d2847cbd685c9825cdd8ac2"))
    """
    ending_blocknumber = w3.eth.blockNumber
    starting_blocknumber = ending_blocknumber - 10000 
    # 过滤区块并查找涉及该地址的交易
    blockchain_address = "0xfb10f18da15d70771cbceb2dbdb443887663278f"
    
    getTransactions(w3, starting_blocknumber, ending_blocknumber, blockchain_address)


def getTransactions(w3, start, end, address):
    '''This function takes three inputs, a starting block number, ending block number
    and an Ethereum address. The function loops over the transactions in each block and
    checks if the address in the to field matches the one we set in the blockchain_address.
    Additionally, it will write the found transactions to a pickle file for quickly serializing and de-serializing
    a Python object.'''
    # create an empty dictionary we will add transaction data to
    tx_dictionary = {}

    print(f"Started filtering through block number {start} to {end} for transactions involving the address - {address}...")
    for x in range(start, end):
        block = w3.eth.getBlock(x, True)
        for transaction in block.transactions:
            if transaction['to'] == address or transaction['from'] == address:
                print('transaction', transaction)
                with open("transactions.pkl", "wb") as f:
                    hashStr = transaction['hash'].hex()
                    tx_dictionary[hashStr] = transaction
                    pickle.dump(tx_dictionary, f)
                f.close()
    print(f"Finished searching blocks {start} through {end} and found {len(tx_dictionary)} transactions")
    

if __name__ == '__main__':
    get_token_transcation_detail()