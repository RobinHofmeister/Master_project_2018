import os
import subprocess


# 0. Download index to convert hg19 -> hg38
p0=subprocess.Popen('wget http://hgdownload.cse.ucsc.edu/goldenpath/hg19/liftOver/hg19ToHg38.over.chain.gz', shell=True)
p0.wait()

p0_1=subprocess.Popen('gunzip hg19ToHg38.over.chain.gz', shell= True)
p0_1.wait()



# 	1. Overlap enhancers with DHSI regions to get accessible enhancers


## 1.a chromHMM:

p1a_1=subprocess.Popen('wget ftp://ftp.ncbi.nlm.nih.gov/geo/series/GSE57nnn/GSE57498/suppl/GSE57498%5FMCF7%5FChromHMM%2Ebed%2Egz', shell=True)
p1a_1.wait()

p1a_2=subprocess.Popen('gunzip GSE57498_MCF7_ChromHMM.bed.gz', shell=True)
p1a_2.wait()

### 1.a.1 remove first line to allow the conversion

file1=open('GSE57498_MCF7_ChromHMM.bed')
outfile1=open('ChromHMM_MCF7_hg19.bed','w')
for line in file1:
	if line.find('track')==0:
		pass
	else:
		outfile1.write(line)
outfile1.close()
file1.close()


### 1.a.2 convert to hg38

p1a2=subprocess.Popen('liftOver -minMatch=0.2 -minBlocks=0.01 ChromHMM_MCF7_hg19.bed hg19ToHg38.over.chain ChromHMM_MCF7_hg38.bed ChromHMM_MCF7_unlifted.bed', shell=True)
p1a2.wait()

p1a2_2=subprocess.Popen('bedtools sort -i ChromHMM_MCF7_hg38.bed > ChromHMM_MCF7_hg38_sorted.bed', shell=True)
p1a2_2.wait()

## 1.b DHSI

p1b_1=subprocess.Popen('wget http://hgdownload.cse.ucsc.edu/goldenpath/hg19/encodeDCC/wgEncodeUwDnase/wgEncodeUwDnaseMcf7PkRep1.narrowPeak.gz', shell=True)
p1b_1.wait()
p1b_2=subprocess.Popen('wget http://hgdownload.cse.ucsc.edu/goldenpath/hg19/encodeDCC/wgEncodeUwDnase/wgEncodeUwDnaseMcf7PkRep2.narrowPeak.gz', shell=True)
p1b_2.wait()

p1b_1a=subprocess.Popen('gunzip wgEncodeUwDnaseMcf7PkRep1.narrowPeak.gz', shell=True)
p1b_1a.wait()
p1b_2a=subprocess.Popen('gunzip wgEncodeUwDnaseMcf7PkRep2.narrowPeak.gz', shell=True)
p1b_2a.wait()


### 1.b.1 modification to bed format

p1b1_1=subprocess.Popen('cut -f 1-6 wgEncodeUwDnaseMcf7PkRep1.narrowPeak > wgEncodeUwDnaseMcf7PkRep1.bed', shell=True)
p1b1_1.wait()
p1b1_2=subprocess.Popen('cut -f 1-6 wgEncodeUwDnaseMcf7PkRep2.narrowPeak > wgEncodeUwDnaseMcf7PkRep2.bed', shell=True)
p1b1_2.wait()

p1b1_3=subprocess.Popen('bedtools sort -i wgEncodeUwDnaseMcf7PkRep1.bed > wgEncodeUwDnaseMcf7PkRep1_sorted.bed', shell=True)
p1b1_3.wait()
p1b1_4=subprocess.Popen('bedtools sort -i wgEncodeUwDnaseMcf7PkRep2.bed > wgEncodeUwDnaseMcf7PkRep2_sorted.bed', shell=True)



### 1.b.2 convert to hg38

p1b2_1=subprocess.Popen('liftOver -minMatch=0.2 -minBlocks=0.01 wgEncodeUwDnaseMcf7PkRep1_sorted.bed hg19ToHg38.over.chain wgEncodeUwDnaseMcf7PkRep1_hg38.bed wgEncodeUwDnaseMcf7PkRep1_unlifted.bed', shell=True)
p1b2_1.wait()
p1b2_2=subprocess.Popen('liftOver -minMatch=0.2 -minBlocks=0.01 wgEncodeUwDnaseMcf7PkRep2_sorted.bed hg19ToHg38.over.chain wgEncodeUwDnaseMcf7PkRep2_hg38.bed wgEncodeUwDnaseMcf7PkRep2_unlifted.bed', shell=True)
p1b2_2.wait()


### 1.b.3 Merge replicates

p1b3=subprocess.Popen('~/bedops/bin/bedops -m wgEncodeUwDnaseMcf7PkRep1_hg38.bed wgEncodeUwDnaseMcf7PkRep2_hg38.bed > DHSI_MCF7_rep1_2.bed', shell= True)
p1b3.wait()

p1b3_2=subprocess.Popen('bedtools sort -i DHSI_MCF7_rep1_2.bed > DHSI_MCF7_rep1_2_sorted.bed', shell=True)
p1b3_2.wait()


## 1.c OVERLAP DHSI WITH CHROMHMM:

p1c=subprocess.Popen('bedtools intersect -a ChromHMM_MCF7_hg38_sorted.bed -b DHSI_MCF7_rep1_2_sorted.bed -u > ChromHMM_DHSI_intersect.bed', shell=True)
p1c.wait()

p1c_2=subprocess.Popen('bedtools sort -i ChromHMM_DHSI_intersect.bed > ChromHMM_DHSI_intersect_sorted.bed', shell=True)
p1c_2.wait()



# 	2. Get intergenic regions of the genome (genome excluding annotated PCGs)


## 2.a download data:

	#chrom size
p2a_1a=subprocess.Popen('wget http://hgdownload.cse.ucsc.edu/goldenpath/hg38/bigZips/hg38.chrom.sizes', shell=True)
p2a_1a.wait()
p2a_1b=subprocess.Popen('sort -k1,1 -k2,2n hg38.chrom.sizes > hg38.chrom_sorted',shell=True)
p2a_1b.wait()
	#gencode annotations
p2a_2a=subprocess.Popen('wget ftp://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_28/gencode.v28.chr_patch_hapl_scaff.annotation.gtf.gz', shell= True)
p2a_2a.wait()
p2a_2b=subprocess.Popen('gunzip gencode.v28.chr_patch_hapl_scaff.annotation.gtf.gz', shell=True)
p2a_2b.wait()
	#extract PCGs from gencode annotations
p2a_3a=subprocess.Popen('python Python_scripts/select_gencode_proteincoding.py', shell=True)
p2a_3a.wait()
p2a_3b=subprocess.Popen('bedtools sort -i gencode_proteincoding_genes_only.gtf > gencode_proteincoding_genes_only_sorted.gtf', shell=True)
p2a_3b.wait()

## 2.b get intergenic regions

p2b=subprocess.Popen('bedtools complement -i gencode_proteincoding_genes_only_sorted.gtf -g hg38.chrom_sorted > intergenic_regions_hg38.gtf',shell=True)
p2b.wait()

p2b_2=subprocess.Popen('bedtools sort -i intergenic_regions_hg38.gtf > intergenic_regions_hg38_sorted.gtf', shell=True)
p2b_2.wait()


# 	3. Exclude blacklist regions from hg38 intergenic region

## 3.a download data
p3a_1=subprocess.Popen('wget http://mitra.stanford.edu/kundaje/akundaje/release/blacklists/hg38-human/hg38.blacklist.bed.gz', shell=True)
p3a_1.wait()
p3a_2=subprocess.Popen('gunzip hg38.blacklist.bed.gz', shell=True)
p3a_2.wait()
p3a_3=subprocess.Popen('bedtools sort -i hg38.blacklist.bed > hg38.blacklist_sorted.bed', shell=True)
p3a_3.wait()

## 3.b exclude blacklist regions

p3b=subprocess.Popen('~/bedops/bin/bedops --difference intergenic_regions_hg38_sorted.gtf hg38.blacklist_sorted.bed > intergenic_blacklist_region.bed', shell=True)
p3b.wait()
p3b_2=subprocess.Popen('bedtools sort -i intergenic_blacklist_region.bed > intergenic_blacklist_region_sorted.bed', shell=True)
p3b_2.wait()


# 	4. Overlap accessible enhancers with intergenic region to get intergenic enhancers


p4=subprocess.Popen('bedtools intersect -a ChromHMM_DHSI_intersect_sorted.bed -b intergenic_blacklist_region_sorted.bed -f 1.0 -u > intergenic_chromHMM.bed',shell=True)
p4.wait()

p4_2=subprocess.Popen('bedtools sort -i intergenic_chromHMM.bed > intergenic_chromHMM_sorted.bed', shell=True)
p4_2.wait()


# 	5. Overlap intergenic enhancers with CAGE TIRs to get enhancer-associated TIRs


## 5.a.1 get intergenic enhancer and promoters from "intergenic_chromHMM.bed"
p5a_1=subprocess.Popen('python Python_scripts/select_intergenic_enhancer_promoter.py', shell=True) 
p5a_1.wait() # output: intergenic_enhancers.bed, intergenic_promoters.bed

## 5.a.2 get promoters from "ChromoHMM_DHSI_:intersect.bed"
p5a_2=subprocess.Popen('python Python_scripts/select_enhancer_promoters.py',shell=True)
p5a_2.wait() # output: promoters.bed , enhancers.bed



## 5.b Get Cage reads TSS:

subprocess.check_call('python Python_scripts/cluster_CAGE_reads_into_TSS.py', shell= True) # outputs: TSS_cage_cluster.bed





### 5.c Overlaps :

	### intergenic enhancers:

p5c_1=subprocess.Popen('bedtools intersect -a TSS_cage_cluster.bed -b intergenic_enhancers.bed -u > intergenic_enhancer_associated_TIRs.bed', shell=True)
p5c_1.wait()

	### intergenic promoters:
p5c_2=subprocess.Popen('bedtools intersect -a TSS_cage_cluster.bed -b intergenic_promoters.bed -u > intergenic_promoter_associated_TIRs.bed', shell=True)
p5c_2.wait()

	### all promoters:
p5c_3=subprocess.Popen('bedtools intersect -a TSS_cage_cluster.bed -b promoters.bed -u > promoter_associated_TIRs.bed',shell=True)
p5c_3.wait()







#	PART 2: Determine expressed elincRNAs/plincRNAs/PCGs using CAGE data


# 2.1 download, convert, sort CAGE reads:
# 	done in the script 'cluster_CAGE_reads_into_TSS.py'




# 2.2 get first exon of expressed lincRNAs and PCGs:

p22_1=subprocess.Popen('cp /scratch/beegfs/monthly/rhofmeis/MCF/breast_exp_denovo_lincrnas.gtf ./', shell=True)
p22_1.wait()
p22_2=subprocess.Popen('cp /scratch/beegfs/monthly/rhofmeis/MCF/breast_exp_known_lincrnas.gtf ./', shell=True)
p22_2.wait()
p22_3=subprocess.Popen('cp /scratch/beegfs/monthly/rhofmeis/MCF/breast_exp_pcg.gtf ./', shell=True)
p22_3.wait()
#
##
###
file=open('breast_exp_denovo_lincrnas.gtf')
outfile=open('breast_exp_lincrnas_first_exon.gtf','w')


for line in file:
    tmp=line.split()
    if tmp[2]=='exon':
        nbr_exon=tmp[13].strip(';').strip('"')
        if nbr_exon=='1':
            outfile.write(line)
file.close()

file2=open('breast_exp_known_lincrnas.gtf')
for line in file2:
    tmp=line.split()
    if tmp[2]=='exon':
        nbr_exon=tmp[13].strip(';').strip('"')
        if nbr_exon=='1':
            outfile.write(line)
file2.close()
outfile.close()


file3=open('breast_exp_pcg.gtf')
outfile3=open('breast_exp_PCGs_first_exon.gtf','w')
for line in file3:
    tmp=line.split()
    if tmp[2]=='exon':
        nbr_exon=tmp[13].strip(';').strip('"')
        if nbr_exon=='1':
            outfile3.write(line)
file3.close()
outfile3.close()

###
##
#




# 2.3 
# 	A. determine whether there is a read that overlap both an eTIR with a lincRNA (elincRNA)

# A.1 intersect cage reads with TIRS. Outputs cage reads if intersection with TIRs
p23a_1=subprocess.Popen('bedtools intersect -a cage_reads_hg38_rep1_rep2_rep3_sorted.bed -b intergenic_enhancer_associated_TIRs.bed -s -u > cage_associated_eTIRs.bed', shell=True)
p23a_1.wait()
# A.2 intersect cage_intergenic_eTIRs with lincRNAs. Outputs lincRNAs if intersection with cage ( if cage intersect both eTIR and lincRNAs, outputs lincRNAs)
p23a_2=subprocess.Popen('bedtools intersect -a breast_exp_lincrnas_first_exon.gtf -b cage_associated_eTIRs.bed -u -s > elincRNAs.gtf', shell=True)
p23a_2.wait()


#       B. determine whether there is a read that overlap both a pTIR with a lincRNA (plincRNA)

p23b_1=subprocess.Popen('bedtools intersect -a cage_reads_hg38_rep1_rep2_rep3_sorted.bed -b intergenic_promoter_associated_TIRs.bed -s -u > cage_associated_pTIRs.bed', shell=True)
p23b_1.wait()
p23b_2=subprocess.Popen('bedtools intersect -a breast_exp_lincrnas_first_exon.gtf -b cage_associated_pTIRs.bed -u -s > plincRNAs.gtf', shell=True)
p23b_2.wait()


#       C. determine whether there is a read that overlap both a pTIR with a PCG
p23c_1=subprocess.Popen('bedtools intersect -a cage_reads_hg38_rep1_rep2_rep3_sorted.bed -b promoter_associated_TIRs.bed -s -u > cage_associated_pcg_TIRs.bed', shell=True)
p23c_1.wait()
p23c_2=subprocess.Popen('bedtools intersect -a breast_exp_PCGs_first_exon.gtf -b cage_associated_pcg_TIRs.bed -u -s > pPCGs.gtf', shell=True)
p23c_2.wait()



