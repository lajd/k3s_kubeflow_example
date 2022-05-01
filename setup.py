import os
from setuptools import setup

__NAME__ = 'local-kubeflow'
__VERSION = '0.0.1'
__DESCRIPTION__ = 'Experiments with local kubeflow'
__AUTHOR__ = 'Jonathan La'


def get_requirements():
    with open(os.path.abspath('./requirements.txt'), 'r') as f:
        requirements = [i.strip() for i in f.readlines()]
    return requirements


setup(
    name=__NAME__,
    version_info=__VERSION,
    description=__DESCRIPTION__,
    author=__AUTHOR__,
    license='MIT',
    platforms=['any'],
    zip_safe=False,
    python_requires='>=3.9',
    include_package_data=True,
    install_requires=get_requirements(),
    package_data={},
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown'
)
