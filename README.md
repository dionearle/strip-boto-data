# Strip Boto Data

A pre-commit hook which strips any un-used boto3 services from the build.

To setup in your project, add the following to `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/dionearle/strip-boto-data
    rev: 1.0.0
    hooks:
      - id: strip-boto-data
```

as well as updating your `serverless.yml` to include the following:

```yaml
custom:
  pythonRequirements:
    slim: true
    slimPatterns:
      - ${file(./cloudformation/strip_boto_pattern.yml)}
```
