#!/usr/bin/env python
import os
import re
import shutil
import subprocess
import sys


toplevel = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


re_setup = re.compile(r'setup\(')
re_version = re.compile(r'(?<=\bversion=[\'"])([0-9a-zA-Z._+-]+)')


version_mode = None


def update_version(gitversion, foundversion):
    """Chooses version string to write to setup.py.
    """
    if version_mode == 'setuppy':
        return foundversion
    else:
        return gitversion


def make_pkg():
    # Get version from git describe
    version = subprocess.check_output(['git', 'describe',
                                       '--always', '--tags'],
                                      cwd=toplevel).strip()

    dest = os.path.join(toplevel, 'dist')

    if not os.path.exists(dest):
        os.mkdir(dest)

    for project in ('reprozip', 'reprounzip', 'reprounzip-docker',
                    'reprounzip-vagrant', 'reprounzip-vistrails'):
        pdir = os.path.join(toplevel, project)
        setup_py = os.path.join(pdir, 'setup.py')

        # Update setup.py file
        with open(setup_py, 'rb') as fp:
            lines = fp.readlines()

        i = 0
        setup_found = False
        while i < len(lines):
            line = lines[i]
            if not setup_found and re_setup.search(line):
                setup_found = True
            if setup_found:
                m = re_version.search(line)
                if m is not None:
                    version = update_version(version, m.group(1))
                    lines[i] = re_version.sub(version, line)
                    break
            i += 1

        with open(setup_py, 'wb') as fp:
            for line in lines:
                fp.write(line)

        # Run sdist
        subprocess.check_call([sys.executable, setup_py, 'sdist'])

        # Run bdist_wheel
        try:
            __import__('wheel')
        except ImportError:
            pass
        else:
            subprocess.check_call([sys.executable, setup_py, 'bdist_wheel'])

        # Move output to top-level dist/
        for f in os.listdir(os.path.join(pdir, 'dist')):
            shutil.copyfile(os.path.join(pdir, 'dist', f),
                            os.path.join(dest, f))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: buildpkgs.py (release|nightly)\n")
        sys.exit(1)

    if sys.argv[1] == 'release':
        version_mode = 'setuppy'
    elif sys.argv[1] == 'nightly':
        version_mode = 'git'

    make_pkg()
