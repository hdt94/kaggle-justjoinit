# Análisis descriptivo: [JustJoinIT job offers data (2021.10 - 2023-09)](https://www.kaggle.com/datasets/jszafranqb/justjoinit-job-offers-data-2021-10-2023-09)

Análisis descriptivo de los datos [JustJoinIT job offers data (2021.10 - 2023-09)](https://www.kaggle.com/datasets/jszafranqb/justjoinit-job-offers-data-2021-10-2023-09) basado en requerimientos dados.

## Datos

El directorio de datos puede ser cualquier ruta del sistema.

## Configuración

Linux o macOS:
```shell
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

Windows:
```
python -m venv venv
source venv/bin/activate.bat
pip3 install -r requirements.txt
```

## Ejecución

Usando Shell:
```shell
DATA_DIR="$(realpath ./data)"
python3 src/main.py --data-dir="$DATA_DIR"
python3 src/main.py --data-dir="$DATA_DIR" --prefix="small"
```

Usando módulos:
```python
from main import main

data_dir = ""
prefix = ""
main(data_dir)
main(data_dir, prefix)
```
