
from datetime import datetime
import pytz

class FileNameGenerator:
    @staticmethod
    def generate(category: str, date: datetime = None) -> str:
        hcm_tz = pytz.timezone('Asia/Ho_Chi_Minh')
        if date is None:
            date = datetime.now(hcm_tz)
        elif date.tzinfo is None:
            date = hcm_tz.localize(date)
        else:
            date = date.astimezone(hcm_tz)
        date_str = date.strftime("%d_%m_%Y")
        return f"{category}_{date_str}"