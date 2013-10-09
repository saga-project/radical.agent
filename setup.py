#!/usr/bin/env python
# encoding: utf-8

"""Setup for rhythmos.agent package
"""

__author__    = "Ole Weidner"
__copyright__ = "Copyright 2013, Ole Weidner"
__email__     = "ole.weidner@icloud.com"
__license__   = "MIT"

import os, sys
from distutils.command.install_data import install_data
from distutils.command.sdist import sdist
from setuptools import setup, find_packages

#-----------------------------------------------------------------------------
# figure out the current version
def update_version():
    """
    Updates the version based on git tags
    """

    version = 'latest'

    try:
        cwd = os.path.dirname(os.path.abspath(__file__))
        fn = os.path.join(cwd, 'src/rhythmos/agent/VERSION')
        version = open(fn).read().strip()
    except IOError:
        from subprocess import Popen, PIPE, STDOUT
        import re

        VERSION_MATCH = re.compile(r'\d+\.\d+\.\d+(\w|-)*')

        try:
            p = Popen(['git', 'describe', '--tags', '--always'],
                      stdout=PIPE, stderr=STDOUT)
            out = p.communicate()[0]

            if (not p.returncode) and out:
                v = VERSION_MATCH.search(out)
                if v:
                    version = v.group()
        except OSError:
            pass

    return version

#-----------------------------------------------------------------------------
# check python version. we need > 2.5
if sys.hexversion < 0x02050000:
    raise RuntimeError("Rhythmos.agent requires Python 2.5 or better")

#-----------------------------------------------------------------------------
# 
class rhythmos_agent_install_data(install_data):
    """
    Defines the installation install_data
    """

    def finalize_options(self): 
        self.set_undefined_options('install',
                                   ('install_lib', 'install_dir'))
        install_data.finalize_options(self)

    def run(self):
        install_data.run(self)
        # ensure there's a saga/VERSION file
        fn = os.path.join(self.install_dir, 'src/rhythmos/agent/', 'VERSION')
        open(fn, 'w').write(update_version())
        self.outfiles.append(fn)

#-----------------------------------------------------------------------------
# 
class rhythmos_agent_sdist(sdist):

    def make_release_tree(self, base_dir, files):
        sdist.make_release_tree(self, base_dir, files)

        fn = os.path.join(base_dir, 'src/rhythmos/agent/', 'VERSION')
        open(fn, 'w').write(update_version())


#-----------------------------------------------------------------------------
#
def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

#-----------------------------------------------------------------------------
#
setup(name='rhythmos.agent',
      version=update_version(),
      author='Ole Weidner',
      author_email='ole.weidner@icloud.com',
      description="Pilot agent for the Rhythmos framework",
      long_description=(read('README.rst') + '\n\n' + read('CHANGES.rst')),
      license='MIT',
      keywords="rhythmos agent",
      classifiers = [
          'Development Status :: 5 - Production/Stable',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Topic :: Internet :: WWW/HTTP',
          'Framework :: Rhythmos'],
      url='https://github.com/oweidner/rhythmos.agent',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['rhythmos'],
      scripts=['bin/rhythmos-agent',
               'bin/rhythmos-node-monitor',
               'bin/rhythmos-process-wrapper'],
      #dependency_links=['https://github.com/oweidner/rhythmos.common/zipball/master#egg=rhythmos.common'],
      install_requires=['setuptools',
                        'psutil',
                        'colorama',
                        'python-hostlist'
                        #'rhythmos.common'
                        ],
      #extras_require=dict(
      #test=['zope.testing >= 3.8']),
      test_suite = 'rhythmos.agent.tests',
      package_data = {'': ['*.sh']},
      include_package_data = True,
      zip_safe = False,
      cmdclass = {
          'install_data': rhythmos_agent_install_data,
          'sdist': rhythmos_agent_sdist
      },
)
