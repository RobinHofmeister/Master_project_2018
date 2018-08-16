

#!/bin/bash

#BSUB -L /bin/bash
#BSUB -o /scratch/beegfs/monthly/rhofmeis_sra/dbGaP-8031/mapping/mapp_SRRxxx/SRRxxx.out
#BSUB -e /scratch/beegfs/monthly/rhofmeis_sra/dbGaP-8031/mapping/mapp_SRRxxx/SRRxxx.err
#BSUB -R "select[mem>12000]"
#BSUB -R "select[tmp>12000]"
#BSUB -R "rusage[mem=12000]"
#BSUB -R "rusage[tmp=12000]"
#BSUB -M 12000000
#BSUB -u robin.hofmeister@unil.ch
#BSUB -N



module add UHTS/Aligner/hisat/2.1.0;
module add UHTS/Analysis/sratoolkit/2.8.2.1;
module add UHTS/Analysis/trimmomatic/0.36;
module add UHTS/Analysis/samtools/1.8;
module add UHTS/Aligner/stringtie/1.3.3b;


python python_SRRxxx.py


