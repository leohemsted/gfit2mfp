from setuptools import setup, find_packages

LONG_DESC = '''
Google Fit -> My Fitness Pal
============================

A script that pulls your google fit data and adds it to your myfitnesspal account
'''

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
    ],
    extras_require={
        'tests': [
            'coverage'
        ]
    },
    test_suite="tests",
)
