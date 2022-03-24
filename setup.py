from distutils.core import setup

setup(
    name="segments-ai",  # How you named your package folder (MyLib)
    package_dir={"": "src"},
    packages=["segments"],  # Chose the same as "name"
    version="0.58",  # Start with a small number and increase it with every change you make
    license="MIT",  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description="",  # Give a short description about your library
    author="Segments.ai",  # Type in your name
    author_email="bert@segments.ai",  # Type in your E-Mail
    url="https://github.com/segments-ai/segments-ai",  # Provide either the link to your github or to your website
    download_url="https://github.com/segments-ai/segments-ai/archive/v0.58.tar.gz",
    keywords=[
        "image",
        "segmentation",
        "labeling",
        "vision",
    ],  # Keywords that define your package best
    install_requires=[
        "numpy",
        "requests",
        "Pillow",
        "scikit-image",
        "tqdm",
        'pycocotools;platform_system!="Windows"',
        'pycocotools-windows;platform_system=="Windows"',
        # Type hints
        "typing_extensions",
        # "dataclasses",
        "typing",
        "enum",
        "mypy",
        "pydantic",
        # Tests
        # "dotenv",
        # Documentation
        "sphinx",
        # "myst-parser",
        "furo",
        # "sphinx-book-theme",
        # "nbsphinx",
        # "pandoc",
        "sphinx-autoapi",
    ],
    python_requires=">=3.6.0",
    classifiers=[
        "Development Status :: 3 - Alpha",  # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        "Intended Audience :: Developers",  # Define that your audience are developers
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",  # Again, pick a license
        "Programming Language :: Python :: 3",  # Specify which python versions that you want to support
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
