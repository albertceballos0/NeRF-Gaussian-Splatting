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
source /hhome/aceballosa/tfg/bin/activate
# Ejecutar el comando de entrenamiento de NeRFStudio
pip uninstall tinycudann
pip install git+https://github.com/NVlabs/tiny-cuda-nn.git --no-cache-dir

# Desactivar el entorno virtua
deactivate