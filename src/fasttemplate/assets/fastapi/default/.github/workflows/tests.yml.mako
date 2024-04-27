# This workflow will install Python dependencies, run tests and lint with a single version of Python
# For more information see: https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python

name: Tests

on:
  push:
    branches: ["main"]
  pull_request:
    branches: ["main"]

permissions:
  contents: read

jobs:
  tests:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: "3.12"

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        python -m pip install poetry
        make install

    - name: Code style
      run: |
        poetry run pre-commit run --all-files

    - name: Pytest
      run: |
        make test

    - name: Build & Install test
      run: |
        poetry build
        pip install dist/${project["name"]}-*.tar.gz
