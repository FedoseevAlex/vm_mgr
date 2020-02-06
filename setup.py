from setuptools import setup, find_packages


def get_readme() -> str:
    """
    This function returns contents of README.md file in the repository.

    :return: File contents as string
    """
    with open("README.md") as readme:
        contents = readme.read()
    return contents


setup(
    name="vm_mgr",
    version="0.0.1",
    author="Fedoseev Aleksander",
    author_email="fedoseevalex@inbox.ru",
    description="Virtual machine manager",
    long_description=get_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/FedoseevAlex/vm_mgr",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.6",
)
