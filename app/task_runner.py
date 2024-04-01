"""
This module defines the ThreadPool class and the TaskRunner class.
"""

import os

from queue import Queue
from threading import Thread, Lock

class ThreadPool:
    """
    A class representing a thread pool.

    Attributes:
    - job_queue (Queue): A queue to store the jobs to be executed.
    - job_status (dict): A dictionary to store the status of each job.
    - job_status_lock (Lock): A lock to synchronize access to the job_status dictionary.
    - shutdown_flag (bool): A flag indicating whether the shutdown procedure has started.
    - workers (list): A list of TaskRunner instances representing the worker threads.

    Methods:
    - __init__(): Initializes the ThreadPool instance.
    - add_job(job, job_id): Adds a job to the job queue.
    - update_job_status(job_id, status): Updates the status of a job.
    - shutdown(): Initiates a graceful shutdown of the thread pool.
    """

    def __init__(self):
        # Define the number of threads to be used by the thread pool
        num_threads = int(os.getenv('TP_NUM_OF_THREADS', os.cpu_count()))

        # Define the job queue
        self.job_queue = Queue()

        # Define the job status dictionary and its lock
        self.job_status = {}
        self.job_status_lock = Lock()

        # Define the shutdown flag
        self.shutdown_flag = False

        # Create the workers
        self.workers = [TaskRunner(self.job_queue) for _ in range(num_threads)]

        # Start the workers
        for worker in self.workers:
            worker.start()


    def add_job(self, job, job_id):
        """
        Add a job to the queue (called by the webserver when a new reqquest is made)
        """

        # If the shutdown procedure has started, do not add any more jobs
        if self.shutdown_flag:
            return False

        # Add the job to the job status dictionary as "running"
        with self.job_status_lock:
            self.job_status[job_id] = "running"

        # Add the job to the job queue (a job consists of a closure and an id)
        self.job_queue.put((job, job_id))
        return True


    def update_job_status(self, job_id, status):
        """
        Update the status of a job (called by the webserver when a job is completed)
        """

        # Update the job status in the job status dictionary
        with self.job_status_lock:
            self.job_status[job_id] = status


    def shutdown(self):
        """
        Graceful shutdown
        """

        # Mark the start of the shutdown procedure
        self.shutdown_flag = True

        # Add a None (shutdown signal) for each worker to the job queue
        for _ in self.workers:
            self.job_queue.put(None)

        # Wait for all workers to finish
        for worker in self.workers:
            worker.join()


class TaskRunner(Thread):
    """
    A class representing a worker thread that executes jobs from the job queue.

    Attributes:
    - job_queue (Queue): A queue to store the jobs to be executed.

    Methods:
    - __init__(job_queue): Initializes the TaskRunner instance.
    - run(): The main function of the worker thread.
    """

    def __init__(self, job_queue):
        # init necessary data structures
        super().__init__()
        self.job_queue = job_queue

    def run(self):
        from app import webserver

        while True:
            # Get pending job
            task = self.job_queue.get()

            # If shutdown signal was received, break out of the loop
            if task is None:
                break

            job, job_id = task

            # Execute the job
            job()

            # Update job status to "done"
            webserver.tasks_runner.update_job_status(job_id, "done")

            # Mark the job as done (decrement the queue's internal counter)
            self.job_queue.task_done()
