import pathlib
from setuptools import setup, find_packages

with open('README.md') as readme:
    README = readme.read()

setup(
    name='django-stash-tag',
    version='19.3.0',
    description='A Django Template Tag that stashes content for dynamic reuse.',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/l4nk332/django-stash-tag',
    author='Ian Jabour',
    author_email='l4nk332@gmail.com',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='django, templatetag, template, tag, stash, dynamic',
    packages=find_packages(),
    install_requires=['django>=1.11']
)
