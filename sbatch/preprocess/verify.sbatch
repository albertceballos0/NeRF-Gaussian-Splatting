#!/bin/bash
#SBATCH --gres gpu:1
#SBATCH -p dcca40
#SBATCH --mem 8192
#SBATCH -o test_gpu_%j.out
#SBATCH -e test_gpu_%j.err

source /hhome/aceballosa/tfg/bin/activate
python -c "import torch; print(torch.cuda.is_available())"
deactivate
