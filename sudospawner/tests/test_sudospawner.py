import os
import shutil
import sys
import time
from unittest.mock import Mock

import pytest
import requests
from tornado import ioloop

from sudospawner import SudoSpawner


@pytest.fixture(scope="module")
def io_loop(request):
    """Same as pytest-tornado.io_loop, but re-scoped to module-level"""
    io_loop = ioloop.IOLoop()
    io_loop.make_current()

    def _close():
        io_loop.clear_current()
        io_loop.close(all_fds=True)

    request.addfinalizer(_close)
    return io_loop


@pytest.fixture
def user():
    """pytest fixture creating a mock user"""
    user = Mock()
    user.name = "lutier"
    return user


_mock_server_sh = """
#!/bin/sh
exec "{}" -m sudospawner.tests.mockserver "$@"
""".format(
    sys.executable
).lstrip()


@pytest.fixture(autouse=True)
def mockserver(request):
    script_dir = os.path.dirname(shutil.which("sudospawner"))
    sudospawner_singleuser = os.path.join(script_dir, "sudospawner-singleuser")

    if os.path.exists(sudospawner_singleuser):
        restore_existing = True
        shutil.move(sudospawner_singleuser, sudospawner_singleuser + ".save")
    else:
        restore_existing = False

    with open(sudospawner_singleuser, "w") as f:
        os.fchmod(f.fileno(), 0o755)
        f.write(_mock_server_sh)

    def restore_singleuser():
        if restore_existing:
            shutil.move(sudospawner_singleuser + ".save", sudospawner_singleuser)
        else:
            os.remove(sudospawner_singleuser)

    request.addfinalizer(restore_singleuser)


class MockSudoSpawner(SudoSpawner):
    def get_env(self):
        env = dict(os.environ)
        env.update(self.environment)
        return env

    def do(self, *args, **kwargs):
        kwargs['_skip_sudo'] = True
        return super().do(*args, **kwargs)


@pytest.mark.gen_test
def test_spawn(user):
    spawner = MockSudoSpawner(user=user)
    ip, port = yield spawner.start()
    pid = spawner.pid
    status = yield spawner.poll()
    assert status is None
    url = "http://{}:{}".format(ip, port)
    r = requests.get(url)
    r.raise_for_status()
    yield spawner.stop()
    # check that the process is gone
    with pytest.raises(ProcessLookupError):
        os.kill(pid, 0)


@pytest.mark.gen_test
def test_poll(user):
    spawner = MockSudoSpawner(user=user)
    ip, port = yield spawner.start()
    pid = spawner.pid
    status = yield spawner.poll()
    assert status is None
    os.kill(pid, 9)
    for i in range(10):
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            break
        else:
            time.sleep(1)
    status = yield spawner.poll()
    assert isinstance(status, int)


@pytest.mark.gen_test
def test_env(user):
    spawner = MockSudoSpawner(user=user)
    spawner.environment["TEST_KEY"] = "TEST_VALUE"
    ip, port = yield spawner.start()
    status = yield spawner.poll()
    time.sleep(1)
    assert status is None
    url = "http://{}:{}/env".format(ip, port)
    r = requests.get(url)
    yield spawner.stop()
    r.raise_for_status()
    env = r.json()
    assert "TEST_KEY" in env
    assert env["TEST_KEY"] == "TEST_VALUE"
