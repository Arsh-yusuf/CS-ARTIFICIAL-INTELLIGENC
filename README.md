# Movie Recommender System

A sophisticated movie recommendation engine built with Python, Streamlit, and Scikit-learn. This project uses Cosine Similarity to recommend movies based on their genres and overviews.

## Features
- **Smart Recommendations**: Suggests 5 similar movies based on your selection.
- **Dynamic Spotlight**: An interactive carousel showcasing popular movies.
- **Rich Visuals**: Automatically fetches movie posters from the TMDB API.
- **Optimized Performance**: Implements advanced caching to ensure instant responses.

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd CS-ARTIFICIAL-INTELLIGENC
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv env
   source env/Scripts/activate  # On Windows: env\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Setup & Data Preparation

The project uses large similarity matrices stored as `.pkl` files. If you encounter a `NotImplementedError` or a version mismatch warning, you can recreate these files locally:

1. **Run the data fix script**:
   ```bash
   python fix_data.py
   ```
   *This script reads `top10K-TMDB-movies.csv` and generates fresh `.pkl` files compatible with your environment.*

## Running the Application

Start the Streamlit server:
```bash
streamlit run app.py
```

## Project Structure
- `app.py`: The main Streamlit application.
- `fix_data.py`: Utility script to resolve data incompatibility issues.
- `top10K-TMDB-movies.csv`: Source dataset.
- `frontend/`: Custom interactive components.
- `Movie Recommendation.ipynb`: Research and development notebook.

## Technologies Used
- **Frontend**: Streamlit, Svelte (custom component)
- **Backend**: Python
- **Data Science**: Pandas, Scikit-learn, Numpy
- **API**: TMDB API for movie posters
