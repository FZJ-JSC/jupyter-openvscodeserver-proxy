![build](https://github.com/FZJ-JSC/jupyter-openvscodeserver-proxy/workflows/build/badge.svg)

# jupyter-openvscodeserver-proxy
Integrate [OpenVSCode-Server](https://github.com/gitpod-io/openvscode-server) in your Jupyter environment for an fast, feature-rich and easy to use remote desktop in the browser.

--------------------------------
**ATTENTION - NOT functional!**  
jupyter-openvscodeserver-proxy requires a missing feature in VSCode/OpenVSCode to function.  
If you want to help, please support the following feature request: https://github.com/microsoft/vscode/issues/153679  

--------------------------------

![Jupyter-openvscodeserver-proxy example](docs/screenshot.png 'Jupyter-openvscodeserver-proxy example')

## Requirements
- Python 3.6+
- Jupyter Notebook 6.0+
- JupyterLab >= 3.x
- jupyter-server-proxy >= 3.1.0

This package executes the `openvscode-server` command.  
It tries to find the `openvscode-server` executable checking the following:  
- 1. environment variable $OPENVSCODESERVER_BIN
- 2. `<dir-of-__init__.py>/bin/openvscode-server`
- 3. `which openvscode-server` (searching standard $PATH)
- 4. special locations:
     - `/opt/openvscode-server/bin/openvscode-server`

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
Click on the code-server icon from the Jupyter Lab Launcher or the openvscode-server item from the New dropdown in Jupyter Classic.  
Connect to your database as instructed in the Quickstart section.

## Configuration
This package calls `openvscode-server` with a bunch of settings.  
You have to modify `setup_openvscodeserver()` in `jupyter_openvscodeserver_proxy/__init__.py` for change.

## Credits
- [openvscode-server](https://github.com/gitpod-io/openvscode-server) 
- jupyter-server-proxy

## License
BSD 3-Clause
