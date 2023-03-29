import re
from fnmatch import fnmatch
from glob import iglob
from sys import argv


def main():
    boto_imports = ["*.json", "ssm"]
    boto_imports.extend(argv[1:])

    for filename in iglob("**/*.py", recursive=True):
        if fnmatch(filename, "node_modules/*"):
            continue
        with open(filename) as f:
            file_content = "".join([line.strip() for line in f.readlines()])
            if re.search(r"boto3", file_content):
                services_used = re.findall(
                    r"(?:resource|client)\((?:service_name=|)['\"](.*?)['\"]", file_content
                )
                if services_used:
                    boto_imports.extend(services_used)

    boto_imports.sort()
    import_str = "|".join(list(dict.fromkeys(boto_imports)))

    with open("cloudformation/strip_boto_pattern.yml", "w") as f:
        f.write(f"botocore/data/!({import_str})\n")


if __name__ == "__main__":
    main()
