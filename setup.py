import glob
from pathlib import Path
from setuptools import setup, find_packages
import sys

if sys.version_info[:2] < (3, 5):
    raise RuntimeError("Python version >= 3.5 required.")


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

MAJOR = 0
MINOR = 1
MICRO = 0
VERSION = '%d.%d.%d' % (MAJOR, MINOR, MICRO)

setup(
    name='kakeibo',
    version=VERSION,
    description="Kakeibo",
    long_description=readme,
    author='pn11',
    author_email='pn11@users.noreply.github.com',
    url='https://github.com/pn11/kakeibo',
    license=license,
    packages=find_packages(
        where=".",
        exclude=('tests', 'docs')
    ),
    data_files=[(str(Path.home())+'/.notebook-template/', glob.glob('notebook-template/*.ipynb'))],
    python_requires='>=3.5',
    install_requires=[
        'jupyter',
        'papermill',
        'pandas',
        'matplotlib',
        'japanize_matplotlib'
      ],
)
