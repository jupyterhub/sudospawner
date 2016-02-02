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


def finish(data, fp=sys.stdout):
    """write JSON to stdout"""
    json.dump(data, fp)
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
    cmd = ['jupyterhub-singleuser'] + args
    cmd_s = ' '.join(pipes.quote(s) for s in cmd)
    app_log.info("Spawning %s", cmd_s)
    if 'PYTHONPATH' in env:
        app_log.warn("PYTHONPATH env not allowed for security reasons")
        env.pop('PYTHONPATH')
    
    # use fork to prevent zombie process
    # create pipe to get PID from descendant
    r, w = os.pipe()
    if os.fork(): # parent
        # wait for data on pipe and relay it to stdout
        os.close(w)
        r = os.fdopen(r)
        sys.stdout.write(r.read())
    else:
        os.close(r)
        
        # don't inherit signals from Hub
        os.setpgrp()
        
        # detach child FDs, to allow parent process to exit while child waits
        null = os.open(os.devnull, os.O_RDWR)
        for fp in [sys.stdin, sys.stdout, sys.stderr]:
            os.dup2(null, fp.fileno())
        os.close(null)
        
        # launch the single-user server from the subprocess
        # TODO: If we want to see single-user log output,
        # we should send stderr to a file
        p = Popen(cmd, env=env,
            cwd=os.path.expanduser('~'),
            stdout=open(os.devnull, 'w'),
        )
        # pipe finish message to parent
        w = os.fdopen(w, 'w')
        finish({'pid': p.pid}, w)
        w.close()
        
        # wait for subprocess, so it doesn't get zombified
        p.wait()


def main():
    """parse JSON from stdin, and take the appropriate action"""
    parse_command_line()
    app_log.debug("Starting mediator for %s", getpass.getuser())
    try:
        kwargs = json.load(sys.stdin)
    except ValueError as e:
        app_log.error("Expected JSON on stdin, got %s" % e)
        sys.exit(1)
    
    action = kwargs.pop('action')
    if action == 'kill':
        kill(**kwargs)
    elif action == 'spawn':
        spawn(**kwargs)
    else:
        raise TypeError("action must be 'spawn' or 'kill'")

if __name__ == '__main__':
    main()
