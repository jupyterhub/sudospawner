# example showing sudo config
# build from root with:
#    docker build -t jupyterhub-sudo -f examples/Dockerfile .
# run with:
#    docker run -it -p 8000:8000 jupyterhub-sudo
# visit http://127.0.0.1:8000 and login with username: io, password: io

FROM quay.io/jupyterhub/jupyterhub:latest

RUN apt-get -y update \
    && apt-get -y install sudo \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install jupyterlab

# add the rhea user, who will run the server
# she needs to be in the shadow group in order to access the PAM service
RUN useradd -m -G shadow -p $(openssl passwd -1 rhea) rhea

# Give rhea passwordless sudo access to run the sudospawner mediator on behalf of users:
COPY examples/sudoers /etc/sudoers.d/sudospawner

# add some regular users
RUN for name in io europa; do \
        useradd --create-home --password $(openssl passwd -1 $name) $name; \
    done

COPY . /srv/sudospawner
WORKDIR /srv/sudospawner
RUN python3 -m pip install .

# make the working dir owned by rhea, so she can create the state database
RUN chown rhea .

USER rhea
COPY examples/jupyterhub_config.py ./jupyterhub_config.py
