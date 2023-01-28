contract BaddToken {  
  uint _totalSupply = 0; string _symbol;  
  mapping(address => uint) balances;  
  mapping(address => mapping(address => uint)) public allowance_storage;
  constructor () public {
    _totalSupply = 1000000;
    balances[msg.sender] = _totalSupply;  
  }
  
  function transfer(address receiver, uint amount) public returns (bool) {    
    require(amount <= balances[msg.sender]);        
    balances[msg.sender] = balances[msg.sender] - amount;    
    balances[receiver] = balances[receiver] + amount;    
    return true;  
  }

  function balanceOf(address account) public view returns(uint256){
    return balances[account];
  }
  
  function approve(address spender, uint amount) external returns (bool) {
        allowance_storage[msg.sender][spender] = amount;
        return true;
    }
  function allowance(address owner, address spender) external view returns (uint256)
  {
    return allowance_storage[owner][spender];
  }
    function transferFrom(
        address sender,
        address recipient,
        uint amount
    ) external returns (bool) {
        allowance_storage[sender][msg.sender] -= amount;
        balances[sender] -= amount;
        balances[recipient] += amount;
        return true;
    }
  
  }
