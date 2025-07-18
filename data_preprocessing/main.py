from data_reader import DataReader
from video_details_process import VideoDetailsProcessor

# Read from ./mock/details_video_info.csv
# proecesss
# Save to ./mock/details_video_info_processed.csv


def main():
    """
    Main function for the data preprocessing script.
    """
    print("Starting data preprocessing...")

    # Define file paths
    input_path = "./mock/details_video_info.csv"
    output_path = "./mock/details_video_info_processed.csv"

    # Read input data
    io_handler = DataReader()
    data = io_handler.read_csv(input_path)
    if data is None:
        print("Failed to read input data. Exiting...")
        return

    print("Input data preview:")
    print(data.head())

    # Process data
    processor = VideoDetailsProcessor()
    processed_data = processor.process(data)
    if processed_data is None:
        print("Data processing failed. Exiting...")
        return

    print("Processed data preview:")
    print(processed_data.head())

    # Save processed data
    io_handler.save_csv(processed_data, output_path)
    print("Data preprocessing completed successfully.")


if __name__ == "__main__":
    main()
