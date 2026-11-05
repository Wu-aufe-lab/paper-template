# <Paper short title>: code and data

<!-- Replace the badge once Zenodo mints a DOI for the first release.
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
-->

Code and data for:

> Author A, Author B, Author C (2026). **Paper title**. *Journal*. https://doi.org/10.xxxx/xxxxx

This repository is the version of record for the analysis in the paper. Cite the
archived release (see *Data availability* below), not the `main` branch.

## What is here

| Path | Contents |
|---|---|
| `src/` | analysis code, one entry point per stage |
| `data/` | small demo data + a manifest describing the full data set |
| `scripts/` | helpers: data download, figure export |
| `docs/` | published figures, notes |
| `outputs/` | produced at run time, not committed |

## Quick start

Runs on the built-in demo data, no download needed:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate      Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt

python src/train.py --seed 0
```

Expected output: `outputs/metrics.json` and `outputs/predictions.csv`.

## Reproduce the paper

```bash
# 1. fetch the full data set (verifies sha256 against data/MANIFEST.json)
python scripts/download_data.py

# 2. run the pipeline
python src/train.py --data data/raw/<your_file> --seed 0 --out outputs/paper

# 3. figures
python scripts/make_figures.py --run outputs/paper --out docs/figures
```

Every stage takes `--seed`; the paper reports `seed = 0` unless stated otherwise
in the Methods.

## Data availability

| Layer | Where | Committed? |
|---|---|---|
| demo subset (a few hundred rows) | `data/demo/` | yes |
| full data set | Zenodo / institutional repository, see `data/MANIFEST.json` | no |
| frozen code | git tag `v1.0.0`, archived at the DOI above | — |

`data/MANIFEST.json` records the URL, size and sha256 of every external file, so a
reader can verify that the download matches what the paper used.

Third-party data keep their original licences; they are **not** relicensed by
this repository.

## Environment

Python 3.12, exact pins in `requirements.txt`. The demo path only needs
numpy / pandas / scikit-learn.

## License

Code: Apache-2.0, see `LICENSE`.
Text and figures: CC BY 4.0 unless stated otherwise.
Data: see `data/README.md`.
