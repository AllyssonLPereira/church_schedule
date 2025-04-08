import pandas as pd
import sys, os


class ChurchSchedule:

    def __init__(self, df):
        self.dataset = df

    @classmethod
    def get_dataset(cls, file_path_origin):
        return pd.read_csv(file_path_origin)

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

        self.dataset.replace({"ç": "c", "ã": "a", "õ": "o"}, regex=True, inplace=True)

    def save_to_csv(self, path_destination):
        """Save the formatted dataset to a CSV file."""

        self.dataset.to_csv(path_destination, index=False)


if __name__ == "__main__":

    file_path_origin = os.path.abspath(sys.argv[1])
    path_destination = os.path.abspath(sys.argv[2])

    # Loading the dataset
    df = ChurchSchedule.get_dataset(file_path_origin)

    # Instantiating the class
    schedule = ChurchSchedule(df)

    # Processing data
    schedule.missing_values()
    schedule.normalize_data()

    # Saving the corrected file
    schedule.save_to_csv(path_destination)
