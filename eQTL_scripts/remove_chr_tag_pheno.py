file=open('myQTLtoolsPhenotypes.bed')
outfile=open('myQTLtoolsPhenotypes_chrless.bed','w')

for line in file:
	if line.find('chr')==0:
		outfile.write(line.replace('chr',''))
	else:
		outfile.write(line)
		

file.close()
outfile.close()



