from setuptools import setup, find_packages

setup(
    name="TinyPacketFabricFramework",
    version="1.0.0",
    description='Tiny testing framework',
    author="WhoAmI",
    packages=find_packages(),
    install_requires=[
        "mock==3.0.5",
        "Pyyaml==5.3.1",
        "pytest==3.1.0",
        "requests==2.22.0"]
)
