name_file=input('Which file? (full path): ')

file=open(str(name_file))

d_transcripts=dict()
d_genes=dict()
count=0
for line in file:
    if line.find('#')==0:
	pass
    else:
	tmp=line.split()
    	transcript_id=tmp[11].strip(';').strip('"')
    	gene_id=tmp[9].strip(';').strip('"')
    	
	d_transcripts[transcript_id]=count
	d_genes[gene_id]=count

	count+=1	
	#if transcript_id not in transcripts_id_file:
     	 #  transcripts_id_file.append(transcript_id)

    	#if gene_id not in genes_id_file:
	#	genes_id_file.append(gene_id)

print('Number of transcripts in '+str(name_file)+' : '+str(len(d_transcripts)))
print('Number of genes in '+str(name_file)+' : '+str(len(d_genes)))
