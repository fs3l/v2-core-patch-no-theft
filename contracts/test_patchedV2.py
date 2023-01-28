import web3
from web3 import Web3
import inspect
url = "http://127.0.0.1:8545"
w3 = Web3(Web3.HTTPProvider(url))

from solc import compile_source
import time
from solcx import compile_standard, install_solc
import solcx
import json
import os
import binascii

last_txhash = ''
chain_id = 89992018
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

Account0_address = Web3.toChecksumAddress("0x1a50c5cc2ce227e9a110b9b35c560a997265b84a")
private0_key = "0x6402ed458788691998e3ef18eb68c8215e015bc081cd94c6e75cfaaf4555ba13" 

pooladdr = ''
pool_abi = {}
candidatelist = []
candidateindex = 0
acc= []
pool_contracts = []
addrmap = {}
current_target = 0




def giveoneether(addr):
    w3.eth.defaultAccount = w3.eth.accounts[0]
    w3.eth.send_transaction({'to':addr,'value':1000000000000000000})
count=0





def createnewaccount():
    w3.geth.personal.new_account('')
    giveoneether(w3.eth.accounts[-1])
    w3.geth.personal.unlock_account(w3.eth.accounts[-1],'',1000000)
def giveoneether(addr):
    w3.eth.defaultAccount = w3.eth.accounts[0]
    w3.eth.send_transaction({'to':addr,'value':1000000000000000000})
def getabi(abi):
    global pool_abi
    for element in abi:
        if 'name' not in element:
            continue
        if 'inputs' not in element:
            continue
        paralist = []
        
        for inputtype in element['inputs']:
            paralist.append(inputtype['type'])
        pool_abi[element['name']] = paralist


  
def deployContract(contract_file,contract_name,solc_version):
    with open(contract_file, "r") as file:
        contact_list_file = file.read()

    install_solc(solc_version)
    os.system("solc-select use "+solc_version)

    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {contract_file: {"content": contact_list_file}},
            "settings": {
                "outputSelection": {
                    "*": {
                        "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"] # output needed to interact with and deploy contract
                    }
                }
            },
        },
        solc_version=solc_version,
    )
    # print(compiled_sol)

    with open("compiled_code.json", "w") as file:
        json.dump(compiled_sol, file)

    # get bytecode
    bytecode = compiled_sol["contracts"][contract_file][contract_name]["evm"]["bytecode"]["object"]

    # get abi
    abi = json.loads(compiled_sol["contracts"][contract_file][contract_name]["metadata"])["output"]["abi"]

    # For connecting to ganache
    # Create the contract in Python
    ContactList = w3.eth.contract(abi=abi, bytecode=bytecode)
    # Get the number of latest transaction
    nonce = w3.eth.getTransactionCount(Account0_address)

    # build transaction
    #print(abi,bytecode)
    #print(abi)
    #print(chain_id,w3.eth.gas_price,Account0_address,nonce)
    transaction = ContactList.constructor().buildTransaction(
        {
            "chainId": chain_id,
            "gasPrice": 10000,
            "from": Account0_address,
            "nonce": nonce,
            
        }
    )
    # Sign the transaction
    sign_transaction = w3.eth.account.sign_transaction(transaction, private_key=private0_key)
    #print("Deploying Contract!")
    # Send the transaction
    transaction_hash = w3.eth.send_raw_transaction(sign_transaction.rawTransaction)
    # Wait for the transaction to be mined, and get the transaction receipt
    #print("Waiting for transaction to finish...")

    w3.geth.miner.start(4)
    transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)
    #print(f"Done! Contract deployed to {transaction_receipt.contractAddress}")
    w3.geth.miner.stop()

    contact_list = w3.eth.contract(address=transaction_receipt.contractAddress, abi=abi)


    #print(transaction_receipt)
    if contract_name == 'UFragments':
        getabi(contact_list.abi)
    return transaction_receipt.contractAddress,contact_list


def getbalance(contract,addr):
    #try:

        balance = contract.functions.balanceOf(addr).call()
        #print(addr,balance)
        return balance
def getreserve(contract):
    #try:
        blockno = w3.eth.blockNumber
        reserve0,reserve1,reserve2 = contract.functions.getReserves().call()
        #print(balance)
        return reserve0,reserve1,reserve2
def token0(contract):
    #try:
        blockno = w3.eth.blockNumber
        token0 = contract.functions.token0().call()
        #print(balance)
        return token0

       
def functionX(contract,fromaddr,functionname,args):
    global last_txhash
    global current_target
    w3.eth.defaultAccount = fromaddr
    
    func = functionname
    
    arglist ="" 
    count = 0
    for arg in args:
        str1 = str(arg)
        
        
        if len(str1) == 42 and arg[0:2] == '0x':
            normalized_address = '"0x{}"'.format(str1[-40:])
            str1 = 'Web3.toChecksumAddress('+normalized_address+')'
        if str1 == '0x':
            str1 = '\"0x\"'
        if count == 0:
            arglist+=str1
        else:
            arglist+=','+str1
        count+=1
    #print('--------------------------')
    
    str_command = "tx_hash = contract.functions.{}({}).transact()".format(func,arglist)
    #print(str_command)
    #print('fromaddr=',fromaddr)

    loc = {}
    bal_before = {}
    bal_after = {}
    try:
        exec(str_command,{'contract':contract,'Web3':Web3},loc)
        tx_hash = loc['tx_hash']
        w3.geth.miner.start(4)
        flag = True
        while flag:
            
            try:
                tx_receipt = w3.eth.get_transaction_receipt(tx_hash)
                flag = False
                #print(tx_receipt)
                #print('flag=',flag)
            except:
                flag = True
                time.sleep(1)
                count+=1
                #print(count)
        w3.geth.miner.stop()
    except Exception as e:
        print('transaction failed!')
        print(e)
    return  


def normal_swap_test():
    w3.eth.defaultAccount = w3.eth.accounts[0]
    filename = 'UniswapV2Pair.sol'
    pooladdr,contract_pool = deployContract(filename,"UniswapV2Pair","0.5.16")
    filename = 'tokenA.sol'
    token0addr,contract_token0 = deployContract(filename,"BaddToken","0.4.24")
    token1addr,contract_token1 = deployContract(filename,"BaddToken","0.4.24")
    functionX(contract_pool,w3.eth.accounts[0],"initialize",[token0addr,token1addr])
    functionX(contract_token0,w3.eth.accounts[0],"transfer",[pooladdr,10000])
    functionX(contract_token1,w3.eth.accounts[0],"transfer",[pooladdr,10000])
    functionX(contract_pool,w3.eth.accounts[0],"sync",[])
    functionX(contract_token0,w3.eth.accounts[0],"transfer",[w3.eth.accounts[1],10000])
    print("------------------Normal swap test start-----------------")
    functionX(contract_token0,w3.eth.accounts[1],"approve",[pooladdr,10000])
    print("balance of pool of token0:",getbalance(contract_token0,pooladdr))
    print("balance of pool of token1:",getbalance(contract_token1,pooladdr))
    print("balance of Alice of token0:",getbalance(contract_token0,w3.eth.accounts[1]))
    print("balance of Alice of token1:",getbalance(contract_token1,w3.eth.accounts[1]))
    print("-----------Alice approve 10000 token0 to pool------------")
    functionX(contract_token0,w3.eth.accounts[1],"approve",[pooladdr,10000])
    print("-----------Alice swap 10000 token0 to 4950 token1 ------------")
    functionX(contract_pool,w3.eth.accounts[1],"swap",[10000,0,0,4950,w3.eth.accounts[1],'0x'])
    print("balance of Alice of token0:",getbalance(contract_token0,w3.eth.accounts[1]))
    print("balance of Alice of token1:",getbalance(contract_token1,w3.eth.accounts[1]))    
    print("------------------Normal swap test End-----------------")
    return    
def permissionless_swap_test():
    w3.eth.defaultAccount = w3.eth.accounts[0]
    filename = 'UniswapV2Pair.sol'
    pooladdr,contract_pool = deployContract(filename,"UniswapV2Pair","0.5.16")
    filename = 'tokenA.sol'
    token0addr,contract_token0 = deployContract(filename,"BaddToken","0.4.24")
    token1addr,contract_token1 = deployContract(filename,"BaddToken","0.4.24")
    functionX(contract_pool,w3.eth.accounts[0],"initialize",[token0addr,token1addr])
    print("------------------Permissionless test start-----------------")
    functionX(contract_token0,w3.eth.accounts[0],"transfer",[pooladdr,10000])
    functionX(contract_token1,w3.eth.accounts[0],"transfer",[pooladdr,10000])
    functionX(contract_pool,w3.eth.accounts[0],"sync",[])
    functionX(contract_token0,w3.eth.accounts[0],"transfer",[w3.eth.accounts[1],10000])
    print("balance of pool of token0:",getbalance(contract_token0,pooladdr))
    print("balance of pool of token1:",getbalance(contract_token1,pooladdr))
    print("balance of Alice of token0:",getbalance(contract_token0,w3.eth.accounts[1]))
    print("balance of Alice of token1:",getbalance(contract_token1,w3.eth.accounts[1]))
    print("-----------Alice send 10000 token0 to pool------------")
    functionX(contract_token0,w3.eth.accounts[1],"transfer",[pooladdr,10000])
    print("balance of pool of token0:",getbalance(contract_token0,pooladdr))
    print("balance of pool of token1:",getbalance(contract_token1,pooladdr))
    print("balance of Alice of token0:",getbalance(contract_token0,w3.eth.accounts[1]))
    print("balance of Alice of token1:",getbalance(contract_token1,w3.eth.accounts[1]))
    print("balance of Bob of token0:",getbalance(contract_token0,w3.eth.accounts[2]))
    print("balance of Bob of token1:",getbalance(contract_token1,w3.eth.accounts[2]))
    print("-----------Bob try to withdral tokens ------------")
    functionX(contract_pool,w3.eth.accounts[2],"swap",[10000,0,0,4950,w3.eth.accounts[1],'0x'])
    print("balance of Alice of token0:",getbalance(contract_token0,w3.eth.accounts[1]))
    print("balance of Alice of token1:",getbalance(contract_token1,w3.eth.accounts[1]))
    print("balance of Bob of token0:",getbalance(contract_token0,w3.eth.accounts[2]))
    print("balance of Bob of token1:",getbalance(contract_token1,w3.eth.accounts[2]))
    print("Bob failed to withdraw tokens!")
    print("------------------Permissionless test End-----------------")
def main():
    normal_swap_test()
    permissionless_swap_test()

    


if __name__=="__main__":
    main()#### main() ####