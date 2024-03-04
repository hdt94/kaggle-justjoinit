from pathlib import Path

import pandas as pd


READING_CONFIG = {
    "employments_types": {
        "names": ["type", "id", "currency_salary", "salary_from", "salary_to"]
    },
    "jobs": {},
    "multilocations": {"names": ["city", "street", "id"]},
    "skills": {"names": ["name", "level", "id"]},
}


def read_data_dir(data_dir: str, prefix: str):
    assert isinstance(data_dir, str), f"invalid data_dir type: {type(data_dir)}"
    assert isinstance(prefix, str), f"invalid prefix type: {type(prefix)}"

    ddir = Path(data_dir)
    assert ddir.exists(), f'data_dir not found: "{data_dir}"'

    data = {}
    for dataset in READING_CONFIG.keys():
        file_path = ddir / f"{prefix}-{dataset}.csv"
        try:
            data[dataset] = pd.read_csv(file_path, sep=";", **READING_CONFIG[dataset])
        except FileNotFoundError as ex:
            raise FileNotFoundError(f"Archivo no encontrado: {ex}")

    return data
