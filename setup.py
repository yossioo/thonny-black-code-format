import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="thonny-black-format",
    version="0.0.1",
    author="Franccisco",
    description="A plugin to format your python code with Black in Thonny IDE.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Franccisco/thonny-black-code-format",
    packages=["thonnycontrib.thonny-black-format"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
