"""bg-test-data: Comprehensive Bulgarian test data generator with valid checksums."""

__version__ = "0.1.0"

from bg_test_data.address import generate_address
from bg_test_data.company import generate_company
from bg_test_data.egn import generate_egn, parse_egn, validate_egn
from bg_test_data.eik import generate_eik, validate_eik
from bg_test_data.export import to_csv, to_csv_file, to_dict, to_json
from bg_test_data.iban import format_iban, generate_iban, validate_iban
from bg_test_data.names import generate_name
from bg_test_data.person import generate_person
from bg_test_data.phone import generate_phone
from bg_test_data.providers import BgTestData

__all__ = [
    "__version__",
    "BgTestData",
    "generate_address",
    "generate_company",
    "generate_egn",
    "generate_eik",
    "generate_iban",
    "generate_name",
    "generate_person",
    "generate_phone",
    "format_iban",
    "parse_egn",
    "validate_egn",
    "validate_eik",
    "validate_iban",
    "to_csv",
    "to_csv_file",
    "to_dict",
    "to_json",
]
