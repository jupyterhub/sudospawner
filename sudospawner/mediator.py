"""Middleman script for interacting with single-user servers via sudo.

This script is run as the user via sudo. It takes input via JSON on stdin,
and executes one of two actions:

- kill: send signal to process via os.kill
- spawn: spawn a single-user server

When spawning, uses `{sys.executable} -m jupyterhub.singleuser`, to ensure
that single-user servers are the only things this script grants permission
to spawn.
"""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import errno
import getpass
import json
import pipes
import os
import sys

from subprocess import Popen

from tornado import log
from tornado.options import parse_command_line
app_log = log.app_log


def finish(data):
    """write JSON to stdout"""
    json.dump(data, sys.stdout)
    app_log.debug("mediator result: %s", data)
    sys.stdout.flush()


def kill(pid, signal):
    """send a signal to a PID"""
    app_log.debug("Sending signal %i to %i", signal, pid)
    try:
        os.kill(pid, signal)
    except OSError as e:
        if e.errno == errno.ESRCH:
            # not running
            alive = False
        else:
            raise
    else:
        alive = True
    
    finish({'alive': alive})


def spawn(args, env):
    """spawn a single-user server
    
    Takes args *not including executable* for security reasons.
    Start the single-user server via `python -m jupyterhub.singleuser`,
    and prohibit PYTHONPATH from env for basic protections.
    """
    cmd = [sys.executable, '-m', 'jupyterhub.singleuser'] + args
    cmd_s = ' '.join(pipes.quote(s) for s in cmd)
    app_log.info("Spawning %s", cmd_s)
    if 'PYTHONPATH' in env:
        app_log.warn("PYTHONPATH env not allowed for security reasons")
        env.pop('PYTHONPATH')
    
    p = Popen(cmd, env=env, stdout=open(os.devnull, 'w'))
    finish({'pid': p.pid})


def main():
    """parse JSON from stdin, and take the appropriate action"""
    parse_command_line()
    app_log.debug("Starting mediator for %s", getpass.getuser())
    kwargs = json.load(sys.stdin)
    action = kwargs.pop('action')
    if action == 'kill':
        kill(**kwargs)
    elif action == 'spawn':
        spawn(**kwargs)
    else:
        raise TypeError("action must be 'spawn' or 'kill'")

if __name__ == '__main__':
    main()
