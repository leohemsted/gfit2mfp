from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

LONG_DESC = '''
Google Fit -> My Fitness Pal
============================

A script that pulls your google fit data and adds it to your myfitnesspal account
'''
class PyTest(TestCommand):
    '''
    See https://pytest.org/latest/goodpractises.html#integration-with-setuptools-test-commands
    '''
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest, sys
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name='gfit2mfp',
    description='Google Fit -> My Fitness Pal',
    long_description=LONG_DESC,
    version='0.2',
    url='https://github.com/leohemsted/gfit2mfp/',
    author='Leo Hemsted',
    author_email='leohemsted@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License'
    ],
    keywords='googlefit fit myfitnesspal mfp excercise',
    packages=find_packages(),
    install_requires=[
        'requests>=2.7.0',
        'google-api-python-client>=1.4.0',
        'oauth2client>=1.4.6',
        'httplib2>=0.9.1',
        'enum34'
    ],
    tests_require=[
        'pytest',
        'pytest-cov'
    ],
    cmdclass = {'test': PyTest},
)
