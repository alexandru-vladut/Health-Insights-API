"""
This module initializes the Flask application and sets up the global variables
that will be used throughout the application.
"""

import os

from flask import Flask
from app.logger import MyLogger
from app.task_runner import ThreadPool
from app.data_ingestor import DataIngestor
from app.job_handler import JobHandler

webserver = Flask(__name__)
webserver.tasks_runner = ThreadPool(webserver)

webserver.data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")

# Initialize the job handler
webserver.job_handler = JobHandler(webserver)

# Initialize the logger
webserver.logger = MyLogger()

# Create a results directory if it does not exist
if not os.path.exists('results'):
    os.makedirs('results')

from app import routes
