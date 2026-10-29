# Movie Recommendation

A small web app that recommends movies by a selected title or by preferred genres. The interface is built with Streamlit; recommendations use content-based filtering with TF-IDF vectors and cosine similarity.

## Features
- Discover movies similar to a chosen title.
- Recommend films by one or more genres.
- Browse and search the included movie catalog.
- Animated dark-cinematic interface with movie poster cards.
- Local sample dataset; no movie API key is needed for recommendations.

## Project files
```text
Movie_Recommendation/
├── app.py             # Streamlit web interface
├── main.py            # Recommendation logic
├── movies.csv         # Sample movie catalog
├── requirements.txt   # Python dependencies
├── README.md
└── TESTING.md
```

## Requirements
- Python 3.9 or later
- Internet access to install libraries and load remote poster images

## Install and run on Windows
Open a terminal in the folder that contains `app.py` and `requirements.txt`.

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Open the local URL shown by Streamlit, usually `http://localhost:8501`. Keep the terminal open while using the app. Press `Ctrl+C` in the terminal to stop it.

If a virtual environment already exists in a parent folder, use that environment's Python executable instead of creating a second `.venv`.

## How recommendations work
The app combines each movie's genre labels and overview, converts that text to TF-IDF vectors, and ranks similar movies using cosine similarity. Genre-based recommendations match the selected genre labels against each film's genres.

## Image note
Poster artwork is loaded from TMDB's image CDN, so the posters require internet access. The recommendation engine and sample data run locally. This demonstration is not endorsed or certified by The Movie Database (TMDB).
