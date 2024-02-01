// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract MyToken is ERC20 {
	address public owner;
    constructor() ERC20("MyToken", "MTK") {
		owner=msg.sender;
        _mint(msg.sender, 100000000 * 10**18); // Mint 100,000,000 tokens and send them to the deployer
    }
}
