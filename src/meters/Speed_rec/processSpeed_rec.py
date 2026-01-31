if __name__ == "__main__":
    import sys
    sys.path.insert(0, "../../..")

from src.templates.workerprocess import WorkerProcess
from src.meters.Speed_rec.threads.threadSpeed_rec import threadSpeed_rec
class processSpeed_rec(WorkerProcess):
    """This process handles Speed_rec.
    Args:
        queueList (dictionary of multiprocessing.queues.Queue): Dictionary of queues where the ID is the type of messages.
        logging (logging object): Made for debugging.
        debugging (bool, optional): A flag for debugging. Defaults to False.
    """

    def __init__(self, queueList, logging, debugging=False):
        self.queuesList = queueList
        self.logging = logging
        self.debugging = debugging
        super(processSpeed_rec, self).__init__(self.queuesList)

    def run(self):
        """Apply the initializing methods and start the threads."""
        super(processSpeed_rec, self).run()

    def _init_threads(self):
        """Create the Speed_rec Publisher thread and add to the list of threads."""
        Speed_recTh = threadSpeed_rec(
            self.queuesList, self.logging, self.debugging
        )
        self.threads.append(Speed_recTh)

    def _stop(self):
        for t in self.threads:
            t.stop()
            t.join()
        super(processSpeedSerial, self).stop()