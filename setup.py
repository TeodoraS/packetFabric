from setuptools import setup, find_packages

setup(
    name="TinyPacketFabricFramework",
    version="1.0.0",
    description='Tiny testing framework',
    author="WhoAmI",
    packages=find_packages(),
    install_requires=[
        "mock==3.0.5",
        "Pyyaml==5.4",
        "pytest==5.4.1",
        "requests==2.22.0"]
)
