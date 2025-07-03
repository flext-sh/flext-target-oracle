#!/usr/bin/env python3
"""
Restore connectors.py to a working state by regenerating it properly.
"""

import subprocess

def restore_connectors():
    """Restore connectors.py from git."""
    # Reset to last known good state
    subprocess.run(["git", "checkout", "HEAD", "flext_target_oracle/connectors.py"], check=True)
    
    # Remove the type ignore comments that are no longer needed  
    with open("flext_target_oracle/connectors.py", "r") as f:
        content = f.read()
    
    # Remove type ignore comments
    content = content.replace("  # type: ignore[no-untyped-call]", "")
    
    with open("flext_target_oracle/connectors.py", "w") as f:
        f.write(content)
    
    print("✅ Restored connectors.py and removed type ignore comments")

if __name__ == "__main__":
    restore_connectors()