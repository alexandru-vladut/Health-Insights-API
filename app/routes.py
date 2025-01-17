"""
This module defines the routes that the webserver will respond to.
It also defines the logic for handling the requests.
"""

import os
import json

from flask import request, jsonify
from app import webserver, request_methods


# ================== POST ROUTES ==================

@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    """
    Handle the states_mean request.
    """

    # Get request data
    data = request.json
    question = data.get('question')

    webserver.logger.info(f"Received states_mean request.\nQuestion: {question}")

    # Register job. Don't wait for task to finish
    register_job_result = webserver.job_handler.register_job(request_methods.states_mean, question)

    # Return associated job_id or error message if shutdown procedure has started
    return register_job_result


@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    """
    Handle the state_mean request.
    """

    # Get request data
    data = request.json
    question = data.get('question')
    state = data.get('state')

    webserver.logger.info(f"Received state_mean request.\nQuestion: {question}\nState: {state}")

    # Register job. Don't wait for task to finish
    register_job_result = webserver.job_handler.register_job(
        request_methods.state_mean, question, state)

    # Return associated job_id or error message if shutdown procedure has started
    return register_job_result


@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    """
    Handle the best5 request.
    """

    # Get request data
    data = request.json
    question = data.get('question')

    webserver.logger.info(f"Received best5 request.\nQuestion: {question}")

    # Register job. Don't wait for task to finish
    register_job_result = webserver.job_handler.register_job(request_methods.best5, question)

    # Return associated job_id or error message if shutdown procedure has started
    return register_job_result


@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    """
    Handle the worst5 request.
    """

    # Get request data
    data = request.json
    question = data.get('question')

    webserver.logger.info(f"Received worst5 request.\nQuestion: {question}")

    # Register job. Don't wait for task to finish
    register_job_result = webserver.job_handler.register_job(request_methods.worst5, question)

    # Return associated job_id or error message if shutdown procedure has started
    return register_job_result


@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    """
    Handle the global_mean request.
    """

    # Get request data
    data = request.json
    question = data.get('question')

    webserver.logger.info(f"Received global_mean request.\nQuestion: {question}")

    # Register job. Don't wait for task to finish
    register_job_result = webserver.job_handler.register_job(request_methods.global_mean, question)

    # Return associated job_id or error message if shutdown procedure has started
    return register_job_result


@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    """
    Handle the diff_from_mean request.
    """

    # Get request data
    data = request.json
    question = data.get('question')

    webserver.logger.info(f"Received diff_from_mean request.\nQuestion: {question}")

    # Register job. Don't wait for task to finish
    register_job_result = webserver.job_handler.register_job(
        request_methods.diff_from_mean, question)

    # Return associated job_id or error message if shutdown procedure has started
    return register_job_result


@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    """
    Handle the state_diff_from_mean request.
    """

    # Get request data
    data = request.json
    question = data.get('question')
    state = data.get('state')

    webserver.logger.info(
        f"Received state_diff_from_mean request.\nQuestion: {question}\nState: {state}")

    # Register job. Don't wait for task to finish
    register_job_result = webserver.job_handler.register_job(
        request_methods.state_diff_from_mean, question, state)

    # Return associated job_id or error message if shutdown procedure has started
    return register_job_result


@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    """
    Handle the mean_by_category request.
    """

    # Get request data
    data = request.json
    question = data.get('question')

    webserver.logger.info(f"Received mean_by_category request.\nQuestion: {question}")

    # Register job. Don't wait for task to finish
    register_job_result = webserver.job_handler.register_job(
        request_methods.mean_by_category, question)

    # Return associated job_id or error message if shutdown procedure has started
    return register_job_result


@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    """
    Handle the state_mean_by_category request.
    """

    # Get request data
    data = request.json
    question = data.get('question')
    state = data.get('state')

    webserver.logger.info(
        f"Received state_mean_by_category request.\nQuestion: {question}\nState: {state}")

    # Register job. Don't wait for task to finish
    register_job_result = webserver.job_handler.register_job(
        request_methods.state_mean_by_category, question, state)

    # Return associated job_id or error message if shutdown procedure has started
    return register_job_result


# ================== GET ROUTES ==================

@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    """
    Get the result of a job based on the job_id.
    """

    webserver.logger.info(f"Received get_results request for job with ID: {job_id}")

    # Check if job_id is valid and get its status
    with webserver.tasks_runner.job_status_lock:
        if job_id not in webserver.tasks_runner.job_status:
            webserver.logger.error(f"Invalid job_id: {job_id}")
            return jsonify({"status": "error", "reason": "Invalid job_id"})

        job_status = webserver.tasks_runner.job_status[job_id]

    # Define the path to the job's result file
    result_file_path = f"./results/{job_id}.json"

    # If the job is still running
    if job_status == "running":
        webserver.logger.info(f"Job with ID {job_id} is still running.")
        return jsonify({"status": "running"})

    # If the job is done, check if the file exists and return its content
    if os.path.exists(result_file_path):
        with open(result_file_path, 'r', encoding='utf-8') as file:
            res = json.load(file)
            webserver.logger.info(f"Job with ID {job_id} is done. Returning result...")
            return jsonify({"status": "done", "data": res})

    # Handle the case where the job is done but the file does not exist
    webserver.logger.error(f"Job with ID {job_id} is done, but result file is missing.")
    return jsonify({"status": "error", "reason": "Job completed, but result file is missing"})


@webserver.route('/api/graceful_shutdown', methods=['GET'])
def graceful_shutdown_request():
    """
    Handle the graceful_shutdown request.
    """

    webserver.logger.info("Received graceful_shutdown request. Initiating shutdown procedure...")

    # Trigger the shutdown of the ThreadPool
    webserver.tasks_runner.shutdown()

    webserver.logger.info("Shutdown procedure completed.")

    # Return server status
    return jsonify({"status": "shutting down"})


@webserver.route('/api/jobs', methods=['GET'])
def jobs_request():
    """
    Handle the jobs request.
    """

    webserver.logger.info("Received jobs request.")

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

    webserver.logger.info("Received num_jobs request.")

    # Get the number of running jobs
    with webserver.tasks_runner.job_status_lock:
        running_jobs = sum(status == "running" for status in
                           webserver.tasks_runner.job_status.values())

    # Return the number of running jobs
    return jsonify({"num_jobs": running_jobs})


# ================== EXAMPLE ROUTES ==================

@webserver.route('/api/post_endpoint', methods=['POST'])
def post_endpoint():
    """
    Example POST endpoint that receives JSON data and returns a JSON response.
    """

    if request.method == 'POST':
        # Assuming the request contains JSON data
        data = request.json

        # Process the received data
        # For demonstration purposes, just echoing back the received data
        response = {"message": "Received data successfully", "data": data}

        # Sending back a JSON response
        return jsonify(response)

    # Method Not Allowed
    return jsonify({"error": "Method not allowed"}), 405


# You can check localhost in your browser to see what this displays
@webserver.route('/')
@webserver.route('/index')
def index():
    """
    Display the available routes when accessing the root URL.
    """

    routes = get_defined_routes()
    msg = "Hello, World!\n Interact with the webserver using one of the defined routes:\n"

    # Display each route as a separate HTML <p> tag
    paragraphs = "".join([f"<p>{route}</p>" for route in routes])
    msg += paragraphs
    return msg

def get_defined_routes():
    """
    Get the defined routes in the webserver.
    """

    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")
    return routes
