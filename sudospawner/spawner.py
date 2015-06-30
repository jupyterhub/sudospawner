"""A Spawner for JupyterHub to allow the Hub to be run as non-root.

This spawns a mediator process with sudo, which then takes actions on behalf of the user.
"""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.


import json

from tornado import gen
from tornado.process import Subprocess

from traitlets import List, Unicode, Bool

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
    
    @gen.coroutine
    def do(self, action, **kwargs):
        """Instruct the mediator process to take a given action"""
        kwargs['action'] = action
        cmd = ['sudo', '-u', self.user.name]
        cmd.extend(self.sudo_args)
        cmd.append(self.sudospawner_path)
        if self.debug_mediator:
            cmd.append('--logging=debug')
        
        p = Subprocess(cmd, stdin=Subprocess.STREAM, stdout=Subprocess.STREAM)
        yield p.stdin.write(json.dumps(kwargs).encode('utf8'))
        p.stdin.close()
        data = yield p.stdout.read_until_close()
        if p.returncode:
          raise RuntimeError("Spawner subprocess failed with exit code: %r" % p.returncode)
        return json.loads(data.decode('utf8'))

    @gen.coroutine
    def start(self):
        self.user.server.ip = self.ip
        self.user.server.port = random_port()
        self.db.commit()
        # only args, not the base command
        reply = yield self.do(action='spawn', args=self.get_args(), env=self.env)
        self.pid = reply['pid']

    @gen.coroutine
    def _signal(self, sig):
        reply = yield self.do('kill', pid=self.pid, signal=sig)
        return reply['alive']

