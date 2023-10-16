from setuptools import setup, find_packages

setup(
    name='Siena-MES',
    version='18',
    packages=find_packages(),
    install_requires=[
        'Pillow',
        'scipy',
        'numpy',
        'resizeimage',
        'pi_heif'
    ],
    author='Robin Flatland and Ninad Chaudhari @Siena College',
    author_email='nchaudhari@siena.edu',
    description='Multimedia Environment for Students',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown'
)