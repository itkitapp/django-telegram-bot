from setuptools import setup
from os.path import dirname, join

try:
    with open(join(dirname(__file__), 'README.md')) as f:
        README = f.read()
except IOError:
    README = '<no description>'

install_requires = ['requests']

try:
    import importlib
except ImportError:
    install_requires.append('importlib')


setup(
    name='kitappbot',
    version='0.0.18',
    description='KitApp bots app',
    long_description=README,
    url='https://git.kit-app.ru/integrationslibs/kitapp-django-bot',
    author='Kit App LLC',
    author_email='it@kit-app.ru',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    license='MIT',
    install_requires=install_requires,
    packages=['kitappbot'],
)
