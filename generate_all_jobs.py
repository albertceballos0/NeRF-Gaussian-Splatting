import argparse
import random
from subprocess import call

LR_OPTIONS = [1e-4, 1e-3]
COARSE_SAMPLES_OPTIONS = [32, 96]
NUM_RAYS_PER_BATCH_OPTIONS = [1024, 8192, 16384]
NUM_STEPS = [10000, 60000, 200000]

def call_train_script(dataset, model, data_type, lr, coarse_samples, num_rays_per_batch, num_iterations):
    extra_args = (
        f"--optimizers.fields.optimizer.lr {lr} "
        f"--pipeline.model.num-coarse-samples {coarse_samples} "
        #f"--pipeline.model.num-importance-samples {importance_samples} "
        f"--pipeline.datamanager.train-num-rays-per-batch {num_rays_per_batch} "
        f"--max-num-iterations {num_iterations} "
        f""
    )

    command = [
        "python3", "setup_nerf_project.py", "create",
        "--dataset", dataset,
        "--model", model,
        "--data-type", data_type,
        "--extra-train-args", extra_args
    ]

    print(f"🔁 Ejecutando:\n{' '.join(command)}\n")
    call(command)


def main():
    parser = argparse.ArgumentParser(description="Random Search de Scripts de Entrenamiento NeRF")
    parser.add_argument("--dataset", required=True, help="El dataset a usar para el entrenamiento")
    parser.add_argument("--model", required=True, help="El modelo NeRF a usar para el entrenamiento")
    parser.add_argument("--data-type", choices=["dnerf", ""], default="dnerf", help="Tipo de datos")
    parser.add_argument("--search", type=int, default=0, help="0: Random Search, 1: Grid Search (default: 0)")
    parser.add_argument("--samples", type=int, default=10, help="Número de combinaciones aleatorias a generar")
    args = parser.parse_args()

    i = 0
    used_combinations = set()
    if args.search == 1:
        # Generar combinaciones de parámetros para Grid Search
        for lr in LR_OPTIONS:
            for coarse_samples in COARSE_SAMPLES_OPTIONS:
                for num_rays_per_batch in NUM_RAYS_PER_BATCH_OPTIONS:
                    for num_steps in NUM_STEPS:
                        combo = (lr, coarse_samples, num_rays_per_batch, num_steps)
                        print(f"\nGenerando entrenamiento {i} con parámetros:")
                        print(f"lr={lr}, coarse_samples={coarse_samples} rays_batch={num_rays_per_batch}, num_steps={num_steps}")
                        call_train_script(args.dataset, args.model, args.data_type, lr, coarse_samples, num_rays_per_batch, num_steps)
                        i += 1
    else:
        while i < args.samples:
            combo = (
                random.choice(LR_OPTIONS),
                random.choice(COARSE_SAMPLES_OPTIONS),
                random.choice(NUM_RAYS_PER_BATCH_OPTIONS),
                random.choice(NUM_STEPS)
            )
            # Evitar duplicados
            if combo in used_combinations:
                continue
            used_combinations.add(combo)
            i += 1
            combo = (lr, coarse_samples, num_rays_per_batch, num_steps)
            print(f"\nGenerando entrenamiento {i} con parámetros:")
            print(f"lr={lr}, num_samples={coarse_samples} rays_batch={num_rays_per_batch}, num_steps={num_steps}")
            call_train_script(args.dataset, args.model, args.data_type, lr, coarse_samples, num_rays_per_batch, num_steps)

if __name__ == "__main__":
    main()
