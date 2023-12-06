// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./MyToken.sol";

contract VotingSystem {
    MyToken public myToken;  // Reference to the ERC-20 token contract
    address public chairperson;  // Chairperson's address
    string[] private encryptedVotes;  // List to store encrypted votes
    address[] public voters;  // Array to track the addresses of voters

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
        require(myToken.balanceOf(msg.sender) < 2, "Balance exceedes normal balance, the tokens are more than two");

        // Transfer the fee to the voting system contract
        require(myToken.transferFrom(msg.sender, address(this), 1), "Token transfer failed");

        // Record the encrypted vote
        encryptedVotes.push(encryptedVote);
        voters.push(msg.sender); // Record the voter's address

        emit Voted(msg.sender, encryptedVote);
    }

    function getAllVoters() external view returns (address[] memory) {
        return voters;
    }

    function getEncryptedVotes() external view returns (string[] memory) {
        return encryptedVotes;
    }
}
