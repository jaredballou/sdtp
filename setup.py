# -*- coding: utf-8 -*-
"""
A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# To use a consistent encoding
#from cx_Freeze import setup, Executable
from codecs import open
from esky import bdist_esky
from esky.bdist_esky import Executable
from os import path
# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# version
#version_api = 0
#version_feature = 9
#version_bug = 0
from sdtp.version import api, feature, bug

here = path.abspath ( path.dirname ( __file__ ) )

# Get the long description from the relevant file
with open ( path.join ( here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read ( )

# esky
executables = [ Executable ( "sdt.py", gui_only = True ) ]
#executables = [ Executable ( "sdtp/gui/main_window.py", gui_only = True, icon = "something.ico" ) ]
    
setup (
    name='SDTP',

    # cx_Freeze
    ###########
    #executables = [ Executable ( "sdtp/gui/main_window.py" ) ],
    
    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='{}.{}.{}'.format ( api, feature, bug ),
    
    description='Seven Days To Py - A server manager and mod framework for 7 Days to Die, in Python.',
    long_description=long_description,
    
    # The project's main homepage.
    url='https://github.com/rcbrgs/sdtp',
    
    # Author details
    author='Renato Callado Borges',
    author_email='rcbrgs@hush.com',
    
    # Choose your license
    license='GNU General Public License v3 (GPLv3)',
    
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        
        # Indicate who your project is intended for
        #'Intended Audience :: Science/Research',
        #'Topic :: Scientific/Engineering :: Astronomy',
        
        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        #'Programming Language :: Python :: 2',
        #'Programming Language :: Python :: 2.6',
        #'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    
    # https://pythonhosted.org/setuptools/setuptools.html#dependencies-that-aren-t-in-pypi
    dependency_links = [
        #"git+https://github.com/evertrol/mpyfit.git#egg=mpyfit"
    ],
    
    # What does your project relate to?
    keywords='games server mod',

    # esky
    options = { "bdist_esky" : { "freezer_module" : "cxfreeze",
                                 "includes" : [ "pygeoip" ] } },
    scripts = executables,
    data_files = [ ( "", [ "GeoIP.dat" ] ) ],
    
    package_dir = { '' : 'sdtp' },
    
    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    #packages=find_packages ( exclude = [ 'docs', 'test' ] ),
    #packages = [
    #    'console',
    #    'io',
    #    'log',
    #    'models',
    #    'repo',
    #    'tools',
    #    'zeromq'
    #],
    packages = find_packages ( "sdtp" ),
    
    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires = [
        #'ipython', # Some OSX error.
        #'pymysql',
        "pygeoip",
        #'PySide', # Requires system cmake, tricky.
        "PyQt4",
        "sqlalchemy",
    ],
    
    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        'dev': [ 'sphinx' ],
        'test': [ 'coverage' ],
    },

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data={
        #'sample': [ 'package_data.dat' ],
        #'geoip': [ 'GeoIP.dat' ],
    },
    
    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    #data_files=[('my_data', ['data/data_file'])],
    
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    #entry_points={
    #    'console_scripts': [
    #        'sample=sample:main',
    #    ],
    #},
)
