"""Export the site's chart data from the source spreadsheets into JSON.

Run locally from the repo root:  python scripts/export_data.py
Requires pandas and openpyxl. Nothing here runs on the live site; the
site only reads the JSON files this script writes to docs/data/.
"""
import json
from pathlib import Path

import openpyxl
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "Data"
OUT = ROOT / "docs" / "data"


def write(name, payload):
    path = OUT / name
    path.write_text(json.dumps(payload, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {path.relative_to(ROOT)}")


def monthly_hauls():
    """Monthly construction diversion from the Turner/GreenHalo haul records.

    Includes general materials (GM) and earthwork (EW). Row 8 of the sheet
    holds the headers; the first data row is a project-total row with a date
    range instead of a date, so only rows with a real haul date are used.
    """
    hauls = pd.read_excel(DATA / "ZWR_C1_update.xlsx", sheet_name="Worksheet", header=7)
    tons = [f"{group} {kind} Tons" for group in ("GM", "EW") for kind in ("Reused", "Recycled", "Disposed", "Total")]
    for column in tons:
        hauls[column] = pd.to_numeric(hauls[column], errors="coerce").fillna(0)
    hauls["date"] = pd.to_datetime(hauls["Haul Date"], format="%m/%d/%Y", errors="coerce")
    hauls = hauls.dropna(subset=["date"])

    hauls["diverted"] = hauls[["GM Reused Tons", "GM Recycled Tons", "EW Reused Tons", "EW Recycled Tons"]].sum(axis=1)
    hauls["landfilled"] = hauls[["GM Disposed Tons", "EW Disposed Tons"]].sum(axis=1)
    hauls["total"] = hauls[["GM Total Tons", "EW Total Tons"]].sum(axis=1)
    hauls["month"] = hauls["date"].dt.to_period("M")

    monthly = hauls.groupby("month")[["diverted", "landfilled", "total"]].sum()
    months = pd.period_range(monthly.index.min(), monthly.index.max(), freq="M")
    monthly = monthly.reindex(months, fill_value=0)

    rows = []
    for month, row in monthly.iterrows():
        rate = round(row["diverted"] / row["total"] * 100, 2) if row["total"] else None
        rows.append({
            "month": month.strftime("%Y-%m"),
            "rate": rate,
            "diverted_tons": round(row["diverted"], 1),
            "landfilled_tons": round(row["landfilled"], 1),
            "total_tons": round(row["total"], 1),
        })
    return {"haul_records": int(len(hauls)), "months": rows}


def materials():
    """All construction material streams by weight (earthwork excluded)."""
    sheet = pd.read_excel(DATA / "Gateway_Graphs.xlsx", sheet_name="C&D Diversion Data")
    sheet = sheet.dropna(subset=["Material", "Tons"])
    return [{"material": str(m).strip(), "tons": round(float(t), 2)} for m, t in zip(sheet["Material"], sheet["Tons"])]


def hauling_costs():
    """Project-total hauling cost with and without TRUE source separation."""
    workbook = openpyxl.load_workbook(DATA / "Cost_Benefit_Analysis.xlsx", data_only=True, read_only=True)
    sheet = workbook["Entire Project Overiew"]
    costs = {"with_true": sheet["D4"].value, "without_true": sheet["D5"].value}
    workbook.close()
    return {key: round(value, 2) for key, value in costs.items()}


def embodied_carbon():
    sheet = pd.read_csv(DATA / "embodied_carbon_reductions.csv")
    return sheet.to_dict(orient="records")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    write("construction.json", {
        "monthly": monthly_hauls(),
        "materials": materials(),
        "hauling_costs": hauling_costs(),
        "embodied_carbon": embodied_carbon(),
    })
