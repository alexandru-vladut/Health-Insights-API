from queue import Queue
from threading import Thread, Event
import time
import os

class ThreadPool:
    def __init__(self):
        # You must implement a ThreadPool of TaskRunners
        # Your ThreadPool should check if an environment variable TP_NUM_OF_THREADS is defined
        # If the env var is defined, that is the number of threads to be used by the thread pool
        # Otherwise, you are to use what the hardware concurrency allows
        # You are free to write your implementation as you see fit, but
        # You must NOT:
        #   * create more threads than the hardware concurrency allows
        #   * recreate threads for each task

        # Define the number of threads to be used by the thread pool
        num_threads = int(os.getenv('TP_NUM_OF_THREADS', os.cpu_count()))

        # Define the job queue
        self.job_queue = Queue()

        # Create the workers
        self.workers = [TaskRunner(self.job_queue) for _ in range(num_threads)]
        
        # Start the workers
        for worker in self.workers:
            worker.start()

    # Add a job to the queue (called by the webserver when a new reqquest is made)
    def add_job(self, job, job_id):
        # A job consists of a closure and an id
        self.job_queue.put((job, job_id))


class TaskRunner(Thread):
    def __init__(self, job_queue):
        # TODO: init necessary data structures
        super().__init__()
        self.job_queue = job_queue

    def run(self):
        while True:
            # TODO

            # Get pending job
            job, job_id = self.job_queue.get()

            # Execute the job and save the result to disk
            job()

            # Mark the job as done (decrement the queue's internal counter)
            self.job_queue.task_done()

            # Repeat until graceful_shutdown
