from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="jotts",
    version="0.3",
	license="MIT",
    author="Jonas Freiknecht",
    author_email="j.freiknecht@googlemail.com",
    description="JoTTS is a German text-to-speech engine.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/padmalcom/jotts",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
		"Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
		"Programming Language :: Python :: 3.6",
		"Programming Language :: Python :: 3.7",
		"Programming Language :: Python :: 3.8",
		"Programming Language :: Python :: 3.9",
		"Programming Language :: Python :: 3.10"
    ],
    python_requires='>=3.6',
)