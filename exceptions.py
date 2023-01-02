class InsufficientFundsException(Exception):
    """当用户想要发送ETH但地址余额不足时抛出"""
    pass

class InsufficientERC20FundsException(Exception):
    """当用户想要发送ERC-20但地址余额不足时抛出"""
    pass

class ERC20NotExistsException(Exception):
    """当用户想要操作钱包中不存在的 Token时抛出"""
    pass

class InvalidTransactionNonceException(Exception):
    """当出现重复的 nonce 或其他问题时抛出"""
    pass

class InvalidValueException(Exception):
    pass

class InvalidPasswordException(Exception):
    pass

class InfuraErrorException(Exception):
    """当钱包无法正确连接到 infura 节点时触发 """