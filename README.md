# Análisis descriptivo: [JustJoinIT job offers data (2021.10 - 2023-09)](https://www.kaggle.com/datasets/jszafranqb/justjoinit-job-offers-data-2021-10-2023-09)

Análisis descriptivo de los datos [JustJoinIT job offers data (2021.10 - 2023-09)](https://www.kaggle.com/datasets/jszafranqb/justjoinit-job-offers-data-2021-10-2023-09) basado en requerimientos dados.

Repositorio de Notebooks: https://github.com/hdt94/kaggle-justjoinit-notebooks

Notebooks:
- [notebooks/tasks.ipynb](https://github.com/hdt94/kaggle-justjoinit-notebooks/blob/master/notebooks/tasks.ipynb): descripción, explicación, y muestra de la solución a los requerimientos (tareas).
- [notebooks/performance.ipynb](https://github.com/hdt94/kaggle-justjoinit-notebooks/blob/master/notebooks/performance.ipynb): evaluación de desempeño de los algoritmos y funciones desarrollados.


## Datos

El directorio de datos puede ser cualquier ruta del sistema.

## Configuración
- Se utilizó Python3.8

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
