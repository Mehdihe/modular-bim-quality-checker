
import csv

from bim_checker.checker import check_components


def test_duplicate_component_id(tmp_path):

    input_file = tmp_path / "components.csv"

    rows = [
        {
            "component_id": "ST-001",
            "discipline": "Structure",
            "component_type": "Beam",
            "material": "Steel",
            "length": "9000",
            "width": "200",
            "height": "300",
            "unit": "mm",
        },
        {
            "component_id": "ST-001",
            "discipline": "Structure",
            "component_type": "Beam",
            "material": "Steel",
            "length": "6000",
            "width": "200",
            "height": "300",
            "unit": "mm",
        },
    ]

    with open(input_file, "w", newline="") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=rows[0].keys(),
        )

        writer.writeheader()
        writer.writerows(rows)

    issues = check_components(input_file)

    assert any(
        issue["issue"] == "Duplicate component ID"
        for issue in issues
    )
