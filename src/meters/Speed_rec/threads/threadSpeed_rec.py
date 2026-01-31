# src/custom/threads/threadSpeed_rec.py

from src.templates.threadwithstop import ThreadWithStop
from src.utils.messages.messageHandlerSubscriber import messageHandlerSubscriber
from src.utils.messages.messageHandlerSender import messageHandlerSender
from src.utils.messages.allMessages import SpeedMotor, CurrentSpeed, Klem
import threading

class threadSpeed_rec(ThreadWithStop):
    def __init__(self, queuesList, logging, debugger=False):
        super(threadSpeed_rec, self).__init__()
        self.queuesList = queuesList
        self.logging = logging

        self.klem_pub = messageHandlerSender(self.queuesList, Klem)
        self.speed_sub = messageHandlerSubscriber(self.queuesList, SpeedMotor, "lastOnly", True)
        self.speed_pub = messageHandlerSender(self.queuesList, SpeedMotor)
        self.current_speed = 200.0
        self.klem_pub.send("30") # Example value for Klem

    def publish(self):  
        if self._blocker.is_set():
            return
        
        # Publish the current speed
        self.speed_pub.send(self.current_speed)
        threading.Timer(1.0, self.publish).start()

    def subscribe(self):
        # This connects the serial handler speed messages to this thread
        while not self._blocker.is_set():
            # wait for new speed message
            msg = self.speed_sub.receive()

            if msg is not None:
                # extract speed (BFMC message format)
                print("[SPEED SERIAL] Received speed message:", msg)

    def run(self):
        self.publish()
        self.subscribe()

    def stop(self):
        super(threadSpeed_rec, self).stop()