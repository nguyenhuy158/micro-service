import os
import re
import sys

def bump_version(part):
    version_file = "shared/version.py"
    pyproject_file = "pyproject.toml"
    readme_file = "README.md"

    # Read current version
    with open(version_file, "r") as f:
        content = f.read()
        match = re.search(r'VERSION = "(\d+\.\d+\.\d+)"', content)
        if not match:
            print("Could not find version in shared/version.py")
            sys.exit(1)
        current_version = match.group(1)

    major, minor, patch = map(int, current_version.split("."))

    if part == "major":
        major += 1
        minor = 0
        patch = 0
    elif part == "minor":
        minor += 1
        patch = 0
    elif part == "patch":
        patch += 1
    else:
        print(f"Invalid part: {part}")
        sys.exit(1)

    new_version = f"{major}.{minor}.{patch}"

    # Update shared/version.py
    with open(version_file, "w") as f:
        f.write(f'VERSION = "{new_version}"\n')

    # Update pyproject.toml
    if os.path.exists(pyproject_file):
        with open(pyproject_file, "r") as f:
            content = f.read()
        new_content = re.sub(r'version = "\d+\.\d+\.\d+"', f'version = "{new_version}"', content)
        with open(pyproject_file, "w") as f:
            f.write(new_content)

    # Update README.md
    if os.path.exists(readme_file):
        with open(readme_file, "r") as f:
            content = f.read()
        new_content = re.sub(r'version-\d+\.\d+\.\d+-blue', f'version-{new_version}-blue', content)
        with open(readme_file, "w") as f:
            f.write(new_content)

    print(f"Bumped version from {current_version} to {new_version}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python bump_version.py [major|minor|patch]")
        sys.exit(1)
    bump_version(sys.argv[1])
