import csv
import re
from dataclasses import dataclass
from pathlib import Path


SUPPORTED_TYPES = {
    "Bool",
    "Int",
    "DInt",
    "Real",
    "String",
    "Time",
}


TAG_NAME_PATTERN = re.compile(r"^[A-Z][A-Za-z0-9_]*$")


@dataclass
class ValidationIssue:
    row: int
    field: str
    severity: str
    message: str


def read_tags(csv_path: str | Path) -> list[dict[str, str]]:
    """Read PLC/HMI/SCADA tags from a CSV file."""
    path = Path(csv_path)

    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")

    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        return list(reader)


def validate_tags(tags: list[dict[str, str]]) -> list[ValidationIssue]:
    """Validate tag list and return detected issues."""
    issues: list[ValidationIssue] = []

    seen_names: dict[str, int] = {}
    seen_addresses: dict[str, int] = {}

    for index, tag in enumerate(tags, start=2):
        name = (tag.get("name") or "").strip()
        data_type = (tag.get("type") or "").strip()
        address = (tag.get("address") or "").strip()
        description = (tag.get("description") or "").strip()

        if not name:
            issues.append(
                ValidationIssue(
                    row=index,
                    field="name",
                    severity="error",
                    message="Tag name is missing.",
                )
            )
        elif not TAG_NAME_PATTERN.match(name):
            issues.append(
                ValidationIssue(
                    row=index,
                    field="name",
                    severity="warning",
                    message="Tag name does not match the recommended naming convention.",
                )
            )

        if name:
            if name in seen_names:
                issues.append(
                    ValidationIssue(
                        row=index,
                        field="name",
                        severity="error",
                        message=f"Duplicated tag name. First occurrence is on row {seen_names[name]}.",
                    )
                )
            else:
                seen_names[name] = index

        if not data_type:
            issues.append(
                ValidationIssue(
                    row=index,
                    field="type",
                    severity="error",
                    message="Data type is missing.",
                )
            )
        elif data_type not in SUPPORTED_TYPES:
            issues.append(
                ValidationIssue(
                    row=index,
                    field="type",
                    severity="error",
                    message=f"Unsupported data type: {data_type}.",
                )
            )

        if address:
            if address in seen_addresses:
                issues.append(
                    ValidationIssue(
                        row=index,
                        field="address",
                        severity="warning",
                        message=f"Duplicated address. First occurrence is on row {seen_addresses[address]}.",
                    )
                )
            else:
                seen_addresses[address] = index

        if not description:
            issues.append(
                ValidationIssue(
                    row=index,
                    field="description",
                    severity="warning",
                    message="Description is missing.",
                )
            )
        elif len(description) < 10:
            issues.append(
                ValidationIssue(
                    row=index,
                    field="description",
                    severity="warning",
                    message="Description is suspiciously short.",
                )
            )

    return issues
