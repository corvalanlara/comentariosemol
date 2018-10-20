from setuptools import setup, find_packages

def extras():
    import sys
    return ['unicodecsv'] if sys.version_info < (3,) else []

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = "comentariosemol",
    version = "0.1.1",
    author = "Daniel Corvalán",
    author_email = "corvalanlara@protonmail.com",
    description = "Extrae los comentarios de las noticias de EMOL en formato csv",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/corvalanlara/comentariosemol",
    packages = find_packages(),
    license = 'GPLv3',
    entry_points = {
        'console_scripts':[
            'comentariosemol = comentariosemol.comentariosemol:main'
        ]
    },
    install_requires = ['beautifulsoup4', 'selenium'] + extras(),
    include_package_data = True,
    package_data = {
        'facebookreport' : ['cuentas.fbr'],
    },
    classifiers = (
        "Environment :: Console",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Topic :: Documentation",
    ),
)
