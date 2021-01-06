import datetime
from subprocess import check_output, PIPE, Popen
import subprocess
import shlex
import threading
import os

import sys
from twisted.python import log
from twisted.internet import reactor, protocol
from twisted.internet.protocol import ServerFactory, Protocol
import NodeManager as neigh

#SERVER SECTION
class MessageServerProtocol(Protocol):
    node = None
    ''' As soon as you receive something then send it to the neighbors '''
    
    def dataReceived(self,data):
        connected = self.transport.getPeer().host
        print("Connected with",connected)
        nlist = data.decode('utf-8').split('#') # received measurements
        self.node.receiveCount += 1
        self.node.process(nlist, connected)
        self.transport.loseConnection()
    
    def connectionLost(self, reason):
        return
