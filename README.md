# casbin-python-cli

![PyPI - Python Version](https://img.shields.io/badge/python-3.6%2B-blue)
![PyPI - License](https://img.shields.io/badge/license-Apache%202.0-green)
![PyPI - PyCasbin Version](https://img.shields.io/badge/pycasbin-1.17.0%2B-orange)

## Features

- **casbin-editor Integration**: Full API compatibility with casbin-editor for multi-language backend support
- **Unified JSON Response Format**: Standardized `{"allow": boolean|null, "explain": array|null}` response format
- **Method Name Mapping**: Automatic conversion between Java-style command names and Python method names
- **Comprehensive API Coverage**: Support for policy execution, management, RBAC operations, and data retrieval
- **Cross-platform Binaries**: Automated builds for Windows, macOS, and Linux
- **Dynamic Command Execution**: Reflection-based method invocation similar to Java version

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

## Usage

### Basic Command Structure

```bash
python -m casbin_cli.client [command] [options] [args]
```

### Examples

**Policy Execution**:
```bash
# Basic enforcement
python -m casbin_cli.client enforce -m "examples/rbac_model.conf" -p "examples/rbac_policy.csv" "alice" "data1" "read"
{"allow":true,"explain":null}

# Enforcement with explanation
python -m casbin_cli.client enforceEx -m "examples/rbac_model.conf" -p "examples/rbac_policy.csv" "alice" "data1" "read"
{"allow":true,"explain":["alice","data1","read"]}
```

**Policy Management**:
```bash
# Add policy
python -m casbin_cli.client addPolicy -m "examples/rbac_model.conf" -p "examples/rbac_policy.csv" "eve" "data3" "read"
{"allow":true,"explain":null}

# Get all policies
python -m casbin_cli.client getPolicy -m "examples/rbac_model.conf" -p "examples/rbac_policy.csv"
{"allow":null,"explain":[["alice","data1","read"],["bob","data2","write"]]}
```

**RBAC Operations**:
```bash
# Get user roles
python -m casbin_cli.client getRolesForUser -m "examples/rbac_model.conf" -p "examples/rbac_policy.csv" "alice"
{"allow":null,"explain":["data2_admin"]}

# Get role users
python -m casbin_cli.client getUsersForRole -m "examples/rbac_model.conf" -p "examples/rbac_policy.csv" "data2_admin"
{"allow":null,"explain":["alice"]}
```

**Data Retrieval**:
```bash
# Get all subjects
python -m casbin_cli.client getAllSubjects -m "examples/rbac_model.conf" -p "examples/rbac_policy.csv"
{"allow":null,"explain":["alice","bob","data2_admin"]}

# Get all objects
python -m casbin_cli.client getAllObjects -m "examples/rbac_model.conf" -p "examples/rbac_policy.csv"
{"allow":null,"explain":["data1","data2"]}
```

### API Compatibility

The Python CLI maintains full compatibility with the Java version through:

- **Command Interface**: Identical command-line arguments (`-m`, `-p`, etc.)
- **Method Name Mapping**: Automatic conversion from Java camelCase to Python snake_case
- **Response Format**: Standardized JSON responses matching Java implementation
- **Error Handling**: Consistent error reporting across all backends

### Supported APIs

| Category              | Commands                                                     | Status |
| --------------------- | ------------------------------------------------------------ | ------ |
| **Policy Execution**  | `enforce`, `enforceEx`, `enforceWithMatcher`                 | ✅      |
| **Policy Management** | `addPolicy`, `removePolicy`, `getPolicy`, `hasPolicy`        | ✅      |
| **RBAC Operations**   | `getRolesForUser`, `getUsersForRole`, `hasRoleForUser`       | ✅      |
| **Data Retrieval**    | `getAllSubjects`, `getAllObjects`, `getAllActions`           | ✅      |
| **Grouping Policies** | `getGroupingPolicy`, `addGroupingPolicy`, `removeGroupingPolicy` | ✅      |
| **Named Policies**    | `getNamedPolicy`, `getAllNamedRoles`                         | ✅      |
| **Filtered Queries**  | `getFilteredPolicy`, `getFilteredGroupingPolicy`             | ✅      |

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
│   ├── __version__.py            # Version information
│   ├── client.py                 # Main CLI entry point & argument parsing
│   ├── command_executor.py       # Dynamic command execution & method mapping
│   ├── enforcer_factory.py       # PyCasbin enforcer creation
│   ├── response.py               # Standardized JSON response formatting
│   └── utils.py                  # Utility functions
├── examples/                     # Example model and policy files
│   ├── rbac_model.conf          # RBAC model configuration
│   ├── rbac_policy.csv          # RBAC policy data
│   ├── basic_model.conf         # Basic model configuration
│   └── basic_policy.csv         # Basic policy data
├── tests/                       # Test files (if any)
├── .releaserc.json              # Semantic release configuration
├── package.json                 # Node.js dependencies for release automation
├── requirements.txt             # Python dependencies
├── setup.py                     # Package setup and distribution
└── README.md                    # This file
```

## Requirements

- Python 3.6+
- PyCasbin 1.17.0+

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

---

**Note**: This Python CLI is part of the Casbin ecosystem and designed to work seamlessly with casbin-editor for multi-language backend support. For more information about Casbin, visit [casbin.org](https://casbin.org).
