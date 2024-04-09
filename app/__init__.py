"""
This module initializes the Flask application and sets up the global variables
that will be used throughout the application.
"""

from flask import Flask
from app.task_runner import ThreadPool
from app.data_ingestor import DataIngestor
from app.job_handler import JobHandler

webserver = Flask(__name__)
webserver.tasks_runner = ThreadPool()

webserver.data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")

# Initialize the job handler
job_handler = JobHandler(webserver)

from app import routes
