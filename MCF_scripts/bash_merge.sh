#!/bin/bash

#BSUB -L /bin/bash
#BSUB -o /scratch/beegfs/monthly/rhofmeis/Merged_assembly/bash_merge.out
#BSUB -e /scratch/beegfs/monthly/rhofmeis/Merged_assembly/bash_merge.err
#BSUB -R "select[mem>15000]"
#BSUB -R "select[tmp>15000]"
#BSUB -R "rusage[mem=15000:swp=15000]"
#BSUB -R "rusage[tmp=15000]"
#BSUB -M 15000000
#BSUB -u robin.hofmeister@unil.ch
#BSUB -N


mkdir Merged_assembly

module add UHTS/Quality_control/fastqc/0.11.5;
module add UHTS/Aligner/hisat/2.1.0;
module add UHTS/Analysis/sratoolkit/2.8.2.1;
module add UHTS/Analysis/trimmomatic/0.36;
module add UHTS/Analysis/samtools/1.8;
module add UHTS/Aligner/stringtie/1.3.3b;
module add UHTS/Analysis/BEDTools/2.26.0;

python python_merge.py
