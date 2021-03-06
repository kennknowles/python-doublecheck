import setuptools 
import os.path
import datetime

setuptools.setup(   
    name = "doublecheck",
    version = "0.1pre" + datetime.datetime.utcnow().replace(microsecond=0).isoformat(),
    url = "https://github.com/kennknowles/python-doublecheck",
    maintainer = "Kenn Knowles",
    maintainer_email = "kenn.knowles@gmail.com",
    license = 'Apache 2.0',
    packages = setuptools.find_packages(),
    description = "Pythonic library for QuickCheck-style randomized testing and SmallCheck-style exhaustive testing of the same test suite.",
    long_description = open(os.path.join(os.path.dirname(__file__), 'README')).read(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Software Development :: Testing",
        "License :: OSI Approved :: Apache Software License",
    ],
)
