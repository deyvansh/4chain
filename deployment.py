from web3 import Web3
import json
import solcx

GANACHE_URL = "http://127.0.0.1:7545"
PRIVATE_KEY = "0x1a00ba755ccb0dc9fc3cccd7d7f73c4af17267c5462b5aa9b847d9316aa77d74" 
def compile_contract():
    try:
        solcx.install_solc('0.8.0')
    except:
        pass
    
    solcx.set_solc_version('0.8.0')
    
    with open('contractstuff.sol', 'r') as file:
        contract_source = file.read()
    #
    #
    #
    #
    compiled_sol = solcx.compile_standard({
        "language": "Solidity",
        "sources": {
            "CertificateVerification.sol": {
                "content": contract_source
            }
        },
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                }
            }
        }
    }, solc_version="0.8.0")
    
    
    contract_interface = compiled_sol['contracts']['CertificateVerification.sol']['CertificateVerification']
    
    return {
        'abi': contract_interface['abi'],
        'bytecode': contract_interface['evm']['bytecode']['object']
    }

def deploy_contract():
   
    w3 = Web3(Web3.HTTPProvider(GANACHE_URL))
    
    if not w3.is_connected():
        print("Failed to connect to blockchain")
        return None
    
    print(" Connected to Ganache")
    

    contract_interface = compile_contract()
    print(" Contract compiled ")
    

    account = w3.eth.account.from_key(PRIVATE_KEY)
    print(f" Using account: {account.address}")
    
   
    contract = w3.eth.contract(
        abi=contract_interface['abi'],
        bytecode=contract_interface['bytecode']
    )
    
   
    transaction = contract.constructor().build_transaction({
        'chainId': 1337,
        'gas': 2000000,
        'gasPrice': w3.to_wei('20', 'gwei'),
        'nonce': w3.eth.get_transaction_count(account.address),
    })
    
    #
    #
    #
    #
    #
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    
    print("Waiting for deployment...")
    #
    #
    #
    # 
    #
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    

    contract_data = {
        'address': tx_receipt.contractAddress,
        'abi': contract_interface['abi'],
        'transaction_hash': tx_receipt.transactionHash.hex()
    }
    
    with open('contract_details.json', 'w') as f:
        json.dump(contract_data, f, indent=4)
    
    print(f" Contract deployed at: {tx_receipt.contractAddress}")
    print(f" Transaction hash: {tx_receipt.transactionHash.hex()}")
    print(" Contract details saved to contract_details.json")
    
    return tx_receipt.contractAddress

if __name__ == "__main__":
    deploy_contract()
