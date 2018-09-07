#!/usr/bin/env R



library(peer, lib.loc="/Home/rhofmeis/R")

e=read.table('GTEx_phenotype_TPM_normalized_table_columns_sorted_full.bed')

e2<-e[1:dim(e)[1],5:dim(e)[2]]
e2<-as.matrix(e2)

model = PEER()

e3<-t(e2)

PEER_setPhenoMean(model,e3)


PEER_setNk(model,48)

PEER_setNmax_iterations(model, 15000)

PEER_setAdd_mean(model, TRUE)

PEER_update(model)

factors = PEER_getX(model)

## get sample id
exp=read.table('GTEx_phenotype_TPM_normalized_table_columns_sorted_full_v2.bed')

sample_id<-t(exp[1, 5:dim(exp)[2]])


df<-cbind(sample_id,factors)

write.table(t(df), "GTEx.peer-factors_full.tab", sep='\t', quote=F, col.names=F, row.names=F)
