from setuptools import setup, find_packages

setup(
    name='TwitterScraper',
    version='0.1',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='Acquiring data from Twitter',
    long_description=open('README.md').read(),
    install_requires=['numpy','pandas','tweepy'],
    url='https://github.com/KeletsoM/TwitterScraper',
    author='<Keletso Maleka>',
    author_email='<u14062552@tuks.co.za>'
)