import logging
from typing import Dict, List

from web3 import Web3
from .roles_modifier import RolesMod
from .constants import Blockchain
from .generic_method import TxData
from .utils import multi_or_one

logger = logging.getLogger(__name__)


def check(txs: List[TxData],
          role: int,
          account: str,
          roles_mod_address: str,
          blockchain: Blockchain,
          web3: Web3,
          block='latest'
          ) -> bool:
    """Test the transaction with static call

    Args:
        txs (List[GenericMethodTransaction]): list of transactions
        role (int): role that wants to execute
        account (str): account that wants to execute
        roles_mod_address (str): address to call execTransactionWithRole
        blockchain (Blockchain)
        web3 (Web3)

    Returns:
        bool: status
    """
    tx_data = multi_or_one(txs, blockchain)
    roles_mod = RolesMod(
        role=role,
        contract_address=roles_mod_address,
        account=account,
        operation=tx_data.operation,
        web3=web3,
        value=tx_data.value
    )
    return roles_mod.check(tx_data.contract_address, tx_data.data, block=block)


def send(txs: List[TxData],
         role: int,
         private_key: str,
         roles_mod_address: str,
         blockchain: Blockchain,
         web3: Web3,
         ) -> bool:
    """Send transactions to the blockchain.

    Args:
        txs (List[TxData]): list of transactions
        role (int): role that wants to execute
        private_key (str): to access the EOA
        roles_mod_address (str): address to call execTransactionWithRole
        blockchain (Blockchain)
        web3 (Web3)

    Returns:
        (bool) status
    """
    tx_data = multi_or_one(txs, blockchain)
    roles_mod = RolesMod(
        role=role,
        contract_address=roles_mod_address,
        private_key=private_key,
        operation=tx_data.operation,
        web3=web3,
        value=tx_data.value
    )
    roles_mod_execute = roles_mod.execute(tx_data.contract_address, tx_data.data)
    logger.info('building receipt....')
    roles_mod_tx1 = roles_mod.get_tx_receipt(roles_mod_execute)
    logger.info(roles_mod_tx1)
    return roles_mod_tx1.status == 1
