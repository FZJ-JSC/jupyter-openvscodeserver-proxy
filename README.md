![build](https://github.com/FZJ-JSC/jupyter-openvscodeserver-proxy/workflows/build/badge.svg)

# jupyter-openvscodeserver-proxy
Integrate [OpenVSCode-Server](https://github.com/gitpod-io/openvscode-server) in your Jupyter environment for an fast, feature-rich and easy to use remote desktop in the browser.

--------------------------------

![Jupyter-openvscodeserver-proxy example](docs/screenshot.png 'Jupyter-openvscodeserver-proxy example')

## Requirements
- Python 3.6+
- Jupyter Notebook 6.0+
- JupyterLab >= 3.x
- jupyter-server-proxy >= 3.2.3
- OpenVSCode-server >= 1.97.0

## Configuration
This package executes the `openvscode-server` command.  
It tries to find the `openvscode-server` executable checking the following:  
- 1. environment variable $OPENVSCODESERVER_BIN
- 2. `<dir-of-__init__.py>/bin/openvscode-server`
- 3. `which openvscode-server` (searching standard $PATH)
- 4. special locations:
     - `/opt/openvscode-server/bin/openvscode-server`

The jupyter-openvscodeserver-proxy can be configures via the following environment variables

- `JUPYTER_OPENVSCODE_PROXY_TIMEOUT` = `<int>` , default = 60
    - Specifies how long jupyter-openvscodeserver-proxy shall wait for the OpenVSCode-Server to startup until it gives up.
- `JUPYTER_OPENVSCODE_PROXY_USE_SOCKET` = `'FALSE' | 'TRUE'` ,  default = `FALSE`
    - Use unix sockets for highest security standards.
- `JUPYTER_OPENVSCODE_PROXY_DEBUG` = `'FALSE' | 'TRUE'` ,  default = `FALSE`
    - Enable to print some log messages to stderr.
- `JUPYTER_OPENVSCODE_PROXY_DEFAULT_FOLDER` = `<path>`, default = None
    - Specifies the directory that OpenVSCode will use as default folder.

- `JUPYTER_OPENVSCODE_PROXY_SERVER_DATA_DIR` = `<path>`
    - Specifies the directory that server data is kept in. If not set the default is used.
- `JUPYTER_OPENVSCODE_PROXY_USER_DATA_DIR` = `<path>`
    - Specifies the directory that user data is kept in. If not set the default is used.
- `JUPYTER_OPENVSCODE_PROXY_EXTENSIONS_DIR` = `<path>`
    - Specifies the directory that extensions are kept in. If not set the default is used.

## Install 

#### Create and Activate Environment
```
virtualenv -p python3 venv
source venv/bin/activate
```

#### Install jupyter-openvscodeserver-proxy
```
pip install git+https://github.com/FZJ-JSC/jupyter-openvscodeserver-proxy.git
```

#### Enable jupyter-openvscodeserver-proxy extensions
For Jupyter Classic, activate the jupyter-server-proxy extension:
```
jupyter serverextension enable --sys-prefix jupyter_server_proxy
```

For Jupyter Lab, install the @jupyterlab/server-proxy extension:
```
jupyter labextension install @jupyterlab/server-proxy
jupyter lab build
```

#### Start Jupyter Classic or Jupyter Lab
Click on the openvscode-server icon from the Jupyter Lab Launcher or the openvscode-server item from the New dropdown in Jupyter Classic.  
Connect to your database as instructed in the Quickstart section.

This package calls `openvscode-server` with a bunch of settings.  

## Credits
- [openvscode-server](https://github.com/gitpod-io/openvscode-server) 
- [jupyter-server-proxy](https://github.com/jupyterhub/jupyter-server-proxy)

## License
BSD 3-Clause
