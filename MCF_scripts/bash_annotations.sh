#!/bin/bash

#BSUB -L /bin/bash
#BSUB -o /scratch/beegfs/monthly/rhofmeis/Annotations/bash_annotations.out
#BSUB -e /scratch/beegfs/monthly/rhofmeis/Annotations/bash_annotations.err
#BSUB -R "select[mem>15000]"
#BSUB -R "select[tmp>15000]"
#BSUB -R "rusage[mem=15000]"
#BSUB -R "rusage[tmp=15000]"
#BSUB -M 15000000
#BSUB -u robin.hofmeister@unil.ch
#BSUB -N

mkdir Annotations

python python_annotations.py
