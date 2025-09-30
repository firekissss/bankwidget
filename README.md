# 𝔹𝕒𝕟𝕜 𝕨𝕚𝕕𝕘𝕖𝕥 𝕓𝕒𝕔𝕜𝕖𝕟𝕕

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![PyCharm](https://img.shields.io/badge/pycharm-143?style=for-the-badge&logo=pycharm&logoColor=black&color=black&labelColor=green)
![Poetry](https://img.shields.io/badge/Poetry-%233B82F6.svg?style=for-the-badge&logo=poetry&logoColor=0B3D8D)
![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)

The backend of a widget that deals with client cards, bank accounts and (possibly in the future) operations with them.
No frontend yet, but going to do that soon.

## Ｃｏｎｔａｉｎｓ

- [Technologies](#technologies)
- [Getting started](#getting-started)
- [Testing](#testing)
- [Deploy и CI/CD](#deploy-and-cicd)
- [Contributing](#contributing)
- [To do](#to-do)
- [Project team](#project-team)

## Technologies

- Nothing
- Something else
- ...

## Getting started

Install this project from git:

```commandline
gh repo clone firekissss/bankwidget
```

Do not launch it in any possible way! There's nothing to launch yet!

# Modules Overview

This project contains several properly-working modules with utility functions:

### `masks.py`
- **`get_mask_card_number`** – returns a masked card number in `XXXX XX** **** XXXX` format.
- **`get_mask_account`** – returns a masked bank account number in `**XXXX` format.

### `widget.py`
- **`mask_account_card`** – returns a masked account or card number, using both functions from `masks.py`.
- **`get_date`** – extracts the date in `DD.MM.YYYY` format from an ISO datetime string.

### `processing.py`
- **`filter_by_state`** – filters a list of dictionaries by the `'state'` key (defaults to `'EXECUTED'`).
- **`sort_by_date`** – sorts a list of dictionaries by the `'date'` key (ISO format), in descending order by default (ascending optional).

### `generators.py`
- **`filter_by_currency`** – returns an iterator of transactions that match the specified currency.
- **`transaction_descriptions`** – yields the description of each transaction from a given list.
- **`card_number_generator`** – generates card numbers as an iterator, from a specified start to end value.

### `decorators.py`

- **`log`** – decorator that logs function calls: timestamp, function name, arguments, result, and exceptions. If a filename is provided, logs are written to that file; otherwise they are printed to the console/
## Usage Examples

You can run these functions by calling them in Python with some input data and optionally printing the results.

---
### `sort_by_date`
```python
from src.processing import sort_by_date

data = [
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
]

# Sort in ascending order
print(sort_by_date(data, is_reversed=False))

```
---
### `filter_by_currency`

```python
from src.generators import filter_by_currency

transactions = [
    {"operationAmount": {"currency": {"code": "USD"}}, "description": "Payment 1"},
    {"operationAmount": {"currency": {"code": "RUB"}}, "description": "Payment 2"},
]

# Filter only USD transactions
for t in filter_by_currency(transactions, "USD"):
    print(t["description"])
# Output:
# Payment 1
```
---
###  `transaction_descriptions`
```python
from src.generators import transaction_descriptions

transactions = [
    {"description": "Payment 1"},
    {"description": "Payment 2"},
]

for desc in transaction_descriptions(transactions):
    print(desc)
# Output:
# Payment 1
# Payment 2
```
---
### `card_number_generator`
```python
from src.generators import card_number_generator

# Generate card numbers from 1 to 5
for number in card_number_generator(1, 5):
    print(number)
# Output:
# 0000 0000 0000 0001
# 0000 0000 0000 0002
# 0000 0000 0000 0003
# 0000 0000 0000 0004
# 0000 0000 0000 0005
```
---
### `log`
```python
from src.decorators import log

# Example 1: logging to console
@log()
def add(a, b):
    return a + b

print(add(5, 10))  # logs call, args, result to console

# Example 2: logging to a file
@log(filename="function_calls.log")
def divide(a, b):
    return a / b

try:
    divide(10, 0)  # logs call and exception to the file
except ZeroDivisionError:
    pass
```

## Development

In progress...

ＷＡＲＮＩＮＧ
everything development-related in this paragraph does not work yet... Hope it will, but later xD

### Requirements

The following are necessary to install and launch this project:

- 1
- 2
- 3
- ...

### Installing dependencies

For installing dependencies run this command:

```sh
$ npm i
```

### Run Development server

To run Development server, do this command:

```sh
npm start
```

### Build

To make a production build, run this command:

```sh
npm run build
```

## Testing

Automated testing is implemented using [pytest](https://docs.pytest.org/).  
The project includes unit tests for key functions, organized in the `tests/` directory. Fixtures are used for reusable
test data, including valid and invalid input sets, as well as edge cases.

### How to Run Tests

To run all tests, use:

```bash
pytest
```

or, for verbose output:

```bash
pytest -v
```

### Test Coverage

- Valid and invalid input dictionaries
- Edge cases with missing or malformed data
- Handling of various `state` values (`EXECUTED`, `CANCELED`, etc.)
- Filtering and sorting logic
- Reusability with fixtures for:
    - Valid card numbers
    - Correct and incorrect operation data
    - Duplicate and identical data scenarios

You can also run specific test files or functions using:

```bash
pytest tests/test_module_name.py
pytest tests/test_module_name.py::test_function_name
```

> Manual testing was used during initial development. Now, automated tests are used to ensure stability and prevent
> regressions.

## Deploy and CI/CD

IDK what is it, will figure it out later on.

## Contributing

If you have suggestions, send a [message](https://t.me/firekissss) to me.
![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)

## FAQ

Empty for now.

### I do this project for education purposes, do not judge me if I do smth wrong pls.

## To do

- [x] Make some progress at studying python
- [ ] Get a job

## Project team

- Me (-> [write me](https://t.me/firekissss) <-)
  ![Xiaomi](https://img.shields.io/badge/Xiaomi-%23FF6900.svg?style=for-the-badge&logo=xiaomi&logoColor=white)
  ![Windows 11](https://img.shields.io/badge/Windows%2011-%230079d5.svg?style=for-the-badge&logo=Windows%2011&logoColor=white)
  ![Vivaldi](https://img.shields.io/badge/Vivaldi-EF3939?style=for-the-badge&logo=Vivaldi&logoColor=white)
  ![ChatGPT](https://img.shields.io/badge/chatGPT-74aa9c?style=for-the-badge&logo=openai&logoColor=white)

## Sources

[Skypro](https://skyeng.ru/home) - one of the best educational platforms in Russia.
Visit their page, they have been helping me study Python since 2024!