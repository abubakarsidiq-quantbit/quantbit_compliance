from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in quantbit_compliance/__init__.py
from quantbit_compliance import __version__ as version

setup(
	name="quantbit_compliance",
	version=version,
	description="quantbit_compliance",
	author="abub.patel@erpdata.in",
	author_email="abub.patel@erpdata.in",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
