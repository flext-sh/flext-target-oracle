#!/usr/bin/env python3
"""Fix G004 and E116 violations in the codebase."""

import re
import sys
from pathlib import Path


def fix_g004_violations(content: str) -> str:
    """Fix G004 violations (f-strings in logging)."""
    lines = content.split("\n")
    modified = False

    for i, line in enumerate(lines):
        # Match logging statements with f-strings
        match = re.match(
            r'^(\s*)(log\.(debug|info|warning|error|critical))\(f["\'](.+)["\'](.*)$',
            line,
        )
        if match:
            indent = match.group(1)
            log_method = match.group(2)
            message = match.group(4)
            rest = match.group(5)

            # Extract variables from f-string
            # Find all {variable} patterns
            var_pattern = r"\{([^}]+)\}"
            variables = re.findall(var_pattern, message)

            if variables:
                # Replace {var} with %s in message
                new_message = re.sub(var_pattern, "%s", message)

                # Build new line with proper format
                if rest.strip() == ",":
                    # Simple case with no other args
                    new_line = (
                        f'{indent}{log_method}("{new_message}", {", ".join(variables)})'
                    )
                elif rest.strip() == "),":
                    # Has trailing comma and closing paren
                    new_line = (
                        f'{indent}{log_method}("{new_message}", {", ".join(variables)})'
                    )
                else:
                    # More complex case - preserve rest
                    new_line = f'{indent}{log_method}("{new_message}", {", ".join(variables)}{rest}'

                lines[i] = new_line
                modified = True

    return "\n".join(lines) if modified else content


def fix_e116_violations(content: str) -> str:
    """Fix E116 violations (unexpected indentation)."""
    lines = content.split("\n")
    modified = False

    for i, line in enumerate(lines):
        # Check if line is an improperly indented comment after a statement
        if i > 0 and line.strip().startswith("# "):
            prev_line = lines[i - 1]
            # If previous line ends with a continuation or is a statement
            if prev_line.strip() and not prev_line.strip().startswith("#"):
                # Check if comment is at wrong indentation (column 1)
                if len(line) - len(line.lstrip()) < 4:
                    # Get indentation of previous line
                    prev_indent = len(prev_line) - len(prev_line.lstrip())
                    # Add proper indentation (same as previous line)
                    lines[i] = " " * prev_indent + line.strip()
                    modified = True

    return "\n".join(lines) if modified else content


def process_file(file_path: Path) -> bool:
    """Process a single file to fix violations."""
    try:
        content = file_path.read_text()
        original_content = content

        # Fix G004 violations
        content = fix_g004_violations(content)

        # Fix E116 violations
        content = fix_e116_violations(content)

        if content != original_content:
            file_path.write_text(content)
            return True

        return False
    except Exception:
        return False


def main() -> int:
    """Main function."""
    files_to_fix = [
        "tests/helpers.py",
        "tests/test_bulk_operations.py",
        "tests/test_connection.py",
        "tests/test_e2e_basic_functionality.py",
        "tests/test_e2e_integration.py",
        "tests/test_e2e_oracle_autonomous.py",
        "tests/test_enterprise_features.py",
        "tests/test_error_handling.py",
        "tests/test_performance_benchmarks.py",
        "tests/test_real_world_scenarios.py",
    ]

    fixed_count = 0
    for file_path in files_to_fix:
        path = Path(file_path)
        if path.exists() and process_file(path):
            fixed_count += 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
