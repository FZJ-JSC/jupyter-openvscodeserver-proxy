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
        'username=' + getuser(),
        'password=' + _openvscodeserver_passwd,
        'sharing=true',
    ])

    return url_params


def _openvscodeserver_mappath(path):

    # always pass the url parameter
    if path in ('/', '/index.html', ):
        url_params = _openvscodeserver_urlparams()
        path = '/index.html' + url_params

    return path


def setup_openvscodeserver():
    """ Setup commands and and return a dictionary compatible
        with jupyter-server-proxy.
    """
    from tempfile import mkstemp
    from random import choice
    from string import ascii_letters, digits

    global _openvscodeserver_passwd, _openvscodeserver_aeskey

    # password generator
    def _get_random_alphanumeric_string(length):
        letters_and_digits = ascii_letters + digits
        return (''.join((choice(letters_and_digits) for i in range(length))))

    # generate file with random one-time-password
    _openvscodeserver_passwd = _get_random_alphanumeric_string(16)
    try:
        fd_passwd, fpath_passwd = mkstemp()
        logger.info('Created secure password file for openvscode-server: ' + fpath_passwd)

        with open(fd_passwd, 'w') as f:
            f.write(_openvscodeserver_passwd)

    except Exception:
        logger.error("Passwd generation in temp file FAILED")
        raise FileNotFoundError("Passwd generation in temp file FAILED")

    # launchers url file including url parameters
    # path_info = 'openvscodeserver/index.html' + _openvscodeserver_urlparams()

    # create command
    cmd = [
        get_openvscodeserver_executable('openvscode-server'),
        '--auth=none',  # password
        '--disable-telemetry',
        '--disable-update-check',
        '--bind-addr=0.0.0.0:{port}',
        # '--user-data-dir=<path>',  # default: ~/.local/share/openvscode-server
        # '--config=<path>',  # default: ~/.config/openvscode-server/config.yaml
        # '--extensions-dir=<path>',  # default: .local/share/openvscode-server/extensions
        '--verbose',
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
            'title': 'VS Code (OpenVSCode-Server)',
            # 'path_info': path_info,
        },
    }
