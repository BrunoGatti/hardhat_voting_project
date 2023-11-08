//const { ethers, network } = require("hardhat");
const { ethers } = require("hardhat");


async function main() {
  // Replace with your actual contract and token addresses
  const contractAddress = "0x9B957D98C985F854ab9f9f39E1Bd9992F1938e68"; // The address of your VotingSystem contract
  const tokenAddress = "0x33286125410a9488d98C65AA18baB01213b5f035"; // The address of your ERC-20 token contract
    // Deploy the VotingSystem contract with gasPrice and gasLimit overrides
  const VotingSystem = await ethers.getContractFactory("VotingSystem");
  //const votingSystem = await VotingSystem.deploy(tokenAddress, {
    //gasPrice: ethers.parseUnits("10", "gwei"), // Set your desired gas price
    //gasLimit: 2000000, // Set your desired gas limit
  //});
  const votingSystem = await VotingSystem.deploy()
  console.log("Deploying VotingSystem. Transaction hash:", deployTransaction.hash);

  await votingSystem.waitForDeployment();
  console.log("VotingSystem deployed to:", votingSystem.address);

  // Add the address of the deployed VotingSystem contract to your token's whitelist
  const Token = await ethers.getContractFactory("MyToken"); // Replace with your actual ERC-20 token contract name
  const token = Token.attach(tokenAddress);
  //await token.addWhitelist(votingSystem.address);

  // Optionally, you can also set the chairperson here if needed
  // await votingSystem.setChairperson("CHAIRPERSON_ADDRESS");

  // Check the network name to determine where the contracts are deployed
  if (network.name === "localhost") {
    console.log("Local deployment. Make sure to fund the contract with tokens.");
  }

  // Optionally, you can interact with the contract further or perform other setup tasks
  // ...

  // Exit the script
  process.exit(0);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
