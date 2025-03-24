#!/bin/bash

# Definir las rutas
WORKSPACE_DIR="../../datasets/${1}"
IMAGES_DIR="${WORKSPACE_DIR}/images"
DATABASE_PATH="${WORKSPACE_DIR}/database.db"
SPARSE_DIR="${WORKSPACE_DIR}/sparse"
DENSE_DIR="${WORKSPACE_DIR}/dense"
POINTS3D_FILE="${DENSE_DIR}/points3D.ply"

# Crear directorios si no existen
mkdir -p ${IMAGES_DIR} ${SPARSE_DIR} ${DENSE_DIR}

# Paso 1: Crear base de datos de COLMAP
echo "Creando base de datos COLMAP..."
colmap database_creator --database_path ${DATABASE_PATH}

# Paso 2: Extraer características de las imágenes
echo "Extrayendo características de las imágenes..."
colmap feature_extractor --database_path ${DATABASE_PATH} --image_path ${IMAGES_DIR}

# Paso 3: Emparejar imágenes
echo "Emparejando imágenes..."
colmap sequential_matcher --database_path ${DATABASE_PATH}

# Paso 4: Ejecutar Structure from Motion (SfM) para reconstrucción 3D
echo "Ejecutando Structure from Motion..."
colmap mapper --database_path ${DATABASE_PATH} --image_path ${IMAGES_DIR} --output_path ${SPARSE_DIR}

# Paso 5: Generar nube de puntos densa (PatchMatch Stereo)
echo "Generando nube de puntos densa..."
colmap patch_match_stereo \
    --workspace_path ${WORKSPACE_DIR} \
    --image_path ${IMAGES_DIR} \
    --output_path ${DENSE_DIR} \
    --DenseStereo.device CPU

# Paso 6: Fusionar la nube de puntos densa
echo "Fusionando nube de puntos..."
colmap stereo_fusion --workspace_path ${WORKSPACE_DIR} --output_path ${POINTS3D_FILE}

# Finalización
echo "El procesamiento ha finalizado. La nube de puntos se encuentra en: ${POINTS3D_FILE}"

