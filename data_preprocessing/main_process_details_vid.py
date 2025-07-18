from data_reader import DataReader
from video_details_process import VideoDetailsProcessor

# Read from ./mock/details_video_info.csv
# proecesss
# Save to ./mock/details_video_info_processed.csv


class FilePaths:
    """
    Class to encapsulate input and output file paths.
    """

    def __init__(self, input_path: str, output_path: str):
        self.input_path = input_path
        self.output_path = output_path


class MainProcessDetailsVid:
    """
    Class to encapsulate the main processing logic for video details.
    """

    def __init__(self, paths: FilePaths):
        self.paths = paths
        self.io_handler = DataReader()
        self.processor = VideoDetailsProcessor()

    def run(self):
        """
        Execute the main processing logic.
        """
        print("Starting data preprocessing...")

        # Read input data
        data = self.io_handler.read_csv(self.paths.input_path)
        if data is None:
            print("Failed to read input data. Exiting...")
            return

        print("Input data preview:")
        print(data.head())

        # Process data
        processed_data = self.processor.process(data)
        if processed_data is None:
            print("Data processing failed. Exiting...")
            return

        print("Processed data preview:")
        print(processed_data.head())

        # Save processed data
        self.io_handler.save_csv(processed_data, self.paths.output_path)
        print("Data preprocessing completed successfully.")


def main():
    """
    Main function for the data preprocessing script.
    """
    paths = FilePaths(
        input_path="./mock/details_video_info.csv",
        output_path="./mock/details_video_info_processed.csv",
    )
    main_process = MainProcessDetailsVid(paths)
    main_process.run()


if __name__ == "__main__":
    main()
