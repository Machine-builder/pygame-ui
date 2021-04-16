import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pygame-ui-mb",
    version="0.1.1",
    author="MACHINE_BUILDER",
    description="A package for fluid uis in PyGame",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Machine-builder/pygame-ui",
    project_urls={
        "Bug Tracker": "https://github.com/Machine-builder/pygame-ui/issues"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent"
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6"
)