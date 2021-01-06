import sys
sys.path.append(".")

import datetime
import time
import os
from twisted.python import log
from twisted.internet import reactor, protocol
from twisted.internet.protocol import ServerFactory, ClientFactory, Protocol

import MessageClientProtocol as client
import MessageServerProtocol as server
import Node as node
import NodeManager as manager

address = str(sys.argv[1])
neighbors = ["10.0.0.2",'10.0.0.3','10.0.0.4']
gateways = ["10.0.1.1",'10.0.1.2', '10.0.1.3']
nd = node.Node(address, True, neighbors)

nm = manager.NodeManager(nd, 120)
nm.isProxy = False

if reactor.running:
    reactor.stop()
    
factory = protocol.ServerFactory()
factory.protocol = server.MessageServerProtocol
factory.protocol.node = nm
reactor.listenTCP(5555, factory)

if nd.isRoot:
    reactor.callLater(15, nm.mainLoop)
    reactor.callLater(nm.period, nm.download)

reactor.run()
