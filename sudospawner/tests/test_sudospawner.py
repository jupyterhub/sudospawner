import os
import shutil
import sys
import time
from unittest.mock import Mock

import pytest
import requests

from sudospawner import SudoSpawner


@pytest.fixture
def user():
    """pytest fixture creating a mock user"""
    user = Mock()
    user.name = "lutier"
    return user


_mock_server_sh = f"""
#!/bin/sh
echo "Running mock server:"
exec "{sys.executable}" -m sudospawner.tests.mockserver "$@"
""".lstrip()


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
        kwargs["_skip_sudo"] = True
        return super().do(*args, **kwargs)

    def get_args(self):
        # Per super().get_args():
        # .. versionchanged:: 2.0
        #     Prior to 2.0, JupyterHub passed some options such as ip, port,
        #     and default_url to the command-line. JupyterHub 2.0 no longer builds
        #     any CLI args other than `Spawner.cmd` and `Spawner.args`. All values
        #     that come from jupyterhub itself will be passed via environment
        #     variables.
        # mock sudospawner needs --port and will fail without it.
        return [f"--port={self.port}"]


async def test_spawn(user):
    spawner = MockSudoSpawner(user=user)
    ip, port = await spawner.start()
    pid = spawner.pid
    status = await spawner.poll()
    assert status is None
    url = f"http://{ip}:{port}"
    r = requests.get(url)
    r.raise_for_status()
    await spawner.stop()
    # check that the process is gone
    with pytest.raises(ProcessLookupError):
        os.kill(pid, 0)


async def test_poll(user):
    spawner = MockSudoSpawner(user=user)
    ip, port = await spawner.start()
    pid = spawner.pid
    status = await spawner.poll()
    assert status is None
    os.kill(pid, 9)
    for i in range(10):
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            break
        else:
            time.sleep(1)
    status = await spawner.poll()
    assert isinstance(status, int)


async def test_env(user):
    spawner = MockSudoSpawner(user=user)
    spawner.environment["TEST_KEY"] = "TEST_VALUE"
    ip, port = await spawner.start()
    status = await spawner.poll()
    time.sleep(1)
    assert status is None
    url = f"http://{ip}:{port}/env"
    r = requests.get(url)
    await spawner.stop()
    r.raise_for_status()
    env = r.json()
    assert "TEST_KEY" in env
    assert env["TEST_KEY"] == "TEST_VALUE"
