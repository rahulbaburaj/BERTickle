import os
import time
import openai
import numpy as np
import pandas as pd
from umap import UMAP
from hdbscan import HDBSCAN
from bertopic import BERTopic
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import CountVectorizer

load_dotenv()
openai.api_type = "azure"
openai.api_version = "2023-05-15" 
openai.api_base = os.getenv("OPENAI_API_BASE")  # Your Azure OpenAI resource's endpoint value.
openai.api_key = os.getenv("OPENAI_API_KEY")

df = pd.read_csv('./data/worldnews_data.csv')
df = df.dropna(subset=['text', 'publish_date'])
# drop duplicates
df = df.drop_duplicates(subset=['text'])
docs = df['text'].tolist()

engine = "embedding_model"
def get_embedding(text, model="text-embedding-ada-002"):
   text = text.replace("\n", " ")
   return openai.Embedding.create(input = [text], engine=engine)['data'][0]['embedding']

# embeddings = df['text'].apply(get_embedding).tolist()

print("Getting embeddings...")
embeddings = []
docs = []
error_idx = []
for i, text in enumerate(df['text'].tolist()):
   try:
      embedding = get_embedding(text)
      embeddings.append(embedding)
      docs.append(text)
   except:
      time.sleep(60)
      try:
         embedding = get_embedding(text)
         embeddings.append(embedding)
         docs.append(text)
      except:
         time.sleep(60)
         try:
            embedding = get_embedding(text)
            embeddings.append(embedding)
            docs.append(text)
         except:
            print(f"Error on {i}")
            error_idx.append(i)
            continue
   
# get embeddings as numpy array
embeddings = np.array(embeddings)

# Define sub-models
vectorizer = CountVectorizer(stop_words="english")
umap_model = UMAP(n_neighbors=15, n_components=5, min_dist=0.0, metric='cosine', random_state=42)
hdbscan_model = HDBSCAN(min_cluster_size=20, min_samples=2, metric='euclidean', cluster_selection_method='eom')

# Train our topic model with BERTopic
topic_model = BERTopic(
    # embedding_model=sentence_model,
    umap_model=umap_model,
    hdbscan_model=hdbscan_model,
    vectorizer_model=vectorizer,
    # representation_model=representation_model
)
topics, _ = topic_model.fit_transform(docs, embeddings)

# save docs and topics in a csv file
df = df.drop(error_idx)
df['topic'] = topics
df.to_csv('./data/news_data_topics_openai.csv', index=False)

# embedding_model = "paraphrase-multilingual-mpnet-base-v2"
embedding_model = "embedding_model"
topic_model.save("./saved_models/topic_model_supplychain_openai", serialization="safetensors", save_ctfidf=True, save_embedding_model=embedding_model)

df['publish_date'] = df['publish_date'].fillna(method='ffill')

timestamps = df['publish_date'].to_list()
topics_over_time = topic_model.topics_over_time(docs, timestamps, global_tuning=True, evolution_tuning=True, nr_bins=20)
topics_over_time.to_csv("./saved_models/topics_over_time_supplychain_openai.csv", index=False)