from setuptools import setup, find_packages  
  
setup(  
    name="casbin-python-cli",  
    version="1.0.0",  
    description="A command-line tool for PyCasbin",  
    packages=find_packages(),  
    install_requires=[  
        "casbin>=1.17.0",  
    ],  
    entry_points={  
        'console_scripts': [  
            'casbin-cli=casbin_cli.client:main',  
        ],  
    },  
    python_requires='>=3.6',  
)