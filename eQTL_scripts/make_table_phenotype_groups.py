


### build dict with transcript as key and gene as value:
file=open('annotations/Final_gtf.gtf')
d_transc_gene=dict()
for line in file:
	tmp=line.split()
	if tmp[2]=='transcript':
		transcript_id=tmp[11].strip(';').strip('"')
		gene_id=tmp[9].strip(';').strip('"')
		d_transc_gene[transcript_id]=gene_id
file.close()



## add gene to phenotype column:
file=open('GTEx_phenotype_qtltools_format_header_copy.bed')
outfile=open('GTEx_phenotype_qtltools_format_header_grouped.bed','w')

for line in file:
	if line.find('#')==0:
		outfile.write(line)
	elif line.find('chr')==0:
		tmp=line.split()
		transc_id=tmp[3]
	
		outfile.write(line.replace('\t.','\t'+d_transc_gene[transc_id]))
		
file.close()
outfile.close()	




