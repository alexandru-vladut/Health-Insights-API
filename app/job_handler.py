"""
This module defines the JobHandler class, which is responsible
for registering jobs in the ThreadPool.
"""

import json

from threading import Lock

class JobHandler:
    """
    The JobHandler class is responsible for registering jobs in the ThreadPool
    and saving the results of the jobs to a JSON file.

    Attributes:
    - webserver: The Flask application instance.
    - job_counter: An integer representing the job counter.
    - job_counter_lock: A Lock object for managing concurrent access to the job_counter.
    
    Methods:
    - register_job: Registers a job in the ThreadPool and returns the associated job_id.
    - assign_new_job_id: Generates a unique job_id and increments the job_counter.
    - save_result: Saves the result of a job to a JSON file.
    """

    def __init__(self, webserver):
        self.webserver = webserver
        self.job_counter = 1
        self.job_counter_lock = Lock()


    def register_job(self, execute_job, question, state=None):
        """
        Registers a job in the ThreadPool and returns the associated job_id.
        """

        job_id = self.assign_new_job_id()

        # Define a job closure
        def job():
            # Execute job
            result = execute_job(question) if state is None else execute_job(question, state)

            # Save the result in a JSON file
            self.save_result(result, job_id)

        # Add job (job closure and its id) to Queue
        add_job_result = self.webserver.tasks_runner.add_job(job, job_id)

        # Return job_id or error message if shutdown procedure has started
        return add_job_result


    def assign_new_job_id(self):
        """
        Generate a unique job_id and increment the job_counter
        Use a Lock to ensure that the job_counter is only accessed by one thread at a time
        """

        with self.job_counter_lock:
            job_id = f"job_id_{self.job_counter}"
            self.job_counter += 1

        return job_id


    def save_result(self, result, job_id):
        """
        Save the result of a job to a JSON file.
        """

        with open(f"results/{job_id}.json", "w", encoding='utf-8') as file:
            json.dump(result, file)
