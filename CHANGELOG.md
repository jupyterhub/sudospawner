# Changes in sudospawner

## 0.4

0.4 adds better error handling:

- report better errors when sudospawner fails; change unhelpful `ValueError: substring not found`
  message when parsing output fails to a more helpful message and log the unparsed data
- treat failures to signal the process as the process being missing, and log the failure, instead of raising errors


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
