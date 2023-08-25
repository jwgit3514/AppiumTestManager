from setuptools import find_packages, setup

setup(
    name='AppiumTestManager',
    version='0.1.1',
    url='https://github.com/jwgit3514/AppiumTestManager',
    install_requires=[
        'streamlit',
        'pytest',
        'pytest-xdist',
        'tk',
        'customtkinter',
        'selenium',
        'Appium-Python-Client',
        'python-tkdnd',
        'tkinterdnd2',
    ],
    packages=find_packages(where='src'),
    python_requires='>=3.11',
    classifiers='Programming Language || Python || 3.11'
)
