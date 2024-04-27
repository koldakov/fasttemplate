[tool.poetry]
name = "${project['name']}"
version = "${project['version']}"
description = "${project['description']}"
% if author:
  % if author["name"] and author["email"]:
authors = ["${author['name']} <${author['email']}>"]
  % endif
  % if author["name"] and not author["email"]:
authors = ["${author['name']}"]
  % endif
  % if not author["name"] and author["email"]:
authors = ["<${author['email']}>"]
  % endif
% endif
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.12"
fastapi = "^0.110.2"
hypercorn = "^0.16.0"
uvloop = "^0.19.0"

[tool.poetry.group.dev.dependencies]
pre-commit = "^3.7.0"

[tool.poetry.group.test.dependencies]
pytest = "^8.1.1"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

[tool.ruff]
exclude = [
    ".eggs",
    ".git",
    ".git-rewrite",
    ".mypy_cache",
    ".pyenv",
    ".pytest_cache",
    ".pytype",
    ".ruff_cache",
    ".tox",
    "build",
    "dist",
    ".venv",
]

fix = true
show-fixes = true
show-source = true

line-length = 120
indent-width = 4

target-version = "py312"

[tool.ruff.lint]
select = [
    "E",
    "F",
    "W",
    "C90",
    "I",
    "N",
    "UP",
    "S",
    "BLE",
    "B",
    "A",
    "C4",
    "DJ",
    "PL",
    "TCH",
    "RUF",
    "TID",
]
ignore = [
    "N818",
]

fixable = ["ALL"]
unfixable = []

dummy-variable-rgx = "^(_+|(_+[a-zA-Z0-9_]*[a-zA-Z0-9]+?))$"

[tool.ruff.format]
quote-style = "double"

[tool.ruff.mccabe]
max-complexity = 10

[tool.ruff.lint.extend-per-file-ignores]
"test_*.py" = [
    "S101",
]

[tool.mypy]
python_version = "3.12"
follow_imports = "skip"
ignore_missing_imports = true
check_untyped_defs = true
files = [
    % for path in project["mypy_files"]:
    "${path}",
    % endfor
]

[tool.pytest.ini_options]
testpaths = [
    "tests",
]
