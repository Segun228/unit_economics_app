from os import name
from typing import Dict, List
import pandas as pd
import numpy as np
import seaborn as sns
import zipfile
import io
import matplotlib as mplb
mplb.use('Agg')
import matplotlib.pyplot as plt
import logging
from pprint import pprint
from django.http.response import HttpResponseBadRequest, HttpResponse
from rest_framework.response import Response

pd.set_option('future.no_silent_downcasting', True)
'''
given fields
data = {
    "user": None,
    "model_set": None,
    "name": "Example Unit",
    "users": 0,
    "customers": 0,
    "AVP": 0,
    "APC": 0,
    "TMS": 0,
    "COGS": 0,
    "COGS1s": 0,
    "FC": 0
}
'''

def unit_calculate_economics(data):
    """
    обработка данных юнита для создания отчета
    """
    try:
        df = pd.DataFrame([data])
        df["Unit"] = "User"
        df["C1"] = df["customers"] / df["users"]
        df["ARPC"] = df["AVP"] * df["APC"]
        df["ARPU"] = df["ARPC"] * df["C1"]
        df["CPA"] = df["TMS"] / df["users"]
        df["CAC"] = df["TMS"] / df["customers"]
        df["CLTV"] = (df["AVP"] - df["COGS"]) * df["APC"] - df["COGS1s"]
        df["LTV"] = df["CLTV"] * df["C1"]
        df["ROI"] = (df["LTV"] - df["CPA"]) / df["CPA"] * 100
        df["UCM"] = df["LTV"] - df["CPA"]
        df["CCM"] = df["CLTV"] - df["CAC"]


        df["Profitable"] = df["UCM"] > 0

        df["Revenue"] = df["ARPU"] * df["users"]
        df["Gross_profit"] = df["CLTV"] * df["customers"]
        df["Margin"] = df["Gross_profit"] - df["TMS"]

        def calculate_required_bep(row: pd.Series):
            ucm = row.get("UCM", 0)
            if ucm > 0:
                return row.get("FC", 0) / ucm
            return None

        df["Required_units_to_BEP"] = df.apply(calculate_required_bep, axis=1)

        df["BEP"] = df["Required_units_to_BEP"] * df["UCM"]
        df["Profit"] = df["Margin"] - df["FC"]

        float_cols = df.select_dtypes(include='float').columns
        df[float_cols] = df[float_cols].round(4)

        df.replace([np.inf, -np.inf, np.nan], 0, inplace=True)
        df = df.infer_objects(copy=False)
        df = df.where(pd.notnull(df), None)[["name", "users", "customers", "AVP", "APC", "TMS", "COGS",	"COGS1s", "FC",	"C1", "ARPC", "ARPU",	"CPA",	"CAC",	"CLTV",	"LTV",	"ROI",	"UCM",	"CCM",	"Revenue",	"Gross_profit",	"Margin",	"Required_units_to_BEP",	"BEP",	"Profit"]]
        df.columns = ["name", "users", "customers", "AVP", "APC", "TMS", "COGS",	"COGS1s", "FC",	"C1", "ARPC", "ARPU",	"CPA",	"CAC",	"CLTV",	"LTV",	"ROI",	"UCM",	"CCM",	"Revenue",	"Gross_profit",	"Margin",	"Required_units_to_BEP",	"BEP",	"Profit"]

        return df.to_dict(orient="records")
    except Exception as e:
        logging.error(f"Ошибка в unit_calculate_economics: {e}")
        return None



def process_dataframe(df:pd.DataFrame):
    try:
        df["Unit"] = "User"
        df["C1"] = df["customers"] / df["users"]
        df["ARPC"] = df["AVP"] * df["APC"]
        df["ARPU"] = df["ARPC"] * df["C1"]
        df["CPA"] = df["TMS"] / df["users"]
        df["CAC"] = df["TMS"] / df["customers"]
        df["CLTV"] = (df["AVP"] - df["COGS"]) * df["APC"] - df["COGS1s"]
        df["LTV"] = df["CLTV"] * df["C1"]
        df["ROI"] = (df["LTV"] - df["CPA"]) / df["CPA"] * 100
        df["UCM"] = df["LTV"] - df["CPA"]
        df["CCM"] = df["CLTV"] - df["CAC"]


        df["Profitable"] = df["UCM"] > 0

        df["Revenue"] = df["ARPU"] * df["users"]
        df["Gross_profit"] = df["CLTV"] * df["customers"]
        df["Margin"] = df["Gross_profit"] - df["TMS"]


        def calculate_required_bep(row: pd.Series):
            ucm = row.get("UCM", 0)
            if ucm > 0:
                return row.get("FC", 0) / ucm
            return None

        df["Required_units_to_BEP"] = df.apply(calculate_required_bep, axis=1)
        
        df["BEP"] = df["Required_units_to_BEP"] * df["UCM"]
        df["Profit"] = df["Margin"] - df["FC"]

        float_cols = df.select_dtypes(include='float').columns
        df[float_cols] = df[float_cols].round(4)

        df.replace([np.inf, -np.inf], np.nan, inplace=True)
        df = df.infer_objects(copy=False)
        df = df.where(pd.notnull(df), None)

        df = df.where(pd.notnull(df), None)[["name", "users", "customers", "AVP", "APC", "TMS", "COGS",	"COGS1s", "FC",	"C1", "ARPC", "ARPU",	"CPA",	"CAC",	"CLTV",	"LTV",	"ROI",	"UCM",	"CCM",	"Revenue",	"Gross_profit",	"Margin",	"Required_units_to_BEP",	"BEP",	"Profit"]]
        df.columns = ["name", "users", "customers", "AVP", "APC", "TMS", "COGS",	"COGS1s", "FC",	"C1", "ARPC", "ARPU",	"CPA",	"CAC",	"CLTV",	"LTV",	"ROI",	"UCM",	"CCM",	"Revenue",	"Gross_profit",	"Margin",	"Required_units_to_BEP",	"BEP",	"Profit"]

        return df

    except Exception as e:
        logging.error(f"Ошибка в unit_calculate_economics: {e}")
        return None


def set_calculate_economics(data):
    calculated_units = []
    errors = []
    try:
        set_name = data.get("name", "Model Set Name")
        units = data.get("units")
        if units is None or not isinstance(units, list):
            raise ValueError("Empty or invalid 'units' list")

        for i, unit in enumerate(units, start=1):
            try:
                result = unit_calculate_economics(unit)
                if result is not None:
                    calculated_units.extend(result)
                else:
                    errors.append({"index": i, "error": "Calculation returned None"})
            except Exception as e:
                logging.warning(f"Ошибка при расчёте unit[{i}]: {e}")
                errors.append({"index": i, "error": str(e)})
        return Response({
            "name":name,
            "success": True,
            "calculated": calculated_units,
            "errors": errors,
        })
    
    except Exception as e:
        logging.error(f"Ошибка в set_calculate_economics: {e}")
        return None


def set_visualize(data, metrics=None):
    """
    data: dict с ключами "name" и "units" (список словарей с результатами расчета unit_calculate_economics)
    metrics: список метрик для построения сравнительных графиков
    """
    if metrics is None:
        metrics = ["CPA", "CAC", "CLTV", "LTV", "UCM", "CCM", "C1"]

    calculated_units = []
    errors = []
    
    try:
        set_name = data.get("name", "Model Set Name")
        units = data.get("units")
        if not units or not isinstance(units, list):
            raise ValueError("Empty or invalid 'units' list")

        for i, unit in enumerate(units, start=1):
            try:
                result = unit_calculate_economics(unit)[0]
                if result is not None:
                    df_unit = pd.DataFrame([result])  
                    df_unit["Unit"] = unit.get("name", f"Unit_{i}") 
                    calculated_units.append(df_unit)
                else:
                    errors.append({"index": i, "error": "Calculation returned None"})
            except Exception as e:
                logging.warning(f"Ошибка при расчёте unit[{i}]: {e}")
                errors.append({"index": i, "error": str(e)})

        if not calculated_units:
            raise ValueError("No valid units for visualization")

        big_df = pd.concat(calculated_units, ignore_index=True)

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for metric in metrics:
                if metric not in big_df.columns:
                    logging.warning(f"Метрика {metric} отсутствует в данных, пропускаем")
                    continue

                plt.figure(figsize=(8, 6))
                sns.barplot(x="Unit", y=metric, data=big_df, palette="tab10", hue="Unit")
                plt.title(f"{metric} comparison - {set_name}")
                plt.ylabel(metric)
                plt.xlabel("Units")
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.grid(True)
                plt.axhline(0, color='black', linewidth=0.5)
                plt.axvline(0, color='black', linewidth=0.5)
                buf = io.BytesIO()
                plt.savefig(buf, format='png', dpi=300)
                plt.close()
                buf.seek(0)
                zipf.writestr(f"{metric}.png", buf.getvalue())

        zip_buffer.seek(0)
        response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="report_bundle.zip"'
        return (response, zip_buffer.getvalue())
    except Exception as e:
        logging.exception(f"Ошибка в set_visualize: {e}")
        return None, errors

if __name__ == "__main__":
    data = {
        "model_set": 1,
        "name": "Example Unit",
        "users": 1000,
        "customers": 10,
        "AVP": 100,
        "APC": 2,
        "TMS": 1000,
        "COGS": 10,
        "COGS1s": 40,
        "FC": 1000
    }

    set = {
        "name":"dummy data",
        "units":[
        {
            "name": "Unit 1",
            "users": 100,
            "customers": 50,
            "AVP": 2000,
            "APC": 500,
            "TMS": 10000,
            "COGS": 5000,
            "COGS1s": 2000,
            "FC": 3000,
            "RR": 0.05,
            "AGR": 0.10
        },
        {
            "name": "Unit 2",
            "users": 80,
            "customers": 40,
            "AVP": 1800,
            "APC": 450,
            "TMS": 9000,
            "COGS": 4000,
            "COGS1s": 1500,
            "FC": 2500,
            "RR": 0.06,
            "AGR": 0.12
        },
        {
            "name": "Unit 3",
            "users": 150,
            "customers": 70,
            "AVP": 2200,
            "APC": 550,
            "TMS": 12000,
            "COGS": 6000,
            "COGS1s": 2500,
            "FC": 3500,
            "RR": 0.07,
            "AGR": 0.15
        }
    ]}
    pprint(set_visualize(data = set))