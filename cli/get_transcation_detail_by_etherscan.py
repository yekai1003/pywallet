import sys 
sys.path.append("..") 
import pickle
from infura import ( Infura, )
import click
# from configuration import Configuration
import requests as rq
import pprint
"""
Get a list of 'Normal' Transactions By Address
 - https://docs.etherscan.io/api-endpoints/accounts#get-a-list-of-normal-transactions-by-address

https://docs.etherscan.io/v/goerli-etherscan/api-endpoints/accounts#get-a-list-of-normal-transactions-by-address

"""



def get_token_transcation_detail():
    """too slow, deprecated"""

    """List all added tokens."""
    w3 = Infura().get_web3()
    """
    # 交易 hash 可以查
    print(w3.eth.getTransaction("0xd6b622f07a29e5cec855745d26dd87c699be99c17d2847cbd685c9825cdd8ac2"))
    """
    ending_blocknumber = w3.eth.blockNumber
    starting_blocknumber = ending_blocknumber - 100
    # 过滤区块并查找涉及该地址的交易
    blockchain_address = "0xfb10f18da15d70771cbceb2dbdb443887663278f"
    
    getTransactions(w3, starting_blocknumber, ending_blocknumber, blockchain_address)


def getTransactions(w3, start, end, address):
    """too slow, deprecated"""

    ''' 
    函数遍历每个块中的交易，并检查 to 字段中的地址是否与我们在 blockchain_address 中设置的地址匹配。
    此外，它会将找到的 transaction 写入 pickle 文件
    。'''
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
    

@click.command()
@click.option('-d', '--address', default='', prompt='address to scan:',
              help='input Ethereum address to list transactions.')
@click.option('-t', '--type_tx', default='normal', prompt='transaction type: {normal/token}',
              help='input Ethereum address to list transactions.')
def get_transcation_detail_by_etherscan(address, type_tx):
    """
    [https://etherscan.io/register] [https://etherscan.io/myapikey]
    :param type_tx: 
     - normal 是 2 个地址之间的互相转账交易
     - token 类型是合约和地址之间的交互交易
     分别对应着参数中的 txlist 或 tokentx
    """
    tx_type_map = {"normal": "txlist", "token": "tokentx"}
    ETHERSCAN_API_KEY = '7KRJKR5DI9RD6YX73JF7278KM9U6AP2HUB'
    base_url = "https://api-goerli.etherscan.io/api\
                   ?module=account\
                   &action={}\
                   &address={}\
                   &startblock=0\
                   &endblock=99999999\
                   &page=1&offset=100&sort=asc\
                   &apikey={}\
    ".format( tx_type_map[type_tx], address, ETHERSCAN_API_KEY).replace(' ','')
    print('base_url', base_url)
    res = rq.get(base_url)
    data = res.json()
    pprint.pprint(data["result"])


if __name__ == '__main__':
    # 0x611e5Bd6Db5a44D645C447aB6F413709f044A12e
    get_transcation_detail_by_etherscan()