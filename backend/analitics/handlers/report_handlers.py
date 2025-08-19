from typing import Dict, List
import pandas as pd
import logging
from pprint import pprint
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
        return df

    except Exception as e:
        logging.error(f"Ошибка в unit_calculate_economics: {e}")
        return None




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
    pprint(unit_calculate_economics(data))