from newsdataapi import NewsDataApiClient
from transformers import pipeline
import openpyxl
import datetime
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

# API key authorization
api = NewsDataApiClient(apikey="pub_20239668dc2992683ebca80bca8b4951aab1e")

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
    stopWords = set(stopwords.words("english"))
    words = word_tokenize(content)
    freqTable = dict()
    for word in words:
        word = word.lower()
        if word in stopWords:
            continue
        if word in freqTable:
            freqTable[word] += 1
        else:
            freqTable[word] = 1
    sentences = sent_tokenize(content)
    sentenceValue = dict()

    for sentence in sentences:
        for word, freq in freqTable.items():
            if word in sentence.lower():
                if sentence in sentenceValue:
                    sentenceValue[sentence] += freq
                else:
                    sentenceValue[sentence] = freq
    sumValues = 0
    for sentence in sentenceValue:
        sumValues += sentenceValue[sentence]

    average = int(sumValues / len(sentenceValue))

    summary = ''
    for sentence in sentences:
        if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.2 * average)):
            summary += " " + sentence
    return summary

    # try:
    #     # Initializing the summarization pipeline
    #     summarizer = pipeline("summarization", model="gpt2", tokenizer="gpt2", framework="tf")

    #     # Generating the summary
    #     summary = summarizer(content, max_length=100, min_length=30, do_sample=False)

    #     # Returning the summary as a string
    #     return summary[0]['summary_text']
    
    # except IndexError:
    #     return False

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