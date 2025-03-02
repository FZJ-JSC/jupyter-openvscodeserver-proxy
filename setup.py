from os import path
from setuptools import setup, find_packages

HERE = path.abspath(path.dirname(__file__))
with open(path.join(HERE, 'README.md'), 'r', encoding='utf-8') as fh:
    long_description = fh.read()

version = '0.9.3'
setup(
    name='jupyter-openvscodeserver-proxy',
    version=version,
    packages=find_packages(),

    url='https://github.com/FZJ-JSC/jupyter-openvscodeserver-proxy',
    download_url='https://github.com/FZJ-JSC/jupyter-openvscodeserver-proxy/archive/refs/tags/v{0}.tar.gz'.format(version),

    author='Jens Henrik Goebbert',
    author_email='j.goebbert@fz-juelich.de',

    description='OpenVSCode-Server for JupyterLab',
    long_description=long_description,
    long_description_content_type='text/markdown',

    keywords=['jupyter', 'openvscode-server', 'jupyterhub', 'jupyter-server-proxy'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Framework :: Jupyter',
    ],

    entry_points={
        'jupyter_serverproxy_servers': [
            'openvscodeserver = jupyter_openvscodeserver_proxy:setup_openvscodeserver',
        ]
    },
    python_requires='>=3.6',
    install_requires=['jupyter-server-proxy>=3.2.3'],
    include_package_data=True,
    zip_safe=False
)
