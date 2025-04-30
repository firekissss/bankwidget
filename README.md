# 𝔹𝕒𝕟𝕜 𝕨𝕚𝕕𝕘𝕖𝕥 𝕓𝕒𝕔𝕜𝕖𝕟𝕕

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![PyCharm](https://img.shields.io/badge/pycharm-143?style=for-the-badge&logo=pycharm&logoColor=black&color=black&labelColor=green)
![Poetry](https://img.shields.io/badge/Poetry-%233B82F6.svg?style=for-the-badge&logo=poetry&logoColor=0B3D8D)
![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)



The backend of a widget that deals with client cards, bank accounts and (possibly in the future) operations with them.
No test and frontend yet, but gonna do that soon.

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

There are some properly-working modules with functions:
- masks.py
  + get_mask_card_number (returns masked card number in XXXX XX** **** XXXX format)
  + get_mask_account (returns masked bank account number in **XXXX format)
- widget.py
  + mask_account_card (returns masked account or card number, uses both of previous functions)
  + get_date (extracts date in DD.MM.YYYY format from ISO datetime string)
- processing.py
  + filter_by_state (filters the list of dictionaries by the 'state' parameter, EXECUTED by default)
  + sort_by_date (sorts an input dictionary list by key 'date' and value in ISO format
    in descending (default) or ascending order)

You can launch these functions by adding `print` command in module you need and give some input data as parameters.


### For example
Add this at the end of processing.py:
```python
print(sort_by_date([{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
                    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
                    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
                    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}],
                   is_reversed=False
                   ))
```
and run processing.py file. It will show you the result of the function.

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
No tests yet, except manual testing of each function.

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