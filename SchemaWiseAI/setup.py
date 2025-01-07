from setuptools import setup, find_packages

setup(
    name="schemawiseAI",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'pyyaml>=6.0',
        'requests>=2.28.0',
        'python-dotenv>=0.19.0',
    ],
    author="Your Name",
    description="Schema-aware middleware for LLM query adaptation",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/SchemaWiseAI",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
