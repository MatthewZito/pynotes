import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pynotes_MatthewZito", 
    version="0.0.1",
    author="Matthew Zito (goldmund)",
    author_email="matthewtzito@gmail.com",
    description="A light command-line utility for keeping and editing notes - from anywhere in the shell.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MatthewZito/py_notes",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)