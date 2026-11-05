"""Reproducible training entry point.

Four habits this file demonstrates - keep them when you swap in your own model:

1. every path is a CLI flag, nothing is hard-coded;
2. every random source is seeded (--seed);
3. results land as machine-readable files under --out;
4. with no --data, a synthetic demo set is generated, so `python src/train.py`
   always runs on a fresh clone (that is what makes the CI smoke test meaningful).
"""

from __future__ import annotations

import argparse
import json
import os
import random
import sys
from pathlib import Path


def set_seed(seed: int) -> None:
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    try:
        import numpy as np
    except ImportError:
        return
    np.random.seed(seed)


def load_frame(path: str | None):
    import numpy as np
    import pandas as pd

    if path:
        p = Path(path)
        if not p.exists():
            sys.exit(f"input not found: {p}")
        return pd.read_csv(p) if p.suffix.lower() == ".csv" else pd.read_pickle(p)

    rng = np.random.default_rng(0)
    n = 600
    centres = {"M0": (-1.0, 0.0, 0.0), "M1": (1.0, 0.0, 0.0), "M2": (0.0, 1.0, 1.0)}
    labels = rng.choice(list(centres), size=n)
    noise = rng.normal(scale=0.6, size=(n, 3))
    features = np.array([centres[label] for label in labels]) + noise
    return pd.DataFrame(
        {
            "sample": [f"S{i:03d}" for i in range(n)],
            "label": labels,
            "feature_1": features[:, 0],
            "feature_2": features[:, 1],
            "feature_3": features[:, 2],
        }
    )


def main() -> None:
    ap = argparse.ArgumentParser(description="train a model and write metrics")
    ap.add_argument("--data", help="CSV or pickle; omit to use synthetic demo data")
    ap.add_argument("--out", default="outputs", help="output directory")
    ap.add_argument("--label", default="label", help="name of the label column")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--test-size", type=float, default=0.2)
    args = ap.parse_args()

    set_seed(args.seed)

    import pandas as pd
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import accuracy_score, classification_report
    from sklearn.model_selection import train_test_split

    frame = load_frame(args.data)
    if args.label not in frame.columns:
        sys.exit(f"label column {args.label!r} not in {list(frame.columns)}")

    features = [c for c in frame.columns if c.startswith("feature")]
    if not features:
        sys.exit("no feature columns found (columns must be named feature_*)")

    x = frame[features].to_numpy(dtype=float)
    y = frame[args.label].astype(str).to_numpy()

    x_tr, x_te, y_tr, y_te = train_test_split(
        x, y, test_size=args.test_size, random_state=args.seed, stratify=y
    )

    model = RandomForestClassifier(n_estimators=200, random_state=args.seed)
    model.fit(x_tr, y_tr)
    pred = model.predict(x_te)

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    metrics = {
        "seed": args.seed,
        "n_rows": int(len(frame)),
        "n_features": len(features),
        "n_train": int(len(x_tr)),
        "n_test": int(len(x_te)),
        "accuracy": float(accuracy_score(y_te, pred)),
        "report": classification_report(y_te, pred, output_dict=True, zero_division=0),
    }
    (out / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    pd.DataFrame({"y_true": y_te, "y_pred": pred}).to_csv(out / "predictions.csv", index=False)

    print(f"rows={metrics['n_rows']} features={metrics['n_features']} seed={args.seed}")
    print(f"accuracy={metrics['accuracy']:.4f}")
    print(f"wrote {out / 'metrics.json'} and {out / 'predictions.csv'}")


if __name__ == "__main__":
    main()
