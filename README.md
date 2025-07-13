# casbin-python-cli

![PyPI - Python Version](https://img.shields.io/badge/python-3.6%2B-blue)
![PyPI - License](https://img.shields.io/badge/license-Apache%202.0-green)
![PyPI - PyCasbin Version](https://img.shields.io/badge/pycasbin-1.17.0%2B-orange)

## Installation

### Prerequisites
- Python 3.6+
- pip package manager

### Installation Methods

**Clone from repository**:

```bash
git clone https://github.com/casbin/casbin-python-cli.git
cd casbin-python-cli
pip install -r requirements.txt
```

### Method

```bash
python -m casbin_cli.client [command] [options] [args]

python -m casbin_cli.client enforce -m "examples/rbac_model.conf" -p "examples/rbac_policy.csv" "alice" "data1" "read"

{"allow":true,"explain":null}
```

## Project Structure

```
casbin-python-cli/  
├── .github/  
│   └── workflows/  
│       └── release.yml           # GitHub Actions CI/CD  
├── scripts/  
│   ├── update_version.py         # Version management  
│   └── build_binaries.py         # Binary building  
├── casbin_cli/  
│   ├── __init__.py  
│   ├── __version__.py            # Version source  
│   ├── client.py                 # Main CLI entry point  
│   ├── command_executor.py       # Command execution  
│   ├── enforcer_factory.py       # Enforcer creation  
│   ├── response.py               # Response formatting  
│   └── utils.py                  # Utilities  
├── examples/                     # Example configurations  
├── .releaserc.json              # Semantic release config  
├── package.json                 # Node.js dependencies  
├── requirements.txt             # Python dependencies  
├── setup.py                     # Package setup  
└── README.md  
```

### Release Process

Releases are automated via GitHub Actions:

1. Push commits to `main` branch
2. Semantic release analyzes commit messages
3. Automatically generates version numbers and changelog
4. Builds cross-platform binaries
5. Publishes to PyPI and GitHub Releases

## Requirements

- Python 3.6+
- PyCasbin 1.17.0+

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.