# hardhat_voting_project

This is an ethereum DAPP that implements a rudimentary voting system.
It consists of a custom token contract and a Voting system contract, interacting with each other.
The idea is that, to vote, an address has to burn a token in order to call the voting function. The token will be given to trusted addresses (that represent the voting machines) from a chairperson (the deployer of the tokens and the owner of the voting system).
This way we will implement a secure voting procedure that has all the advantage of decentralization, but that does not compromise on user vote anonimity and user secure identification.
