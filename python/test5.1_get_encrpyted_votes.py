from ethereum_utils import *

votes_list_encrypted=get_encrypted_votes()

i=0
for encrypted_vote in votes_list_encrypted:
	i=i+1
	print(encrypted_vote)
