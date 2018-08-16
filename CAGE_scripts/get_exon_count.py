file=open('breast_exp_denovo_lincrnas.gtf')
d=dict()
for line in file:
	tmp=line.split()
	transcript=tmp[11].strip(';').strip('"')
	if tmp[2]=='transcript':
		count_exon=0
	elif tmp[2]=='exon':
		count_exon+=1
		d[transcript]=count_exon
file.close()
file2=open('breast_exp_known_lincrnas.gtf')
for line in file2:
        tmp=line.split()
        transcript=tmp[11].strip(';').strip('"')
        if tmp[2]=='transcript':
                count_exon=0
        elif tmp[2]=='exon':
                count_exon+=1
                d[transcript]=count_exon
file2.close()


d_elinc=dict()
file3=open('elincRNAs.gtf')
for line in file3:
        tmp=line.split()
        transcript=tmp[11].strip(';').strip('"')
	d_elinc[transcript]=d[transcript]
#print(d_elinc)
elinc_multiple_exon=[]
elinc_single_exon=[]
elinc_2exon=[]
for k,v in d_elinc.items():
	if v==1:
		elinc_single_exon.append(k)
	elif v==2:
		elinc_2exon.append(k)
	else:
		elinc_multiple_exon.append(k)

ratio_elinc=(len(elinc_2exon)+len(elinc_multiple_exon))/float(len(elinc_single_exon))
print('elincRNAs: one exon- '+str(len(elinc_single_exon))+' / 2 exons - '+str(len(elinc_2exon))+' / multiple exons - '+str(len(elinc_multiple_exon))+ ' / RATIO: '+str(ratio_elinc))
file3.close()


d_plinc=dict()
file4=open('plincRNAs.gtf')
for line in file4:
        tmp=line.split()
        transcript=tmp[11].strip(';').strip('"')
        d_plinc[transcript]=d[transcript]
#print(d_plinc)
plinc_multiple_exon=[]
plinc_single_exon=[]
plinc_2exon=[]
for k,v in d_plinc.items():
        if v==1:
                plinc_single_exon.append(k)
        elif v==2:
                plinc_2exon.append(k)
	else:
		plinc_multiple_exon.append(k)
ratio_plinc=(len(plinc_2exon)+len(plinc_multiple_exon))/float(len(plinc_single_exon))


print('plincRNAs: one exon- '+str(len(plinc_single_exon))+' / 2 exons - '+str(len(plinc_2exon))+' / multiple exons - '+str(len(plinc_multiple_exon))+ ' / RATIO: '+str(ratio_plinc))
file4.close()


file5=open('breast_exp_pcg.gtf')
d2=dict()
for line in file5:
        tmp=line.split()
        transcript=tmp[11].strip(';').strip('"')
        if tmp[2]=='transcript':
                count_exon=0
        elif tmp[2]=='exon':
                count_exon+=1
                d2[transcript]=count_exon
file5.close()

d_pPCG=dict()
file6=open('pPCGs.gtf')
for line in file6:
        tmp=line.split()
        transcript=tmp[11].strip(';').strip('"')
        d_pPCG[transcript]=d2[transcript]

pPCG_multiple_exon=[]
pPCG_single_exon=[]
pPCG_2exon=[]
for k,v in d_pPCG.items():
        if v==1:
                pPCG_single_exon.append(k)
        elif v==2:
                pPCG_2exon.append(k)
	else:
		pPCG_multiple_exon.append(k)
ratio_pPCG=(len(pPCG_2exon)+len(pPCG_multiple_exon))/float(len(pPCG_single_exon))


print('pPCG: one exon- '+str(len(pPCG_single_exon))+' / 2 exons - '+str(len(pPCG_2exon))+' / multiple exons - '+str(len(pPCG_multiple_exon))+' / RATIO: '+str(ratio_pPCG))
file4.close()


