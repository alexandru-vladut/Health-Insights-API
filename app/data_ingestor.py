"""
This module is responsible for reading the data from the CSV file and storing it in a DataFrame.
"""

import pandas

class DataIngestor:
    """
    Class for reading data from a CSV file and storing it in a DataFrame.

    Attributes:
        dataframe: A pandas DataFrame containing the data from the CSV file.
        questions_best_is_min: A list of questions where lower values are considered better.
        questions_best_is_max: A list of questions where higher values are considered better.

    Methods:
        get_columns_to_read: Define the columns to read from the CSV file.
        get_data: Read data from a CSV file and return a DataFrame containing the data.
    """

    def __init__(self, csv_path: str):
        # Read csv from csv_path
        self.dataframe = self.get_data(csv_path)

        self.questions_best_is_min = [
            'Percent of adults aged 18 years and older who have an overweight classification',
            'Percent of adults aged 18 years and older who have obesity',
            'Percent of adults who engage in no leisure-time physical activity',
            'Percent of adults who report consuming fruit less than one time daily',
            'Percent of adults who report consuming vegetables less than one time daily'
        ]

        self.questions_best_is_max = [
            ('Percent of adults who achieve at least 150 minutes a week of moderate-intensity '
             'aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic '
             'activity (or an equivalent combination)'),
            ('Percent of adults who achieve at least 150 minutes a week of moderate-intensity '
             'aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic '
             'physical activity and engage in muscle-strengthening activities on 2 or more '
             'days a week'),
            ('Percent of adults who achieve at least 300 minutes a week of moderate-intensity '
             'aerobic physical activity or 150 minutes a week of vigorous-intensity aerobic '
             'activity (or an equivalent combination)'),
            ('Percent of adults who engage in muscle-strengthening activities on 2 or more days '
             'a week'),
        ]

    def get_columns_to_read(self):
        """
        Defining the columns to read from the CSV file
        (read only necessary columns to save memory)
        """

        return ['LocationDesc', 'Question', 'Data_Value',
                'StratificationCategory1', 'Stratification1']

    def get_data(self, csv_path: str):
        """
        Read data from a CSV file and return a DataFrame containing the data.
        """

        columns_to_read = self.get_columns_to_read()

        # Return DataFrame containing the CSV file data
        return pandas.read_csv(csv_path, usecols=columns_to_read)
