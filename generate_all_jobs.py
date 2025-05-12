import argparse
import random
from subprocess import call

LR_OPTIONS = [1e-4, 5e-4, 1e-3]
COARSE_SAMPLES_OPTIONS = [32, 64, 96]
IMPORTANCE_SAMPLES_OPTIONS = [32, 64, 128]
TEMPORAL_DISTORTION_OPTIONS = [True, False]

def call_train_script(dataset, model, data_type, lr, coarse_samples, importance_samples, temporal_distortion):
    extra_args = (
        f"--optimizers.fields.optimizer.lr {lr} "
        f"--pipeline.model.num-coarse-samples {coarse_samples} "
        f"--pipeline.model.num-importance-samples {importance_samples} "
        f"--pipeline.model.enable-temporal-distortion {temporal_distortion}"
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
    parser.add_argument("--samples", type=int, default=10, help="Número de combinaciones aleatorias a generar")
    args = parser.parse_args()

    used_combinations = set()
    i = 0

    while i < args.samples:
        combo = (
            random.choice(LR_OPTIONS),
            random.choice(COARSE_SAMPLES_OPTIONS),
            random.choice(IMPORTANCE_SAMPLES_OPTIONS),
            random.choice(TEMPORAL_DISTORTION_OPTIONS),
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
