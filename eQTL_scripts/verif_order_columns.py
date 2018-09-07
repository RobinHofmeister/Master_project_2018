
sample_name=input('sample name:')

c=0
file=open('GTEx_phenotype_TPM_table.bed')

for line in file:
	c+=1
	tmp=line.split()
	if line.find('#chr')==0:
		for i in range(len(tmp)):
			if tmp[i]==sample_name:
				pos=i
	else:
		if c<40:	
			print(tmp[0],tmp[1],tmp[2],tmp[pos])
		else:
			pass
file.close()


