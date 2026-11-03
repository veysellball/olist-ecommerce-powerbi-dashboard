"""
Project 3 Monthly KPIs Exporter (Answer Key)
Exports Project 3's monthly KPI definitions as the authoritative ground-truth reference
for validating the Power BI Star Schema model and DAX measures.
"""
import sys
from pathlib import Path

# Set reference path to Project3_Metrics_Dashboard
P3 = Path(__file__).resolve().parents[2] / "Project3_Metrics_Dashboard"
if str(P3) not in sys.path:
    sys.path.insert(0, str(P3))

import pandas as pd

try:
    from src.metrics import MARTS, monthly_kpis  # type: ignore[import-not-found]
except ImportError:
    import importlib.util
    metrics_path = P3 / "src" / "metrics.py"
    spec = importlib.util.spec_from_file_location("metrics", metrics_path)
    metrics_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(metrics_mod)
    MARTS = metrics_mod.MARTS
    monthly_kpis = metrics_mod.monthly_kpis

def main():
    marts_facts = MARTS / "order_facts.parquet"
    if not marts_facts.exists():
        raise FileNotFoundError(f"Missing Project 3 fact table: {marts_facts}")

    print(f"Loading fact table from: {marts_facts}")
    facts = pd.read_parquet(marts_facts)
    
    print("Computing Project 3 monthly KPIs...")
    out = monthly_kpis(facts).reset_index()
    
    output_csv = Path(__file__).with_name("expected_monthly_kpis.csv")
    out.to_csv(output_csv, index=False)
    print(f"Successfully exported answer key to: {output_csv}")
    print("\nSample preview (Last 3 months):")
    print(out[["purchase_month", "orders", "good_orders", "gmv"]].tail(3))

if __name__ == "__main__":
    main()
