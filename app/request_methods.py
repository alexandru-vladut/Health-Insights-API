"""
This module contains the methods that are called by the API endpoints.
"""

import pandas

from app import webserver

def states_mean(question):
    # Filter the DataFrame based on the question
    df_filtered = webserver.data_ingestor.dataframe[
        webserver.data_ingestor.dataframe['Question'] == question
    ]

    # Calculate the average of "Data_Value" for each state
    result_df = df_filtered.groupby('LocationDesc')['Data_Value'].mean().sort_values()

    # Convert DataFrame to dictionary
    result = result_df.to_dict()

    # Return result dictionary
    return result


def state_mean(question, state):
    # Filter the DataFrame based on the question and state
    df_filtered = webserver.data_ingestor.dataframe[
        (webserver.data_ingestor.dataframe['Question'] == question) &
        (webserver.data_ingestor.dataframe['LocationDesc'] == state)
    ]

    # Calculate the average value
    average_value = df_filtered["Data_Value"].mean()

    # Create result dictionary
    result = {state: average_value}

    # Return result dictionary
    return result


def best5(question):
    # Filter the DataFrame based on the question
    df_filtered = webserver.data_ingestor.dataframe[
        webserver.data_ingestor.dataframe['Question'] == question
    ]

    if question in webserver.data_ingestor.questions_best_is_min:
        # Sort the DataFrame in ascending order
        result_df = (df_filtered.groupby('LocationDesc')['Data_Value']
                       .mean().sort_values(ascending=True))
    else:
        # Sort the DataFrame in descending order
        result_df = (df_filtered.groupby('LocationDesc')['Data_Value']
                       .mean().sort_values(ascending=False))

    # Get the top 5 states and convert DataFrame to dictionary
    result = result_df.head(5).to_dict()

    # Return result dictionary
    return result


def worst5(question):
    # Filter the DataFrame based on the question
    df_filtered = webserver.data_ingestor.dataframe[
        webserver.data_ingestor.dataframe['Question'] == question
    ]

    if question in webserver.data_ingestor.questions_best_is_min:
        # Sort the DataFrame in ascending order
        result_df = (df_filtered.groupby('LocationDesc')['Data_Value']
                       .mean().sort_values(ascending=False))
    else:
        # Sort the DataFrame in descending order
        result_df = (df_filtered.groupby('LocationDesc')['Data_Value']
                       .mean().sort_values(ascending=True))

    # Get the top 5 states and convert DataFrame to dictionary
    result = result_df.head(5).to_dict()

    # Return result dictionary
    return result


def global_mean(question):
    # Filter the DataFrame based on the question
    df_filtered = webserver.data_ingestor.dataframe[
        (webserver.data_ingestor.dataframe['Question'] == question)]

    # Calculate the average value
    average_value = df_filtered["Data_Value"].mean()

    # Create result dictionary
    result = {"global_mean": average_value}

    # Return result dictionary
    return result


def diff_from_mean(question):
    # Get the list of states
    states = webserver.data_ingestor.dataframe['LocationDesc'].unique().tolist()

    # Get the global mean value
    global_mean_value = global_mean(question)["global_mean"]

    # Create result dictionary
    result = {}

    # Iterate over the states
    for state in states:
        # Get the state mean value
        state_mean_value = state_mean(question, state)[state]

        # If the state mean value is not NaN, calculate the difference and add to dictionary
        if not pandas.isna(state_mean_value):
            result[state] = global_mean_value - state_mean_value

    # Return result dictionary
    return result


def state_diff_from_mean(question, state):
    # Get the global mean value
    global_mean_value = global_mean(question)["global_mean"]

    # Get the state mean value
    state_mean_value = state_mean(question, state)[state]

    # Create result dictionary
    result = {}

    # Calculate the difference and add to dictionary
    result[state] = global_mean_value - state_mean_value

    # Return result dictionary
    return result


def mean_by_category(question):
    # Filter the DataFrame based on the question
    df_filtered = webserver.data_ingestor.dataframe[
        (webserver.data_ingestor.dataframe['Question'] == question)
    ]

    # Group by state, category, and interval, then calculate the mean
    categories = ['LocationDesc', 'StratificationCategory1', 'Stratification1']
    result_df = df_filtered.groupby(categories)['Data_Value'].mean()

    # Convert group keys to string format and create the result dictionary
    result = {f"('{state}', '{category}', '{interval}')": value
              for (state, category, interval), value in result_df.items()}

    # Return result dictionary
    return result


def state_mean_by_category(question, state):
    # Filter the DataFrame based on the question and state
    df_filtered = webserver.data_ingestor.dataframe[
        (webserver.data_ingestor.dataframe['Question'] == question) &
        (webserver.data_ingestor.dataframe['LocationDesc'] == state)
    ]

    # Group by category and its interval, then calculate the mean
    categories = ['StratificationCategory1', 'Stratification1']
    result_df = df_filtered.groupby(categories)['Data_Value'].mean()

    # Convert group keys to string format and create the result dictionary
    result = {state: {f"('{category}', '{interval}')": value
                      for (category, interval), value in result_df.items()}}

    # Return result dictionary
    return result
