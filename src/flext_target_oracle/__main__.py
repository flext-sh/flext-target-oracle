"""Entry point for flext-data.targets.flext-target-oracle when run as a module.

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT
"""

import sys

from flext_target_oracle.target import main

if __name__ == "__main__":
    sys.exit(main())
