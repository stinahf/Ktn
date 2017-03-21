# -*- coding: utf-8 -*-
from threading import Thread
import json

class MessageReceiver(Thread):
    """
    This is the message receiver class. The class inherits Thread, something that
    is necessary to make the MessageReceiver start a new thread, and it allows
    the chat client to both send and receive messages at the same time
    """

    def __init__(self, client, connection):
        """
        This method is executed when creating a new MessageReceiver object
        """

        # Flag to run thread as a deamon
        self.daemon = True

        Thread.__init__(self)
        self.client = client
        self.connection = connection
        self.stop = False

    def run(self):
        while not self.stop:
            msg = self.connection.recv(4096).decode('utf-8')
            if not msg:
                break
            else:
                self.client.receive_message(json.loads(msg))
        
