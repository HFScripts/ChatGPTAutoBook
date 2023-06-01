# ChatGPT AutoBook

This repository contains a Python script for generating a book using OpenAI's ChatGPT API.

## Table of Contents
1. [Getting Started](#getting-started)
    1. [Prerequisites](#prerequisites)
    1. [Installation](#installation)
2. [Usage](#usage)
3. [Script Explanation](#script-explanation)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.6 or later
- OpenAI's Python client library
- An OpenAI API key

### Installation

1. Clone the repository
    ```bash
    git clone https://github.com/HFScripts/ChatGPTAutoBook.git
    ```

2. Navigate into the cloned directory
    ```bash
    cd ChatGPTAutoBook
    ```

3. Install the OpenAI Python client library
    ```bash
    pip install openai
    ```

4. Create a text file named `key.txt` in the directory one level up from the ChatGPTAutoBook directory and paste your OpenAI API key into it. The structure should look like this:

    ```
    ├── key.txt
    ├── ChatGPTAutoBook
    │   └── ...
    ```

## Usage

To run the script, use the following command:

```bash
python main.py
```

## Script Explanation

- The script presents the user with a list of author types, such as "fiction", "non-fiction", "sci-fi", etc., to choose from. After the user selects a valid author type, the script will prompt the user to input a book topic.

- It then generates a list of chapters, with details to be covered in each chapter. The list is then evaluated to ensure that it is in-depth and contains enough details for each chapter.

- The content of each chapter is subsequently generated, following the details provided in the chapter index. Each detail is explained in-depth using multiple examples to aid understanding.

- Each chapter's content is written into separate Markdown files named ChapterX.md, where X is the chapter number.

### Error Handling
- The script includes rate limit handling with OpenAI's API. If a rate limit error occurs, it will retry the API call a specified number of times before failing.

- If the chapter content generation produces a line that does not match the expected format, the line is flagged as having an invalid format.

### Output
- The script outputs the generated book chapters as separate Markdown files in the same directory as the script. The file names follow the pattern ChapterX.md, where X is the chapter number. It also outputs a Chapters.md file which contains a list of all the chapters.

### Customization
- The script can be easily customized to fit your specific requirements. For example, you can change the list of valid author types, the maximum retries for handling API rate limits, or the format of the chapter files.

