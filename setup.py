import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="swag_auth",
    version="0.0.6",
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
    packages=setuptools.find_packages(),
    python_requires=">=3.5, <4",
    install_requires=[
        "django>=2.2.2",
        "django-allauth==0.44.0",
        "django-rest-auth==0.9.5",
        "requests",
        "django-encrypted-model-fields",
        "PyGithub",
        "djangorestframework",
        "PyYAML",
        "python-gitlab",
        "bitbucket-api",
        "atlassian-python-api",
        "django-environ",
        "giturlparse",
        "google-api-python-client",
        "google-auth-httplib2",
        "google-auth-oauthlib",
        "dropbox",
        "google-cloud-storage",
        'boxsdk',
    ],
    include_package_data=True,
    setup_requires=["wheel"]
)
