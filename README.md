phishing email tool  

## Prerequisites

- Modern version of [python](https://www.python.org/) (3.11+)

## Preparing environment

1. Use python to create a virtual environment `python -m venv venv`
2. Source virtual environment use `source venv/bin/activate` on Linux or MacOS and use `. venv/scripts/activate` in Windows
3. Install python packages `pip install -r requirements.txt`  
4. Create config/credentials.json file
5. Add openapi key to line 7 of [generativeAI_window.py](https://github.com/CColin5/Phishing-Email-Tool/blob/main/generativeAI_window.py)
6. Run application `python main.py`

## Notes

- If you need additional python packages create a new `requirements.txt` with `pip freeze` to replace the old requirements.txt
