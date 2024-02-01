from ethereum_utils import *

votes_list_encrypted=get_encrypted_votes()
i=0
for encrypted_vote in votes_list_encrypted:
	i=i+1
	if len(encrypted_vote)>10:
		print("vote number "+str(i)+" is "+str(decrypt_sequence(bytes.fromhex(encrypted_vote)))+" and encrypted was:  "+encrypted_vote[1:10]+"...")
	else : print(str(encrypted_vote))
