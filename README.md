# Hodgepodge

## Generating monthly calendar for a year in excel file(.xlsx)

- source code: [**calendar_gen.py**](./python/calendar_gen.py)
- sample output: [**calendar-2022.xlsx**](./python/examples/calendar-2022.xlsx)
- screenshots:
- ![calendar-screenshots](./python/examples/calendar-2023-small.gif)

- Dependencies: [openpyxl 3.0.10][openpyxl] - A python library to read/write Excel 2010 xlsx/xlsm files

    ```bash
    pip install openpyxl
    ```
    _openpyxl is compatible to Python 3.6 or higher_

- Usage:  
    
    a) Generate monthly calendar for the current year (*active tab: current month*)
    ```bash
    python calendar_gen.py 
    ```

    b) Generate calendar for the specific year (*active tab: January*)
     ```bash
    python calendar_gen.py [year]
    ```

    c) Generate calendar for the specific year (*active tab: given month*)
    ```bash
    python calendar_gen.py [year] [month]
    ```
    
<br><hr><br>

## Merging PDF files in the current working directory

- source code: [**merge_pdfs.py**](./python/merge_pdfs.py)

- Dependencies: [PyPDF2 2.1.0][PyPDF2] - A free and open-source pure-python PDF library

    ```bash
    pip install PyPDF2
    ```
    _PyPDF2 is compatible to Python 3.6 or higher_

- Usage:
    ```bash
    python merge_pdfs.py [filename]
    ```
<br><hr><br>

## Website Automation using Selenium 4
- Dependencies: [Selenium 4.2.0][Selenium], [webdriver-manager 3.7.0][webdriver-manager]

    ```bash
    pip install selenium==4.2.0
    pip install webdriver-manager
    ```
    _Selenium 4 will require a minimum Python 3.7 or higher_

1. [**Quasarzone point mining**](./python/quasarzone.py)
    - [퀘이사존][quasarzone] 출석체크 및 배너클릭

1. [**Kyobobook daily attendance**](./python/kyobobook.py)
    - [교보문고][kyobo] 출석체크 및 보너스 스탬프

<br><hr><br>

[openpyxl]: https://openpyxl.readthedocs.io/en/stable/
[PyPDF2]: https://pypdf2.readthedocs.io/en/latest/
[Selenium]: https://www.selenium.dev/documentation/webdriver/
[webdriver-manager]: https://pypi.org/project/webdriver-manager/
[quasarzone]: https://quasarzone.com/
[kyobo]: http://www.kyobobook.co.kr