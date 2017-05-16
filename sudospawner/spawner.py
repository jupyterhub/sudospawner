"""A Spawner for JupyterHub to allow the Hub to be run as non-root.

This spawns a mediator process with sudo, which then takes actions on behalf of the user.
"""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.


import json
import sys
import os

from tornado import gen
from tornado.ioloop import IOLoop
from tornado.iostream import StreamClosedError
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
    def relog_stderr(self, stderr):
        while not stderr.closed():
            try:
                line = yield stderr.read_until(b'\n')
            except StreamClosedError:
                return
            else:
                # TODO: log instead of write to stderr directly?
                # If we do that, will get huge double-prefix messages:
                # [I date JupyterHub] [W date SingleUser] msg...
                sys.stderr.write(line.decode('utf8', 'replace'))
    
    @gen.coroutine
    def do(self, action, **kwargs):
        """Instruct the mediator process to take a given action"""
        kwargs['action'] = action
        cmd = ['sudo', '-u', self.user.name]
        cmd.extend(self.sudo_args)
        cmd.append(self.sudospawner_path)
        if self.debug_mediator:
            cmd.append('--logging=debug')
        
        p = Subprocess(cmd, stdin=Subprocess.STREAM, stdout=Subprocess.STREAM, stderr=Subprocess.STREAM)
        stderr_future = self.relog_stderr(p.stderr)
        # hand the stderr future to the IOLoop so it isn't orphaned,
        # even though we aren't going to wait for it unless there's an error
        IOLoop.current().add_callback(lambda : stderr_future)
        
        yield p.stdin.write(json.dumps(kwargs).encode('utf8'))
        p.stdin.close()
        data = yield p.stdout.read_until_close()
        if p.returncode:
            yield stderr_future
            raise RuntimeError("sudospawner subprocess failed with exit code: %r" % p.returncode)

        data_str = data.decode('utf8', 'replace')

        try:
            data_str = data_str[data_str.index('{'):data_str.rindex('}')+1]
            response = json.loads(data_str)
        except ValueError:
            self.log.error("Failed to get JSON result from mediator: %r" % data_str)
            raise
        return response

    @gen.coroutine
    def start(self):
        self.port = random_port()
        # pre-0.7 JupyterHub, store ip/port in user.server:
        self.user.server.ip = self.ip
        self.user.server.port = self.port
        self.db.commit()

        # only args, not the base command
        reply = yield self.do(action='spawn', args=self.get_args(), env=self.get_env())
        self.pid = reply['pid']
        # 0.7 expects ip, port to be returned
        return (self.ip, self.port)

    @gen.coroutine
    def _signal(self, sig):
        if sig == 0:
            # short-circuit existence check without invoking sudo
            try:
                os.kill(self.pid, sig)
            except ProcessLookupError:
                # No such process
                return False
            except PermissionError:
                # When running hub with reduced permissions,
                # we won't have permission to send signals, even 0.
                # PermissionError means process exists.
                pass
            return True
        reply = yield self.do('kill', pid=self.pid, signal=sig)
        return reply['alive']

