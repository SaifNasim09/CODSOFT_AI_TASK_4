# Movie Recommendation System

## Project Overview

Movie Recommendation System is a Python-based web application developed to recommend movies based on user preferences. It uses **content-based filtering** to suggest similar movies based on their genres and descriptions. The application allows users to search for a movie title, explore recommendations by preferred genres, and browse the available movie collection.

## Features

- **Movie-Based Recommendations:** Suggests movies similar to a selected movie title.
- **Genre-Based Recommendations:** Recommends movies based on user-selected genres.
- **Movie Library:** Displays available movies along with their titles and genres.
- **Similarity Scores:** Shows text-similarity scores to indicate how closely recommended movies match the selected movie.
- **Interactive Web Interface:** Provides a user-friendly interface for exploring movie recommendations.
- **Local Dataset:** Uses a sample movie dataset without requiring an external movie API key.

## Technologies Used

- **Programming Language:** Python
- **Web Framework:** Streamlit
- **Data Processing:** Pandas
- **Machine Learning:** Scikit-learn
- **Recommendation Techniques:** TF-IDF Vectorization and Cosine Similarity
- **Dataset:** CSV file containing movie titles, genres, and descriptions

## How It Works

1. The application loads movie titles, genres, and descriptions from a CSV dataset.
2. Movie genres and descriptions are combined to represent each movie's content.
3. TF-IDF Vectorization converts the textual information into numerical vectors.
4. Cosine Similarity measures the similarity between movie representations.
5. The system ranks similar movies and displays recommendations based on the selected title or preferred genres.
6. Users can explore the recommended movies through the web interface.

## Getting Started

### Prerequisites

- Python 3.9 or a compatible newer version.
- Visual Studio Code or another code editor.
- An internet connection to install the required libraries.

### Installation and Execution

1. Download or clone the project repository.
2. Extract the project files and open the project folder in your preferred code editor.
3. Open a terminal in the project directory.
4. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Run the Streamlit web application:

   ```bash
   streamlit run app.py
   ```

6. Open the local URL displayed in the terminal, usually `http://localhost:8501`.
7. Select a movie or preferred genres to explore recommendations.

**Note:** Ensure that `app.py`, `main.py`, `movies.csv`, and `requirements.txt` are available in the project folder.

## Learning Outcomes

This project provides practical experience in Python programming, data preprocessing, text vectorization, similarity measurement, content-based recommendation techniques, and interactive web application development. It also demonstrates how machine learning concepts can be applied to build a personalized movie discovery system.

## Project Purpose

The purpose of this project is to demonstrate how content-based filtering can recommend relevant movies using their textual descriptions and genres. It provides a simple and interactive way for users to discover movies based on their interests without requiring user-rating histories or an external movie recommendation API.
