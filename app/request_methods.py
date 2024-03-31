from app import webserver
from flask import request, jsonify

import os
import json
import re
import pandas

def states_mean(question):
    # Filter the DataFrame based on the question
    df_filtered = webserver.data_ingestor.dataframe[webserver.data_ingestor.dataframe['Question'] == question]

    # Calculate the average of "Data_Value" for each state
    states_mean = df_filtered.groupby('LocationDesc')['Data_Value'].mean().sort_values()

    # Convert DataFrame to dictionary
    result = states_mean.to_dict()

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
    df_filtered = webserver.data_ingestor.dataframe[webserver.data_ingestor.dataframe['Question'] == question]

    if question in webserver.data_ingestor.questions_best_is_min:
        # Sort the DataFrame in ascending order
        states_mean = df_filtered.groupby('LocationDesc')['Data_Value'].mean().sort_values(ascending=True)
    else:
        # Sort the DataFrame in descending order
        states_mean = df_filtered.groupby('LocationDesc')['Data_Value'].mean().sort_values(ascending=False)

    # Get the top 5 states
    best5 = states_mean.head(5)

    # Convert DataFrame to dictionary
    result = best5.to_dict()

    # Return result dictionary
    return result


def worst5(question):
    # Filter the DataFrame based on the question
    df_filtered = webserver.data_ingestor.dataframe[webserver.data_ingestor.dataframe['Question'] == question]

    if question in webserver.data_ingestor.questions_best_is_min:
        # Sort the DataFrame in ascending order
        states_mean = df_filtered.groupby('LocationDesc')['Data_Value'].mean().sort_values(ascending=False)
    else:
        # Sort the DataFrame in descending order
        states_mean = df_filtered.groupby('LocationDesc')['Data_Value'].mean().sort_values(ascending=True)

    # Get the top 5 states
    worst5 = states_mean.head(5)

    # Convert DataFrame to dictionary
    result = worst5.to_dict()

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

