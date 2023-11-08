async function main() {

  console.log("Deploying contracts with the account:", "0xB1256BD26081A5E9e4CdBc8EC89aE19FA9A9Ec00");

  const VotingSystem = await ethers.deployContract("VotingSystem");

  console.log("Voting System address:", await VotingSystem.getAddress());
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
