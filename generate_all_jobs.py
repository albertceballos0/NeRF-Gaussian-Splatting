import argparse
from subprocess import call

# --- CONFIGURACIÓN DE HIPERPARÁMETROS PREDEFINIDOS ---
COMBINATIONS = [
    (64, 1000, True, 100, 1024, 1024),
    (64, 1000, True, 100, 1024, 2048),
    (64, 1000, True, 100, 2048, 1024),
    (64, 1000, True, 100, 2048, 2048),
    (64, 2000, True, 100, 1024, 1024),
    (64, 2000, True, 100, 1024, 2048),
    (64, 2000, True, 100, 2048, 1024),
    (64, 2000, True, 100, 2048, 2048),
    (128, 1000, True, 100, 1024, 1024),
    (128, 1000, True, 100, 1024, 2048),
    (128, 1000, True, 100, 2048, 1024),
    (128, 1000, True, 100, 2048, 2048),
    (128, 2000, True, 100, 1024, 1024),
    (128, 2000, True, 100, 1024, 2048),
    (128, 2000, True, 100, 2048, 1024),
    (128, 2000, True, 100, 2048, 2048),
    (256, 1000, False, 100, 1024, 1024),
    (256, 1000, False, 100, 1024, 2048),
    (256, 1000, False, 100, 2048, 1024),
    (256, 1000, False, 100, 2048, 2048),
    (256, 2000, False, 100, 1024, 1024),
]

# --- FUNCIONES ---
def call_train_script(dataset, model, data_type, extra_train_args, num_samples, max_iters, cones, steps, rays_batch, eval_rays):
    """
    Llama al script principal para crear el script de SLURM de entrenamiento.
    """
    command = [
        "python3", "setup_nerf_project.py", "create",
        "--dataset", dataset,
        "--model", model,
        "--data-type", data_type,
        "--extra-train-args", (
            f"--max-num-iterations {max_iters} "
            f"--pipeline.model.cones-enable {cones} "
            f"--trainer.steps-per-eval-batch {steps} "
            f"--pipeline.datamanager.train-num-rays-per-batch {rays_batch} "
            f"--pipeline.datamanager.eval-num-rays-per-batch {eval_rays}"
        )
    ]
    print(f"Ejecutando: {' '.join(command)}")
    call(command)

def main():
    parser = argparse.ArgumentParser(description="Generador de Scripts de Entrenamiento NeRF")
    parser.add_argument("--dataset", required=True, help="El dataset a usar para el entrenamiento")
    parser.add_argument("--model", required=True, help="El modelo NeRF a usar para el entrenamiento")
    parser.add_argument("--data-type", choices=["dnerf", ""], default="dnerf", help="Tipo de datos")
    args = parser.parse_args()

    # Llamar al script principal para cada combinación predefinida
    for i, (num_samples, max_iters, cones, steps, rays_batch, eval_rays) in enumerate(COMBINATIONS, 1):
        print(f"\nGenerando entrenamiento {i} con parámetros:")
        print(f"num_samples={num_samples}, max_iters={max_iters}, cones={cones}, steps={steps}, rays_batch={rays_batch}, eval_rays={eval_rays}")
        call_train_script(args.dataset, args.model, args.data_type, "", num_samples, max_iters, cones, steps, rays_batch, eval_rays)

if __name__ == "__main__":
    main()
