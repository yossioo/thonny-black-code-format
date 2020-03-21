import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="thonny-black-format",
    version="0.0.2",
    author="Franccisco",
    description="A plugin to format your python code with Black in Thonny IDE.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Franccisco/thonny-black-code-format",
    packages=["thonnycontrib.thonny-black-format"],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["thonny >= 3.0.0", "black"],
    python_requires=">=3.7",
)
