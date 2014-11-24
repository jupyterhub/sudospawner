"""A Spawner for JupyterHub to allow the Hub to be run as non-root.

This spawns a separate service *as root*, which 
"""

import json
import socket

from tornado import gen
from tornado.httpclient import HTTPRequest, AsyncHTTPClient, HTTPError
from tornado.netutil import Resolver


from jupyterhub.spawner import Spawner
from jupyterhub.utils import random_port

from IPython.utils.traitlets import Instance, Unicode

class UnixResolver(Resolver):
    """UnixResolver based on https://gist.github.com/bdarnell/8641880"""
    def initialize(self, resolver, unix_mappings, **kwargs):
        self.resolver = resolver
        self.unix_mappings = unix_mappings
        super().initialize(**kwargs)
    
    def close(self):
        self.resolver.close()
 
    @gen.coroutine
    def resolve(self, host, port, *args, **kwargs):
        if host in self.unix_mappings:
            return [(socket.AF_UNIX, self.unix_mappings[host])]
        
        f = yield self.resolver.resolve(host, port, *args, **kwargs)
        return f


class SudoSpawner(Spawner):
    
    client = Instance(AsyncHTTPClient)
    def _client_default(self):
        resolver = UnixResolver(
            resolver=Resolver(),
            unix_mappings={
                'jupytersudospawner': self.sock
            },
        )
        return AsyncHTTPClient(resolver=resolver)
    
    sock = Unicode('/tmp/sudospawner')
    auth_token = Unicode()
    
    @property
    def url(self):
        return "http://jupytersudospawner/users/" + self.user.name
    
    def request(self, method, body=None):
        req = HTTPRequest(self.url,
            method=method,
            headers={'Authorization': 'token {}'.format(self.auth_token)},
            body=body,
        )
        # import IPython
        # IPython.embed()
        return self.client.fetch(req)
    
    @gen.coroutine
    def start(self):
        self.user.server.port = random_port()
        body = json.dumps(dict(
            args=self.get_args(),
            env=self.env,
        ))
        resp = yield self.request('POST', body)
    
    @gen.coroutine
    def stop(self, now=False):
        resp = yield self.request('DELETE')

    @gen.coroutine
    def poll(self):
        resp = yield self.request('GET')
        reply = json.loads(resp.body.decode('utf8'))
        return reply['status']
    
    