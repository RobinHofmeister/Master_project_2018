#!/usr/bin/env python3


import os
import subprocess


## 1. Processing genotype file:


#### After these steps, we should have:
#       - a compressed genotype table (.vcf.gz)
#       - an indexed genotype table (.tbi)
#       - genotype Principal Components file (tab-separated)



##	 Downloading genotype file:
p00=subprocess.Popen('prefetch -X 460GB cart_WGS_genotype_447Gb.krt', shell=True)
p00.wait()

#       decrypting
#       untar
#       unzip



##	1.a Build a list with GTEx breast sample
p0=subprocess.Popen('python Scripts_geno_pheno/get_liste_sample_id.py', shell=True) #output: sample_id_liste.txt
p0.wait()

##	1.b process genotype file 
#		--maf 0.05 : remove SNPs with MAF lower than 0.05
#		--remove-indels : remove indels, keep only SNPs
#		--recode : used to generate a new file in vcf format
#		--recode-INFO-all: keep all infos line in the output file
#		--keep : keep only sample contained in .txt file (here: sample_id_liste.txt)

p1=subprocess.Popen('vcftools --vcf files/phg000830.v1.GTEx_WGS.genotype-calls-vcf.c1/GTEx_Analysis_2016-01-15_v7_WholeGenomeSeq_652Ind_GATK_HaplotypeCaller.vcf --maf 0.05 --remove-indels --recode --recode-INFO-all --keep ../sample_id_liste.txt --out GTEx_WGS_654Indiv_maf0.05_remove-indels', shell=True)
p1.wait()


## 	1.c Convert genotype file hg19 to hg38:

#		download chain
p2=subprocess.Popen('wget http://hgdownload.soe.ucsc.edu/goldenPath/hg19/liftOver/hg19ToHg38.over.chain.gz', shell=True)
p2.wait()

#	 	download genome file
p3=subprocess.Popen('wget http://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/hg38.fa.gz', shell=True)
p3.wait()
p33=subprocess.Popen('gunzip hg38.fa.gz', shell=True)
p33.wait()

#	 	convert to hg38
#	 	module add UHTS/Analysis/CrossMap/0.2.7;
p4=subprocess.Popen('CrossMap.py vcf hg19ToHg38.over.chain.gz GTEx_WGS_654Indiv_maf0.05_remove-indels.recode.vcf hg38.fa GTEx_WGS_654Indiv_maf0.05_remove-indels_HG38.vcf', shell=True)
p4.wait()


## 	1.d Compute genotype PCs:

p1b=subprocess.Popen('Rscript Scripts_geno_pheno/genotype_PCs.R', shell=True) #output: "Genotype_PCs_full.tab"
p1b.wait()

#		remove first columns (header) that is generated when exporting the file via the R script
p1b2=subprocess.Popen('awk '{$1=""; print $0}' Genotype_PCs_full.tab > Genotype_PCs_full_cut.tab', shell=True)
p1b2.wait()


#		 reformat en tab-sep
file=open('Genotype_PCs_full_cut.tab')
outfile=open('Genotype_PCs_full_cut_tab-sep.tab','w')
for line in file:
	outfile.write(line[1:].replace(' ','\t')) # from 1, because the above command to cut the first columns leave a space at the beginning of each line
file.close()
outfile.close()


## 	1.f To be consistant with the phenotype table: add 'chr' tag to the vcf (genotype) file

#		sort file:
p1c1=subprocess.Popen('vcf-sort -c GTEx_WGS_654Indiv_maf0.05_remove-indels_HG38.recode.vcf > GTEx_WGS_654Indiv_maf0.05_remove-indels_HG38_sorted.recode.vcf', shell=True)
p1c1.wait()

# 		compress and index the sorted file
p1c2=subprocess.Popen('bgzip GTEx_WGS_654Indiv_maf0.05_remove-indels_HG38_sorted.recode.vcf && tabix -p vcf GTEx_WGS_654Indiv_maf0.05_remove-indels_HG38_sorted.recode.vcf.gz', shell=True)
p1c2.wait() # index .tbi needed to add the chr tag

#		add 'chr' tag
p1c3=subprocess.Popen('bcftools annotate --rename-chrs Chromosomes_names.txt GTEx_WGS_654Indiv_maf0.05_remove-indels_HG38_sorted.vcf.gz > GTEx_WGS_HG38_sorted_chrtag.vcf', shell=True)
p1c3.wait()

#		compress and index the final .vcf file
p1c4=subprocess.Popen('bgzip GTEx_WGS_HG38_sorted_chrtag.vcf', shell=True)
p1c4.wait()
p1c5=subprocess.Popen('tabix -p vcf GTEx_WGS_HG38_sorted_chrtag.vcf.gz', shell=True)









## 2. Processing phenotype table:

## 	2.a Build a phenotype table from all fpkm tables.

#		From each file "transcripts_fpkm.txt" for each individuals ( that is, the outputs of processing SRA), this script build a table with transcripts_id as rowns and their expression level in each sample as columns
p5=subprocess.Popen('python Scripts_geno_pheno/make_table_phenotype.py', shell= True) #output: GTEx_phenotype_TPM_table.bed
p5.wait()

#		normalize phenotype table
p6=subprocess.Popen('Rscript Scripts_geno_pheno/normalize_phenotype_table.R', shell=True) #output: Pheno_table_normalized.bed
p6.wait()

#		sort sample columns in the phenotype file according to genotype columns order, and remove sample not contained in the genotype file.


p7=subprocess.Popen('python Scripts_geno_pheno/order_columns.py', shell=True) #output: GTEx_phenotype_TPM_normalized_table_columns_sorted_full.bed
p7.wait()


## 	2.b Compute phenotype PEER factors
p2b=subprocess.Popen('Rscript Scripts_geno_pheno/phenotype_PEER_factors.R', shell=True) #output: "GTEx.peer-factors_full.tab"


## 	2.c Indexing and compress phenotype file

p2c=subprocess.Popen('bgzip GTEx_phenotype_TPM_normalized_table_columns_sorted_full.bed && tabix -p bed GTEx_phenotype_TPM_normalized_table_columns_sorted_full.bed.gz', shell=True)
p2c.wait()




## 3. Combine covariates


p3a=subprocess.Popen('python combine_covariates.py Genotype_PCs_full_cut_tab-sep.tab GTEx.peer-factors_full.tab GTEx', shell=True)
p3a.wait()



