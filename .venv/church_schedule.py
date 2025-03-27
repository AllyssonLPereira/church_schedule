from dotenv import load_dotenv
import pandas as pd
import stat
import os


class ChurchSchedule:

    def __init__(self, df):
        self.dataset = df

    @classmethod
    def get_dataset(cls, file_path):
        return pd.read_csv(file_path)

    @property
    def dataset(self):
        return self._dataset

    @dataset.setter
    def dataset(self, df):
        if not isinstance(df, pd.DataFrame):
            raise ValueError("The dataset must be a pandas DataFrame.")
        self._dataset = df

    def missing_values(self):
        """Fill missing values ​​with null"""

        self.dataset.fillna("null", inplace=True)

    def normalize_data(self):
        """Replaces special characters."""

        self.dataset.replace({"ç": "c", "ã": "a"}, regex=True, inplace=True)

    def save_to_csv(self, output_path):
        """Save the formatted dataset to a CSV file."""

        self.dataset.to_csv(output_path, index=False)


def is_valid_path(path):
    # Checks if path is absolute
    if not os.path.isabs(path):
        return False

    # Sanitizes the path by removing parent directory sequences
    if ".." in path:
        return False
    return True


if __name__ == "__main__":

    # Loading environment variables from the .env file
    load_dotenv()

    file_path = os.getenv("SOURCE_FILE_PATH")
    output_path = os.getenv("OUTPUT_PATH")

    # Check if environment variables are set
    if not file_path or not output_path:
        print("The SOURCE_FILE_PATH and OUTPUT_PATH environment variables must be set.")
        exit(1)

    # Checks the validity of paths
    if not is_valid_path(file_path) or not is_valid_path(output_path):
        print("The paths provided are invalid.")
        exit(1)

    try:
        if os.path.exists(file_path):

            # os.chmod(file_path, stat.S_IWUSR)
            print("File permissions modified successfully!")
        else:
            print("File not found:", file_path)
            
    except PermissionError:
        print(
            "Permission denied: You don't have the necessary permissions to change the permissions of this file."
        )
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


    # Loading the dataset
    df = ChurchSchedule.get_dataset(file_path)

    # Instantiating the class
    schedule = ChurchSchedule(df)

    # Processing data
    schedule.missing_values()
    schedule.normalize_data()

    # Saving the corrected file
    schedule.save_to_csv(output_path)
