from data_reader import DataReader
from utils.file_name import FileNameGenerator
from user_details_process import UserDetailsProcessor
import os

class FilePaths:
    def __init__(self, input_path: str, output_path: str):
        self.input_path = input_path
        self.output_path = output_path

class MainProcessUserDetails:
    def __init__(self, paths: FilePaths):
        self.paths = paths
        self.io_handler = DataReader()
        self.processor = UserDetailsProcessor()

    def run(self):
        print("Starting user details preprocessing...")
        data = self.io_handler.read_csv(self.paths.input_path)
        if data is None:
            print("Failed to read input data. Exiting...")
            return
        print("Input data preview:")
        print(data.head())
        processed_data = self.processor.process(data)
        if processed_data is None:
            print("Data processing failed. Exiting...")
            return
        print("Processed data preview:")
        print(processed_data.head())
        output_dir = "/workspaces/py_env_research/group05-apache-hive-analyst-socialmedia/cleaned_data"
        os.makedirs(output_dir, exist_ok=True)
        output_file = FileNameGenerator.generate("user_info_details") + ".csv"
        output_path = os.path.join(output_dir, output_file)
        self.io_handler.save_csv(processed_data, output_path)
        print(f"User details preprocessing completed successfully. Output saved to: {output_path}")

def main():
    paths = FilePaths(
        input_path="./term/user_info.csv",
        output_path=None,  # Output path will be generated dynamically
    )
    main_process = MainProcessUserDetails(paths)
    main_process.run()

if __name__ == "__main__":
    main()
