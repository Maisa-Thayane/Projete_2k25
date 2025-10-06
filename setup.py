from setuptools import setup, find_packages

setup(
    name="Antlion_plugin",
    version="0.1.0",
    description="Plugin de criptografia e banco de dados para sistemas locais",
    author="Antlion",
    packages=find_packages(include=["Antlion_plugin", "Antlion_plugin.*"]),
    include_package_data=True,
    install_requires=[
        "cryptography",
        "Flask",
        "flask-cors",
        "flask-mail",
        "requests",
        "eciespy",
    ],
    python_requires=">=3.9",
)