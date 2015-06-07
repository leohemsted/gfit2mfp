from setuptools import setup, find_packages
setup(
    name = 'gfit2mfp',
    version='0.1',
    description='Google Fit -> My Fitness Pal',
    author='Leo Hemsted',
    author_email='leohemsted@gmail.com',
    url='https://github.com/leohemsted/gfit2mfp/',
    packages = find_packages(),
    install_requires=[
        'requests>=2.7.0',
        'google-api-python-client>=1.4.0',
        'oauth2client>=1.4.6',
        'httplib2>=0.9.1',
    ]
)
