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
├── casbin_cli/
│   ├── __init__.py
│   ├── client.py          # Main entry point and CLI argument parsing
│   ├── command_executor.py # Dynamic method execution and JSON response
│   ├── enforcer_factory.py # Enforcer creation and input validation
│   ├── response.py        # JSON response formatting
│   └── utils.py           # Utility functions
├── examples/              # Example configuration files
├── requirements.txt       # Python dependencies
├── setup.py               # Package installation script
└── README.md
```

## Requirements

- Python 3.6+
- PyCasbin 1.17.0+

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.