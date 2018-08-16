import subprocess
import pandas as pd

p0=subprocess.Popen('ls mapping/mapp_SRR*/transc* >liste_map.txt', shell=True)
p0.wait()

### built dataframe that will be filled

#### ORIGINAL DATAFRAME TO COMPIL
file=open('annotations/Final_gtf.gtf')
transcripts_id=[]
tr_start=[]
tr_end=[]
tr_chr=[]
for line in file:
    tmp=line.split()
    if tmp[2]=='transcript':
        #print(tmp)
        tr_id=tmp[11].strip(';').strip('"')
        transcripts_id.append(tr_id)
        tr_start.append(tmp[3])
        tr_end.append(tmp[4])
        tr_chr.append(tmp[0])

file.close()
df=pd.DataFrame(list(zip(tr_chr,tr_start,tr_end, transcripts_id)), index=transcripts_id, columns=['#chr','start','end','transcript_id'] )



#### fill the data frame

file=open('liste_map.txt')

for i in file:
    
    path=i.strip('\n')
    name=i.split('/')[1].split('_')[1]
    #sample_id=str(d_srr[name])
    transcripts_id=[]
    transcripts_fpkm=[]
    transcripts_tpm=[]
    file1=open(path)
    for line in file1:
        tmp=line.split()
        if line.find('transcript')==0:
            pass
        else:
	    
            transcripts_id.append(tmp[0])
	    transcripts_fpkm.append(tmp[1])
	    transcripts_tpm.append(tmp[2])
    dff=pd.DataFrame(list(zip(transcripts_tpm)), index=transcripts_id, columns=[name])
    df=pd.DataFrame.join(df,dff)
file.close()
df.to_csv('GTEx_table_tpm.csv',sep="\t",encoding='utf-8')


p0=subprocess.Popen('cut -f2- GTEx_table_tpm.csv > GTEx_table_tpm_cut.txt', shell=True)
p0.wait()


################################### Modification file: convert SRR -> GTEX sample_id

## dictionnary to convert SRR -> sample_id:
file=open('SraRunTable_2.txt')
d_srr=dict()
for line in file:
    tmp=line.split()
    if line.find('RNA')==0:
        for i in tmp:
            if i.find('SRR')==0:
                srr=i
            if i.find('GTEX')==0 and len(i)<15:
                sample_id=i
        d_srr[srr]=sample_id
file.close()



file=open('GTEx_table_tpm_cut.txt')
outfile=open('GTEx_phenotype_TPM_table.bed','w')


## change SRR to GTEx_id
c=0
for line in file:
	if line.find('#')==0:
		a=line  # store the original line
		tmp=line.split()
		for i in tmp:
			if 'SRR' in i:
				line=line.replace(i,d_srr[i])
		

		b=line # store the newline
		

		# verification:
		#for i in range(len(a.split())):
			#if 'SRR' in a.split()[i]:
				#if d_srr[a.split()[i]]==b.split()[i]:
					#c+=1
		#print(c) # ==224

		outfile.write(line)
	else:
		outfile.write(line)
file.close()
outfile.close()
