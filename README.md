# Generative AI Phishing Email Detection Application

## Preparing environment

1. Use python to create a virtual environment `python -m venv venv`
2. Source virtual environment use `source venv/bin/activate` on Linux or MacOS and use `. venv/scripts/activate` in Windows
3. Install python packages `pip install -r requirements.txt`  
4. Create config/credentials.json file by useing the Video: “How to Get Started with Gmail API.” YouTube, 6 May 2022, www.youtube.com/watch?v=7E3NNxeXiys.
(You will need to set up a google cloud console)
5. Due to limits of sharing open ai keys, you will need to create and train a open-ai model. The training data is provided in train.json file. Here is the tutorial for creating and training: www.datacamp.com/tutorial/fine-tuning-openais-gpt-4-step-by-step-guide. 
6. Add openai api key to line 7 of [generativeAI_window.py](https://github.com/CColin5/Phishing-Email-Tool/blob/main/generativeAI_window.py)
7. Run application `python main.py`

## Notes

- If you need additional python packages create a new `requirements.txt` with `pip freeze` to replace the old requirements.txt
