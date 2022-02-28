# Apop idols website crawler

Version 2.0

![Issues](https://img.shields.io/github/issues/peterspbr/apopidols-parser?style=flat-square)
![License](https://img.shields.io/github/license/peterspbr/apopidols-parser?style=flat-square)

## How to use?
### Requirements
- Python >= 3.8
- tqdm
- Beautiful Soup
- Urllib

### Usage:
    Download by idol name:
        apop_parser.py -a <idol name>
        [!] The name must be as follows: surname_name. Example: hirokawa_nanase

    Download by group name:
        apop_parser.py -g <group_name>
        [!] The name must be as follows: idol_group. Example: luce_twinkle_wink

    Download all images:
        apop_parser.py -e folder_name

    Show this help message:
        apop_parser.py -h
> Please keep in mind that if the idol/group name is not written with the "underline", it will return a error! Don't use spaces and or dashes.

### Want to support the projet?
If you want to support the project, please open a issue clearifying what you need or what bug might be solved. If you want to do a pull request, don't forget to fork the repository first.
