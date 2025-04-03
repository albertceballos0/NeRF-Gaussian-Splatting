#!/bin/bash
#SBATCH --gres gpu:1
#SBATCH -p dcca40
#SBATCH --mem 8192
#SBATCH -o test_gpu_%j.out
#SBATCH -e test_gpu_%j.err

conda activate nerfstudio 
python -c "import torch; print(torch.cuda.is_available())"
python -c "import torch; print(torch.__version__, torch.version.cuda, torch.cuda.get_device_name(0))"
python -c "import torch; print('PyTorch:', torch.__version__, '| CUDA:', torch.version.cuda, '| GPU:', torch.cuda.get_device_name(0))"
CUDA_VISIBLE_DEVICES=0 ns-train --help | grep -i "cuda\|gpu"


conda deactivate
