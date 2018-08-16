# 1) get noncoding transcripts id:
file1=open('CPC2/result_cpc2_xaa.txt')
noncoding_id_1=[]

for line in file1:
    tmp=line.split()
    state=tmp[6]
    transcript_id=tmp[0]
    if state=='noncoding':
        noncoding_id_1.append(transcript_id)
file1.close()

#######

file2=open('CPC2/result_cpc2_xab.txt')
noncoding_id_2=[]

for line in file2:
    tmp=line.split()
    state=tmp[6]
    transcript_id=tmp[0]
    if state=='noncoding':
        noncoding_id_2.append(transcript_id)
file2.close()

#######

file3=open('CPC2/result_cpc2_xac.txt')
noncoding_id_3=[]

for line in file3:
    tmp=line.split()
    state=tmp[6]
    transcript_id=tmp[0]
    if state=='noncoding':
        noncoding_id_3.append(transcript_id)
file3.close()

noncoding_id_all=noncoding_id_1+noncoding_id_2+noncoding_id_3

# 1') write the file that contain all lincRNAs.
file=open('transcripts_intergenic_longer200.gtf')
outfile=open('long_intergenic_noncoding.gtf','w')

for line in file:
    tmp=line.split()
    if tmp[2]=='transcript':
            transcript_id=tmp[11].strip(';').strip('"')
            if transcript_id in noncoding_id_all:
                outfile.write(line)
    elif tmp[2]=='exon':
            exon_transcript_id=tmp[11].strip(';').strip('"')
            if exon_transcript_id in noncoding_id_all:
                outfile.write(line)
outfile.close()

# 2) get Gencode lincRNAs and PCG transcripts id:
gencode_file=open('Annotations/gencode.v28.chr_patch_hapl_scaff.annotation.gtf')
gencode_pcg_transcripts=[]
gencode_lincrna=[]
for line in gencode_file:
    if line.find('chr')==0:
   
        tmp=line.split()
        if tmp[2]=='transcript':
    
            transcript_id=tmp[11].strip(';').strip('"')
            gene_type=tmp[13].strip(';').strip('"')
            if gene_type=='protein_coding':
     
                gencode_pcg_transcripts.append(transcript_id)
            elif gene_type=='lincRNA':
                gencode_lincrna.append(transcript_id)
gencode_file.close()

# 3) get transcripts id expressed in both libraries:
# 3.a) get transcripts expressed in library1
output_library1=open('Merged_assembly/merged_library1/output.gtf')
breast_exp_transcripts_id_lib1=[]

dict_lib1=dict()


for line in output_library1:
    if line.find('#')==0:
        pass
    else:
        tmp=line.split()
        if tmp[2]=='transcript':  
            transcript_id=tmp[11].strip(';').strip('"')
            fpkm=float(tmp[15].strip(';').strip('"'))
	    tpm=float(tmp[17].strip(';').strip('"'))
	    dict_lib1[transcript_id]=tpm
            if tpm>0:
                breast_exp_transcripts_id_lib1.append(transcript_id)

# 3.b) get transcripts expressed in library2
output_library2=open('Merged_assembly/merged_library2/output.gtf')
breast_exp_transcripts_id_lib2=[]

dict_lib2=dict()


for line in output_library2:
    if line.find('#')==0:
        pass
    else:
        tmp=line.split()
        if tmp[2]=='transcript':
            transcript_id=tmp[11].strip(';').strip('"')
            tpm=float(tmp[17].strip(';').strip('"'))
            dict_lib2[transcript_id]=tpm
	    if tpm>0:
                breast_exp_transcripts_id_lib2.append(transcript_id)

# 3.c) get transcripts expressed in library 1 AND library 2
expressed_both_library=[]
expressed_outfile=open('all_breast_expressed_transcripts.txt','w')
for i in breast_exp_transcripts_id_lib1:
    if i in breast_exp_transcripts_id_lib2:
        expressed_both_library.append(i)
	expressed_outfile.write(str(i)+'\n\n')
expressed_outfile.close()

# 4) split noncoding transcripts into known transcripts (ref_gene_id) and denovo:
stringtie_file=open('Merged_assembly/stringtie_merged.gtf')

known_noncoding_transcripts=[]
denovo_noncoding_transcripts=[]

for line in stringtie_file:
    tmp=line.split()
    if tmp[2]=='transcript':
        transcript_id=tmp[11].strip(';').strip('"')
        if transcript_id in noncoding_id_all:
            if 'ref_gene_id' in line:
                known_noncoding_transcripts.append(transcript_id)
            else:
                denovo_noncoding_transcripts.append(transcript_id)
stringtie_file.close()



# 5) Built gtf that will be used to assemble GTEx data:
## it includes (i) all gencode PCGs, (ii) gencode lincRNAS (filtered for intergenic, 200bp, non_coding potential), (iii) denovo lincRNAs

Denovo_lincrnas=denovo_noncoding_transcripts
Known_lincrnas=[]
for i in known_noncoding_transcripts:
	if i in gencode_lincrna:
		Known_lincrnas.append(i)


gencode_file=open('Annotations/gencode.v28.chr_patch_hapl_scaff.annotation.gtf')

outfile_final=open('Final_gtf.gtf','w')
Denovo_outfile=open('Denovo_lincrnas.gtf','w')
Known_outfile=open('Known_lincrnas.gtf','w')
for line in gencode_file:
    if line.find('chr')==0:
   
        tmp=line.split()
        if tmp[2]=='transcript':
    
            transcript_id=tmp[11].strip(';').strip('"')
            gene_type=tmp[13].strip(';').strip('"')
            if gene_type=='protein_coding':
                outfile_final.write(line)
        elif tmp[2]=='exon':
            gene_type=tmp[13].strip(';').strip('"')
            if gene_type=='protein_coding':
                outfile_final.write(line)
gencode_file.close()
stringtie_file=open('Merged_assembly/stringtie_merged.gtf')

for line in stringtie_file:
    if line.find('#')==0:
        pass
    else:
        tmp=line.split()
        transcript_id=tmp[11].strip(';').strip('"')
        if transcript_id in Denovo_lincrnas:
		outfile_final.write(line)
		Denovo_outfile.write(line)
        elif transcript_id in Known_lincrnas:
		outfile_final.write(line)
            	Known_outfile.write(line)
stringtie_file.close()
outfile_final.close()
Denovo_outfile.close()
Known_outfile.close()

                                 
# 6) Built final subset of breast-expressed:
breat_exp_noncoding=[]
breast_exp_denovo_lincrnas=[]
breast_exp_known_lincrnas=[]
breast_exp_pcg=[]

for i in expressed_both_library:
    if i in denovo_noncoding_transcripts:
        breast_exp_denovo_lincrnas.append(i)
        
    elif i in known_noncoding_transcripts:
        if i in gencode_lincrna:
            breast_exp_known_lincrnas.append(i)
            
    elif i in gencode_pcg_transcripts:
        breast_exp_pcg.append(i)


                                 
                                 
###########
###########
# 6) write final gtf
mcf7_lincrna_pcg=breast_exp_denovo_lincrnas+breast_exp_known_lincrnas+breast_exp_pcg
stringtie_file=open('Merged_assembly/stringtie_merged.gtf')
outfile_mcf7=open('mcf7_expressed_transcripts.gtf','w')
outfile_breast_exp_denovo_lincrnas=open('breast_exp_denovo_lincrnas.gtf','w')
outfile_breast_exp_known_lincrnas=open('breast_exp_known_lincrnas.gtf','w')
outfile_breast_exp_pcg=open('breast_exp_pcg.gtf','w')


for line in stringtie_file:
	if line.find('#')==0:
		pass
	else:
	    tmp=line.split()
            transcript_id=tmp[11].strip(';').strip('"')
            if transcript_id in breast_exp_denovo_lincrnas:
                outfile_breast_exp_denovo_lincrnas.write(line)
		outfile_mcf7.write(line)
            elif transcript_id in breast_exp_known_lincrnas:
                outfile_breast_exp_known_lincrnas.write(line)
		outfile_mcf7.write(line)
            elif transcript_id in breast_exp_pcg:
                outfile_breast_exp_pcg.write(line)
		outfile_mcf7.write(line)

outfile_mcf7.close()
outfile_breast_exp_denovo_lincrnas.close()
outfile_breast_exp_known_lincrnas.close()
outfile_breast_exp_pcg.close()
stringtie_file.close()



##############
############## Built -csv to plot the expression level:

all_breast_exp_lincrna=breast_expressed_known_lincRNAs+breast_exp_denovo_lincRNAs


tpm_lib1=[]
tpm_lib2=[]
tpm_mean=[]

for i in all_breast_exp_lincrna:
    tpm1=dict_lib1[i]
    tpm2=dict_lib2[i]
    mean=(tpm1+tpm2)/2
 
    fpkm_lib1.append(tpm1)
    fpkm_lib2.append(tpm2)
    fpkm_mean.append(mean)
    
    
df2=pd.DataFrame(list(zip(tpm_lib1,tpm_lib2,tpm_mean)), index=all_breast_exp_lincrna, columns=['library1','library2','mean_tpm'])
df2.to_csv('all_lincRNAs_tpm.csv',encoding='utf-8')


# built dictionary with only expressed protein-coding transcripts

tpm_lib1=[]
tpm_lib2=[]
tpm_mean=[]

for i in breast_expressed_known_coding_transcripts:
    tpm1=dict_lib1[i]
    tpm2=dict_lib2[i]
    mean=(tpm1+tpm2)/2

    
    fpkm_lib1.append(tpm1)
    fpkm_lib2.append(tpm2)
    fpkm_mean.append(mean)

df3=pd.DataFrame(list(zip(tpm_lib1,tpm_lib2,tpm_mean)), index=breast_expressed_known_coding_transcripts, columns=['library1','library2','mean_tpm'])
df3.to_csv('all_proteincoding_tpm.csv',encoding='utf-8')
