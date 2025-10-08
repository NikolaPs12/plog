from setuptools import setup, find_packages

setup(
    name="your-flask-app",
    version="1.0.0",  # явно указанная версия
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "flask",
        "flask-sqlalchemy",
        "flask-login", 
        "flask-mail",
        "flask-wtf",
        "pillow",
        "wtforms"
    ],
)