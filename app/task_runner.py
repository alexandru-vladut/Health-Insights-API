from queue import Queue
from threading import Thread, Lock
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

    # Add a job to the queue (called by the webserver when a new reqquest is made)
    def add_job(self, job, job_id):
        # If the shutdown procedure has started, do not add any more jobs
        if self.shutdown_flag:
            return False
        
        # Add the job to the job status dictionary as "running"
        with self.job_status_lock:
            self.job_status[job_id] = "running"

        # Add the job to the job queue (a job consists of a closure and an id)
        self.job_queue.put((job, job_id))
        return True
    
    # Update the status of a job (called by the webserver when a job is completed)
    def update_job_status(self, job_id, status):
        # Update the job status in the job status dictionary
        with self.job_status_lock:
            self.job_status[job_id] = status

    # Graceful shutdown
    def shutdown(self):
        # Mark the start of the shutdown procedure
        self.shutdown_flag = True

        # Add a None (shutdown signal) for each worker to the job queue
        for _ in self.workers:
            self.job_queue.put(None)

        # Wait for all workers to finish
        for worker in self.workers:
            worker.join()


class TaskRunner(Thread):
    def __init__(self, job_queue):
        # TODO: init necessary data structures
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
