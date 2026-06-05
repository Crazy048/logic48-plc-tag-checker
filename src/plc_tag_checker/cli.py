import argparse
from pathlib import Path

from plc_tag_checker.checker import read_tags, validate_tags
from plc_tag_checker.report import build_markdown_report


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate PLC/HMI/SCADA tag lists."
    )

    parser.add_argument(
        "csv_file",
        help="Path to the CSV tag list.",
    )

    parser.add_argument(
        "--report",
        default="tag_validation_report.md",
        help="Path to the output Markdown report.",
    )

    args = parser.parse_args()

    tags = read_tags(args.csv_file)
    issues = validate_tags(tags)
    report = build_markdown_report(issues)

    report_path = Path(args.report)
    report_path.write_text(report, encoding="utf-8")

    print(f"Checked tags: {len(tags)}")
    print(f"Issues found: {len(issues)}")
    print(f"Report written to: {report_path}")

    return 1 if any(issue.severity == "error" for issue in issues) else 0


if __name__ == "__main__":
    raise SystemExit(main())
