from setuptools import setup,find_packages
import os



def requirement():
    lis_module  = []
    with open('requirements.txt') as f:
        lines : list = f.readlines()

        for i in lines:
            module = i.strip()

            if module and module != '-e .':
                lis_module.append(module)
    return lis_module


setup(
    name='youtube_project',
    version='1.0',
    packages=find_packages(),
    install_requires=requirement(),
    include_package_data=True,
    author='Aman Kumar Choudhary'
)
    