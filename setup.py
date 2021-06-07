import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="swag_auth",
    version="0.0.1",
    author="Likalo Limited",
    author_email="hello@docsie.io",
    description="This is an open source implementation of swag-auth",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LikaloLLC/django-swag-auth",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    package_dir={"": "swag_auth"},
    packages=setuptools.find_packages(where="swag_auth"),
    python_requires=">=3.5, <4",
    install_requires=[
        "django==2.2.2",
        "django-allauth==0.44.0",
        "django-rest-auth==0.9.5",
        "requests>=2.0.0,<2.22.0",
        "django-encrypted-model-fields~=0.5.8",
        "PyGithub~=1.55",
        "djangorestframework >=3.8.0, <3.12.5",
        "PyYAML>=5.0.0,<5.4.2",
        "python-gitlab>=2.0.1,<2.7.2",
        "bitbucket-api>=0.5.0, <1.0.0",
        "atlassian-python-api>=3.10.0, <3.11.0",
        "django-environ~=0.4.5",
    ],
    include_package_data=True,
)
