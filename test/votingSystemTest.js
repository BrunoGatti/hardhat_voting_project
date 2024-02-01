const { expect } = require('chai');
const { ethers } = require('hardhat');

describe('VotingSystem', function () {
    let VotingSystem, MyToken, votingSystem, myToken, ownerAddress, votingBooth;

    before(async () => {
        [ownerAddress,votingBooth] = await ethers.getSigners();

        VotingSystem = await ethers.getContractFactory('contracts/VotingSystem.sol:VotingSystem');
        MyToken = await ethers.getContractFactory('contracts/MyToken.sol:MyToken');

        myToken = await MyToken.deploy();
		await myToken.waitForDeployment();

        votingSystem = await VotingSystem.deploy();
		await votingSystem.waitForDeployment();
    });

    it('should have the same chairperson and owner', async () => {
        const chairperson = await votingSystem.chairperson();
		//const votingSystemAddress= await votingSystem.getAddress()
        const owner = await myToken.owner();

        expect(chairperson).to.equal(ownerAddress.address);
        expect(chairperson).to.equal(owner);
		console.log("chairperson address: ",chairperson)
    });
	it('should have different addresses for VotingSystem and Token', async () => {
    	// Check if the addresses are different
		const votingSystemAddress=await votingSystem.getAddress();
		const myTokenAddress=await myToken.getAddress();
		console.log("voting system adddress:",votingSystemAddress);
		console.log("my token address:",myTokenAddress);
    	expect(votingSystem.getAddress()).to.not.equal(myToken.getAddress());
	});

	it('should set the token contract in VotingSystem', async () => {
        // Set the token contract in VotingSystem
        await votingSystem.setTokenContract( await myToken.getAddress());

        // Verify that the myToken variable in VotingSystem is correctly set
        const votingSystemToken = await votingSystem.myToken();
        expect(votingSystemToken).to.equal(await myToken.getAddress());
    });

	it('should print the address and balance of the voting booth', async () => {

		// Get the address and balance of the voting booth
		const votingBoothAddress = await votingBooth.getAddress();
		const votingBoothBalance = await myToken.balanceOf(votingBoothAddress);

		// Print the address and balance of the voting booth
		console.log('Voting Booth Address:', votingBoothAddress);
		console.log('Voting Booth Balance:', votingBoothBalance.toString());

		
	});
	it('should set the balance of new accounts to 0', async () =>{
        // Verify that the balance of the new account is zero
        const initialBalance = await myToken.balanceOf(votingBooth.address);
        expect(initialBalance).to.equal(0);
        console.log("the balance is 0");	

		});
	it('allowance should be 0 for new accounts', async () =>{
 
		// Verify that there is no allowance for the voting booth
		const initialAllowance = await myToken.allowance(await votingBooth.getAddress(),await votingSystem.getAddress());
		expect(initialAllowance).to.equal(0);
		console.log("the initial allowance is zero");
		});


	it('should allow voting booth to vote after approval', async () => {

		// Verify that the balance of the new account is zero
		const initialBalance = await myToken.balanceOf(votingBooth.address);
		expect(initialBalance).to.equal(0);
		console.log("the balance is 0");

		// Verify that there is no allowance for the voting booth
		const initialAllowance = await myToken.allowance(await votingBooth.getAddress(),await votingSystem.getAddress());
		expect(initialAllowance).to.equal(0);
		console.log("the initial allowance is zero");

		// Sign and send the "approve" transaction
		const approveTransaction = await myToken.connect(votingBooth).approve(await votingSystem.getAddress(),"1000000000000000000");
		await approveTransaction.wait();	
		console.log("approve transaction issued");

		// Verify that the allowance is now 1
		var updatedAllowance = await myToken.allowance(await votingBooth.getAddress(), await votingSystem.getAddress());
		expect(updatedAllowance).to.equal("1000000000000000000");
		console.log("allowance is now",updatedAllowance);

		// Send one token to the voting booth from the owner
		const sendTransaction = await myToken.transfer(await votingBooth.getAddress(),"1000000000000000000");
		await sendTransaction.wait();
		console.log("transaction is sent");

		// Verify that the balance of the voting booth is now 1
		var updatedBalance = await myToken.balanceOf(await votingBooth.getAddress());
		expect(updatedBalance).to.equal("1000000000000000000");
		console.log("the balance of the voting booth is now ",updatedBalance);

		// Voting booth calls the vote transaction
		const voteTransaction = await votingSystem.connect(votingBooth).vote('hello');
		await voteTransaction.wait();
		console.log("the voting booth calls the vote transaction");

		// Verify that the encrypted vote matches with the argument of the vote transaction
		const encryptedVotes = await votingSystem.getEncryptedVotes();
		expect(encryptedVotes[0]).to.equal('hello');
		console.log("the vote is equal to the original vote");

		//verify that the new balance and the new allowance is 0
		updatedAllowance = await myToken.allowance(await votingBooth.getAddress(), await votingSystem.getAddress());
		expect(updatedAllowance).to.equal(0);
		console.log("allowance is now",updatedAllowance);
		updatedBalance = await myToken.balanceOf(await votingBooth.getAddress());
		expect(updatedBalance).to.equal(0);
		console.log("the balance of the voting booth is now ",updatedBalance);



	});
	it('should fail when voting booth does not give allowance', async () => {
		// Send one token to the voting booth from the owner
		const sendTransaction = await myToken.transfer(await votingBooth.getAddress(), "1000000000000000000");
		await sendTransaction.wait();
		console.log("transaction is sent");

		try {
			// Attempt to call the vote transaction without giving allowance
			const voteTransaction = await votingSystem.connect(votingBooth).vote('hello');
			await voteTransaction.wait();

			// If the above line does not throw an error, fail the test
			expect.fail("Vote transaction should fail without allowance");
		} catch (error) {
			// Verify that the error is due to insufficient allowance
			expect(error.message).to.contain("ERC20InsufficientAllowance");
			console.log("Vote transaction failed as expected for insufficient allowance");
		}
	});
	it('should fail when voting booth has insufficient tokens', async () => {
		// Allow the voting system to spend 1 token on behalf of the voting booth
		const approveTransaction = await myToken.connect(votingBooth).approve(await votingSystem.getAddress(), "1000000000000000000");
		await approveTransaction.wait();
		console.log("approve transaction issued");

		try {
			// Attempt to vote with insufficient tokens
			const voteTransaction = await votingSystem.connect(votingBooth).vote('hello');
			await voteTransaction.wait();

			// If the above line does not throw an error, fail the test
			expect.fail("Vote transaction should fail with insufficient tokens");
		} catch (error) {
			// Verify that the error is due to insufficient tokens
			expect(error.message).to.contain("insufficient tokens");
			console.log("Vote transaction failed as expected for insufficient tokens");
		}
	});
	it('should fail when voting booth has too many tokens', async () => {
		// Allow the voting system to spend 2 tokens on behalf of the voting booth
		const approveTransaction = await myToken.connect(votingBooth).approve(await votingSystem.getAddress(), "2000000000000000000");
		await approveTransaction.wait();
		console.log("approve transaction issued");

		// Send 2 tokens to the voting booth from the owner
		const sendTransaction = await myToken.transfer(await votingBooth.getAddress(), "2000000000000000000");
		await sendTransaction.wait();
		console.log("transaction is sent");

		try {
			// Attempt to vote with too many tokens
			const voteTransaction = await votingSystem.connect(votingBooth).vote('hello');
			await voteTransaction.wait();

			// If the above line does not throw an error, fail the test
			expect.fail("Vote transaction should fail with too many tokens");
		} catch (error) {
			// Verify that the error is due to having too many tokens
			console.log(error.message)
			expect(error.message).to.contain("Balance exceedes normal");
			console.log("Vote transaction failed as expected: too many tokens");
		}
	});


});

