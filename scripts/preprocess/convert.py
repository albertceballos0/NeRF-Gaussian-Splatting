import json
import os
import sys


intrinsics = {
    "fx": 1000.0,
    "fy": 1000.0,
    "cx": 320.0,
    "cy": 240.0
}

# Función para modificar el nombre de los archivos en el JSON
def update_file_paths(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    # Recorrer los frames y modificar el nombre del archivo
    for frame in data['frames']:
        # Añadir la extensión '.png' al nombre del archivo
        if not frame['file_path'].endswith('.png'):
            frame['file_path'] += '.png'
        frame.update(intrinsics)
        
        
    # Sobrescribir el archivo JSON actualizado
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=4)

    print(f"Archivo JSON actualizado y sobrescrito: {json_file}")

if __name__ == "__main__":
    # Verificar si se pasó el nombre del archivo como argumento
    if len(sys.argv) != 2:
        print("Uso: python convert.py <archivo_transforms.json>")
        sys.exit(1)

    # Obtener el nombre del archivo desde los argumentos
    json_file = sys.argv[1]
    
    # Llamar a la función para actualizar los archivos
    update_file_paths(json_file)
