import numpy as np
import pandas as pd
import openai
import os
from openai import OpenAI
from embedding_utils.distance import cosine_similarity

client = OpenAI()

openai.api_key = os.environ["OPENAI_API_KEY"]

df = pd.read_csv('processed/embeddings.csv', index_col=0)
df['embeddings'] = df['embeddings'].apply(eval).apply(np.array)




def create_context(question, df, max_len=1800, size="ada"):
    """
    Create a context for a question by finding the most similar context from the dataframe
    """

    # Get the embeddings for a question
    q_embeddings = client.embeddings.create(input=question, model='text-embedding-ada-002') \
                   .data[0].embedding
    
    df['distances'] = df.embeddings.apply(lambda x: cosine_similarity(q_embeddings, x))

