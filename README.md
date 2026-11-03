# Modular BIM Quality Checker

An open-source Python tool for validating BIM component data exported from Revit and other BIM software.

## Overview

Modular BIM Quality Checker identifies common data quality issues in modular construction models before engineering documentation, coordination, and fabrication.

The project aims to improve the consistency and reliability of BIM data through automated validation.

## Features

- Required field validation
- Duplicate component identification
- Dimension validation
- Unit consistency checks
- Discipline classification checks
- CSV quality report generation
- Automated software testing

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/modular-bim-quality-checker.git

cd modular-bim-quality-checker
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Export BIM component information to CSV using the required columns.

Run:

```bash
python -m bim_checker.checker examples/components.csv
```

Specify an output report:

```bash
python -m bim_checker.checker examples/components.csv --output report.csv
```

## Roadmap

- [ ] Revit parameter export integration
- [ ] IFC model data validation
- [ ] Cross-discipline component checking
- [ ] Configurable project standards
- [ ] HTML report generation
- [ ] Modular building coordination workflows

## Disclaimer

This software performs BIM data quality checks only. It does not perform structural analysis, verify code compliance, or replace professional engineering review.

## License

MIT License.
