"""
This module initializes the Flask application and sets up the global variables
that will be used throughout the application.
"""

from threading import Lock
from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool

webserver = Flask(__name__)
webserver.tasks_runner = ThreadPool()

webserver.data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")

webserver.job_counter = 1

# Define a lock for managing concurrent access to the job_counter, both when
# reading (assigning a job_id to a new request) and writing (incrementing the job_counter).
webserver.job_counter_lock = Lock()
