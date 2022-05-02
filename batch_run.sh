#!/bin/bash
#SBATCH -N 1
#SBATCH -t 0:10:00
#SBATCH -p GPU-shared
#SBATCH --gpus=1 
#SBATCH --mail-type=ALL 

module purge
module load AI/anaconda3-tf1.2020.11
source activate $AI_ENV


cd /ocean/projects/cis220010p/wzhangk/cv_project

for 



