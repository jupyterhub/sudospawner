"""A Spawner for JupyterHub to allow the Hub to be run as non-root.

This spawns a mediator process with sudo, which then takes actions on behalf of the user.
"""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.


import json
from subprocess import Popen, PIPE

from tornado import gen
from tornado.concurrent import Future
from tornado.process import Subprocess

from IPython.utils.traitlets import List, Unicode, Bool

from jupyterhub.spawner import LocalProcessSpawner
from jupyterhub.utils import random_port

class SudoSpawner(LocalProcessSpawner):
    
    sudospawner_path = Unicode('sudospawner', config=True,
        help="Path to sudospawner script"
    )
    sudo_args = List(['-nH'], config=True,
        help="Extra args to pass to sudo"
    )
    debug_mediator = Bool(False, config=True,
        help="Extra log output from the mediator process for debugging",
    )
    
    def do(self, action, **kwargs):
        """Instruct the mediator process to take a given action"""
        kwargs['action'] = action
        cmd = ['sudo', '-u', self.user.name]
        cmd.extend(self.sudo_args)
        cmd.append(self.sudospawner_path)
        if self.debug_mediator:
            cmd.append('--logging=debug')
        
        p = Popen(cmd, stdin=PIPE, stdout=PIPE)
        data = json.dumps(kwargs).encode('utf8')
        stdout, _ = p.communicate(data)
        f = Future()
        f.set_result(json.loads(stdout.decode('utf8')))
        # def finish(returncode):
        #     buf = p.stdout.read().decode('utf8')
        #     f.set_result(json.loads(buf))
        #
        # p.set_exit_callback(finish)
        return f

    @gen.coroutine
    def start(self):
        self.user.server.port = random_port()
        # only args, not the base command
        reply = yield self.do(action='spawn', args=self.get_args(), env=self.env)
        self.pid = reply['pid']

    @gen.coroutine
    def _signal(self, sig):
        reply = yield self.do('kill', pid=self.pid, signal=sig)
        return reply['alive']

