from setuptools import find_packages, setup

setup(
    name='AppiumTestManager',
    version='0.1.1',
    url='https://github.com/jwgit3514/AppiumTestManager',
    install_requires=[
        'streamlit',
        'pytest',
        'pytest-xdist',
        'selenium',
        'Appium-Python-Client',
    ],
    packages=find_packages(),
    python_requires='>=3.11',
    classifiers='Programming Language || Python || 3.11'
)
