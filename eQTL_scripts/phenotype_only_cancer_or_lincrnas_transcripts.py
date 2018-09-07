import os
import subprocess


# get cancer transcripts
file=open('/scratch/beegfs/monthly/rhofmeis_sra/TEST2_qtltools/Cosmic_transcripts.txt')
cosmic_transcripts=[]
for line in file:
	tmp=line.split()
	cosmic_transcripts.append(tmp[0])
file.close()

## get lincRNAs id:
file=open('/scratch/beegfs/monthly/rhofmeis/MCF/all_lincRNAs.gtf')
lincrnas_id=[]
for line in file:
        tmp=line.split()
        if tmp[2]=='transcript':
                #print(tmp)
                transcript_id=tmp[11].strip(';').strip('"')
                lincrnas_id.append(transcript_id)
file.close()

## Build subset of phenotype table

file=open('GTEx_phenotype_qtltools_format_header_copy.bed')
outfile=open('GTEx_phenotype_qtltools_cancer_transcripts.bed','w')
outfile2=open('GTEx_phenotype_qtltools_lincRNAs_transcripts.bed','w')
for line in file:
	tmp=line.split()
	if line.find('#chr')==0:
		outfile.write(line)
		outfile2.write(line)
	elif tmp[3] in cosmic_transcripts:
		outfile.write(line)
	elif tmp[3] in lincrnas_id:
		outfile2.write(line)
outfile.close()
outfile2.close()
file.close()




