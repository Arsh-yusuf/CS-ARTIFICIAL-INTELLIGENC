import pandas as pd
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

print("Starting to recreate pickle files...")

# 1. Load CSV
if not os.path.exists("top10K-TMDB-movies.csv"):
    print("Error: top10K-TMDB-movies.csv not found!")
    exit(1)

print("Loading CSV...")
movies = pd.read_csv("top10K-TMDB-movies.csv")

# 2. Recreate movies_list.pkl
print("Recreating movies_list.pkl...")
movies_small = movies[['id', 'title']]
pickle.dump(movies_small, open("movies_list.pkl", 'wb'))
print("movies_list.pkl created successfully.")

# 3. Recreate similarity.pkl (This might take some memory/time)
print("Recreating similarity.pkl (this may take a minute)...")
# Combine overview and genre for tags
movies['tags'] = movies['overview'].fillna('') + movies['genre'].fillna('')

cv = CountVectorizer(max_features=5000, stop_words='english')
vector = cv.fit_transform(movies['tags']).toarray()
similarity = cosine_similarity(vector)

pickle.dump(similarity, open("similarity.pkl", 'wb'))
print("similarity.pkl created successfully.")

print("\nAll done! You can now run 'streamlit run app.py' again.")
