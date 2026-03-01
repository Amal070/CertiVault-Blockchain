from web3 import Web3

# Connect to Ganache
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

if not web3.is_connected():
    print("❌ Blockchain not connected")
else:
    print("✅ Blockchain connected")

# Replace with your Ganache account address
account_address = "PASTE_ACCOUNT_ADDRESS"

# Replace with private key (click key icon in Ganache)
private_key = "PASTE_PRIVATE_KEY"

# Replace with deployed contract address
contract_address = "PASTE_CONTRACT_ADDRESS"

# Paste ABI JSON here
contract_abi = [
    # PASTE ABI HERE
]

contract = web3.eth.contract(
    address=contract_address,
    abi=contract_abi
)


def store_hash_on_blockchain(hash_value):

    nonce = web3.eth.get_transaction_count(account_address)

    transaction = contract.functions.storeCertificate(hash_value).build_transaction({
        'from': account_address,
        'nonce': nonce,
        'gas': 2000000,
        'gasPrice': web3.to_wei('20', 'gwei')
    })

    signed_tx = web3.eth.account.sign_transaction(transaction, private_key)

    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    return receipt.transactionHash.hex()


def verify_hash_from_blockchain(hash_value):

    return contract.functions.verifyCertificate(hash_value).call()