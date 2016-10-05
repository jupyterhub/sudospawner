# Changes in sudospawner

## 0.3

- return ip, port from Spawner.start (future-compatibility, as setting ip, port directly is deprecated in JupyterHub 0.7)
- better handling of errors in the mediator
- allow overriding single-user spawn via sudospawner-singleuser script

## 0.2

- Fixes for compatibility with jupyterhub-0.4
- Relay subprocess output to Hub, to reduce silent errors
- `sudospawner` executable **must** be in the same dir as `jupyterhub-singleuser`

## 0.1

First release
