import os
import logging
import pwd
import getpass

logger = logging.getLogger(__name__)
logger.setLevel('INFO')

HERE = os.path.dirname(os.path.abspath(__file__))

global _openvscodeserver_token

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

    # return url prefix
    def _get_urlprefix():
        url_prefix = os.environ.get('JUPYTERHUB_SERVICE_PREFIX')
        return url_prefix

    # return url parameters
    def _get_urlparams():
        url_params = '?' + '&'.join([
            'tkn=' + _openvscodeserver_token,
        ])
        return url_params

    # return the map path
    # def _get_mappath(path):
    #     # always pass the url parameter
    #     if path in ('/', '/index.html', ):
    #         path = '/index.html' + _get_urlparams()
    #     return path

    # return command
    def _get_cmd(port):

        # generate file with random one-time-token
        from tempfile import mkstemp
        from random import choice
        from string import ascii_letters, digits

        letters_and_digits = ascii_letters + digits
        token = (''.join((choice(letters_and_digits) for i in range(length))))

        try:
            fd_token, fpath_token = mkstemp()
            logger.info('Created secure token file for openvscode-server: ' + fpath_token)

            with open(fd_token, 'w') as f:
                f.write(token)

        except Exception:
            logger.error("Token generation in temp file FAILED")
            raise FileNotFoundError("Token generation in temp file FAILED")

        # create command
        cmd = [
            _get_executable('openvscode-server'),
            # '--host=<ip-address>',
            '--port={port}',
            # '--socket-path=<path>',
            '--server-base-path={}'.format(_get_urlprefix()),
            # '--connection-token=<token>',
            '--connection-token-file={}'.format(fpath_token),
            # '--without-connection-token',
            '--accept-server-license-terms',
            # '--server-data-dir=<dir>',
            '--disable-telemetry',
            # '--default-folder=<dir',
            # '--user-data-dir=<dir>',
            # '--extensions-dir=<dir>',
            # '--log=<level>',
        ]
        logger.info('OpenVSCode-Server command: ' + ' '.join(cmd))

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
        return os.path.join(HERE, 'icons/openvscode-server-logo.svg'),

    # return path info = launchers url file including url parameters
    def _get_pathinfo():
        path_info = 'openvscodeserver/' + _get_urlparams()
        logger.info('OpenVSCode-Server path-info: ' + path_info)

    server_process = {
        'command': _get_cmd,
        'timeout': _get_timeout(),
        'environment': _get_env,
        # 'mappath': _get_mappath,
        'new_browser_tab': True,
        'launcher_entry': {
            'enabled': True,
            'title': 'VS Code (OpenVSCode)',
            'icon_path': _get_iconpath()
            # 'path_info': _get_pathinfo,
        }
    }

    return server_process