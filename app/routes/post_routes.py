"""
This module defines the POST routes that the webserver will respond to.
It also defines the logic for handling the POST requests.
"""

from flask import request
from app import job_handler, webserver, request_methods


@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    """
    Handle the states_mean request.
    """

    # Get request data
    data = request.json
    print(f"Got request {data}")
    question = data.get('question')

    # Register job. Don't wait for task to finish
    register_job_result = job_handler.register_job(request_methods.states_mean, question)

    # Return associated job_id or error message if shutdown procedure has started
    return register_job_result


@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    """
    Handle the state_mean request.
    """

    # Get request data
    data = request.json
    print(f"Got request {data}")
    question = data.get('question')
    state = data.get('state')

    # Register job. Don't wait for task to finish
    register_job_result = job_handler.register_job(request_methods.state_mean, question, state)

    # Return associated job_id or error message if shutdown procedure has started
    return register_job_result


@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    """
    Handle the best5 request.
    """

    # Get request data
    data = request.json
    print(f"Got request {data}")
    question = data.get('question')

    # Register job. Don't wait for task to finish
    register_job_result = job_handler.register_job(request_methods.best5, question)

    # Return associated job_id or error message if shutdown procedure has started
    return register_job_result


@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    """
    Handle the worst5 request.
    """

    # Get request data
    data = request.json
    print(f"Got request {data}")
    question = data.get('question')

    # Register job. Don't wait for task to finish
    register_job_result = job_handler.register_job(request_methods.worst5, question)

    # Return associated job_id or error message if shutdown procedure has started
    return register_job_result


@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    """
    Handle the global_mean request.
    """

    # Get request data
    data = request.json
    print(f"Got request {data}")
    question = data.get('question')

    # Register job. Don't wait for task to finish
    register_job_result = job_handler.register_job(request_methods.global_mean, question)

    # Return associated job_id or error message if shutdown procedure has started
    return register_job_result


@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    """
    Handle the diff_from_mean request.
    """

    # Get request data
    data = request.json
    print(f"Got request {data}")
    question = data.get('question')

    # Register job. Don't wait for task to finish
    register_job_result = job_handler.register_job(request_methods.diff_from_mean, question)

    # Return associated job_id or error message if shutdown procedure has started
    return register_job_result


@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    """
    Handle the state_diff_from_mean request.
    """

    # Get request data
    data = request.json
    print(f"Got request {data}")
    question = data.get('question')
    state = data.get('state')

    # Register job. Don't wait for task to finish
    register_job_result = job_handler.register_job(request_methods.state_diff_from_mean,
                                                   question, state)

    # Return associated job_id or error message if shutdown procedure has started
    return register_job_result


@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    """
    Handle the mean_by_category request.
    """

    # Get request data
    data = request.json
    print(f"Got request {data}")
    question = data.get('question')

    # Register job. Don't wait for task to finish
    register_job_result = job_handler.register_job(request_methods.mean_by_category, question)

    # Return associated job_id or error message if shutdown procedure has started
    return register_job_result


@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    """
    Handle the state_mean_by_category request.
    """

    # Get request data
    data = request.json
    print(f"Got request {data}")
    question = data.get('question')
    state = data.get('state')

    # Register job. Don't wait for task to finish
    register_job_result = job_handler.register_job(request_methods.state_mean_by_category,
                                                   question, state)

    # Return associated job_id or error message if shutdown procedure has started
    return register_job_result
