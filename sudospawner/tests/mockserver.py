"""Mock single-user server for testing

basic HTTP Server that echos URLs back,
and allow retrieval of sys.argv.

Handlers and their purpose include:

- EchoHandler: echoing URLs back
- ArgsHandler: allowing retrieval of `sys.argv`
- ArgsHandler: allowing retrieval of `os.environ`

Copied from JupyterHub test suite.

"""
import argparse
import json
import os
import sys

from tornado import web, httpserver, ioloop, log


class EchoHandler(web.RequestHandler):
    def get(self):
        self.write(self.request.path)


class ArgsHandler(web.RequestHandler):
    def get(self):
        self.write(json.dumps(sys.argv))


class EnvHandler(web.RequestHandler):
    """Reply to an HTTP request with the service's environment as JSON."""

    def get(self):
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(dict(os.environ)))


def main(args):
    log.enable_pretty_logging()

    app = web.Application(
        [(r".*/args", ArgsHandler), (r".*/env", EnvHandler), (r".*", EchoHandler)]
    )

    server = httpserver.HTTPServer(app)
    server.listen(args.port, '127.0.0.1')
    log.app_log.info("Starting mock server on 127.0.0.1:%i" % args.port)
    loop = ioloop.IOLoop.current()
    # stop after 60 seconds
    # so we don't leave orphaned processes lying about
    # if test cleanup gets skipped
    loop.call_later(60, loop.stop)
    try:
        loop.start()
    except KeyboardInterrupt:
        log.app_log.info("\nInterrupted")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int)
    args, extra = parser.parse_known_args()
    main(args)
