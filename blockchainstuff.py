from web3 import Web3
import json
import os

GANACHE_URL = "http://127.0.0.1:7545"
PRIVATE_KEY = "0x1a00ba755ccb0dc9fc3cccd7d7f73c4af17267c5462b5aa9b847d9316aa77d74"  
CONTRACT_ADDRESS = "0x743347C7BDF07c9660945077FfD0F64393cbC6Cb" 

CONTRACT_ABI = json.loads('[{"inputs":[{"internalType":"string","name":"_cid","type":"string"},{"internalType":"string","name":"_hash","type":"string"}],"name":"storeCertificate","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"_cid","type":"string"}],"name":"verifyCertificate","outputs":[{"internalType":"bool","name":"","type":"bool"},{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"","type":"string"}],"name":"certificates","outputs":[{"internalType":"string","name":"hash","type":"string"},{"internalType":"uint256","name":"timestamp","type":"uint256"},{"internalType":"bool","name":"exists","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}]')

def init_web3():
    try:
        w3 = Web3(Web3.HTTPProvider(GANACHE_URL))
        if not w3.is_connected():
            raise Exception(f"Failed to connect to Ganache at {GANACHE_URL}. Make sure Ganache is running.")
        print(f" ganesh url {GANACHE_URL}")
        return w3
    except Exception as e:
        raise Exception(f"Blockchain connection failed: {str(e)}")

#conso
def get_contract():
    try:
        w3 = init_web3()
        contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)
        print(f"cont add: {CONTRACT_ADDRESS}")
        return w3, contract
    except Exception as e:
        raise Exception(f"Failed to load contract: {str(e)}")

def store_certificate(cid, file_hash):
    try:
        print(f" Storing certificate on blockchain...")
        print(f"   CID: {cid}")
        print(f"   Hash: {file_hash[:20]}...")
        
        w3, contract = get_contract()
        
        
        if not PRIVATE_KEY or len(PRIVATE_KEY) != 66:
            raise Exception(f"Invalid private key format. Expected 66 characters, got {len(PRIVATE_KEY) if PRIVATE_KEY else 0}")
        
        #  acc
        account = w3.eth.account.from_key(PRIVATE_KEY)
        
        if not hasattr(account, 'address') or not account.address:
            raise Exception("Failed to create account from private key - account object is empty")
        
        print(f" acc add: {account.address}")
        
        balance = w3.eth.get_balance(account.address)
        balance_eth = w3.from_wei(balance, 'ether')
        print(f"pls bal : {balance_eth} ETH")
        
        if balance == 0:
            raise Exception("Account has no ETH for gas fees")
        
        nonce = w3.eth.get_transaction_count(account.address)
        
        transaction = contract.functions.storeCertificate(cid, file_hash).build_transaction({
            'chainId': 1337,  
            'gas': 200000,   
            'gasPrice': w3.to_wei('20', 'gwei'),
            'nonce': nonce,
        })
        
        print(f" Gas req: {transaction['gas']}")

        #
        #
        #
        #
        #
        
        signed_txn = w3.eth.account.sign_transaction(transaction, private_key=PRIVATE_KEY)
        
      
        if hasattr(signed_txn, 'raw_transaction'):
            raw_tx = signed_txn.raw_transaction
        else:
            raw_tx = signed_txn.rawTransaction
            
        tx_hash = w3.eth.send_raw_transaction(raw_tx)
        
        print(f" Transaction sent: {tx_hash.hex()}")
        
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=60)
        
        print(f"Certificate stored successfully!")
        print(f"   Block: {tx_receipt.blockNumber}")
        print(f"   Gas used: {tx_receipt.gasUsed}")
        
        return tx_receipt.transactionHash.hex()
        
    except Exception as e:
        print(f" Blockchain storage failed: {str(e)}")
        raise Exception(f"Failed to store certificate on blockchain: {str(e)}")

#
#
#
#
#
def verify_certificate(cid):
    try:
        print(f" Verifying certificate: {cid}")
        w3, contract = get_contract()
        
        result = contract.functions.verifyCertificate(cid).call()
        exists = result[0]
        stored_hash = result[1]
        
        print(f" Verification result: {'Found' if exists else 'Not found'}")
        
        return {
            'exists': exists,
            'hash': stored_hash,
            'verified': exists
        }
        
    except Exception as e:
        print(f"Verification failed: {str(e)}")
        raise Exception(f"Failed to verify certificate: {str(e)}")


def get_certificate_details(cid):
    try:
        w3, contract = get_contract()
        
       
        result = contract.functions.certificates(cid).call()
        certificate_hash = result[0]
        timestamp = result[1]
        exists = result[2]
        
        return {
            'hash': certificate_hash,
            'timestamp': timestamp,
            'exists': exists
        }
        
    except Exception as e:
        print(f" Failed to get certificate details: {str(e)}")
        raise Exception(f"Failed to get certificate details: {str(e)}")


def test_connection():
    try:
        w3 = init_web3()
        print(f" Web3 version: {w3.api}")
        print(f" Latest block: {w3.eth.block_number}")
        print(f" Chain ID: {w3.eth.chain_id}")
        
        account = w3.eth.account.from_key(PRIVATE_KEY)
        print(f" Account address: {account.address}")
        
        balance = w3.eth.get_balance(account.address)
        print(f" Account balance: {w3.from_wei(balance, 'ether')} ETH")
        
        return True
    except Exception as e:
        print(f" Connection test failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing blockchain connection...")
    test_connection()
