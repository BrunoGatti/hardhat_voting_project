from ethereum_utils import *

allowance = get_allowance(TOKEN_CONTRACT,BOOTH1_PUBLIC_ADDRESS,VOTING_SYSTEM_CONTRACT_ADDRESS)
print(f"allowance: {allowance}")
