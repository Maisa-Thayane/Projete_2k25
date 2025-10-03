from setuptools import setup, find_packages

setup(
    name="clinica_plugin",
    version="0.1.0",
    description="Plugin de criptografia e banco de dados para sistemas locais",
    author="Antlion",
    packages=find_packages(include=["clinica_plugin", "clinica_plugin.*"]),
    include_package_data=True,
    install_requires=[
        "cryptography",
        "Flask",
        "flask-cors",
        "flask-mail",
        "requests",
    ],
    python_requires=">=3.9",
)