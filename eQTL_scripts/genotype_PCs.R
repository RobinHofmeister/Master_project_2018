#!/usr/bin/env R


# source: https://bioconductor.org/packages/devel/bioc/vignettes/SNPRelate/inst/doc/SNPRelateTutorial.html#format-conversion-from-vcf-files

library(methods)

library(SNPRelate)
library(SeqArray, lib.loc="/Home/rhofmeis/R")

vcf.fn <- "/scratch/beegfs/monthly/rhofmeis_sra/dbGaP-8031/files/phg000830.v1.GTEx_WGS.genotype-calls-vcf.c1/GTEx_WGS_654Indiv_maf0.05_remove-indels.recode.vcf"
print('vcf.fn <- "/scratch/beegfs/monthly/rhofmeis_sra/dbGaP-8031/files/phg000830.v1.GTEx_WGS.genotype-calls-vcf.c1/GTEx_WGS_654Indiv_maf0.05_remove-indels.recode.vcf"')
seqVCF2GDS(vcf.fn, "test_full.gds")
print('seqVCF2GDS(vcf.fn, "test_full.gds")')
genofile <- seqOpen("test_full.gds")
print('genofile <- seqOpen("test_full.gds")')

snpset <- snpgdsLDpruning(genofile, ld.threshold=0.2)
print('snpset <- snpgdsLDpruning(genofile, ld.threshold=0.2)')
snpset.id <- unlist(snpset)
print('snpset.id <- unlist(snpset)')
pca <- snpgdsPCA(genofile, snp.id=snpset.id, num.thread=2)
print('pca <- snpgdsPCA(genofile, snp.id=snpset.id, num.thread=2)')
tab2 <- data.frame(sample.id = pca$sample.id, pca$eigenvect, stringsAsFactors = FALSE)
print('tab2 <- data.frame(sample.id = pca$sample.id, pca$eigenvect, stringsAsFactors = FALSE)')

write.table(t(tab2), "Genotype_PCs_full.tab",sep='\t', quote=F, col.names=F)



