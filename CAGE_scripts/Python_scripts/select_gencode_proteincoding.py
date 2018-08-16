#!/usr/bin/env python

file=open('./gencode.v28.chr_patch_hapl_scaff.annotation.gtf')
outfile=open('gencode_proteincoding_genes_only.gtf','w')
for line in file:
    tmp=line.split()
    if line.find('#')==0:
        outfile.write(line)
    elif line.find('chr')==0:
	if tmp[2]=='gene':
        	gene_type=tmp[11].strip(';').strip('"')
    
     		if gene_type=='protein_coding':
            		outfile.write(line)
file.close()
outfile.close()
