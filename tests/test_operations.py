from rolling_roles import check, send, GenericMethodTransaction, Operation, Chain
from rolling_roles.constants import GCAddr
from rolling_roles.utils import multi_or_one, MULTISENDS
from .utils import web3_gnosis, web3_eth

CURVE_USDC_USDT_REWARD_GAUGE = "0x7f90122BF0700F9E7e1F688fe926940E8839F353"

approve = GenericMethodTransaction(
    function_name="approve",
    function_args=[CURVE_USDC_USDT_REWARD_GAUGE, 1000],
    contract_address=GCAddr.USDT,
    contract_abi='[{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve",'
                 '"outputs":[{"name":"result","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"}]',
    operation=Operation.CALL,
    value=0,
)
add_liquidity = GenericMethodTransaction(
    function_name="add_liquidity",
    function_args=[[0, 0, 100], 0],
    contract_address=CURVE_USDC_USDT_REWARD_GAUGE,
    contract_abi='[{"stateMutability":"nonpayable","type":"function","name":"add_liquidity","inputs":[{"name":"_amounts","type":"uint256[3]"},'
                 '{"name":"_min_mint_amount","type":"uint256"}],"outputs":[{"name":"","type":"uint256"}],"gas":7295966}]',
    operation=Operation.CALL,
    value=0,
)

def test_multi_or_one_one():
    operation, contract_address, data = multi_or_one([approve], blockchain=Chain.GC)
    assert operation == Operation.CALL
    assert contract_address == GCAddr.USDT
    assert data == ("0x095ea7b30000000000000000000000007f90122bf0700f9e7e1f688fe926940e8839f353000000000000000000000000000000"
                    "00000000000000000000000000000003e8")

def test_multi_or_one_multi():
    operation, contract_address, data = multi_or_one([approve, add_liquidity], blockchain=Chain.GC)
    # when building more than one transaction the Multisend contract is used
    assert operation == Operation.DELEGATE_CALL
    assert contract_address == MULTISENDS[Chain.GC]
    assert data == ('0x8d80ff0a000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000'
                    '00000000000000000000000000000000172004ecaba5870353805a9f068101a40e0f32ed605c600000000000000000000000000'
                    '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000440'
                    '95ea7b30000000000000000000000007f90122bf0700f9e7e1f688fe926940e8839f35300000000000000000000000000000000'
                    '000000000000000000000000000003e8007f90122bf0700f9e7e1f688fe926940e8839f35300000000000000000000000000000'
                    '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000844515'
                    'cef3000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
                    '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000640000000000'
                    '0000000000000000000000000000000000000000000000000000000000000000000000000000000000'
                    )


def test_check_one(web3_gnosis):
    ROLES_MOD_ADDRESS = "0xB6CeDb9603e7992A5d42ea2246B3ba0a21342503"
    ACCOUNT = "0x7e19DE37A31E40eec58977CEA36ef7fB70e2c5CD"
    status = check(txs=[approve], role=2, account=ACCOUNT, roles_mod_address=ROLES_MOD_ADDRESS,
                   web3=web3_gnosis, blockchain=Chain.GC)
    assert status


def test_check_multi(web3_gnosis):
    ROLES_MOD_ADDRESS = "0xB6CeDb9603e7992A5d42ea2246B3ba0a21342503"
    ACCOUNT = "0x7e19DE37A31E40eec58977CEA36ef7fB70e2c5CD"
    status = check(txs=[approve, add_liquidity], role=2, account=ACCOUNT, roles_mod_address=ROLES_MOD_ADDRESS,
                   web3=web3_gnosis, blockchain=Chain.GC)
    assert status
