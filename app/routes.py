from app import webserver
from flask import request, jsonify

import os
import json
import re
import app.request_methods as request_methods

# Example endpoint definition
@webserver.route('/api/post_endpoint', methods=['POST'])
def post_endpoint():
    if request.method == 'POST':
        # Assuming the request contains JSON data
        data = request.json
        print(f"got data in post {data}")

        # Process the received data
        # For demonstration purposes, just echoing back the received data
        response = {"message": "Received data successfully", "data": data}

        # Sending back a JSON response
        return jsonify(response)
    else:
        # Method Not Allowed
        return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    print(f"JobID is {job_id}")
    # TODO

    # Extract the job_id number
    match = re.search(r'\d+$', job_id)
    job_id_int = int(match.group())
    
    # Check if job_id is valid
    if (job_id_int < 1 or job_id_int > webserver.job_counter):
        return jsonify({"status": "error", "reason": "Invalid job_id"})
    
    # Define the path to the job's result file
    result_file_path = f"./results/{job_id}.json"

    # Check if the job's result file exists
    if not os.path.exists(result_file_path):
        # If the file doesn't exist, the job is still running
        return jsonify({"status": "running"})

    # If the file exists, read file content and return it
    with open(result_file_path, 'r') as file:
        res = json.load(file)
        return jsonify({"status": "done", "data": res})


@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():

    # Get request data
    data = request.json
    print(f"Got request {data}")
    question = data.get('question')

    # Generate a unique job_id and increment the job_counter
    # Use a Lock to ensure that the job_counter is only accessed by one thread at a time
    with webserver.job_counter_lock:
        job_id = "job_id_" + str(webserver.job_counter)
        webserver.job_counter += 1

    # Register job. Don't wait for task to finish
    # Define a job closure
    def job():
        # Execute job
        result = request_methods.states_mean(question)

        # Save the result in a JSON file
        with open(f"results/{job_id}.json", "w") as file:
            json.dump(result, file)

    # Add job to ThreadPool
    webserver.tasks_runner.add_job(job, job_id)

    # Return associated job_id
    return jsonify({"job_id": job_id})


@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():

    # Get request data
    data = request.json
    print(f"Got request {data}")
    question = data.get('question')
    state = data.get('state')
    
    # Generate a unique job_id and increment the job_counter
    # Use a Lock to ensure that the job_counter is only accessed by one thread at a time
    with webserver.job_counter_lock:
        job_id = "job_id_" + str(webserver.job_counter)
        webserver.job_counter += 1

    # Register job. Don't wait for task to finish
    # Define a job closure
    def job():
        # Execute job
        result = request_methods.state_mean(question, state)

        # Save the result in a JSON file
        with open(f"./results/{job_id}.json", "w") as file:
            json.dump(result, file)

    # Add job to ThreadPool
    webserver.tasks_runner.add_job(job, job_id)

    # Return associated job_id
    return jsonify({"job_id": job_id})


@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id

    return jsonify({"status": "NotImplemented"})

@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id

    return jsonify({"status": "NotImplemented"})

@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    
    # Get request data
    data = request.json
    print(f"Got request {data}")
    question = data.get('question')
    
    # Generate a unique job_id and increment the job_counter
    # Use a Lock to ensure that the job_counter is only accessed by one thread at a time
    with webserver.job_counter_lock:
        job_id = "job_id_" + str(webserver.job_counter)
        webserver.job_counter += 1

    # Register job. Don't wait for task to finish
    # Define a job closure
    def job():
        # Execute job
        result = request_methods.global_mean(question)

        # Save the result in a JSON file
        with open(f"./results/{job_id}.json", "w") as file:
            json.dump(result, file)

    # Add job to ThreadPool
    webserver.tasks_runner.add_job(job, job_id)

    # Return associated job_id
    return jsonify({"job_id": job_id})


@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    
    # Get request data
    data = request.json
    print(f"Got request {data}")
    question = data.get('question')
    
    # Generate a unique job_id and increment the job_counter
    # Use a Lock to ensure that the job_counter is only accessed by one thread at a time
    with webserver.job_counter_lock:
        job_id = "job_id_" + str(webserver.job_counter)
        webserver.job_counter += 1

    # Register job. Don't wait for task to finish
    # Define a job closure
    def job():
        # Execute job
        result = request_methods.diff_from_mean(question)

        # Save the result in a JSON file
        with open(f"./results/{job_id}.json", "w") as file:
            json.dump(result, file)

    # Add job to ThreadPool
    webserver.tasks_runner.add_job(job, job_id)

    # Return associated job_id
    return jsonify({"job_id": job_id})


@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():

    # Get request data
    data = request.json
    print(f"Got request {data}")
    question = data.get('question')
    state = data.get('state')
    
    # Generate a unique job_id and increment the job_counter
    # Use a Lock to ensure that the job_counter is only accessed by one thread at a time
    with webserver.job_counter_lock:
        job_id = "job_id_" + str(webserver.job_counter)
        webserver.job_counter += 1

    # Register job. Don't wait for task to finish
    # Define a job closure
    def job():
        # Execute job
        result = request_methods.state_diff_from_mean(question, state)

        # Save the result in a JSON file
        with open(f"./results/{job_id}.json", "w") as file:
            json.dump(result, file)

    # Add job to ThreadPool
    webserver.tasks_runner.add_job(job, job_id)

    # Return associated job_id
    return jsonify({"job_id": job_id})


@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id

    return jsonify({"status": "NotImplemented"})

@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id

    return jsonify({"status": "NotImplemented"})

# You can check localhost in your browser to see what this displays
@webserver.route('/')
@webserver.route('/index')
def index():
    routes = get_defined_routes()
    msg = f"Hello, World!\n Interact with the webserver using one of the defined routes:\n"

    # Display each route as a separate HTML <p> tag
    paragraphs = ""
    for route in routes:
        paragraphs += f"<p>{route}</p>"

    msg += paragraphs
    return msg

def get_defined_routes():
    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")
    return routes
