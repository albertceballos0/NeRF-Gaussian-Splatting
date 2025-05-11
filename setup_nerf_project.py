# === SCRIPT PRINCIPAL: setup_nerf_project.py ===

import argparse
import os
from pathlib import Path

# --- CONFIGURACIÓN ---

DATA_BASE = "/hhome/aceballosa/NeRF-Gaussian-Splatting/datasets"
OUTPUT_BASE = "/hhome/aceballosa/NeRF-Gaussian-Splatting/outputs"
EXPORT_BASE = "/hhome/aceballosa/NeRF-Gaussian-Splatting/exports"
TRAIN_BASE = "./sbatch/train"
SBATCH_DIR = "./sbatch"
SCRIPT_PATH = "/hhome/aceballosa/NeRF-Gaussian-Splatting/setup_nerf_project.py"
CONDA_ENV = "nerfstudio"

SBATCH_TRAIN_TEMPLATE = """#!/bin/bash
#SBATCH -n 4
#SBATCH -N 1
#SBATCH -D /tmp
#SBATCH -t 2-00:00
#SBATCH -p dcca40
#SBATCH --mem 8192
#SBATCH --gres gpu:1
#SBATCH -o train_%u_%j.out
#SBATCH -e train_%u_%j.err

conda activate nerfstudio

# Entrenamiento
ns-train {model} --data {data_path} --output-dir {output_path} {data_type} {extra_train_args}

# Encontrar el último timestamp generado
OUTPUT_MODEL_PATH="{output_path}/{dataset}/{model}"
NEW_TIMESTAMP=$(ls -d "$OUTPUT_MODEL_PATH"/*/ | sort -n | tail -n 1)
NEW_TIMESTAMP=$(basename "$NEW_TIMESTAMP")

# Comprobar si existe el config.yml
CONFIG_PATH="$OUTPUT_MODEL_PATH/$NEW_TIMESTAMP/config.yml"
if [ ! -f "$CONFIG_PATH" ]; then
  echo "❌ No se encontró config.yml en $CONFIG_PATH"
  exit 1
fi

# Crear automáticamente el script de exportación
echo "Generando script de exportación para $NEW_TIMESTAMP"
python3 {script_path} export --dataset {dataset} --model {model} --train-number "$NEW_TIMESTAMP"

# Lanzar exportación directamente
EXPORT_PATH="{export_base}/{train_name}/{dataset}/{model}/$NEW_TIMESTAMP"
mkdir -p "$EXPORT_PATH"

ns-export pointcloud --load-config "$CONFIG_PATH" --output-dir "$EXPORT_PATH" \
  --num-points 1000000 --remove-outliers True --normal-method open3d --save-world-frame False

ns-export poisson --load-config "$CONFIG_PATH" --output-dir "$EXPORT_PATH" \
  --num-points 1000000 --remove-outliers True --normal-method open3d

conda deactivate
"""

SBATCH_EXPORT_TEMPLATE = """#!/bin/bash
#SBATCH -n 4
#SBATCH -N 1
#SBATCH -D /tmp
#SBATCH -t 2-00:00
#SBATCH -p dcca40
#SBATCH --mem 8192
#SBATCH --gres gpu:1
#SBATCH -o export_%u_%j.out
#SBATCH -e export_%u_%j.err

conda activate {conda_env}

ns-export pointcloud --load-config {config_path} --output-dir {export_path} \
  --num-points {num_points} --remove-outliers {remove_outliers} --normal-method {normal_method} --save-world-frame {save_world_frame} {extra_export_args}

ns-export poisson --load-config {config_path} --output-dir {export_path} \
  --num-points {num_points} --remove-outliers {remove_outliers} --normal-method {normal_method} {extra_export_args}

conda deactivate
"""

def get_next_number(base_path, prefix):
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    existing = [f for f in os.listdir(base_path) if f.startswith(prefix)]
    numbers = [int(f[len(prefix):].split('.')[0]) for f in existing if f[len(prefix):].split('.')[0].isdigit()]
    return max(numbers) + 1 if numbers else 1

def create_train_script(args):
    data_path = args.dataset
    dataset = os.path.basename(args.dataset)
    model = args.model
    data_type = "dnerf-data" if args.data_type == "dnerf" else ""
    extra_args = args.extra_train_args

    output_dir = Path(TRAIN_BASE) / dataset / model
    output_dir.mkdir(parents=True, exist_ok=True)
    train_number = get_next_number(output_dir, "train_")
    train_name = f"train_{train_number:02d}"

    data_path = os.path.join(DATA_BASE, data_path)
    output_path = Path(OUTPUT_BASE) / train_name
    sbatch_path = Path(TRAIN_BASE) / dataset / model
    sbatch_path.mkdir(parents=True, exist_ok=True)
    train_script_path = sbatch_path / f"{train_name}.qsub"

    script_content = SBATCH_TRAIN_TEMPLATE.format(
        model=model,
        data_path=data_path,
        output_path=output_path,
        data_type=data_type,
        extra_train_args=extra_args,
        dataset=dataset,
        script_path=SCRIPT_PATH,
        export_base=EXPORT_BASE,
        train_number=train_number,
        train_name=train_name
    )

    train_script_path.write_text(script_content)
    print(f"✅ Entrenamiento creado: {train_script_path}")

def create_export_script(args):
    dataset = args.dataset
    model = args.model
    train_number = str(args.train_number)
    export_dir = Path(SBATCH_DIR) / "export" / dataset / model / train_number
    export_dir.mkdir(parents=True, exist_ok=True)

    next_export_number = get_next_number(export_dir, "export_")
    export_name = f"export_{next_export_number:02d}"

    config_path = None
    for root, dirs, files in os.walk(os.path.join(OUTPUT_BASE, dataset, model)):
        if "config.yml" in files and train_number in root:
            config_path = os.path.join(root, "config.yml")
            break

    if not config_path:
        print(f"❌ Error: No se encontró el archivo de configuración para el entrenamiento {train_number}")
        return

    export_path = os.path.join(EXPORT_BASE, dataset, model, train_number)
    export_script_path = export_dir / f"{export_name}.qsub"

    script_content = SBATCH_EXPORT_TEMPLATE.format(
        conda_env=CONDA_ENV,
        config_path=config_path,
        export_path=export_path,
        num_points=args.num_points,
        remove_outliers=str(args.remove_outliers),
        normal_method=args.normal_method,
        save_world_frame=str(args.save_world_frame),
        extra_export_args=args.extra_export_args
    )

    export_script_path.write_text(script_content)
    print(f"✅ Export creado: {export_script_path}")

def main():
    parser = argparse.ArgumentParser(description="Gestor de entrenamientos y exports NeRF-Gaussian.")
    subparsers = parser.add_subparsers(dest="command")

    create_parser = subparsers.add_parser("create", help="Crear entrenamiento")
    create_parser.add_argument("--dataset", required=True)
    create_parser.add_argument("--model", required=True)
    create_parser.add_argument("--data-type", choices=["dnerf", ""], default="")
    create_parser.add_argument("--extra-train-args", default="")

    export_parser = subparsers.add_parser("export", help="Crear export de un entrenamiento")
    export_parser.add_argument("--dataset", required=True)
    export_parser.add_argument("--model", required=True)
    export_parser.add_argument("--train-number", type=str, required=True)
    export_parser.add_argument("--num-points", type=int, default=1000000)
    export_parser.add_argument("--remove-outliers", action="store_true")
    export_parser.add_argument("--normal-method", default="open3d")
    export_parser.add_argument("--save-world-frame", action="store_true")
    export_parser.add_argument("--extra-export-args", default="")

    args = parser.parse_args()

    if args.command == "create":
        create_train_script(args)
    elif args.command == "export":
        create_export_script(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()


# === SCRIPT DE COMBINACIONES: generate_combinations.py ===

import argparse
from subprocess import call

COMBINATIONS = [
    (64, 1000, True, 100, 1024, 1024),
    (64, 1000, True, 100, 1024, 2048),
    # ... (recorta o amplía aquí si es necesario)
]

def call_train_script(dataset, model, data_type, num_samples, max_iters, cones, steps, rays_batch, eval_rays):
    extra_train_args = (
        f"--pipeline.model.num_samples_per_ray={num_samples} "
        f"--max_num_iterations={max_iters} "
        f"--pipeline.model.cones_enable={str(cones).lower()} "
        f"--pipeline.model.steps_per_eval_batch={steps} "
        f"--pipeline.model.train_num_rays_per_batch={rays_batch} "
        f"--pipeline.model.eval_num_rays_per_batch={eval_rays}"
    )
    command = [
        "python3", "setup_nerf_project.py", "create",
        "--dataset", dataset,
        "--model", model,
        "--data-type", data_type,
        "--extra-train-args", extra_train_args
    ]
    print(f"\n[RUNNING] {' '.join(command)}")
    call(command)

def main():
    parser = argparse.ArgumentParser(description="Generador de Scripts de Entrenamiento NeRF")
    parser.add_argument("--dataset", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--data-type", choices=["dnerf", ""], default="dnerf")
    args = parser.parse_args()

    for i, (num_samples, max_iters, cones, steps, rays_batch, eval_rays) in enumerate(COMBINATIONS, 1):
        print(f"\nCombinación {i}: ns={num_samples}, it={max_iters}, cone={cones}, steps={steps}, rb={rays_batch}, eval={eval_rays}")
        call_train_script(args.dataset, args.model, args.data_type, num_samples, max_iters, cones, steps, rays_batch, eval_rays)

if __name__ == "__main__":
    main()
