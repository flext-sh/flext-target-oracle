#!/usr/bin/env python3
"""
Fix integration tests to properly skip when Oracle is not available.
"""

import re
from pathlib import Path

# List of test files that need Oracle connection decorators
test_files_needing_decorators = [
    "test_bulk_operations.py",
    "test_connection.py",
    "test_e2e_basic_functionality.py",
    "test_enterprise_features.py",
    "test_error_handling.py",
    "test_logging_monitoring.py",
    "test_oracle_connection.py",
    "test_oracle_features.py",
    "test_performance_benchmarks.py",
    "test_real_world_scenarios.py",
    "test_type_mapping.py"
]

def fix_test_file(file_path: Path) -> bool:
    """Fix a single test file to include the requires_oracle_connection decorator."""
    print(f"Processing {file_path}")

    try:
        content = file_path.read_text()
        
        # Check if file uses Oracle fixtures
        oracle_fixtures = ["oracle_target", "oracle_engine", "oracle_config"]
        uses_oracle = any(fixture in content for fixture in oracle_fixtures)

        if not uses_oracle:
            print(f"  ⚠️  {file_path.name} doesn't use Oracle fixtures - skipping")
            return False

        # Check if already has the import
        has_import = "from tests.helpers import requires_oracle_connection" in content
        
        # Check if already has decorators
        has_decorator = "@requires_oracle_connection" in content

        if has_import and has_decorator:
            print(f"  ✅ {file_path.name} already properly configured")
            return False

        # Add import if missing
        if not has_import:
            # Find the imports section and add our import
            import_pattern = r"(from flext_target_oracle.*?\n)"
            if re.search(import_pattern, content):
                content = re.sub(
                    import_pattern,
                    r"\1from tests.helpers import requires_oracle_connection\n",
                    content
                )
            else:
                # Fallback: add after other imports
                lines = content.split('\n')
                insert_idx = 0
                for i, line in enumerate(lines):
                    if line.startswith('import ') or line.startswith('from '):
                        insert_idx = i + 1
                lines.insert(
                    insert_idx, "from tests.helpers import requires_oracle_connection"
                )
                content = '\n'.join(lines)

        # Add decorators to test classes that use Oracle fixtures
        class_pattern = r"^class (Test\w+):"

        def add_decorator(match):
            # Check if this class has methods that use Oracle fixtures
            class_start = match.start()
            # Find the end of this class (next class or end of file)
            next_class = re.search(
                r"\n^class ", content[class_start + 1:], re.MULTILINE
            )
            if next_class:
                class_content = content[
                    class_start:class_start + 1 + next_class.start()
                ]
            else:
                class_content = content[class_start:]

            # Check if this class uses Oracle fixtures
            if any(fixture in class_content for fixture in oracle_fixtures):
                return f"@requires_oracle_connection\n{match.group(0)}"
            return match.group(0)

        content = re.sub(class_pattern, add_decorator, content, flags=re.MULTILINE)

        # Write back the modified content
        file_path.write_text(content)
        print(f"  ✅ Fixed {file_path.name}")
        return True

    except Exception as e:
        print(f"  ❌ Error processing {file_path.name}: {e}")
        return False

def main():
    """Fix all integration test files."""
    tests_dir = Path("tests")
    
    if not tests_dir.exists():
        print("❌ Tests directory not found")
        return

    fixed_count = 0

    # Process specific test files that need decorators
    for test_file in test_files_needing_decorators:
        file_path = tests_dir / test_file
        if file_path.exists():
            if fix_test_file(file_path):
                fixed_count += 1
        else:
            print(f"⚠️  {test_file} not found")

    print(f"\n🎯 Fixed {fixed_count} test files")
    print(
        "✅ All integration tests should now properly skip when Oracle is not "
        "available"
    )

if __name__ == "__main__":
    main()