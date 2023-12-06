// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./MyToken.sol";

contract VotingSystem {
    MyToken public myToken;  // Reference to the ERC-20 token contract
    address public chairperson;  // Chairperson's address
    mapping(address => string) public encryptedVotes;  // Mapping to store encrypted votes by address
    uint256[] public candidateVotes;  // Array to track votes for each candidate

    event Voted(address indexed voter, string encryptedVote);

    constructor() {
        chairperson = msg.sender;
    }

    function setTokenContract(address _tokenAddress) external {
        require(msg.sender == chairperson, "Only the chairperson can set the token contract");
        myToken = MyToken(_tokenAddress);
    }

    function vote(string calldata encryptedVote) external {
        require(msg.sender != address(0), "Invalid sender address");
        require(myToken != MyToken(address(0)), "Token contract not set");
        require(myToken.balanceOf(msg.sender) >= 1, "Insufficient tokens to vote");

        // Transfer the fee to the voting system contract
        require(myToken.transferFrom(msg.sender, address(this), 1), "Token transfer failed");

        // Record the encrypted vote
        encryptedVotes[msg.sender] = encryptedVote;

        emit Voted(msg.sender, encryptedVote);
    }

    function getVotingResults() external view returns (uint256[] memory) {
        return candidateVotes;
    }

    function getEncryptedVote(address voter) external view returns (string memory) {
        return encryptedVotes[voter];
    }
}
