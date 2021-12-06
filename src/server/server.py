# coding=utf-8
# Copyright 2018-2020 EVA
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
import string
import os

from signal import signal
from signal import SIGINT, SIGTERM, SIGHUP, SIGUSR1

from src.server.networking_utils import realtime_server_status,\
    set_socket_io_timeouts

from src.utils.logging_manager import LoggingManager, LoggingLevel

from src.server.command_handler import handle_request

from src.server.async_protocol import EvaProtocolBuffer


class EvaServer(asyncio.Protocol):

    """
    Receives messages and offloads them to another task for processing them.

    - It never creates any asynchronous tasks itself
    - It doesn't have to know anything about any event loops
    - It tracks its progress via the class-level counters
    """

    # These counters are used for realtime server monitoring
    __connections__ = 0
    __errors__ = 0
    _socket_timeout = 0

    def __init__(self, socket_timeout):
        self.transport = None
        self._socket_timeout = socket_timeout
        self.buffer = EvaProtocolBuffer()

    def connection_made(self, transport):
        self.transport = transport

        # Set timeout for sockets
        if not set_socket_io_timeouts(self.transport,
                                      self._socket_timeout, 0):
            self.transport.abort()
            return

        # Each client connection creates a new protocol instance
        peername = transport.get_extra_info('peername')
        LoggingManager().log('Connection from client: ' + str(peername) +
                             str(self._socket_timeout))
        EvaServer.__connections__ += 1

    def connection_lost(self, exc):
        # free sockets early, free sockets often
        if exc:
            EvaServer.__errors__ += 1
            self.transport.abort()
        else:
            self.transport.close()
        EvaServer.__connections__ -= 1

    def data_received(self, data):

        message = data.decode()
        LoggingManager().log('Request from client: --|' +
                             str(message) +
                             '|--')

        self.buffer.feed_data(message)
        while self.buffer.has_complete_message():
            request_message = self.buffer.read_message()

            if request_message in ["quit", "exit"]:
                LoggingManager().log('Close client socket')
                return self.transport.close()
            else:
                LoggingManager().log('Handle request')
                asyncio.create_task(
                    handle_request(self.transport, request_message)
                )


def start_server(host: string,
                 port: int,
                 loop,
                 socket_timeout: int,
                 stop_server_future):
    """
        Start the server.
        Server objects are asynchronous context managers.

        hostname: hostname of the server
        stop_server_future: future for externally stopping the server
    """

    LoggingManager().log('Start Server', LoggingLevel.CRITICAL)

    # Register signal handler
    def raiseSystemExit(_, __):
        raise SystemExit

    signals = [SIGINT, SIGTERM, SIGHUP, SIGUSR1]

    for handled_signal in signals:
        signal(handled_signal, raiseSystemExit)

    # Get a reference to the event loop
    # loop = asyncio.get_event_loop()

    # Start the eva server
    coro = loop.create_server(lambda: EvaServer(socket_timeout), host, port)
    server = loop.run_until_complete(coro)

    for socket in server.sockets:
        LoggingManager().log('PID(' + str(os.getpid()) + ') serving on '
                             + str(socket.getsockname()),
                             LoggingLevel.CRITICAL)

    server_closed = loop.create_task(server.wait_closed())

    # Start the realtime status monitor
    monitor = loop.create_task(realtime_server_status(EvaServer,
                                                      server_closed))

    try:
        loop.run_until_complete(stop_server_future)

    except KeyboardInterrupt:

        LoggingManager().log("Server process interrupted")

    finally:
        # Stop monitor
        monitor.cancel()

        # Close server
        server.close()

        # Stop event loop
        loop.run_until_complete(server.wait_closed())
        loop.close()

        LoggingManager().log("Successfully shutdown server.")
