"""Service for spawning JupyterHub single-user servers."""

import json
import os
import re
import sys

from tornado import gen, web, log, ioloop, httpserver, options
from tornado.log import app_log
from tornado.netutil import bind_unix_socket

from jupyterhub.spawner import LocalProcessSpawner

from IPython.utils.traitlets import (
    HasTraits, Unicode, Integer, Instance, List, Dict,
)

# pattern for the authentication token header
auth_header_pat = re.compile(r'^token\s+([^\s]+)$')


class ServiceSpawner(LocalProcessSpawner):
    def _env_default(self):
        return {}
    
    args = List()
    def get_args(self):
        return self.args


class Server(HasTraits):
    """Dummy Server mimicking JupyterHub ORM Server"""
    ip = Unicode()
    port = Integer()
    

class User(HasTraits):
    """Dummy User, mimicking ORM User"""
    name = Unicode()
    server = Instance(Server)
    spawner = Instance(ServiceSpawner)
    state = Dict()


class BaseHandler(web.RequestHandler):
    
    # auth
    
    @property
    def api_token(self):
        return self.settings['api_token']
    
    def get_current_user(self):
        """get_current_user from Authorization header token"""
        if not self.api_token:
            return 'authenticated'
        auth_header = self.request.headers.get('Authorization', '')
        match = auth_header_pat.match(auth_header)
        if not match:
            return None
        token = match.group(1)
        if token == self.api_token:
            return 'authenticated'
    
    @property
    def jpy_config(self):
        return None
    
    @property
    def users(self):
        return self.settings.setdefault('users', {})
    
    @property
    def json_body(self):
        try:
            return json.loads(self.request.body.decode('utf8'))
        except Exception as e:
            app_log.warn("Invalid JSON body", exc_info=True)
            raise web.HTTPError(400, "Body must be JSON")


# /user/:name
class UserHandler(BaseHandler):
    """Handle /users/:name requests for start/stop/poll"""
    
    @web.authenticated
    @gen.coroutine
    def get(self, name):
        """GET /users/:name polls a spawner"""
        if name not in self.users:
            app_log.warn("User %s doesn't exist", name)
            status = 0
        else:
            status = yield self.users[name].spawner.poll()
            if status is not None:
                self.users.pop(name)
        self.finish({
            'status': status,
        })
    
    @web.authenticated
    @gen.coroutine
    def post(self, name):
        """POST /users/:name starts a spawner"""
        if name in self.users:
            raise web.HTTPError(400, "User %s exists" % name)
        body = self.json_body
        args = body.get('args', [])
        env = body.get('env', None)
        user = self.users[name] = User(name=name)
        # only create the server to capture the port from the Spawner
        user.server = Server()
        user.spawner = ServiceSpawner(
            args=args,
            env=env,
            user=user,
            config=self.jpy_config,
        )
        yield user.spawner.start()

    @web.authenticated
    @gen.coroutine
    def delete(self, name):
        """DELETE /users/:name stops a spawner"""
        if name not in self.users:
            raise web.HTTPError(404, "User %s doesn't exist" % name)
        user = self.users.pop(name)
        yield user.spawner.stop()


def main():
    options.parse_command_line()
    app = web.Application([
            (r"/users/([^/]+)", UserHandler),
        ],
        users={},
        api_token='',
    )
    server = httpserver.HTTPServer(app)
    socket = bind_unix_socket('/tmp/sudospawner')
    server.add_socket(socket)
    ioloop.IOLoop.instance().start()
    
if __name__ == '__main__':
    main()
