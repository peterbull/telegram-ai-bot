import os
import pandas as pd
import tiktoken

from dotenv import load_dotenv
from openai import OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter

load_dotenv()
client = OpenAI()

client.api_key = os.environ['OPENAI_API_KEY']

DOMAIN = "developer.mozilla.org"

def remove_newlines(series):
    series = series.str.replace('\n', ' ')
    series = series.str.replace('\\n', ' ')
    series = series.str.replace('  ', ' ')
    series = series.str.replace('  ', ' ')
    return series

# List to store texts files
texts = []

# Get all the text files in the text directory
for file in os.listdir("text/" + DOMAIN + "/"):

  # Open the file and read the text
  with open("text/" + DOMAIN + "/" + file, "r", encoding="UTF-8") as f:
    text = f.read()
    # we replace the last 4 characters to get rid of .txt, and replace _ with / to generate the URLs we scraped
    filename = file[:-4].replace('_', '/')
    """
    There are a lot of contributor.txt files that got included in the scrape, this weeds them out. There are also a lot of auth required urls that have been scraped to weed out as well
    """ 
    if filename.endswith(".txt") or 'users/fxa/login' in filename:
      continue

    # then we replace underscores with / to get the actual links so we can cite contributions
    texts.append(
      (filename, text))

# Create dataframe
df = pd.DataFrame(texts, columns=['fname', 'text'])

# Set the text column to be the raw text with the newlines removed
df['text'] = df.fname + ". " + remove_newlines(df.text)
df.to_csv('processed/scraped.csv')

# Load the cl100k_base tokenizer, which is designed to work with the ada-02 model
tokenizer = tiktoken.get_encoding("cl100k_base")

df = pd.read_csv('processed/scraped.csv', index_col=0)
df.columns = ['title', 'text']

# Tokenize the text and save the number of tokens to a new column
df['n_tokens'] = df.text.apply(lambda x: len(tokenizer.encode(x)))
df.head()

chunk_size = 1000

text_splitter = RecursiveCharacterTextSplitter(
   length_function = len,
   chunk_size = chunk_size,
   chunk_overlap = 0,
   add_start_index = False
)

shortened = []

for row in df.iterrows():
    
    # if the text is none, go to the next row
    if row[1]['text'] is None:
        continue
   
    # If the number of tokens is greater than the max number of tokens, split the text into chunks
    if row[1]['n_tokens'] > chunk_size:
      # Split the text using LangChain's text splitter
        chunks = text_splitter.create_documents([row[1]['text']])
        # Append the content of each chunk to the 'shortened' list
        for chunk in chunks:
            shortened.append(chunk.page_content)

    # Otherwise, add the text to the list of shortened texts
    else:
        shortened.append(row[1]['text'])

df = pd.DataFrame(shortened, columns=['text'])
df['n_tokens'] = df.text.apply(lambda x: len(tokenizer.encode(x)))

if not os.path.exists('processed/embeddings.csv'):
    df['embeddings'] = df.text.apply(lambda x: client.embeddings.create(input=x, model='text-embedding-ada-002').data[0].embedding)
    df.to_csv('processed/embeddings.csv')
else:
    print("Embeddings already exist")
