import os
import logging

logger = logging.getLogger(__name__)
logger.setLevel('INFO')

HERE = os.path.dirname(os.path.abspath(__file__))


def get_openvscodeserver_executable(prog):
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


def _openvscodeserver_urlparams():
    from getpass import getuser

    url_params = '?' + '&'.join([
        'tkn=' + _openvscodeserver_token,
    ])

    return url_params


# def _openvscodeserver_mappath(path):
#
#     # always pass the url parameter
#     if path in ('/', '/index.html', ):
#         url_params = _openvscodeserver_urlparams()
#         path = '/index.html' + url_params
# 
#     return path


def setup_openvscodeserver():
    """ Setup commands and and return a dictionary compatible
        with jupyter-server-proxy.
    """
    from tempfile import mkstemp
    from random import choice
    from string import ascii_letters, digits

    global _openvscodeserver_token

    # password generator
    def _get_random_alphanumeric_string(length):
        letters_and_digits = ascii_letters + digits
        return (''.join((choice(letters_and_digits) for i in range(length))))

    # generate file with random one-time-token
    _openvscodeserver_token = _get_random_alphanumeric_string(16)
    try:
        fd_token, fpath_token = mkstemp()
        logger.info('Created secure token file for openvscode-server: ' + fpath_token)

        with open(fd_token, 'w') as f:
            f.write(_openvscodeserver_token)

    except Exception:
        logger.error("Token generation in temp file FAILED")
        raise FileNotFoundError("Token generation in temp file FAILED")

    # launchers url file including url parameters
    path_info = 'openvscodeserver/' + _openvscodeserver_urlparams()
    # logger.info('OpenVSCode-Server path-info: ' + path_info)

    # create command
    cmd = [
        get_openvscodeserver_executable('openvscode-server'),
        # '--host=<ip-address>',
        '--port={port}',
        # '--socket-path=<path>',
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

    return {
        'environment': {},
        'command': cmd,
        # 'mappath': _openvscodeserver_mappath,
        'absolute_url': False,
        'timeout': 90,
        'new_browser_tab': True,
        'launcher_entry': {
            'enabled': True,
            'icon_path': os.path.join(HERE, 'icons/openvscode-server-logo.svg'),
            'title': 'VS Code (OpenVSCode)',
            # 'path_info': path_info,
        },
    }
