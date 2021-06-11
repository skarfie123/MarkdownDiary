# MarkdownDiary

![GitHub release (latest by date)](https://img.shields.io/github/v/release/skarfie123/MarkdownDiary)
![GitHub all releases](https://img.shields.io/github/downloads/skarfie123/MarkdownDiary/total)
![GitHub issues](https://img.shields.io/github/issues/skarfie123/MarkdownDiary)
![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)

## Options

- daily : create a file per day instead of the default file per month
- index : link to an index, useful if you have multiple diaries

## Example

Create a diary called Diary, with years 2021 and 2022, linked to index Main.md.

> `MarkdownDiary.exe -n Diary -y 2021 2022 -i Main.md`

Add 2023 to Diary

> `MarkdownDiary.exe -n Diary -y 2023 -i Main.md`

## Build

> `pyinstaller --onefile MarkdownDiary.py`

## Installation

1. Place the file `MarkdownDiary.exe` in a folder such as `C:\...\cmd`
1. Add that folder to the `PATH` environment variable (so you can run the tool from anywhere)

NB. you can use this folder for other tools and scripts, such as [these](https://github.com/skarfie123/cmd).
