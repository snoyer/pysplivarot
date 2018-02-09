import os
import subprocess
import setuptools
from setuptools.command.install import install
from setuptools.command.install_lib import install_lib


def setup() :
    PACKAGE_NAME = 'pysplivarot'

    INKSCAPE_HOME = find_include_dir_for('src/inkscape.h')
    INKSCAPE_SRC = os.path.join(INKSCAPE_HOME, 'src')
    INKSCAPE_LIB = os.path.join(INKSCAPE_HOME, 'build', 'lib')

    FIXLIB_NAME = 'fixlivarotlib'

    include_dirs = [
        'src', 'src/inkscape-fix',
        INKSCAPE_SRC,
        find_include_dir_for('glib.h'),
        find_include_dir_for('glibconfig.h'),
    ]

    class InstallCommand(install):
        """"compile .a file with missing symbols before compiling extension so we can link against it"""

        def run(self) :
            cmd = [
                'x86_64-linux-gnu-gcc', '-Wall', '-g', #TODO un-harcode compiler
                '-I'+INKSCAPE_SRC, '-Isrc/inkscape-fix',
                '-c', '-fPIC',
                '-o', os.path.join(PACKAGE_NAME, FIXLIB_NAME+'.o'),
                'src/inkscape-fix/stringstream.cpp',
            ]
            subprocess.check_call(cmd)
            subprocess.check_call(['ar', 'rcs',
                os.path.join(PACKAGE_NAME, 'lib%s.a' % FIXLIB_NAME),
                os.path.join(PACKAGE_NAME, FIXLIB_NAME+'.o'),
            ])

            install.run(self)

    class InstallLibCommand(install_lib):
        """copy missing symbols .a to module directory to be available at runtime"""
        def run(self):
            install_lib.run(self)

            dest = os.path.join(self.install_dir, PACKAGE_NAME)
            subprocess.check_call(['mv',
                os.path.join(PACKAGE_NAME, 'lib'+FIXLIB_NAME+'.a'),
                dest
            ])

            txt_path = os.path.join(dest, 'ld_library_path')
            with open(txt_path, 'w') as out :
                print >>out, ':'.join([
                    os.path.abspath(dest),
                    INKSCAPE_HOME+'/build/lib',
                ])


    setuptools.setup(
        name=PACKAGE_NAME,
        version='0.0.1',
        description='inkscape splivarot bindings',
        url='http://github.com/snoyer/pytwogeom',
        author='snoyer',
        author_email='reach me on github',
        packages=[PACKAGE_NAME],
        install_requires=[],
        ext_modules=[
            setuptools.Extension(
                PACKAGE_NAME+'._'+PACKAGE_NAME,
                ['src/pysplivarot.cpp'],
                include_dirs=include_dirs,
                library_dirs=[INKSCAPE_LIB, PACKAGE_NAME],
                libraries=['boost_python', 'livarot_LIB', '2geom_LIB', FIXLIB_NAME, 'gsl', 'blas', 'cairo', 'glib-2.0'],
            ),
        ],
        cmdclass = {
            'install': InstallCommand,
            'install_lib': InstallLibCommand,
        },

    )


def locate(*names) :
    p = subprocess.Popen(['locate']+list(names), stdout=subprocess.PIPE, stderr=subprocess.PIPE,)
    out,err = p.communicate()
    return out.splitlines()

def find_include_dir_for(name) :
    def score(path) :
        folders = os.path.normpath(path).split(os.sep)
        return (
            0 if 'include' in folders else 1,
            len([f for f in folders if f.startswith('.')]),
            len(folders),
        )

    candidates = (path for path in locate(name) if path.endswith(name))
    for best in sorted(candidates, key=score) :
        best_dir = best[:-len(name)-1]
        if os.path.isdir(best_dir) :
            return best_dir


setup()
