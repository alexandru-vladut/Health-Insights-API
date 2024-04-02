"""
This module defines the GET routes that the webserver will respond to.
It also defines the logic for handling the GET requests.
"""

import os
import json

from flask import jsonify
from app import webserver


@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    """
    Get the result of a job based on the job_id.
    """

    print(f"JobID is {job_id}")

    # Check if job_id is valid and get its status
    with webserver.tasks_runner.job_status_lock:
        if job_id not in webserver.tasks_runner.job_status:
            return jsonify({"status": "error", "reason": "Invalid job_id"})

        job_status = webserver.tasks_runner.job_status[job_id]

    # Define the path to the job's result file
    result_file_path = f"./results/{job_id}.json"

    # If the job is still running
    if job_status == "running":
        return jsonify({"status": "running"})

    # If the job is done, check if the file exists and return its content
    if os.path.exists(result_file_path):
        with open(result_file_path, 'r', encoding='utf-8') as file:
            res = json.load(file)
            return jsonify({"status": "done", "data": res})

    # Handle the case where the job is done but the file does not exist
    return jsonify({"status": "error", "reason": "Job completed, but result file is missing"})


@webserver.route('/api/graceful_shutdown', methods=['GET'])
def graceful_shutdown_request():
    """
    Handle the graceful_shutdown request.
    """

    # Trigger the shutdown of the ThreadPool
    webserver.tasks_runner.shutdown()

    # Return server status
    return jsonify({"status": "shutting down"})


@webserver.route('/api/jobs', methods=['GET'])
def jobs_request():
    """
    Handle the jobs request.
    """

    # Get the status of all jobs
    with webserver.tasks_runner.job_status_lock:
        jobs_data = [{"job_id": job_id, "status": status} for job_id, status in
                     webserver.tasks_runner.job_status.items()]
    # Return the status of all jobs
    return jsonify({"status": "done", "data": jobs_data})


@webserver.route('/api/num_jobs', methods=['GET'])
def num_jobs_request():
    """
    Handle the num_jobs request.
    """

    # Get the number of running jobs
    with webserver.tasks_runner.job_status_lock:
        running_jobs = sum(status == "running" for status in
                           webserver.tasks_runner.job_status.values())

    # Return the number of running jobs
    return jsonify({"num_jobs": running_jobs})
