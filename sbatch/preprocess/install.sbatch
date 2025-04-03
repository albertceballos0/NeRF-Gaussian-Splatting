#!/bin/bash
#SBATCH -n 4                 
#SBATCH -N 1                 
#SBATCH -D /tmp              
#SBATCH -t 2-00:00           
#SBATCH -p dcca40               # Usar la cola TFG
#SBATCH --mem 8192           
#SBATCH --gres gpu:1         
#SBATCH -o trex_%u_%j.out  
#SBATCH -e trex_%u_%j.err  

# Activar el entorno virtual
conda activate nerfstudio


# Ejecutar el comando de entrenamiento de NeRFStudio
pip install git+https://github.com/NVlabs/tiny-cuda-nn/#subdirectory=bindings/torch

# Desactivar el entorno virtua
conda deactivate