
import csv
import argparse
from pathlib import Path


REQUIRED_FIELDS = [
    "component_id",
    "discipline",
    "component_type",
    "material",
    "length",
    "width",
    "height",
    "unit",
]

VALID_DISCIPLINES = {
    "Architecture",
    "Structure",
    "Mechanical",
}

VALID_UNITS = {
    "mm",
    "cm",
    "m",
    "in",
    "ft",
}


def check_components(input_file):
    """
    Validate BIM component data exported to CSV.

    This tool checks data completeness and consistency.
    It does not perform structural engineering calculations.
    """

    issues = []
    seen_ids = set()

    with open(input_file, newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames:
            raise ValueError("The CSV file is empty.")

        missing_columns = [
            field for field in REQUIRED_FIELDS
            if field not in reader.fieldnames
        ]

        if missing_columns:
            raise ValueError(
                f"Missing required columns: {missing_columns}"
            )

        for row_number, row in enumerate(reader, start=2):

            component_id = row["component_id"].strip()

            # Missing component ID
            if not component_id:
                issues.append({
                    "row": row_number,
                    "component_id": "",
                    "severity": "ERROR",
                    "issue": "Missing component ID",
                })

            # Duplicate component ID
            elif component_id in seen_ids:
                issues.append({
                    "row": row_number,
                    "component_id": component_id,
                    "severity": "ERROR",
                    "issue": "Duplicate component ID",
                })

            else:
                seen_ids.add(component_id)

            # Missing required information
            for field in REQUIRED_FIELDS:
                if not row[field].strip():
                    issues.append({
                        "row": row_number,
                        "component_id": component_id,
                        "severity": "ERROR",
                        "issue": f"Missing value: {field}",
                    })

            # Discipline validation
            discipline = row["discipline"].strip()

            if discipline and discipline not in VALID_DISCIPLINES:
                issues.append({
                    "row": row_number,
                    "component_id": component_id,
                    "severity": "WARNING",
                    "issue": f"Unknown discipline: {discipline}",
                })

            # Unit validation
            unit = row["unit"].strip()

            if unit and unit not in VALID_UNITS:
                issues.append({
                    "row": row_number,
                    "component_id": component_id,
                    "severity": "ERROR",
                    "issue": f"Unsupported unit: {unit}",
                })

            # Dimension validation
            for dimension in ["length", "width", "height"]:

                value = row[dimension].strip()

                if not value:
                    continue

                try:
                    numeric_value = float(value)

                    if numeric_value <= 0:
                        issues.append({
                            "row": row_number,
                            "component_id": component_id,
                            "severity": "ERROR",
                            "issue": (
                                f"Invalid {dimension}: "
                                f"{numeric_value}"
                            ),
                        })

                except ValueError:
                    issues.append({
                        "row": row_number,
                        "component_id": component_id,
                        "severity": "ERROR",
                        "issue": f"Non-numeric dimension: {dimension}",
                    })

    return issues


def export_report(issues, output_file):

    fieldnames = [
        "row",
        "component_id",
        "severity",
        "issue",
    ]

    with open(
        output_file,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(issues)


def main():

    parser = argparse.ArgumentParser(
        description="Modular BIM Quality Checker"
    )

    parser.add_argument(
        "input",
        help="Path to BIM component CSV file",
    )

    parser.add_argument(
        "--output",
        default="quality_report.csv",
        help="Output report filename",
    )

    args = parser.parse_args()

    issues = check_components(args.input)

    export_report(issues, args.output)

    print("BIM quality check completed.")
    print(f"Total issues found: {len(issues)}")
    print(f"Report saved to: {args.output}")


if __name__ == "__main__":
    main()

