import streamlit as st
import pickle
import requests
import os
import pandas as pd

# Caching the TMDB API calls to improve performance
@st.cache_data(show_spinner=False)
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=ec33fcc1c8061dab5bcc691a1b5f5641&language=en-US".format(movie_id)
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
    except Exception as e:
        # Fallback to a placeholder image if the API call fails
        pass
    return "https://via.placeholder.com/500x750?text=Poster+Not+Found"

# Caching the large pickle files to avoid reloading on every script rerun
@st.cache_resource
def load_data():
    try:
        movies = pickle.load(open("movies_list.pkl", 'rb'))
        similarity = pickle.load(open("similarity.pkl", 'rb'))
    except (NotImplementedError, AttributeError, ImportError, pickle.UnpicklingError) as e:
        st.warning("Pickle files are incompatible with current environment. Attempting to load from CSV...")
        try:
            movies = pd.read_csv("top10K-TMDB-movies.csv")
            # Select only necessary columns to match expected structure
            movies = movies[['id', 'title']]
            # We still need similarity, but recreating it might be too heavy.
            # For now, let's try to load it separately.
            similarity = pickle.load(open("similarity.pkl", 'rb'))
        except Exception as csv_e:
            st.error(f"Failed to load data from CSV: {csv_e}")
            raise e
    return movies, similarity

with st.spinner("Loading movie data..."):
    try:
        movies, similarity = load_data()
        movies_list = movies['title'].values
    except Exception as e:
        st.error(f"Critical error loading data: {e}")
        st.stop()

st.header("Movie Recommender System")

# Robust path for the custom component
curr_dir = os.path.dirname(os.path.abspath(__file__))
frontend_path = os.path.join(curr_dir, "frontend", "frontend", "public")

if os.path.exists(frontend_path):
    imageCarouselComponent = st.components.v1.declare_component("image-carousel-component", path=frontend_path)
else:
    st.error(f"Frontend component path not found: {frontend_path}")
    imageCarouselComponent = None

def get_carousel_urls():
    movie_ids = [1632, 299536, 17455, 2830, 429422, 9722, 13972, 240, 155, 598, 914, 255709, 572154]
    return [fetch_poster(mid) for mid in movie_ids]

if imageCarouselComponent:
    with st.spinner("Fetching spotlight movies..."):
        imageUrls = get_carousel_urls()
        imageCarouselComponent(imageUrls=imageUrls, height=200)

selectvalue = st.selectbox("Select movie from dropdown", movies_list)

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    recommend_movies = []
    recommend_poster = []
    for i in distance[1:6]:
        movies_id = movies.iloc[i[0]].id
        recommend_movies.append(movies.iloc[i[0]].title)
        recommend_poster.append(fetch_poster(movies_id))
    return recommend_movies, recommend_poster

if st.button("Show Recommend"):
    with st.spinner("Generating recommendations..."):
        movie_name, movie_poster = recommend(selectvalue)
        col1, col2, col3, col4, col5 = st.columns(5)
        for i, col in enumerate([col1, col2, col3, col4, col5]):
            with col:
                st.text(movie_name[i])
                st.image(movie_poster[i])
