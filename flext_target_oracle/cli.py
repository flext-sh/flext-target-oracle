"""CLI interface for flext-target-oracle."""

import sys
import json
import argparse
from flext_target_oracle.target import TargetOracle


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description='Singer Target for Oracle Database')
    parser.add_argument(
        '--config',
        required=True,
        help='Configuration file path'
    )
    parser.add_argument(
        '--state',
        help='State file path'
    )
    
    args = parser.parse_args()
    
    # Load configuration
    with open(args.config) as f:
        config = json.load(f)
    
    # Load state if provided
    state = {}
    if args.state:
        with open(args.state) as f:
            state = json.load(f)
    
    # Initialize target
    target = TargetOracle(config, state)
    
    # Process stdin
    target.listen()


if __name__ == '__main__':
    main()