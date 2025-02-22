import os
from web3 import Web3
import json
from dotenv import load_dotenv

load_dotenv()
# Get the account from environment variables
account = os.getenv("ETH_ACCOUNT")
if not account:
    raise Exception("ETH_ACCOUNT environment variable must be set")

# Connect to your local Ganache node
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

# Load the ABI for the JobMatch contract from the Truffle build artifacts
with open("../blockchain/build/contracts/JobMatch.json") as f:
    contract_json = json.load(f)
    contract_abi = contract_json["abi"]

# Replace with your deployed contract address (from your Truffle deployment)
CONTRACT_ADDRESS = "0x6f1D300588336f33B0D2603BAeBEbB12B13Ba089"
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)

def store_prediction(job_title, reasoning, account):
    # Check if the account has already made a prediction
    if contract.functions.hasPredicted(account).call():
        raise Exception("This account has already made a prediction. Please use a different account.")
    
    tx_hash = contract.functions.storePrediction(job_title, reasoning).transact({
        'from': account,
        'gas': 1000000,
        'gasPrice': w3.to_wei('50', 'gwei'),
    })
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print("Transaction successful with hash:", tx_receipt['transactionHash'].hex())
    return tx_receipt

def get_all_predictions():
    count = contract.functions.getPredictionCount().call()
    predictions = []
    for i in range(count):
        user, job_title, reasoning, timestamp = contract.functions.getPrediction(i).call()
        predictions.append({
            'user': user,
            'job_title': job_title,
            'reasoning': reasoning,
            'timestamp': timestamp
        })
    return predictions

if __name__ == '__main__':
    preds = get_all_predictions()
    for pred in preds:
        print(f"User: {pred['user']}, Job Title: {pred['job_title']}, Reasoning: {pred['reasoning']}, Timestamp: {pred['timestamp']}")
