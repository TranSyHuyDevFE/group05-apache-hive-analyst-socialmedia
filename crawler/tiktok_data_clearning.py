from datetime import timedelta
import pytz  # Add this import for timezone handling


class DataCleaning:
    @staticmethod
    def convert_text_date_to_time_stamp(date_str):
        """
        Convert a single text-based date format to a Unix timestamp.
        :param date_str: A string representing the date.
        :return: Unix timestamp or None if conversion fails.
        """
        from datetime import datetime
        import time

        hcm_tz = pytz.timezone('Asia/Ho_Chi_Minh')  # Define HCM timezone

        try:
            # Attempt to parse the date in various formats
            if "ago" in date_str:
                # Handle relative dates like "1d ago", "1s ago"
                time_units = {'d': 'days', 's': 'seconds',
                              'm': 'minutes', 'h': 'hours'}
                for unit, kwarg in time_units.items():
                    if unit in date_str:
                        value = int(date_str.split(unit)[0])
                        dt = datetime.now() - timedelta(**{kwarg: value})
                        # Localize to HCM timezone
                        dt = hcm_tz.localize(dt)
                        break
                else:
                    raise ValueError("Unsupported relative time format")
            else:
                try:
                    # Handle absolute dates like "2023-10-01 12:00:00"
                    dt = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    # Handle short date format like "7-8" (month-day)
                    dt = datetime.strptime(date_str, '%m-%d')
                    # Assume current year
                    dt = dt.replace(year=datetime.now().year)
                dt = hcm_tz.localize(dt)  # Localize to HCM timezone

            return int(time.mktime(dt.timetuple()))
        except Exception as e:
            print(f"Error processing date '{date_str}'. Error: {e}")
            return None

    @staticmethod
    def convert_text_to_number(text_value):
        """
        Convert text-based numbers with suffixes like 'K', 'M' to actual numbers.
        :param text_value: A string representing the number (e.g., '266.4K').
        :return: A float or int representing the number, or None if conversion fails.
        """
        try:
            if text_value[-1] in ['K', 'M']:
                multiplier = {'K': 1_000, 'M': 1_000_000}
                return float(text_value[:-1]) * multiplier[text_value[-1]]
            return int(text_value)
        except Exception as e:
            print(f"Error processing value '{text_value}'. Error: {e}")
            return None


if __name__ == "__main__":
    # Test cases for convert_text_to_number
    cleaner = DataCleaning()
    test_values = [
        {"input": "266.4K", "expected": 266400},
        {"input": "15.3K", "expected": 15300},
        {"input": "1M", "expected": 1000000},
        {"input": "5640", "expected": 5640},
        {"input": "invalid", "expected": None}
    ]

    print("Testing convert_text_to_number:")
    for test in test_values:
        result = cleaner.convert_text_to_number(test["input"])
        print(
            f"Input: {test['input']}, Expected: {test['expected']}, Result: {result}")
        assert result == test["expected"], f"Test failed for input: {test['input']}"

    print("All tests passed!")
#     for entry in raw_data:
#         entry['timestamp'] = cleaner.convert_text_date_to_time_stamp(
#             entry['date'])

#     # Print the cleaned data
#     print("Cleaned TikTok data:")
#     for entry in raw_data:
#         print(entry)
