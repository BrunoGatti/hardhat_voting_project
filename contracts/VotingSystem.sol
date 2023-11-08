// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./MyToken.sol";

contract VotingSystem {
    MyToken public myToken;  // Reference to the ERC-20 token contract
    address public chairperson;  // Chairperson's address
    mapping(address => uint256) public votes;  // Mapping to track votes by address
    uint256[] public candidateVotes;  // Array to track votes for each candidate

    event Voted(address indexed voter, uint256 candidateIndex);

    constructor(token_address) {
        chairperson = msg.sender;
		setTokenContract(token_address)
    }

    function setTokenContract(address _tokenAddress) external {
        require(msg.sender == chairperson, "Only the chairperson can set the token contract");
        myToken = MyToken(_tokenAddress);
    }

    function vote(uint256 candidateIndex) external {
        require(msg.sender != address(0), "Invalid sender address");
        require(myToken != MyToken(address(0)), "Token contract not set");
        require(myToken.balanceOf(msg.sender) >= fee, "Insufficient tokens to vote");
        require(candidateIndex < candidateVotes.length, "Invalid candidate index");

        // Transfer the fee to the voting system contract
        require(myToken.transferFrom(msg.sender, address(this), fee), "Token transfer failed");

        // Record the vote
        votes[msg.sender]++;
        candidateVotes[candidateIndex]++;

        emit Voted(msg.sender, candidateIndex);
    }

    function getVotingResults() external view returns (uint256[] memory) {
        return candidateVotes;
    }
}

