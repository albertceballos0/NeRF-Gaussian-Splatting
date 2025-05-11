import argparse
import random
from subprocess import call

# --- RANGOS DE HIPERPARÁMETROS ---
NUM_SAMPLES_OPTIONS = [64, 128, 256]
MAX_ITERS_OPTIONS = [1000, 2000]
CONES_OPTIONS = [True, False]
RAYS_BATCH_OPTIONS = [1024, 2048]

# --- FUNCIONES ---
def call_train_script(dataset, model, data_type, num_samples, max_iters, cones, rays_batch):
    command = [
        "python3", "setup_nerf_project.py", "create",
        "--dataset", dataset,
        "--model", model,
        "--data-type", data_type,
        "--extra-train-args", f"--num_samples_per_ray {num_samples} --max_num_iterations {max_iters} --cones_enable {cones} --train_num_rays_per_batch {rays_batch}"
    ]
    print(f"Ejecutando: {' '.join(command)}")
    call(command)

def main():
    parser = argparse.ArgumentParser(description="Random Search de Scripts de Entrenamiento NeRF")
    parser.add_argument("--dataset", required=True, help="El dataset a usar para el entrenamiento")
    parser.add_argument("--model", required=True, help="El modelo NeRF a usar para el entrenamiento")
    parser.add_argument("--data-type", choices=["dnerf", ""], default="dnerf", help="Tipo de datos")
    parser.add_argument("--samples", type=int, default=10, help="Número de combinaciones aleatorias a generar")
    args = parser.parse_args()

    used_combinations = set()
    i = 0

    while i < args.samples:
        combo = (
            random.choice(NUM_SAMPLES_OPTIONS),
            random.choice(MAX_ITERS_OPTIONS),
            random.choice(CONES_OPTIONS),
            random.choice(RAYS_BATCH_OPTIONS),
        )
        # Evitar duplicados
        if combo in used_combinations:
            continue
        used_combinations.add(combo)
        i += 1
        num_samples, max_iters, cones, rays_batch = combo
        print(f"\nGenerando entrenamiento {i} con parámetros:")
        print(f"num_samples={num_samples}, max_iters={max_iters}, cones={cones}, rays_batch={rays_batch}")
        call_train_script(args.dataset, args.model, args.data_type, num_samples, max_iters, cones, rays_batch)

if __name__ == "__main__":
    main()
