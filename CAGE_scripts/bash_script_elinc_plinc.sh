#!/bin/bash

#BSUB -L /bin/bash
#BSUB -o /scratch/beegfs/monthly/rhofmeis/CAGE/Out.out
#BSUB -e /scratch/beegfs/monthly/rhofmeis/CAGE/Err.err
#BSUB -R "select[mem>18000]"
#BSUB -R "select[tmp>18000]"
#BSUB -R "rusage[mem=18000]"
#BSUB -R "rusage[tmp=18000]"
#BSUB -M 18000000
#BSUB -u robin.hofmeister@unil.ch
#BSUB -N


module add Utility/UCSC-utils/359;
module add UHTS/Analysis/BEDTools/2.26.0;

python script_elinc_plinc.py

