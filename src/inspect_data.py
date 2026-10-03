"""Inspeciona o CSV bruto sem alterar os dados ou treinar modelos."""

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


def inspect_csv(path, required):
    """Conta linhas, vazios e duplicatas exatas após validar colunas obrigatórias."""
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"CSV ausente: {path.name}. Consulte data/README.md.")

    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        columns = reader.fieldnames or []
        missing = sorted(set(required) - set(columns))
        if missing:
            raise ValueError(f"Colunas obrigatórias ausentes: {missing}")
        rows = list(reader)

    if not rows:
        raise ValueError("CSV sem registros.")

    nulls = {col: sum(not (r.get(col) or "").strip() for r in rows) for col in columns}
    keys = [tuple(r.get(col) for col in columns) for r in rows]
    return {
        "file": path.name,
        "rows": len(rows),
        "columns": columns,
        "empty_cells": nulls,
        "exact_duplicate_excess": sum(n - 1 for n in Counter(keys).values()),
        "scope": "Contagem, células vazias e duplicatas exatas; não valida domínio ou tempo.",
    }

## RA: 10356420 - KAYO OLIVEIRA NUKUI ##

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("--required", nargs="+", required=True)
    args = parser.parse_args()
    print(json.dumps(inspect_csv(args.file, args.required), ensure_ascii=False, indent=2))
