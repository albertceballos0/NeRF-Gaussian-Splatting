#!/bin/bash
#SBATCH -n 4                 
#SBATCH -N 1                 
#SBATCH -D /tmp              
#SBATCH -t 2-00:00           
#SBATCH -p tfg               # Usar la cola TFG
#SBATCH --mem 8192           
#SBATCH --gres gpu:1         
#SBATCH -o lego_%u_%j.out  
#SBATCH -e lego_%u_%j.err  

# Activar el entorno virtual
source /fhome/aceballos/venvs/nerfstudio/bin/activate

# Ejecutar el comando de entrenamiento de NeRFStudio
ns-export gaussian-splat --load-config /fhome/aceballos/tfg/NeRF-Gaussian-Splatting/outputs/lego/gaussian_splatting/lego/splatfacto/2025-03-27_173621 --output-dir /fhome/aceballos/tfg/NeRF-Gaussian-Splatting/exports/lego/gaussian_splatting 


deactivate