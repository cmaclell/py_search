import setuptools

setuptools.setup(
    name='py_search',
    version='0.2.0',
    author='Christopher J. MacLellan',
    author_email='maclellan.christopher@gmail.com',
    packages=setuptools.find_packages(),
    include_package_data = True,
    url='http://pypi.python.org/pypi/py_search/',
    license='LICENSE.txt',
    description='A library of uninformed and heuristic search/optimization algorithms.',
    long_description=open('README.rst').read(),
    install_requires=['tabulate', 'blist'],
)
