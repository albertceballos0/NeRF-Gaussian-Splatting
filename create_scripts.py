import os
import random
from pathlib import Path
from nerfstudio.engine.trainer import TrainerConfig

# Número de combinaciones
NUM_EXPERIMENTS = 5

# Hiperparámetros a variar (puedes expandir)
param_grid = {
    "fields_lr": [1e-2, 5e-3],
    "hidden_dim": [64, 128, 256],
    "max_iterations": [10000, 20000, 30000],
}

# Directorios
base_config_path = "base_config.yaml"
configs_dir = Path("configs_auto")
scripts_dir = Path("scripts")
configs_dir.mkdir(exist_ok=True)
scripts_dir.mkdir(exist_ok=True)

# Función para crear combinaciones
def generate_random_config(index: int):
    cfg = TrainerConfig.load_config(base_config_path)

    # Asignar hiperparámetros
    cfg.optimizers["fields"].optimizer.lr = random.choice(param_grid["fields_lr"])
    cfg.pipeline.model.hidden_dim = random.choice(param_grid["hidden_dim"])
    cfg.max_num_iterations = random.choice(param_grid["max_iterations"])

    # Guardar config
    config_name = f"config_{index:02d}.yaml"
    config_path = configs_dir / config_name
    cfg.save_config(config_path)
    return config_name

# Generar scripts
for i in range(NUM_EXPERIMENTS):
    config_file = generate_random_config(i)
    script_path = scripts_dir / f"train_{i:02d}.py"

    with open(script_path, "w") as f:
        f.write(f"""\
from nerfstudio.engine.trainer import TrainerConfig

cfg = TrainerConfig.load_config("configs_auto/{config_file}")
cfg.setup().train()
""")

print(f"{NUM_EXPERIMENTS} scripts generados en '{scripts_dir}' y configs en '{configs_dir}'")
