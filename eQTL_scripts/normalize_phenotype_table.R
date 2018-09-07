#!/usr/bin/env R
library(preprocessCore)


a<-read.delim('GTEx_phenotype_TPM_table.bed', check.names=FALSE)


## short file that is used to validate the format
df1_short<-a[0:4,5:10]

### complete table
df1<-a[0:dim(a)[1],5:dim(a)[2]]
## extract chr, start, end, transcript id
df2<-a[0:dim(a)[1],0:4]
df2_short<-a[0:4,0:4]

## Normalization

df1_norm<-data.frame(normalize.quantiles(as.matrix(df1)))
df1_short_norm<-data.frame(normalize.quantiles(as.matrix(df1_short)))

colnames(df1_norm)<-names(df1)
colnames(df1_short_norm)<-names(df1_short)

## attach chr,start,end,transcript id

df1_norm_full<-cbind(df2,df1_norm)
df1_short_norm_full<-cbind(df2_short,df1_short_norm)


write.table(df1_short_norm_full, "Pheno_table_short_normalized.bed",sep='\t', quote=F, row.names=F)
write.table(df1_norm_full, "Pheno_table_normalized.bed",sep='\t', quote=F, row.names=F)




