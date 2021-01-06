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
neighbors = []
gateways = ['10.139.40.85','10.139.40.122','10.138.57.2']
nd = node.Node(address, True, neighbors)

nm = manager.NodeManager(nd, 120, gateways)
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
