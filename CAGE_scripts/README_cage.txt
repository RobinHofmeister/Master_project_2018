ElincRNAs, plincRNAs, PCGs annotation using CAGE


A. Determine transcription initiation regions within active enhancers and promoters:

	A1. 	Overlap enhancers with DHSI regions to get accessible enhancers
	A2. 	Get intergenic regions of the genome
	A3. 	Exclude blacklist regions from hg38 intergenic region
	A4. 	Overlap accessible enhancers with intergenic region to get intergenic enhancers
	A5. 	Overlap intergenic enhancers with CAGE TIRs to get enhancer-associated TIRs (eTIRs) and promoter-associated TIRs (pTIRs)
		
		A5.a 	Annotate TSS from CAGE reads: script 'cluster_CAGE_reads_into_TSS.py'
			Method:	- get the three replicates of Mcf7 CAGE reads and merge them
				- extract 5' ends of each reads
				- cluster 5' ends closer than 20bp on the same strand (-> cluster20bp)
				- cluster20bp closer than 400bp and on the same strand are considered in the same TSS.
				- keep TSS supported by more than 4 CAGE reads.


B. Determine expressed elincRNAs/plincRNAs/PCGs using CAGE data

	B1.	Intersect CAGE reads with TSS. Outputs CAGE read if intersect with eTIRs, pTIRs or pcgTIRs.
	B2.	Intersect the previous output with the first exon of lincRNAs or PCGs. Output lincRNAs or PCGs if intersected. 
					-> elincRNAs if CAGE reads intersect both a eTIRs and lincRNA first exon
					-> plincRNAs if CAGE reads intersect both a pTIRs and lincRNA first exon
					-> pPCGs if CAGE reads intersect both pcgTIRs and PCG first exon



				bsub < bash_script_elinc_plinc.sh
