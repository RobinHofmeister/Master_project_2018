import os
import subprocess


sample_id=[]
sample_id2=[]
file=open('files/phg000830.v1.GTEx_WGS.genotype-calls-vcf.c1/GTEx_WGS_654Indiv_maf0.05_remove-indels.recode.vcf')
for line in file:
	if line.find('#CHROM')==0:
		tmp=line.split()
		for i in tmp:
			if i.find('GTEX')==0:
				sample_id.append(i)
file.close()



file=open('Pheno_table_normalized.bed')
for line in file:
	if line.find('#chr')==0:
		tmp=line.split()

		for i in tmp:
			if i.find('GTEX')==0:
				sample_id2.append(i)
file.close()



# built a dict with sample position in genotype file as key and sample position in phenotype file as value.
d_pos=dict()
for i in range(len(sample_id)):
	pos=sample_id2.index(sample_id[i])
	d_pos[i]=pos+4



## write the command line that shoulb be run to order the columns of the phenotype file according to the order of samples in the genotype file.

command='print "$F[0] $F[1] $F[2] $F[3]'

for i in range(len(sample_id)):
	command+=''.join(' $F['+str(d_pos[i])+']')

command2="perl -ane '"+command+r"\n"+'"'+"'"+"< Pheno_table_normalized.bed >testbbb.bed"


p0=subprocess.Popen(command2, shell=True)
p0.wait()

# Modify the output file so that it is tab-separated

file=open('testbbb.bed')
outfile=open('GTEx_phenotype_TPM_normalized_table_columns_sorted_full.bed','w')
for line in file:
	outfile.write(line.replace(' ','\t'))
file.close()
outfile.close()
p1=subprocess.Popen('rm testbbb.bed', shell=True)
p1.wait()
#print('ok')
