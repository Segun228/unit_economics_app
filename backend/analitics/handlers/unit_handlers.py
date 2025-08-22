from math import inf
from typing import Dict, List
from h11 import Response
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib as mplb
mplb.use('Agg')
import logging
from pprint import pprint
from django.http.response import HttpResponseBadRequest
from analitics.handlers.report_handlers import process_dataframe
import matplotlib.pyplot as plt
import io
from django.http import HttpResponse
from io import BytesIO
from openpyxl.utils import get_column_letter
from openpyxl.styles import Alignment, Font

def unit_count_bep(data):
    try:
        df = pd.DataFrame([data])
        proc = process_dataframe(df)
        if proc is None:
            raise ValueError("Error while calculating BEP")

        proc = proc.to_dict(orient="records")[0]


        k_val = proc.get("UCM")
        a_val = proc.get("FC")
        bep_val = proc.get("Required_units_to_BEP")
        

        if k_val is None or a_val is None or bep_val is None:
            raise ValueError(f"Missing required data: UCM={k_val}, FC={a_val}, Required_units_to_BEP={bep_val}")


        k = float(k_val)
        a = float(a_val)
        bep_units = int(bep_val) + 1

        x = list(range(0, 2 * bep_units))
        y1 = [-a for _ in x]
        y2 = [-a + k * xi for xi in x]

        fig, ax = plt.subplots()
        ax.plot(x, y1, label="Постоянные издержки", linewidth=2)
        ax.plot(x, y2, label="Юниты масштабирования", linewidth=2)

        ax.set_xlim(0, max(x))
        min_y = min(min(y1), min(y2))
        max_y = max(max(y1), max(y2))
        ax.set_ylim(min_y - abs(min_y)*0.2, max_y + abs(max_y)*0.2)

        ax.set_xlabel("Units")
        ax.set_ylabel("Cash flow")
        ax.set_title("Расчет точки безубыточности")
        ax.axhline(0, color='black', linewidth=0.5)
        ax.axvline(0, color='black', linewidth=0.5)
        ax.grid(False)


        ax.scatter(bep_units, 0, color='red', zorder=5, label=f"BEP = {bep_units}")
        ax.annotate(f'BEP = {bep_units}', xy=(bep_units, 0), xytext=(bep_units+1, a/4),
                    arrowprops=dict(facecolor='black', arrowstyle='->'))

        ax.legend()
        fig.subplots_adjust(left=0.15)


        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=300, bbox_inches='tight')
        buf.seek(0)
        plt.close(fig)

        return proc, buf

    except Exception as e:
        logging.error(f"Error in unit_count_bep: {e}")
        raise

def unit_generate_report(data):
    try:
        df = pd.DataFrame([data])
        result = process_dataframe(df)
        if result is None:
            raise ValueError("Error while calculating economics")
        else:
            result_dict = result.to_dict(orient="records")[0]
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                result.to_excel(
                    writer,
                    index=False,
                    sheet_name="Текущие посты"
                )
                worksheet = writer.sheets["Текущие посты"]
                header_font = Font(bold=True)
                for col_num, column_title in enumerate(result.columns, 1):
                    cell = worksheet.cell(row=1, column=col_num)
                    cell.font = header_font
                    cell.alignment = Alignment(horizontal='center', vertical='center')
                for column_cells in worksheet.columns:
                    length = max(len(str(cell.value)) if cell.value else 0 for cell in column_cells)
                    col_letter = get_column_letter(column_cells[0].column)
                    worksheet.column_dimensions[col_letter].width = length + 4
            buffer.seek(0)
            response = HttpResponse(
                buffer.getvalue(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = f'attachment; filename={result_dict.get("name", "Model")}.xlsx'
            return response

    except Exception as e:
        logging.exception(e)
        raise


if __name__ == "__main__":
    dummy_data = {
        "name": "Тестовая модель",
        "users": 1000,
        "customers": 100,
        "AVP": 300,
        "APC": 2,
        "TMS": 20000,
        "COGS": 100,
        "COGS1s": 20,
        "FC": 10000
    }
    print(unit_count_bep(dummy_data))