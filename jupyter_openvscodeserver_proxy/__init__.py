import os
import logging
import pwd
import getpass

import subprocess
import re

from random import choice
from string import ascii_letters, digits

import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

log_debug = os.getenv('JUPYTER_OPENVSCODE_PROXY_DEBUG')
if log_debug is not None:
    if log_debug.casefold() not in ('no', 'false'):
        handler = logging.StreamHandler(sys.stderr)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("[D %(asctime)s %(name)s] %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

HERE = os.path.dirname(os.path.abspath(__file__))

_openvscodeserver_token = None

def get_system_user():
    try:
        user = pwd.getpwuid(os.getuid())[0]
    except:
        user = os.getenv('NB_USER', getpass.getuser())
    return(user)

def setup_openvscodeserver():

    # return path to openvscode executable
    def _get_executable(prog):
        from shutil import which

        # check the special environment variable
        if os.getenv("OPENVSCODESERVER_BIN") is not None:
            return os.getenv("OPENVSCODESERVER_BIN")

        # check the bin directory of this package
        wp = os.path.join(HERE, 'bin', prog)
        if os.path.exists(wp):
            return wp

        # check the system path
        if which(prog):
            return prog

        # check at known locations
        other_paths = [
            os.path.join('/opt/openvscode-server/bin', prog),
        ]
        for op in other_paths:
            if os.path.exists(op):
                return op

        raise FileNotFoundError(f'Could not find {prog} in PATH')

    # return supported arguments
    def _support_args(args):
        ret = subprocess.check_output([_get_executable('openvscode-server'), '--help'])
        help_output = ret.decode()
        return {arg: (help_output.find(f"--{arg}") != -1) for arg in args}

    # check the version number
    def _is_version_supported(major_min, minor_min):
        try:
            ret = subprocess.check_output([_get_executable('openvscode-server'), '--version'])
            version_line = ret.decode().splitlines()[0]

            match = re.match(r"(\d+)\.(\d+)", version_line)
            if not match:
                raise ValueError("Could not extract version number")

            major, minor = map(int, match.groups())
            logger.debug(f'Found OpenVSCoder-Server in version {major}.{minor}')
            return (major > major_min) or (major == major_min and minor >= minor_min)

        except (subprocess.CalledProcessError, IndexError, ValueError) as e:
            logger.error(f"Error checking version: {e}")
            return False

    # return url prefix
    def _get_urlprefix():
        url_prefix = os.environ.get('JUPYTERHUB_SERVICE_PREFIX')
        return url_prefix

    # return command
    def _get_cmd(port, unix_socket):

        # generate file with random one-time-token
        from tempfile import mkstemp
        global _openvscodeserver_token
        try:
            fd_token, fpath_token = mkstemp()
            with open(fd_token, 'w') as f:
                f.write(_openvscodeserver_token)

        except Exception:
            logger.error("Token generation in temp file FAILED")
            raise FileNotFoundError("Token generation in temp file FAILED")

        # check for supported arguments
        supported_args = _support_args([
            'version',
            'socket-path',
            'server-base-path',
            'server-data-dir',
            'user-data-dir',
            'extensions-dir',
        ])

        # check the version
        if supported_args['version']:
            if not _is_version_supported(1, 97):
                raise NotImplementedError(
                    'OpenVSCode-Server is not installed in the required version of >= 1.97'
                )
        else:
            raise NotImplementedError(
                'Checking the version number of OpenVSCode-Server failed'
            )

        # check if settig a base-path is supported
        if not supported_args['server-base-path']:
            raise NotImplementedError(
                'OpenVSCode Server does not support --server-base-path, which is crucial.'
            )

        # create command
        cmd = [
            _get_executable('openvscode-server'),
            # '--host=<ip-address>',
            '--server-base-path={}'.format(_get_urlprefix()),
            '--connection-token-file={}'.format(fpath_token),
            '--accept-server-license-terms',
            '--disable-telemetry',
            # '--log=<level>',
        ]

        if unix_socket != "":
            if supported_args['socket-path']:
                cmd.append('--socket-path={unix_socket}')
            else:
                raise NotImplementedError(f'openvscode-server does not support requested socket connection')
        else:
            cmd.append('--port={port}')

        if supported_args['server-data-dir']:
            server_data_dir = os.getenv('JUPYTER_OPENVSCODE_PROXY_SERVER_DATA_DIR', None)
            if server_data_dir is not None:
                cmd.append('--server-data-dir=' + str(server_data_dir))

        if supported_args['user-data-dir']:
            user_data_dir = os.getenv('JUPYTER_OPENVSCODE_PROXY_USER_DATA_DIR', None)
            if user_data_dir is not None:
                cmd.append('--user-data-dir=' + str(user_data_dir))

        if supported_args['extensions-dir']:
            extensions_dir = os.getenv('JUPYTER_OPENVSCODE_PROXY_EXTENSIONS_DIR', None)
            if extensions_dir is not None:
                cmd.append('--extensions-dir=' + str(extensions_dir))

        logger.debug('OpenVSCode-Server command: ' + ' '.join(cmd))
        return cmd

    # return timeout
    def _get_timeout(default=60):
        try:
            return float(os.getenv('JUPYTER_OPENVSCODE_PROXY_TIMEOUT', default))
        except Exception:
            return default

    # return environment
    def _get_env(port, unix_socket):
        return dict(USER=get_system_user())

    # return icon path
    def _get_iconpath():
        icon_path = os.path.join(HERE, 'icons/openvscode-server-logo.svg')
        return icon_path

    # return path info = launchers url file including url parameters
    def _get_pathinfo():
        global _openvscodeserver_token
        params = ['tkn=' + _openvscodeserver_token]

        default_folder = os.getenv('JUPYTER_OPENVSCODE_PROXY_DEFAULT_FOLDER', None)
        if default_folder is not None:
            params.append(f'folder={default_folder}')

        url_params = '?' + '&'.join(params)

        path_info = 'openvscodeserver' + url_params
        return path_info

    # create random token
    global _openvscodeserver_token
    letters_and_digits = ascii_letters + digits
    _openvscodeserver_token = (''.join((choice(letters_and_digits) for i in range(16))))

    server_process = {
        'command': _get_cmd,
        'timeout': _get_timeout(),
        'environment': _get_env,
        'new_browser_tab': True,
        'launcher_entry': {
            'enabled': True,
            'title': 'VSCode (OpenVSCode)',
            'icon_path': _get_iconpath(),
            'path_info': _get_pathinfo(),
        }
    }

    use_socket = os.getenv('JUPYTER_OPENVSCODE_PROXY_USE_SOCKET')
    if use_socket is not None:
        # If this env var is anything other than case insensitive 'no' or 'false',
        # use unix sockets instead of tcp sockets. This allows us to default to
        # using unix sockets by default in the future once this feature is better
        # tested, and allow people to turn it off if needed.
        if use_socket.casefold() not in ('no', 'false'):
            server_process['unix_socket'] = True
            logger.debug('OpenVSCode-Server uses unix-sockets')

    return server_process
