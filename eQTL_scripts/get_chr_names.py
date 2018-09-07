file=open('GTEx_WGS_654Indiv_maf0.05_remove-indels_HG38.recode.vcf')
start=False
d_chr=dict()
for line in file:
	if line.find('#CHROM')==0:
		start=True
	elif start:
		tmp=line.split()
		d_chr[tmp[0]]='chr'+tmp[0]

print(d_chr)

outfile=open('Chromosomes_names.txt','w')
for k,v in d_chr.items():
	outfile.write(k+' '+v+'\n')
outfile.close()	
