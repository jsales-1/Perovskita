#!/bin/bash
#SBATCH -n 18
#SBATCH --ntasks-per-node=18
#SBATCH -p batch-AMD
#SBATCH --job-name=graph-groups

source ~/.bashrc
conda activate ilumpy
python -u "Rede de Citações".py 
deactivate