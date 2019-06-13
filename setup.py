import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="atihelper",
    version="0.0.1",
    author="Philipp Jaeckle",
    author_email="p.a.jaeckle@gmail.com",
    description="Python helper class to easily fetch data from AT Internet RESTful API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/datapip/atihelper",
    packages=setuptools.find_packages(),
    install_requires=['requests'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
