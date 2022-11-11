import re
from glob import iglob


def main():
    boto_imports = ["*.json", "ssm"]
    for filename in iglob("**/*.py", recursive=True):
        with open(filename) as f:
            file_content = "".join([line.strip() for line in f.readlines()])
            if re.search(r"boto3", file_content):
                services = re.findall(
                    r"(?:resource|client)\((?:service_name=|)['\"](.*?)['\"]", file_content
                )
                if services:
                    boto_imports.extend(services)

    boto_imports.sort()
    import_str = "|".join(list(dict.fromkeys(boto_imports)))

    with open("cloudformation/strip_boto_pattern.yml", "w") as f:
        f.write(f"botocore/data/!({import_str})")


if __name__ == "__main__":
    main()
