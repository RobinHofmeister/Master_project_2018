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

### 1.b.2 convert to hg38

p1b2_1=subprocess.Popen('liftOver -minMatch=0.2 -minBlocks=0.01 wgEncodeUwDnaseMcf7PkRep1.bed hg19ToHg38.over.chain wgEncodeUwDnaseMcf7PkRep1_hg38.bed wgEncodeUwDnaseMcf7PkRep1_unlifted.bed', shell=True)
p1b2_1.wait()
p1b2_2=subprocess.Popen('liftOver -minMatch=0.2 -minBlocks=0.01 wgEncodeUwDnaseMcf7PkRep2.bed hg19ToHg38.over.chain wgEncodeUwDnaseMcf7PkRep2_hg38.bed wgEncodeUwDnaseMcf7PkRep2_unlifted.bed', shell=True)
p1b2_2.wait()


### 1.b.3 Merge replicates

p1b3=subprocess.Popen('~/bedops/bin/bedops -m wgEncodeUwDnaseMcf7PkRep1_hg38.bed wgEncodeUwDnaseMcf7PkRep2_hg38.bed > DHSI_MCF7_rep1_2.bed', shell= True)
p1b3.wait()




## 1.c OVERLAP DHSI WITH CHROMHMM:

p1c=subprocess.Popen('bedtools intersect -a ChromHMM_MCF7_hg38.bed -b DHSI_MCF7_rep1_2.bed -u > ChromHMM_DHSI_intersect.bed', shell=True)
p1c.wait()





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



# 	3. Exclude blacklist regions from hg38 intergenic region

## 3.a download data
p3a_1=subprocess.Popen('wget http://mitra.stanford.edu/kundaje/akundaje/release/blacklists/hg38-human/hg38.blacklist.bed.gz', shell=True)
p3a_1.wait()
p3a_2=subprocess.Popen('gunzip hg38.blacklist.bed.gz', shell=True)
p3a_2.wait()
p3a_3=subprocess.Popen('bedtools sort -i hg38.blacklist.bed > hg38.blacklist_sorted.bed', shell=True)
p3a_3.wait()

## 3.b exclude blacklist regions

p3b=subprocess.Popen('~/bedops/bin/bedops --difference intergenic_regions_hg38.gtf hg38.blacklist_sorted.bed > intergenic_blacklist_region.bed', shell=True)
p3b.wait()



# 	4. Overlap accessible enhancers with intergenic region to get intergenic enhancers


p4=subprocess.Popen('bedtools intersect -a ChromHMM_DHSI_intersect.bed -b intergenic_blacklist_region.bed -f 1.0 -u > intergenic_chromHMM.bed',shell=True)
p4.wait()



# 	5. Overlap intergenic enhancers with CAGE TIRs to get enhancer-associated TIRs


## 5.a.1 get intergenic enhancer and promoters from "intergenic_chromHMM.bed"
p5a_1=subprocess.Popen('python Python_scripts/select_intergenic_enhancer_promoter.py', shell=True) 
p5a_1.wait() # output: intergenic_enhancers.bed, intergenic_promoters.bed

## 5.a.2 get promoters from "ChromoHMM_DHSI_:intersect.bed"
p5a_2=subprocess.Popen('python Python_scripts/select_enhancer_promoters.py',shell=True)
p5a_2.wait() # output: promoters.bed , enhancers.bed

## 5.b get cage peaks for Mcf7:

	###download and unzip data:
p5b1=subprocess.Popen('wget http://fantom.gsc.riken.jp/5/datafiles/latest/extra/CAGE_peaks/hg19.cage_peak_phase1and2combined_tpm_ann.osc.txt.gz', shell= True)
p5b1.wait()
p5b1_0=subprocess.Popen('gunzip hg19.cage_peak_phase1and2combined_tpm_ann.osc.txt.gz', shell=True)
p5b1_0.wait()
	###select Mcf7 cage peaks
p5b_1=subprocess.Popen('python Python_scripts/select_cage_peak_mcf7.py', shell=True)
p5b_1.wait()
	###convert to hg38 and sort
p5b_2=subprocess.Popen('liftOver -minMatch=0.2 -minBlocks=0.01 Mcf7_cage_peak_tpm_ann.osc.txt hg19ToHg38.over.chain Mcf7_cage_peak_tpm_ann_hg38.osc.txt Mcf7_cage_peak_tpm_ann_hg38_unlifted.osc.txt', shell= True)
p5b_2.wait()
p5b_3=subprocess.Popen('bedtools sort -i Mcf7_cage_peak_tpm_ann_hg38.osc.txt > Mcf7_cage_peak_tpm_ann_hg38.osc_sorted.txt', shell=True)
p5b_3.wait()



## 5.c Overlaps :

	### intergenic enhancers:

p5c_1=subprocess.Popen('bedtools intersect -a Mcf7_cage_peak_tpm_ann_hg38.osc_sorted.txt -b intergenic_enhancers.bed -u > intergenic_enhancer_associated_TIRs.bed', shell=True)
p5c_1.wait()

	### intergenic promoters:
p5c_2=subprocess.Popen('bedtools intersect -a Mcf7_cage_peak_tpm_ann_hg38.osc_sorted.txt -b intergenic_promoters.bed -u > intergenic_promoter_associated_TIRs.bed', shell=True)
p5c_2.wait()

	### all promoters:
p5c_3=subprocess.Popen('bedtools intersect -a Mcf7_cage_peak_tpm_ann_hg38.osc_sorted.txt -b promoters.bed -u > promoter_associated_TIRs.bed',shell=True)
p5c_3.wait()





#####
####
###
##
#	PART 2: Determine expressed elincRNAs/plincRNAs/PCGs using CAGE data

# 2.1 download, convert, sort cage data:

p21_1=subprocess.Popen('wget http://fantom.gsc.riken.jp/5/datafiles/latest/basic/human.cell_line.hCAGE/breast%2520carcinoma%2520cell%2520line%253aMCF7.CNhs11943.10482-107A5.hg19.nobarcode.bam', shell=True)
p21_1.wait()
p21_2=subprocess.Popen('bedtools bamtobed -i breast%20carcinoma%20cell%20line%3aMCF7.CNhs11943.10482-107A5.hg19.nobarcode.bam > cage_reads_hg19.bed', shell=True)
p21_2.wait()

p21_3=subprocess.Popen('liftOver -minMatch=0.2 -minBlocks=0.01 cage_reads_hg19.bed hg19ToHg38.over.chain cage_reads_hg38.bed cage_reads_hg38_unlifted.bed', shell=True)
p21_3.wait()

p21_4=subprocess.Popen('bedtools sort -i cage_reads_hg38.bed > cage_reads_hg38_sorted.bed', shell=True)
p21_4.wait()


# 2.2 get first exon of expressed lincRNAs and PCGs:

p22_1=subprocess.Popen('cp /scratch/beegfs/monthly/rhofmeis/MCF/breast_exp* ./', shell=True)
p22_1.wait()


p22_2=subprocess.Popen('Python_scripts/select_first_exon_v2.py', shell=True)
p22_2.wait() #outputs: 'breast_exp_lincrnas_first_exon.gtf' ; 'breast_exp_PCGs_first_exon.gtf'

p22_3=subprocess.Popen('~/bin/gtf2bed < breast_exp_lincrnas_first_exon.gtf > breast_exp_lincrnas_first_exon.bed', shell=True)
p22_3.wait()
p22_4=subprocess.Popen('~/bin/gtf2bed < breast_exp_PCGs_first_exon.gtf > breast_exp_PCGs_first_exon.bed', shell=True)


