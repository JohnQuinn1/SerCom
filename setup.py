try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='sercom',
    version='1.0',
    author='John Quinn',
    author_email='john.quinn@ucd.ie',
    packages=['sercom'],
    license='LICENSE.txt',
    description='Python classes to simplify PySerial communications',
)
