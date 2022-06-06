# Hodgepodge

## Website Automation using Selenium 4
- Dependencies: Selenium 4, webdriver-manager 3.7.0

    ```bash
    pip install selenium==4.2.0
    pip install webdriver-manager
    ```
    _Selenium 4 will require a minimum Python 3.7 or higher_

1. [**Quasarzone point mining**](./python/quasarzone.py)
    - [퀘이사존][quasarzone] 출석체크 및 배너클릭

1. [**Kyobobook daily attendance**](./python/kyobobook.py)
    - [교보문고][kyobo] 출석체크 및 보너스 스탬프

<hr>

## Merging PDF files in the current working directory

- source code: [**merge_pdfs.py**](./python/merge_pdfs.py)

- Dependencies: [PyPDF2][PyPDF2] - A free and open-source pure-python PDF library

    ```bash
    pip install PyPDF2
    ```
    _PyPDF2 is compatible to Python 3.6 or higher_

- Usage:
    ```bash
    python merge_pdfs.py [filename]
    ```
<hr>

## Generating monthly calendar for printing on A4

- source code: [**merge_pdfs.py**](./python/merge_pdfs.py)

- Dependencies: [openpyxl][openpyxl] - A python library to read/write Excel 2010 xlsx/xlsm files

    ```bash
    pip install openpyxl
    ```
    _openpyxl is compatible to Python 3.6 or higher_

- Usage:  
    
    a) Generate calendar for the current month
    ```bash
    python calendar_gen.py 
    ```

    b) Generate calendar for a specific month
    ```bash
    python calendar_gen.py [year] [month]
    ```

[quasarzone]: https://quasarzone.com/
[kyobo]: http://www.kyobobook.co.kr
[PyPDF2]: https://pypdf2.readthedocs.io/en/latest/
[openpyxl]: https://openpyxl.readthedocs.io/en/stable/