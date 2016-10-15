import setuptools

setuptools.setup(
    name='py_search',
    version='1.0.4',
    author='Christopher J. MacLellan',
    author_email='maclellan.christopher@gmail.com',
    packages=setuptools.find_packages(),
    include_package_data = True,
    url='http://pypi.python.org/pypi/py_search/',
    license='LICENSE.txt',
    description='A library of uninformed, informed, and optimization search algorithms',
    long_description=open('README.rst').read(),
    install_requires=['tabulate', 'blist', 'munkres'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
