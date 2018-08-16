0)	Download annotations files

		bsub < bash_annotations.sh


1) 	Trimming, QC, mapping, transcripts assembly

		1a) bsub < bash_library1.sh

		1b) bsub < bash_library2.sh

2) 	a. Merge transcript from library 1 and 2 into a non redundant set of transcripts.
	b. Use the non redundant set of transcript as annotations in Stringtie to quantify transcripts expression level.
	c. Annotate long intergenic noncoding RNAs.
	d. This script ends with a set of long intergenic transcripts (split in three files). Run CPC2 on those three files-> three CPC2 results files.

		bsub < bash_merge.sh

3)	a. Use CPC2 results to call denovo and known lincRNAs
	b. Use expression level in both library to create set of breast expressed transcripts
	c. Create a gtf file with gencode PCGs, known and denovo lincRNAs, that will be used to as annotations to quantify GTEx transcripts.
	d. Create .csv file with expression level (TPM and FPKM) of lincRNAs and PCGs

		bsub < bash_after_cpc2.sh

The main outputs of these commandes are i) a gtf file 'Final_gtf.gtf' use to quantify GTEx transcripts, ii) two .csv files that contain lincRNAs and PCGs expression level (library1, library 2, mean expression level)
