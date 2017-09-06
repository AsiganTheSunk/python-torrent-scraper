#!/usr/bin/env python

import random

import stem
import sys
from TorInstance import TorInstance

DEFAULT_ID = 0
DEFAULT_PROXY_PORT = 9050
DEFAULT_CNTRL_PORT = 9051
DEFAULT_INSTANCE_NICK_NAMES = ['Moctezuma','Catherine','Ghandi', 'Ragnar', 'Tokugawa', 'Sitting Bull', 'Joao II']
DEFAULT_CONNECTION_USE_LIMIT = 30
DEFAULT_PROXY_MODE = 'random'


class ProxyRotator():
    """Class

    Attributes:
    """
    def __init__(self):
        #  threading.Thread.__init__(self)
        self.tor_instance_list = []
        self.tor_last_connected = -1

        # Read from configuration file in the future
        self.tor_connection_limit = DEFAULT_CONNECTION_USE_LIMIT
        self.tor_instance_list.append(TorInstance(DEFAULT_ID, DEFAULT_INSTANCE_NICK_NAMES[0] ,
                                                  DEFAULT_PROXY_PORT, DEFAULT_CNTRL_PORT, None, None))

        self.tor_instance_counter = len(self.tor_instance_list) - 1
        self.proxy_connection_mode = DEFAULT_PROXY_MODE

    def __str__(self):
        result = '\nProxyRotator Instance\n Number of Instances: %s, Connection Mode: %s\n' %\
                 (self.tor_instance_counter +1, self.proxy_connection_mode)
        for item in self.tor_instance_list:
            result = result + '\n' + str(item) + '\n'
        return(result)

    def run(self):
        return

    def add_tor_instance(self, nickname, socks_port, cntrl_port, exit_policy, circuit_hops):
        """
        Function

        Attributes:
            - nickname: nickname of the Tor instance you have created, just an easter egg for now
            - socks_port: socks5 connection port
            - cntrl_port: cntrl connection port to manage tor over stem library
            - exit_policy: allow, deny policy
            - circuit_hops: number of hops in the tor circuit (future!!)

        """
        if nickname is None:
            nickname = DEFAULT_INSTANCE_NICK_NAMES[self.tor_instance_counter + 1]
            self.tor_instance_list.append(TorInstance(self._new_tor_instance_id(), nickname, socks_port, cntrl_port,
                                                      exit_policy, circuit_hops))


        # eval if the instance it's actually running, and change the state acordingly if needed
        try:
            control_port = stem.socket.ControlPort(port=cntrl_port)
        except stem.SocketError as exc:
            print 'Unable to connect to port %s (%s)' % (cntrl_port, exc)
            sys.exit(1)
        return

    def _new_tor_instance_id(self):
        """Function

            Attributes:
        """
        self.tor_instance_counter += 1
        return self.tor_instance_counter


    def get_tor_instance(self):
        """Function

            Attributes:
        """
        try:
            if self.proxy_connection_mode == 'sequential':
                tor_instance = self._sequential_tor_mode()
                self.eval_tor_instance(tor_instance)
                return tor_instance

            if self.proxy_connection_mode == 'random':
                tor_instance = self._random_tor_mode()
                self.eval_tor_instance(tor_instance)
                return tor_instance

        except:
            return

    def set_proxy_connection_mode(self, mode):
        self.proxy_connection_mode = mode

    def _random_tor_mode(self):
        return random.choice(self.tor_instance_list)

    def add_last_connected_count(self):
        self.tor_last_connected += 1

    def _sequential_tor_mode(self):
        self.add_last_connected_count()
        result = self.tor_instance_list[self.tor_last_connected % (self.tor_instance_counter + 1)]
        return result

    def eval_tor_instance(self, tor_instance):
        """Function

            Attributes:
            """
        if tor_instance.connection_count >= tor_instance.connection_reset_threshold:
            print '[ %s ]: %s - %s TOR Circuit should reset shortly...' % (tor_instance.nickname, tor_instance.socks_port, tor_instance.cntrl_port)
            tor_instance.reset()
            return False
        return True

    def increment_connection_count(self, tor_instance_id):
        """Function

            Attributes:
        """
        tor_instance = self.tor_instance_list[tor_instance_id]
        tor_instance.increment_connection_count()
        return