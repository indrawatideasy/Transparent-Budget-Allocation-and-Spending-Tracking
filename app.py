from flask import Flask, jsonify, request
from web3 import Web3

app = Flask(__name__)

# Connect to Ethereum (Ganache)
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
contract_address = "YOUR_CONTRACT_ADDRESS"
contract_abi = [...]  # ABI from Truffle compile

contract = web3.eth.contract(address=contract_address, abi=contract_abi)

@app.route("/allocate", methods=["POST"])
def allocate_budget():
    data = request.json
    department_id = data["department_id"]
    name = data["name"]
    amount = data["amount"]
    tx = contract.functions.allocateBudget(department_id, name, amount).transact({"from": web3.eth.accounts[0]})
    return jsonify({"message": "Budget allocated", "tx_hash": tx.hex()})

@app.route("/spend", methods=["POST"])
def spend_budget():
    data = request.json
    department_id = data["department_id"]
    amount = data["amount"]
    tx = contract.functions.spendBudget(department_id, amount).transact({"from": web3.eth.accounts[0]})
    return jsonify({"message": "Budget spent", "tx_hash": tx.hex()})

@app.route("/department/<int:department_id>", methods=["GET"])
def get_department(department_id):
    name, allocated, spent = contract.functions.getDepartment(department_id).call()
    return jsonify({"name": name, "allocated_budget": allocated, "spent_budget": spent})

if __name__ == "__main__":
    app.run(debug=True)
