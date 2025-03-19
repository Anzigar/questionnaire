#!/usr/bin/env python
import os
import sys
import subprocess
from pathlib import Path

def run_migrations():
    """Run alembic migrations using the proper CLI command"""
    # Get the project root directory (adjust if needed)
    project_dir = Path(__file__).parent.parent
    
    # Change to project directory
    os.chdir(project_dir)
    
    try:
        # Run migrations using alembic CLI
        result = subprocess.run(
            ["alembic", "upgrade", "head"],
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Migration failed: {e}", file=sys.stderr)
        print(f"Error output: {e.stderr}", file=sys.stderr)
        return False

if __name__ == "__main__":
    success = run_migrations()
    sys.exit(0 if success else 1)
