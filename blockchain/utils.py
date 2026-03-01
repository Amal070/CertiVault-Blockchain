from web3 import Web3
from eth_account import Account
from .config import GANACHE_RPC, PRIVATE_KEY, CONTRACT_ADDRESS


# Paste ABI returned from deploy here
contract_abi = [
    {
        'inputs': [{'internalType': 'string', 'name': '', 'type': 'string'}],
        'name': 'certificates',
        'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}],
        'stateMutability': 'view',
        'type': 'function'
    },
    {
        'inputs': [{'internalType': 'string', 'name': '_hash', 'type': 'string'}],
        'name': 'storeCertificate',
        'outputs': [],
        'stateMutability': 'nonpayable',
        'type': 'function'
    },
    {
        'inputs': [{'internalType': 'string', 'name': '_hash', 'type': 'string'}],
        'name': 'verifyCertificate',
        'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}],
        'stateMutability': 'view',
        'type': 'function'
    }
]


# Connect to Ganache
web3 = Web3(Web3.HTTPProvider(GANACHE_RPC))

if not web3.is_connected():
    raise Exception("❌ Blockchain not connected")


# Load contract
contract = web3.eth.contract(
    address=CONTRACT_ADDRESS,
    abi=contract_abi
)

# Load account
account = Account.from_key(PRIVATE_KEY)
account_address = account.address


# -----------------------------
# Store Certificate Hash
# -----------------------------
def store_hash_on_blockchain(hash_value):

    nonce = web3.eth.get_transaction_count(account_address)

    transaction = contract.functions.storeCertificate(hash_value).build_transaction({
        "from": account_address,
        "nonce": nonce,
        "gas": 2000000,
        "gasPrice": web3.eth.gas_price,
    })

    signed_tx = account.sign_transaction(transaction)

    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)

    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    return receipt.transactionHash.hex()


# -----------------------------
# Verify Certificate Hash
# -----------------------------
def verify_hash_from_blockchain(hash_value):

    return contract.functions.verifyCertificate(hash_value).call()