# Testing checklist

Run the web app with `streamlit run app.py` and check:

1. The page title and heading display **Movie Recommendation** only.
2. The **By movie** tab returns recommendations for `The Dark Knight`.
3. The **By genre** tab returns results for Action and Sci-Fi.
4. The **Browse library** tab displays and filters the catalog.
5. Recommendation cards show title, genres, overview, and a match score.
6. An unknown or empty genre selection produces a helpful message.
7. The interface remains usable if some poster images cannot load.
