from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="year365win",
    version="1.0.0",
    author="大河马",
    author_email="your.email@example.com",
    description="爱国键盘侠个性化信息茧房系统",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/365win",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Communications",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "365win=src.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "year365win": ["config/*.yaml", "config/*.json"],
    },
)