from pathlib import Path
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DATA_FILE = Path(__file__).with_name("movies.csv")


class MovieRecommender:
    """Content-based movie recommender using TF-IDF and cosine similarity."""

    def __init__(self, data_file=DATA_FILE):
        self.movies = pd.read_csv(data_file).fillna("")
        required = {"title", "genres", "overview"}
        if not required.issubset(self.movies.columns):
            raise ValueError(f"movies.csv must contain columns: {sorted(required)}")

        self.movies["content"] = (
            self.movies["genres"].astype(str) + " " +
            self.movies["overview"].astype(str)
        )
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.matrix = self.vectorizer.fit_transform(self.movies["content"])
        self.similarity = cosine_similarity(self.matrix)

    def list_movies(self):
        return self.movies["title"].tolist()

    def recommend(self, title, number=5):
        matches = self.movies.index[
            self.movies["title"].str.casefold() == title.strip().casefold()
        ].tolist()
        if not matches:
            return None

        chosen = matches[0]
        ranked = sorted(enumerate(self.similarity[chosen]),
                        key=lambda pair: pair[1], reverse=True)
        output = []
        for index, score in ranked:
            if index == chosen:
                continue
            row = self.movies.iloc[index]
            output.append({"title": row["title"], "genres": row["genres"],
                           "score": float(score)})
            if len(output) >= max(1, number):
                break
        return output

    def recommend_by_genres(self, genres, number=5):
        wanted = {g.strip().casefold() for g in genres if g.strip()}
        if not wanted:
            return []
        results = []
        for _, row in self.movies.iterrows():
            available = {g.casefold() for g in str(row["genres"]).split()}
            matched = wanted.intersection(available)
            if matched:
                results.append({
                    "title": row["title"],
                    "genres": row["genres"],
                    "score": len(matched) / len(wanted)
                })
        results.sort(key=lambda item: item["score"], reverse=True)
        return results[:max(1, number)]


def display(results):
    if not results:
        print("No recommendations found. Try a different title or genre.")
        return
    print("\nRecommended movies")
    print("-" * 55)
    for i, movie in enumerate(results, 1):
        print(f"{i}. {movie['title']} | Genres: {movie['genres']} "
              f"| Match score: {movie['score']:.2f}")


def main():
    try:
        recommender = MovieRecommender()
    except (OSError, ValueError, pd.errors.ParserError) as error:
        print(f"Could not load the dataset: {error}")
        return

    print("\n=== MOVIE RECOMMENDATION ===")
    while True:
        print("\n1. Recommend by movie title")
        print("2. Recommend by preferred genres")
        print("3. Show all movies")
        print("4. Exit")
        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            title = input("Enter a movie title: ").strip()
            try:
                count = min(max(int(input("Number of recommendations (1-10): ")), 1), 10)
            except ValueError:
                count = 5
                print("Invalid number; showing 5 recommendations.")
            results = recommender.recommend(title, count)
            if results is None:
                print("Movie not found. Choose a title from option 3.")
            else:
                display(results)
        elif choice == "2":
            print("Example genres: Action, Adventure, Animation, Comedy, Drama, Romance, Sci-Fi")
            genres = input("Enter genres separated by commas: ").split(",")
            try:
                count = min(max(int(input("Number of recommendations (1-10): ")), 1), 10)
            except ValueError:
                count = 5
                print("Invalid number; showing 5 recommendations.")
            display(recommender.recommend_by_genres(genres, count))
        elif choice == "3":
            print("\nAvailable movies:")
            for title in recommender.list_movies():
                print("-", title)
        elif choice == "4":
            print("Thank you for using the recommender!")
            break
        else:
            print("Invalid choice. Enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
