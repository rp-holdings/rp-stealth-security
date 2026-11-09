from setuptools import setup, find_packages

setup(
    name="rp-stealth-security",
    version="9.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.110.0",
        "uvicorn[standard]>=0.28.0",
        "stripe>=11.0.0",
        "cryptography>=42.0.0",
        "pydantic>=2.6.0",
    ],
    author="RP LLC",
    author_email="support@rp-sec.com",
    description="RP Stealth Security V9 Suite",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
