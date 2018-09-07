#!/usr/bin/env R


# source: https://bioconductor.org/packages/devel/bioc/vignettes/SNPRelate/inst/doc/SNPRelateTutorial.html#format-conversion-from-vcf-files

library(methods)

library(SNPRelate)
library(SeqArray, lib.loc="/Home/rhofmeis/R")

vcf.fn <- "/scratch/beegfs/monthly/rhofmeis_sra/dbGaP-8031/files/phg000830.v1.GTEx_WGS.genotype-calls-vcf.c1/GTEx_lincrna_eQTL.recode.vcf"
seqVCF2GDS(vcf.fn, "test_full_lincRNA-eQTL.gds")

genofile <- seqOpen("test_full_lincRNA-eQTL.gds")

snpset <- snpgdsLDpruning(genofile, ld.threshold=0.2)

snpset.id <- unlist(snpset)

pca <- snpgdsPCA(genofile, snp.id=snpset.id, num.thread=2)


tab2 <- data.frame(sample.id = pca$sample.id, pca$eigenvect, stringsAsFactors = FALSE)

write.table(t(tab2), "Genotype_PCs_full_lincRNA-eQTL.tab",sep='\t', quote=F, col.names=F)



