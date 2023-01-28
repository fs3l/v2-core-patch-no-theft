# Uniswap V2

[![Actions Status](https://github.com/Uniswap/uniswap-v2-core/workflows/CI/badge.svg)](https://github.com/Uniswap/uniswap-v2-core/actions)
[![Version](https://img.shields.io/npm/v/@uniswap/v2-core)](https://www.npmjs.com/package/@uniswap/v2-core)

In-depth documentation on Uniswap V2 is available at [uniswap.org](https://uniswap.org/docs).

The built contract artifacts can be browsed via [unpkg.com](https://unpkg.com/browse/@uniswap/v2-core@latest/).

# Local Development

The following assumes the use of `node@>=10`.

## Install Dependencies

`yarn`

## Compile Contracts

`yarn compile`

## Run Tests

`yarn test`

## Test permissionless swap
- Install `python3`,`solc-select`,`solcx`,`web3`
- Setup a private geth node
- set configure variable in contract/test_patchV2.py as
```
chainID = {chain id of private network}
Account0_address = Web3.toChecksumAddress("{address of eth.accounts[0]}")
private0_key = "{private key of eth.accounts[0]}"
```
- unlock `eth.accounts[0]`,`eth.accounts[1]`,`eth.accounts[2]` and initiate with 1 eth
```
personal.newAccount()
personal.unlockAccount(eth.accounts[0/1/2])
miner.start(4)
miner.setEtherbase(eth.accounts[0/1/2])

```
- Run test file
```
cd contracts
python3 test_patchV2.py
python3 
```
- We can find the permissionless swap cannot work in the patched contract.
