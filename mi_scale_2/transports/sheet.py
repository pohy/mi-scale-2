from datetime import datetime

import gspread
from gspread.worksheet import Worksheet

from mi_scale_2.config import SPREADSHEET_URL
from mi_scale_2.transports.weight_transport import WeightTransport

# # Now in format 2024-07-05 12:00:00
# date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# weight = 70 + random() * 2

# worksheet.append_row([date, weight])

class SheetTransport(WeightTransport):
    worksheet: Worksheet

    def __init__(self):
        # Loaded from ~/.config/gspread/service_account.json
        gc = gspread.service_account()
        spreadsheet = gc.open_by_url(SPREADSHEET_URL)

        self.worksheet = spreadsheet.worksheet('data')

    def on_measurement(self, weight_kg: float, unit: str, date: datetime):
        date_string = date.strftime('%Y-%m-%d %H:%M:%S')
        self.worksheet.append_row([date_string, weight_kg, unit])
