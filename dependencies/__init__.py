"""Dependency Module - Will check and install any dependencies this addon neeeds
"""
import os
import sys
from sys import platform as _platform
import shutil
import logging
from glob import glob

import bpy

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

DIR_NAME = os.path.dirname(__file__)
# PIP_FILE = os.path.join(DIR_NAME, 'get-pip.py')
BINARIES_FOLDER = os.path.join(DIR_NAME, 'binaries')
PYTHON_FOLDER_STRUCTURE = 'python/bin'
PYPROJ = 'pyproj'


def is_windows():
    return _platform == "win32"


def is_osx():
    return _platform == "darwin"


def is_linux():
    return _platform == "linux" or _platform == "linux2"


def get_python_path():
    blender_dir = os.path.dirname(sys.executable)
    version_sub_dir = bpy.app.version_string.split(' ')[0]
    python_dir = os.path.join(
        blender_dir, version_sub_dir, PYTHON_FOLDER_STRUCTURE)
    python_path = sorted(glob(python_dir + '/python*'))[0]
    return python_path

# def get_pip_path(python_path):
#     python_dir = os.path.dirname(python_path)
#     pattern = '/pip*'
#     if is_windows():
#         python_dir = os.path.dirname(python_dir)
#         pattern = '/Scripts/pip*'
#     pip_list = sorted(glob(python_dir + pattern))
#     if len(pip_list) > 0:
#         return pip_list[0]
#     else:
#         return None


def get_site_packages_path(python_path):
    python_dir = os.path.dirname(os.path.dirname(python_path))
    pattern = '/lib/*/site-packages'
    if is_windows():
        pattern = '/lib/site-packages*'
    # import pdb; pdb.set_trace()
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
    # check_install_pip()
    check_install_pyproj()


# def check_install_pip():
#     """Checks if pip is installed, if not installs it
#     """
#     try:
#         import pip  # pylint: disable=I0011, C0413
#         log.info('Pip already installed')
#     except ImportError:
#         log.info("Pip not present! --- installing pip")
#         install_pip()

# def install_pip():
#     """Installs pip in the blender python environment
#     """
#     log.info('Begin pip installation process')
#     # We need Pip 9, Pip 10 doesn't export internals.
#     # https://stackoverflow.com/questions/49839610/attributeerror-module-pip-has-no-attribute-main
#     # sys.argv.append('pip<=9')
#     exec(compile(open(PIP_FILE).read(), PIP_FILE, 'exec'),
#          globals())  # pylint: disable=W0122
#     log.info('Finished Pip installation')


# def run_script(cmd, verbose=False):
#     import subprocess
#     import sys
#     try:
#         if verbose:
#             print('running: {}'.format(cmd))
#         if is_windows():
#             output = subprocess.call(cmd)
#         else:
#             output = subprocess.check_output('{} | tee /dev/stderr'.format(cmd), shell=True)
#     except:
#         print('Error in run_script!')
#         # print(traceback.format_exc())
#         return ''

#     if isinstance(output, str):
#         output = output.decode(sys.getfilesystemencoding(), 'ignore')
#     print(output)
#     return output

def check_install_pyproj():
    """Checks if pyproj is installed, if not installs it
    """
    try:
        import pyproj  # pylint: disable=I0011, C0413
        log.info('Pyproj already installed')
        python_path = get_python_path()
        pip_path = get_pip_path(python_path)
        print(python_path, pip_path)
    except ImportError:
        log.info("Pyproj not present! --- installing Pyproj")
        install_pyproj()


def install_pyproj():
    """Install PyProj Dependencies
    Users must have python-dev installed for linux - https://stackoverflow.com/a/21530768/9341063
    """
    log.info('Begin installing Pyproj')

    python_path = get_python_path()
    pip_path = get_pip_path(python_path)

    from_binary_python_package = os.path.join(binary_os_folder(), PYPROJ)
    to_site_packages_path = os.path.join(
        get_site_packages_path(python_path), PYPROJ)

    if not is_windows():
        shutil.copytree(from_binary_python_package, to_site_packages_path)
        log.info('Finished installing Pyproj')
    else:
        log.error(
            "Can not install this package on Windows. Requires administrator privileges")
        log.error(
            "Please install manually by copying the following folder FROM to TO")
        log.error("FROM: %s; TO: %s", from_binary_python_package,
                  to_site_packages_path)
