from setuptools import setup, find_packages

setup(
    name="clinica_plugin",
    version="0.1.0",
    description="Plugin de criptografia e banco de dados para sistemas locais",
    author="Seu Nome",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "cryptography",  # dependências
        "flask"
    ],
    entry_points={},
)