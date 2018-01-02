from setuptools import find_packages, setup

with open('reqs.in') as f:
    reqs = f.read().splitlines()

with open('reqs-test.in') as f:
    reqs_test = f.read().splitlines()

setup(
    name='gr4-songinator',
    version='0.1.0',
    url='https://github.com/gr4viton/songinator',
    author='gr4viton',
    author_email='lordmutty@gmail.com',
    packages=find_packages(),
    install_requires=reqs,
    tests_require=reqs_test,
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
)
