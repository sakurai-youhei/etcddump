import os
from textwrap import dedent
from time import gmtime

from setuptools import find_packages
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()


setup(name='etcddump',
      version='.'.join(map(str, gmtime()[:3])),
      description="A dump tool for etcd",
      classifiers=dedent("""\
    Topic :: System :: Distributed Computing
    Topic :: Database :: Front-Ends
    Topic :: System :: Recovery Tools
    Topic :: System :: Systems Administration
    License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)
       """).splitlines(),
      long_description=README,
      keywords='etcd datastore dumper program',
      author='Giuseppe Lavagetto',
      author_email='lavagetto@gmail.com',
      url='http://github.com/lavagetto/etcddump',
      license='GPL3',
      include_package_data=True,
      zip_safe=False,
      packages=find_packages(),
      install_requires=['dnspython<2', 'python-etcd>=0.3.0'],
      entry_points={'console_scripts': ['etcdumper = etcddump.cli:main']})
