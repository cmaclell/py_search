import setuptools

setuptools.setup(
    name='py_search',
    version='1.3.0',
    author='Christopher J. MacLellan',
    author_email='maclellan.christopher@gmail.com',
    packages=setuptools.find_packages(),
    include_package_data=True,
    url='http://pypi.python.org/pypi/py_search/',
    license='LICENSE.txt',
    description=('A library of uninformed, informed, '
                 'and optimization search algorithms'),
    long_description=open('README.rst').read(),
    install_requires=['tabulate', 'munkres'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    classifiers=['Development Status :: 4 - Beta',
                 'Intended Audience :: Science/Research',
                 'Topic :: Scientific/Engineering :: Artificial Intelligence',
                 'License :: OSI Approved :: MIT License',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.6'],
)
