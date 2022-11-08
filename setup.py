from setuptools import setup
import eksitui.__main__ as m

with open("README.md", "r", encoding="UTF8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as file:
    requires = [line.strip() for line in file.readlines()]

VERSION = m.__version__
DESCRIPTION = "eksi sozluk terminal user interface."

setup(
    name="eksitui",
    version=VERSION,
    url="https://github.com/agmmnn/eksitui",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="agmmnn",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Environment :: Console",
        "Topic :: Utilities",
    ],
    packages=["eksitui"],
    data_files=[("eksitui", ["eksitui/main.css"])],
    install_requires=requires,
    include_package_data=True,
    package_data={"eksitui": ["eksitui/*"]},
    python_requires=">=3.7",
    entry_points={"console_scripts": ["eksi = eksitui.__main__:cli"]},
)
