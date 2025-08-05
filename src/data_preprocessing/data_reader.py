import pandas as pd


class DataReader:
    @staticmethod
    def read_csv(input_path):
        try:
            data = pd.read_csv(input_path)
            return data
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")
            return None

    @staticmethod
    def save_csv(data, output_path):
        try:
            data.to_csv(output_path, index=False)
            print(f"Data successfully saved to {output_path}.")
        except Exception as e:
            print(f"An error occurred while saving the file: {e}")
