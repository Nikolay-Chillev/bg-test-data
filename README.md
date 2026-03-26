# bg-test-data

[![PyPI version](https://img.shields.io/pypi/v/bg-test-data)](https://pypi.org/project/bg-test-data/)
[![Python versions](https://img.shields.io/pypi/pyversions/bg-test-data)](https://pypi.org/project/bg-test-data/)
[![CI](https://github.com/Nikolay-Chillev/bg-test-data/actions/workflows/ci.yml/badge.svg)](https://github.com/Nikolay-Chillev/bg-test-data/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Comprehensive Bulgarian test data generator with **valid checksums**. Generate realistic EGN (national ID), EIK (company ID), IBAN, names, addresses, phone numbers, persons, and companies -- all with mathematically correct check digits.

## Features

- **EGN** -- valid 10-digit personal identification numbers with correct checksum, gender, and birth date encoding
- **EIK/BULSTAT** -- valid 9- or 13-digit company identification numbers
- **IBAN** -- valid Bulgarian IBANs (BG prefix, real bank codes, correct mod-97 check digits)
- **Names** -- authentic Bulgarian first, middle, and last names in Cyrillic
- **Addresses** -- realistic Bulgarian addresses with city, street, and postal code
- **Phone numbers** -- Bulgarian mobile and landline numbers
- **Persons** -- complete person records combining EGN, name, address, phone, and IBAN
- **Companies** -- complete company records with EIK, name, address, phone, and IBAN
- **Reproducible** -- seed-based generation for deterministic test data
- **Zero dependencies** -- pure Python, nothing to install beyond the package itself
- **Export** -- built-in JSON and CSV serialization
- **CLI** -- command-line interface for quick data generation

## Installation

```bash
pip install bg-test-data
```

## Quick Start

### Python API

```python
from bg_test_data import BgTestData

bg = BgTestData(seed=42)

# Generate a complete person
person = bg.person()
# {
#   "first_name": "Георги", "middle_name": "Иванов", "last_name": "Петров",
#   "full_name": "Георги Иванов Петров",
#   "gender": "male", "birth_date": "1975-09-18",
#   "egn": "7524189245",
#   "phone": "+359 88 123 4567",
#   "email": "georgi.petrov@gmail.com",
#   "address": {"street": "Витоша", "number": "15", "city": "София",
#               "postal_code": "1000", "oblast": "София-град", "full_address": "..."}
# }

# Generate a company
company = bg.company()
# {
#   "name": "Технологии ООД", "eik": "831650349", "vat_number": "BG831650349",
#   "iban": "BG28UNCR70001522345678",
#   "address": {...}, "phone": "+359 32 654 321",
#   "manager": {<person dict>}
# }

# Generate individual data types
egn = bg.egn(gender="female")
eik = bg.eik(length=13)
iban = bg.iban()
phone = bg.phone(phone_type="mobile")
name = bg.name(gender="male")
address = bg.address()
```

### Batch Generation

```python
bg = BgTestData(seed=42)

persons = bg.persons(count=100)
companies = bg.companies(count=50)
```

### Export

```python
from bg_test_data import to_json, to_csv, to_csv_file

# JSON string
print(to_json(person))

# CSV string
print(to_csv(persons))

# Write CSV to file
to_csv_file(persons, "test_persons.csv")
```

### CLI

```bash
# Generate a person (JSON output)
bg-test-data person

# Generate 10 persons as CSV
bg-test-data -n 10 -f csv person

# Generate an EGN for a female
bg-test-data egn --gender female

# Generate a company with a 13-digit EIK
bg-test-data company --eik-length 13

# Generate with a fixed seed for reproducibility
bg-test-data --seed 42 person

# Generate an IBAN
bg-test-data iban

# Generate a phone number
bg-test-data phone --type mobile

# Generate a name
bg-test-data name --gender male

# Generate an address
bg-test-data address --city Sofia
```

## Data Types

| Type | Description | Example |
|------|-------------|---------|
| **EGN** | 10-digit personal ID with valid checksum | `7524189245` |
| **EIK** | 9- or 13-digit company ID with valid checksum | `831650349` |
| **IBAN** | Bulgarian IBAN with valid mod-97 check | `BG80BNBG96611020345678` |
| **Name** | First, middle, and last name in Cyrillic | `Георги Иванов Петров` |
| **Address** | City, street, postal code | `София, ул. Витоша 15, 1000` |
| **Phone** | Mobile or landline number | `+359 88 123 4567` |
| **Person** | Full person record (EGN + name + address + phone + IBAN) | see above |
| **Company** | Full company record (EIK + name + address + phone + IBAN) | see above |

## API Reference

### `BgTestData` class

| Method | Returns | Description |
|--------|---------|-------------|
| `egn(**kwargs)` | `str` | Generate a valid EGN. Options: `gender` |
| `eik(**kwargs)` | `str` | Generate a valid EIK. Options: `length` (9 or 13) |
| `iban(**kwargs)` | `str` | Generate a valid Bulgarian IBAN |
| `phone(**kwargs)` | `str` | Generate a phone number. Options: `phone_type` |
| `name(**kwargs)` | `dict` | Generate a name. Options: `gender` |
| `address(**kwargs)` | `dict` | Generate an address. Options: `city` |
| `person(**kwargs)` | `dict` | Generate a full person. Options: `gender`, `min_age`, `max_age` |
| `company(**kwargs)` | `dict` | Generate a full company. Options: `eik_length` |
| `persons(count, **kwargs)` | `list[dict]` | Generate multiple persons |
| `companies(count, **kwargs)` | `list[dict]` | Generate multiple companies |

### Validation

| Function | Description |
|----------|-------------|
| `validate_egn(egn)` | Returns `True` if the EGN has a valid checksum |
| `validate_eik(eik)` | Returns `True` if the EIK has a valid checksum |
| `validate_iban(iban)` | Returns `True` if the IBAN has a valid mod-97 check |
| `parse_egn(egn)` | Extract birth date, gender, and region from an EGN |

### Export

| Function | Description |
|----------|-------------|
| `to_json(data)` | Serialize to a JSON string |
| `to_csv(data)` | Serialize to a CSV string |
| `to_csv_file(data, path)` | Write CSV to a file |
| `to_dict(data)` | Identity normalizer (returns the same dict/list) |

## Development

```bash
# Clone the repository
git clone https://github.com/Nikolay-Chillev/bg-test-data.git
cd bg-test-data

# Install dev dependencies
make install

# Run tests
make test

# Run tests with coverage
make coverage

# Run linter
make lint

# Format code
make format

# Type checking
make typecheck
```

## Project Structure

```
bg-test-data/
  src/
    bg_test_data/
      __init__.py          # Public API exports
      providers.py         # BgTestData facade class
      egn.py               # EGN generator and validator
      eik.py               # EIK generator and validator
      iban.py              # IBAN generator and validator
      names.py             # Bulgarian name generator
      address.py           # Address generator
      phone.py             # Phone number generator
      person.py            # Person record generator
      company.py           # Company record generator
      export.py            # JSON/CSV export utilities
      cli.py               # Command-line interface
      _random.py           # Seeded random number generator
      _data/               # Static data files (names, cities, etc.)
  tests/                   # Test suite
  pyproject.toml           # Project metadata and tool config
  Makefile                 # Development shortcuts
  LICENSE                  # MIT License
```

## License

MIT License. See [LICENSE](LICENSE) for details.
