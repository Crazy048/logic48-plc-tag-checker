from plc_tag_checker.checker import ValidationIssue


def build_markdown_report(issues: list[ValidationIssue]) -> str:
    """Build a Markdown report from validation issues."""
    lines: list[str] = []

    lines.append("# PLC Tag Validation Report")
    lines.append("")

    if not issues:
        lines.append("No validation issues found.")
        lines.append("")
        return "\n".join(lines)

    error_count = sum(1 for issue in issues if issue.severity == "error")
    warning_count = sum(1 for issue in issues if issue.severity == "warning")

    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Errors: {error_count}")
    lines.append(f"- Warnings: {warning_count}")
    lines.append(f"- Total issues: {len(issues)}")
    lines.append("")

    lines.append("## Issues")
    lines.append("")
    lines.append("| Row | Severity | Field | Message |")
    lines.append("|---:|---|---|---|")

    for issue in issues:
        lines.append(
            f"| {issue.row} | {issue.severity} | {issue.field} | {issue.message} |"
        )

    lines.append("")
    return "\n".join(lines)
