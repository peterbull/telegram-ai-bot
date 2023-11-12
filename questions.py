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
    
    df['distances'] = df.embeddings.apply(
                      lambda x: cosine_similarity(np.array(q_embeddings), np.array(x)))

    returns = []
    cur_len = 0

    # Sort by distance and add the text to the context until the context is too long
    for i, row in df.sort_values('distances', ascending=True).iterrows():

        # Add the length of the text to the current length
        cur_len += row['n_tokens'] + 4

        # If the context is too long, break
        if cur_len > max_len:
            break

        # Else add it to the text that is being returned
        returns.append(row["text"])

    # Return the context
    return "\n\n###\n\n".join(returns)


create_context(question='What is CSS?', df=df)

