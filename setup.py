from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="jotts",
    version="1.0.4",
	license="MIT",
    author="Jonas Freiknecht",
    author_email="j.freiknecht@googlemail.com",
    description="JoTTS is a German text-to-speech engine.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/padmalcom/jotts",
    packages=find_packages(exclude=("tests", "requirements.txt",)),
	include_package_data=True,
	install_requires=[
		"appdirs==1.4.4",
		"audioread==3.0.0",
		"certifi==2021.10.8",
		"cffi==1.15.0",
		"charset-normalizer==2.1.1",
		"colorama==0.4.6",
		"contourpy==1.0.6",
		"cycler==0.11.0",
		"decorator==5.1.1",
		"fonttools==4.38.0",
		"idna==3.4",
		"inflect==6.0.2",
		"joblib==1.2.0",
		"kiwisolver==1.4.4",
		"librosa==0.9.2",
		"llvmlite==0.39.1",
		"loguru==0.6.0",
		"matplotlib==3.6.2",
		"numba==0.56.4",
		"numpy==1.23.4",
		"packaging==21.3",
		"Pillow==9.3.0",
		"pooch==1.6.0",
		"pycparser==2.21",
		"pydantic==1.10.2",
		"pyparsing==3.0.9",
		"python-dateutil==2.8.2",
		"requests==2.28.1",
		"resampy==0.4.2",
		"scikit-learn==1.1.3",
		"scipy==1.9.3",
		"six==1.16.0",
		"sounddevice==0.4.5",
		"soundfile==0.11.0",
		"threadpoolctl==3.1.0",
		"torch==1.10.0",
		"tqdm==4.64.1",
		"typing_extensions==4.4.0",
		"Unidecode==1.3.6",
		"urllib3==1.26.12"
	],
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