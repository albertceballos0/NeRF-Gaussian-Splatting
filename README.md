# 🧠 setup_nerf_project.py

Script CLI en Python para automatizar la creación de scripts `.qsub` usados para entrenar y exportar escenas NeRF con [Nerfstudio](https://docs.nerfstudio.org/).

## 🚀 Requisitos
- Python 3.7+
- Entorno Conda con `nerfstudio` instalado y activable con `conda activate nerfstudio`
- Estructura fija de rutas en el sistema de archivos:
  - Datasets: `/hhome/aceballosa/NeRF-Gaussian-Splatting/datasets`
  - Resultados: `/hhome/aceballosa/NeRF-Gaussian-Splatting/outputs`
  - Exportaciones: `/export/hhome/aceballosa/NeRF-Gaussian-Splatting/exports`

## ⚙️ Uso

### 1. Crear script de entrenamiento

```bash
python setup_nerf_project.py create --dataset <ruta_relativa_dataset> --model <modelo>
```

#### Ejemplo:

```bash
python setup_nerf_project.py create --dataset dnerf/trex --model nerfacto
```

#### Estructura generada:
```
sbatch/train/nerfacto/trex/train_01.qsub
```

---

### 2. Crear script de exportación

```bash
python setup_nerf_project.py export --experiment <modelo>/<timestamp>
```

#### Ejemplo:

```bash
python setup_nerf_project.py export --experiment nerfacto/2025-04-04_200704
```

#### Estructura generada:
```
sbatch/export/nerfacto/trex/export_01.qsub
```

---

## 🧾 Detalles de los scripts `.qsub`

### Entrenamiento

```bash
#!/bin/bash
...
ns-train <modelo> --data <ruta_dataset> --output-dir <ruta_output> dnerf-data
...
```

### Exportación

```bash
#!/bin/bash
...
ns-export pointcloud --load-config <ruta_config.yml> --output-dir <ruta_export> ...
...
```

---

## 📁 Estructura esperada

```
.
├── datasets/
├── outputs/
├── exports/
└── sbatch/
    ├── train/
    └── export/
```
