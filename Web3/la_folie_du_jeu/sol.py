from web3 import Web3, HTTPProvider
from solcx import compile_source

compiled_sol = compile_source(
    '''
    pragma solidity 0.8.18;

    contract Jeu {
        bool public isSolved = false;
        uint public m = 0x7fffffff;
        uint public a = 12345;
        uint public c = 1103515245;

        uint private currentState;

        constructor(uint _start) {
            currentState = _start;
        }

        function guess(uint _next) public returns (bool) {
            currentState = (a * currentState + c) % m;
            isSolved = (_next == currentState) || isSolved;
            return isSolved;
        }
    }
    '''
    ,
    output_values = ['abi', 'bin']
)

contract_id, contract_interface = compiled_sol.popitem()
byte_code = contract_interface['bin']
abi = contract_interface['abi']

w3 = Web3(HTTPProvider("https://blockchain.challenges.404ctf.fr/31337"))
addr = '0xa49385A5db5ADe76fD99827eBaAAc806BbeEaab3'
c = w3.eth.contract(address=addr,abi=abi)

is_solved = c.functions.isSolved().call()
print('is_solved', is_solved)

# Get current state at storage position 4
state = int(w3.eth.get_storage_at(addr, 4).hex()[-8:], 16)
print('current_state', hex(state))

# Guess next state
next_ = (12345 * state + 1103515245) % 0x7fffffff
p = c.functions.guess(next_).transact()
print('guess next state', hex(next_))

# Verify we actually solved it
is_solved = c.functions.isSolved().call()
print('is_solved', is_solved)
