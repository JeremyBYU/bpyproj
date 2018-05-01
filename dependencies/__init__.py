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


def get_python_path():
    blender_dir = os.path.dirname(sys.executable)
    # OSX directory stucture is different than linux or windows
    if is_osx():
        blender_dir = os.path.join(os.path.dirname(blender_dir), 'Resources')
    version_sub_dir = bpy.app.version_string.split(' ')[0]
    python_dir = os.path.join(
        blender_dir, version_sub_dir, PYTHON_FOLDER_STRUCTURE)
    python_path = sorted(glob(python_dir + '/python*'))[0]
    return python_path


def get_site_packages_path(python_path):
    python_dir = os.path.dirname(os.path.dirname(python_path))
    pattern = '/lib/*/site-packages'
    if is_windows():
        pattern = '/lib/site-packages*'

    site_list = sorted(glob(python_dir + pattern))
    if site_list:
        return site_list[0]
    else:
        return None


def binary_os_folder():
    """Gets the folder containing appropriate dependencies to be installed
    """
    arch = "64"
    python_ver = "35"
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
        log.info('Pyproj already installed')
    except ImportError:
        log.info("Pyproj not present! --- installing Pyproj")
        install_pyproj()


def install_pyproj():
    """Install PyProj Dependencies
    Users must have python-dev installed for linux - https://stackoverflow.com/a/21530768/9341063
    """
    log.info('Begin installing Pyproj')

    python_path = get_python_path()

    from_binary_python_package = os.path.join(binary_os_folder(), PYPROJ)
    to_site_packages_path = os.path.join(
        get_site_packages_path(python_path), PYPROJ)

    try:
        shutil.copytree(from_binary_python_package, to_site_packages_path)
        log.info('Finished installing Pyproj')
    except Exception as e:
        log.error(
            "Can not automatically install this package on Windows. Requires administrator privileges.")
        log.error(
            "Please install manually by copying the following folders.")
        log.error("FROM: %s; TO: %s", from_binary_python_package,
                  to_site_packages_path)
