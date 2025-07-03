#!/usr/bin/env python3
"""
Fix remaining PEP strict compliance issues.
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd: list[str]) -> tuple[int, str, str]:
    """Run command and return exit code, stdout, stderr."""
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr


def fix_sinks_remaining_issues():
    """Fix remaining issues in sinks.py."""
    print("🔧 Fixing remaining sinks.py issues...")

    sinks_path = "flext_target_oracle/sinks.py"

    with open(sinks_path) as f:
        content = f.read()

    # Fix dict type annotations
    content = content.replace(") -> dict:", ") -> dict[str, Any]:")

    # Add missing type parameters
    content = content.replace("rules: dict", "rules: dict[str, Any]")

    # Fix NUMBER call without type ignore
    content = content.replace(
        (
            "name, NUMBER(1), nullable=True\n"
            "            )  # type: ignore[no-untyped-call]"
        ),
        (
            "name, NUMBER(1), nullable=True  # type: ignore[no-untyped-call]\n"
            "            )"
        ),
    )

    # Remove unused type ignores by checking each line
    lines = content.split("\n")
    new_lines = []

    for line in lines:
        # Remove specific unused type ignores
        if "# type: ignore[misc]" in line and any(
            x in line
            for x in [
                "def full_table_name",
                "def _generate_oracle_ddl",
                "def _convert_to_oracle_type",
                "def _convert_to_oracle_type_fallback",
                "def _build_oracle_merge_statement",
                "def _build_direct_path_insert",
                "def _build_bulk_insert_statement",
                "def _build_merge_statement",
            ]
        ):
            # These return types need fixing, not ignoring
            new_lines.append(line.replace("# type: ignore[misc]", ""))
        elif "# type: ignore[override]" in line and "def full_table_name" in line:
            # Remove unused override ignore
            new_lines.append(line.replace("# type: ignore[override]", ""))
        elif "# type: ignore[no-untyped-call]" in line and "nullable=True" in line:
            # This one is needed - keep it
            new_lines.append(line)
        else:
            new_lines.append(line)

    content = "\n".join(new_lines)

    with open(sinks_path, "w") as f:
        f.write(content)

    print("  ✅ Fixed remaining sinks.py issues")


def fix_line_length_issues():
    """Fix remaining line length issues."""
    print("📏 Fixing line length issues...")

    # Use ruff to auto-fix what it can
    run_command(["ruff", "check", ".", "--fix", "--unsafe-fixes"])

    # Manual fixes for specific long lines
    test_files = [
        "tests/test_target_functionality.py",
        "tests/test_oracle_connection.py",
        "tests/test_oracle_features.py",
        "tests/test_message_processing.py",
    ]

    for file_path in test_files:
        if Path(file_path).exists():
            fix_test_file_line_lengths(file_path)

    print("  ✅ Fixed line length issues")


def fix_test_file_line_lengths(file_path: str):
    """Fix line length issues in test files."""
    with open(file_path) as f:
        lines = f.readlines()

    new_lines = []
    modified = False

    for line in lines:
        if len(line.rstrip()) > 88:
            # Handle specific patterns
            if ") -> None:" in line and "def test_" in line:
                # Test function definitions
                line = line.replace(") -> None:", "\n    ) -> None:")
                modified = True
            elif "oracle_config: dict, oracle_engine: Engine" in line:
                # Common test parameter pattern
                line = line.replace(
                    "oracle_config: dict, oracle_engine: Engine",
                    "oracle_config: dict,\n        oracle_engine: Engine",
                )
                modified = True
            elif "oracle_engine: Engine, query: str, expected: str" in line:
                # Parametrized test pattern
                line = line.replace(
                    "oracle_engine: Engine, query: str, expected: str",
                    (
                        "oracle_engine: Engine,\n"
                        "        query: str,\n"
                        "        expected: str"
                    ),
                )
                modified = True

        new_lines.append(line)

    if modified:
        with open(file_path, "w") as f:
            f.writelines(new_lines)
        print(f"    ✅ Fixed line lengths in {file_path}")


def validate_compliance():
    """Validate final compliance."""
    print("🏆 Validating compliance...")

    # Check ruff
    exit_code, stdout, stderr = run_command(["ruff", "check", "."])
    ruff_ok = exit_code == 0

    if ruff_ok:
        print("  ✅ Ruff: All checks passed!")
    else:
        print(f"  ⚠️  Ruff violations remain: {len(stdout.splitlines())} errors")

    # Check mypy strict on core package
    exit_code, stdout, stderr = run_command(
        ["mypy", "--strict", "flext_target_oracle/", "--show-error-codes"]
    )
    mypy_ok = exit_code == 0

    if mypy_ok:
        print("  ✅ MyPy strict: Success!")
    else:
        print(f"  ⚠️  MyPy violations remain: {len(stderr.splitlines())} errors")

    return ruff_ok and mypy_ok


def main():
    """Main execution."""
    print("🎯 FINAL PEP STRICT COMPLIANCE FIX")
    print("=" * 40)

    # Fix remaining issues
    fix_sinks_remaining_issues()
    fix_line_length_issues()

    # Validate
    success = validate_compliance()

    if success:
        print("\n🎉 ACHIEVED 100% PEP STRICT COMPLIANCE!")
        return 0
    else:
        print("\n⚠️  Some issues remain, but significant progress made.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
