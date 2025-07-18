import zipfile
import os
import logging
from pathlib import Path
from typing import Union, List

class CrawledDataCompressor:
    def __init__(
        self,
        parent_directory: Union[str, Path] = "./raw_data/tiktok",
        output_directory: Union[str, Path] = "./raw_data/tiktok_zipped",
        exclude_patterns: List[str] = None
    ):
        self.parent_directory = Path(parent_directory)
        self.output_directory = Path(output_directory)
        self.exclude_patterns = exclude_patterns or ['*.log', 'temp/*']

    def compress_crawled_data(self, source_path: Union[str, Path], output_zip_path: Union[str, Path]) -> bool:
        """
        Compress crawled data to zip format.
        
        Args:
            source_path: Path to the directory or file to compress
            output_zip_path: Path for the output zip file
            exclude_patterns: List of file patterns to exclude (e.g., ['*.log', 'temp/*'])
        
        Returns:
            bool: True if compression successful, False otherwise
        """
        try:
            source_path = Path(source_path)
            output_zip_path = Path(output_zip_path)
            # Create output directory if it doesn't exist
            output_zip_path.parent.mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                if source_path.is_file():
                    # Compress single file
                    zipf.write(source_path, source_path.name)
                    logging.info(f"Compressed file: {source_path}")
                elif source_path.is_dir():
                    # Compress directory recursively
                    for file_path in source_path.rglob('*'):
                        if file_path.is_file():
                            # Check if file should be excluded
                            relative_path = file_path.relative_to(source_path)
                            if not any(file_path.match(pattern) for pattern in self.exclude_patterns):
                                zipf.write(file_path, relative_path)
                    logging.info(f"Compressed directory: {source_path}")
                else:
                    logging.error(f"Source path does not exist: {source_path}")
                    return False
            logging.info(f"Compression completed: {output_zip_path}")
            return True
        except Exception as e:
            logging.error(f"Error compressing data: {str(e)}")
            return False

    def compress_all_folders(self) -> List[str]:
        """
        Loop through all folders in parent directory and compress each one.
        
        Args:
            parent_directory: Path to the parent directory containing folders to compress
            output_directory: Directory to save zip files (defaults to parent_directory)
            exclude_patterns: List of file patterns to exclude from compression
        
        Returns:
            List[str]: List of successfully created zip file paths
        """
        try:
            parent_path = self.parent_directory
            output_path = self.output_directory
            exclude_patterns = self.exclude_patterns

            if not parent_path.exists() or not parent_path.is_dir():
                logging.error(f"Parent directory does not exist: {parent_path}")
                return []

            output_path.mkdir(parents=True, exist_ok=True)
            successful_compressions = []

            # Loop through all items in parent directory
            for item in parent_path.iterdir():
                if item.is_dir():
                    # Create zip file with same name as folder
                    zip_filename = f"{item.name}.zip"
                    zip_path = output_path / zip_filename

                    # Skip compression if zip file already exists
                    if zip_path.exists():
                        logging.info(f"Zip file already exists, skipping: {zip_filename}")
                        continue

                    logging.info(f"Compressing folder: {item.name}")
                    # Compress the folder
                    if self.compress_crawled_data(item, zip_path):
                        successful_compressions.append(str(zip_path))
                        logging.info(f"Successfully compressed: {item.name} -> {zip_filename}")
                    else:
                        logging.error(f"Failed to compress: {item.name}")
                else:
                    logging.debug(f"Skipping file: {item.name}")

            logging.info(f"Compression batch completed. {len(successful_compressions)} folders compressed.")
            return successful_compressions
        except Exception as e:
            logging.error(f"Error in batch compression: {str(e)}")
            return []

if __name__ == "__main__":
    compressor = CrawledDataCompressor()
    compressed_files = compressor.compress_all_folders()
    print("Compressed zip files:", compressed_files)