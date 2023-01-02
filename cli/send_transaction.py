import click
import sys 
import time
sys.path.append("..") 
import getpass
from contract import ( Contract, )
from Wallet import ( Wallet )
from infura import ( Infura, )
from configuration import ( Configuration, )
from exceptions import *
from web3.exceptions import ( InvalidAddress, )


@click.command()
@click.option('-t', '--to', default='', prompt='To address:',
              help='Ethereum address where to send amount.')
@click.option('-v', '--value', default='', prompt='Value to send:',
              help='Ether value to send.')
@click.option('--token', default=None,
              help='Token symbol.')
def send_transaction(to, value, token):
    """
    签署和发送交易 Sign and send transaction.
    :param to: 接受者的 address
    :param token_symbol: None表示发送ETH； 否则发送 ERC20 Token 
    :param gas_price_speed: gas price 将乘以这个数字来加速交易
    """
    # 从用户输入读取 passphrase
    passphrase = getpass.getpass('passphrase from keystore: ')
    # load 本地的 keystore file
    configuration = Configuration().load_configuration()
    to_address = to
    wallet = Wallet(configuration).load_keystore(passphrase)
    web3 = Infura().get_web3()

    try:
        # send ETH 交易
        if token is None:

            try: float(value)  # 输入检查
            except ValueError: raise InvalidValueException()
                
            # 交易对象构建 transaction object
            raw_txn = {
                'nonce': web3.eth.getTransactionCount(wallet.get_address()),
                'from': wallet.get_address(),
                'to': to_address,
                'value': web3.toWei(value, 'ether'),
                'gasPrice': 25000000000,
                'chainId': 5  # goerli Testnet  
            }
            
            # 执行消息调用或交易并返回预估消耗的 gas fee
            gas = web3.eth.estimateGas(raw_txn)
            raw_txn['gas'] = gas # 修正 gas
            # 使用私钥签署交易
            signed_tx = web3.eth.account.signTransaction(raw_txn, wallet.get_account().privateKey)
            # 发送已签名和被序列化的交易对象；返回 HexBytes 类型的 txhash
            tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
            
            print("Transaction hash: " , tx_hash.hex())
            
        # send erc20 transaction
        else:
            try:  # check if token symbol is added to the wallet
                contract_address = configuration.contracts[token]
            except KeyError:
                raise ERC20NotExistsException()
            # 构建一个 contract 对象，方便后续调用方法
            contract = Contract(configuration, contract_address)
            # 获取代币精度，一般是 18 位
            erc20_decimals = contract.get_decimals()
            # 获取 web3.py 的客户端对象，用来调用链上合约内的方法
            contract_w3 = contract.contract
            # 把 Token 数量改造成合约熟悉的格式（如 18 位）
            token_amount = int(float(value) * (10 ** erc20_decimals))
            # 获取钱包余额，检查是否足够转账
            erc20_balance = contract.get_balance(wallet.get_address())
            if float(value) > erc20_balance:
                raise InsufficientERC20FundsException()

            print('token_amount will be sent ', token_amount )
            print(f"Receiver balance: {contract_w3.functions.balanceOf(to_address).call()} {token} Tokens.")
            # 构建 transaction 交易对象
            # data：调用合约的 transfer 函数，参数分别是 address 和 amt
            raw_txn = {
                "from": wallet.get_address(),
                "gasPrice": web3.eth.gasPrice,
                "gas": 500000,
                "to": contract_address,
                "value": "0x0",
                "data": contract_w3.encodeABI('transfer', args=(to_address, token_amount)),
                "nonce": web3.eth.getTransactionCount(wallet.get_address())
            }
            # 签署交易
            signed_txn = web3.eth.account.signTransaction(raw_txn, wallet.get_account().privateKey)
            # 发送交易
            tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
            print("tx hash: ",tx_hash)
            # 等待交易执行成功 ...
            while True:
                tx_receipt = web3.eth.getTransactionReceipt(tx_hash)
                if tx_receipt is None:
                    print('.', end='', flush=True)
                    time.sleep(0.2)
                else:
                    print("\nTransaction mined!")
                    print(f"Receiver balance: {contract_w3.functions.balanceOf(to_address).call()} {token} Tokens.")
                    break

    except InsufficientFundsException:
        click.echo('Insufficient ETH funds! Check balance on your address.')
    except InsufficientERC20FundsException:
        click.echo('Insufficient ERC20 token funds! Check balance on your address.')
    except InvalidAddress:
        click.echo('Invalid recipient(to) address!')
    except InvalidValueException:
        click.echo('Invalid value to send!')
    except InvalidPasswordException:
        click.echo('Incorrect password!')
    except InfuraErrorException:
        click.echo('Wallet is not connected to Ethereum network!')
    except ERC20NotExistsException:
        click.echo('This token is not added to the wallet!')

if __name__ == '__main__':
    send_transaction()