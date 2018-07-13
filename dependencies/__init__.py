"""Dependency Module - Will check and install any dependencies this addon neeeds
"""
import os
import sys
from sys import platform as _platform
import shutil
import logging
from glob import glob

import bpy  # pylint: disable=E0401

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

DIR_NAME = os.path.dirname(__file__)
BINARIES_FOLDER = os.path.join(DIR_NAME, 'binaries')
PYTHON_FOLDER_STRUCTURE = 'python/bin'
PYPROJ = 'pyproj'

# TODO - Download these URLS dynamically instead of bundling
URLS = {
    'osx_64_35': 'https://anaconda.org/conda-forge/pyproj/1.9.4/download/osx-64/pyproj-1.9.4-py35_0.tar.bz2',
    'windows_64_35': 'https://anaconda.org/conda-forge/pyproj/1.9.5.1/download/win-64/pyproj-1.9.5.1-py35_0.tar.bz2',
    'linux_64_35': 'https://anaconda.org/conda-forge/pyproj/1.9.5.1/download/linux-64/pyproj-1.9.5.1-py35_0.tar.bz2'
}


def is_windows():
    return _platform == "win32"


def is_osx():
    return _platform == "darwin"


def is_linux():
    return _platform == "linux" or _platform == "linux2"


def binary_os_folder():
    """Gets the folder containing appropriate dependencies to be installed
    """
    # Recommended way to check 64 bit architecture
    # https://docs.python.org/3.5/library/platform.html
    is_64bits = sys.maxsize > 2**32

    arch = "64" if is_64bits else "32"

    python_ver = str(sys.version_info.major) + str(sys.version_info.minor)
    os_ = "linux"
    if is_windows():
        os_ = "windows"
    elif is_osx():
        os_ = "osx"

    return os.path.join(BINARIES_FOLDER, "{}_{}_{}".format(os_, arch, python_ver), 'site-packages')


def install_deps():
    """Installs all dependencies
    """
    check_install_pyproj()


def check_install_pyproj():
    """Checks if pyproj is installed, if not installs it
    """
    try:
        import pyproj  # pylint: disable=I0011, C0413, W0612
    except ImportError:
        install_pyproj()


def install_pyproj():
    """Install PyProj Dependencies
    Modified Python path to include the pyproj module that is included in package
    """

    package_dependencies_path = binary_os_folder()
    if os.path.isdir(package_dependencies_path):
        sys.path.insert(0, package_dependencies_path)
        log.info('Finished installing Pyproj')
    else:
        log.error('Pyproj package is not currently available for you system')
        log.error(
            'Can be downloaded manually from this url: https://anaconda.org/conda-forge/pyproj/files')
