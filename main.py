from newsdataapi import NewsDataApiClient
from transformers import pipeline
import openpyxl
import datetime
import os

# API key authorization
api = NewsDataApiClient(os.environ.get('API_KEY'))

# get the news
response = api.news_api(language = "en")
lst = response['results']

# create a new workbook and select the active worksheet
workbook = openpyxl.load_workbook("data.xlsx")
worksheet = workbook.active

def summarize_content(content):
    """
    This function takes a string of text as input and returns a summary of the content.
    """
    try:
        # Initializing the summarization pipeline
        summarizer = pipeline("summarization")

        # Generating the summary
        summary = summarizer(content, max_length=100, min_length=30, do_sample=False)

        # Returning the summary as a string
        return summary[0]['summary_text']
    
    except IndexError:
        return False

# write the news into the worksheet
for news in lst:
    desc = news["description"] or ""
    content = news["content"] or ""
    summary = summarize_content(desc + content)
    today = datetime.date.today()
    today_str = today.strftime("%Y-%m-%d")

    if summary:
        worksheet.append([news["title"], news["link"], summary, today_str])

# save the workbook
workbook.save("data.xlsx")