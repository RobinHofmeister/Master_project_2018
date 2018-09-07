import os
import subprocess


file=open('/scratch/beegfs/monthly/rhofmeis_sra/dbGaP-8031/SraRunTable_2.txt')
outfile=open('sample_id_liste.txt','w')
liste_1=[]
d_srr=dict()
for line in file:
    tmp=line.split()
    if line.find('RNA')==0:
        
        for i in tmp:
            if i.find('SRR')==0:
                srr=i
            if i.find('GTEX')==0 and len(i)<15:
                sample_id=i
		liste_1.append(sample_id)
		outfile.write(sample_id+'\n')
        d_srr[srr]=sample_id
file.close()

