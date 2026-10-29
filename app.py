from html import escape

import streamlit as st
from main import MovieRecommender

st.set_page_config(
    page_title="Movie Recommendation",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Movie poster images are served by TMDB's public image CDN. The recommendation
# engine itself remains local and does not require a movie API key.
POSTER_BASE = "https://image.tmdb.org/t/p/w500/"
POSTERS = {
    "The Dark Knight": "qJ2tW6WMUDux911r6m7haRef0WH.jpg",
    "Batman Begins": "8RW2runSEc34IwKN2kyonk8Y9vT.jpg",
    "Iron Man": "78lPtwv72eTNqFW9COBYI0dWDJa.jpg",
    "The Avengers": "RYMX2wcKCBAr24UyPD7xwmjaTn.jpg",
    "Interstellar": "gEU2QniE6E77NI6lCU6MxlNBvIx.jpg",
    "Inception": "oYuLEt3zVCKq57qu2F8dT7NIa6f.jpg",
    "The Matrix": "f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg",
    "Toy Story": "uXDfjJbdP4ijW5hWSBrPrlKpxab.jpg",
    "Finding Nemo": "eHuGQ10FUzK1mdOY69wF5pGgEf5.jpg",
    "The Lion King": "sKCr78MXSLixwmZ8DyJLrpMsd15.jpg",
    "Forrest Gump": "saHP97rTPS5eLmrLQEcANmKrsFl.jpg",
    "Titanic": "9xjZS2rlVxm8SFx8kPC3aIGCOYQ.jpg",
    "Jurassic Park": "oU7Oq2kFAAlGqbU4VoAE36g4hoI.jpg",
    "The Martian": "5aGhaIHYuQbqlHWvWYqMCnj40y2.jpg",
    "John Wick": "fZPSd91yGE9fCcCe6OoQr6E3Bev.jpg",
    "Coco": "gGEsBPAijhVUFoiNpgZXqRVWJt2.jpg",
    "Shrek": "iB64vpL3dIObOtMZgX3RqdVdQDc.jpg",
    "Mission: Impossible - Fallout": "AkJQpZp9WoNdj7pLYSj1L0RcMMN.jpg",
    "The Social Network": "n0ybibhJtQ5icDqTp8eRytcIHJx.jpg",
}

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

    :root {
        --ink: #f7f5ff;
        --muted: #aaaac2;
        --panel: rgba(20, 22, 42, .76);
        --line: rgba(255,255,255,.10);
        --pink: #ff4f9a;
        --violet: #9a75ff;
        --cyan: #67e8f9;
    }

    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    [data-testid="stAppViewContainer"] {
        background:
          radial-gradient(ellipse at 6% 5%, rgba(126, 72, 224, .23), transparent 34%),
          radial-gradient(ellipse at 92% 16%, rgba(255, 79, 154, .12), transparent 30%),
          linear-gradient(145deg, #080913 0%, #111226 48%, #090a14 100%);
        color: var(--ink);
    }
    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stMainBlockContainer"] { max-width: 1440px; padding-top: 1.4rem; padding-bottom: 4rem; }
    #MainMenu, footer { visibility: hidden; }

    @keyframes riseIn { from {opacity:0; transform:translateY(18px)} to {opacity:1; transform:translateY(0)} }
    @keyframes glowPulse { 0%,100% {opacity:.58; transform:scale(1)} 50% {opacity:.95; transform:scale(1.07)} }
    @keyframes slowFloat { 0%,100% {transform:translateY(0)} 50% {transform:translateY(-8px)} }
    @keyframes shine { 0% {background-position:-180% 0} 100% {background-position:180% 0} }

    .hero {
        position: relative; overflow: hidden; isolation: isolate;
        padding: clamp(1.5rem, 4vw, 3.6rem); border-radius: 28px;
        border: 1px solid rgba(255,255,255,.14);
        background: linear-gradient(115deg, rgba(29,24,58,.95) 0%, rgba(23,19,43,.86) 54%, rgba(48,19,55,.82) 100%);
        box-shadow: 0 26px 90px rgba(0,0,0,.28); animation: riseIn .7s ease-out both;
        margin-bottom: 1.25rem;
    }
    .hero:before, .hero:after { content:""; position:absolute; border-radius:50%; filter:blur(2px); z-index:-1; pointer-events:none; }
    .hero:before { width:320px; height:320px; right:-60px; top:-150px; background:radial-gradient(circle, rgba(255,79,154,.34), transparent 68%); animation:glowPulse 7s ease-in-out infinite; }
    .hero:after { width:280px; height:280px; right:19%; bottom:-205px; background:radial-gradient(circle, rgba(103,232,249,.19), transparent 70%); animation:glowPulse 9s ease-in-out infinite reverse; }
    .eyebrow { color:#c9baff; font-size:.74rem; letter-spacing:.22em; font-weight:700; text-transform:uppercase; margin-bottom:.8rem; }
    .hero-title { font-family:'Space Grotesk',sans-serif; font-size:clamp(2.5rem,6vw,5rem); font-weight:700; line-height:1.02; letter-spacing:-.055em; margin:0; color:#fff; }
    .hero-title span { background:linear-gradient(100deg,#fff 4%,#d6c8ff 42%,#ff82ba 74%,#67e8f9 100%); background-size:200% auto; -webkit-background-clip:text; background-clip:text; color:transparent; animation:shine 8s linear infinite; }
    .hero-copy { max-width:650px; margin-top:1rem; font-size:1.04rem; line-height:1.75; color:#c2c1d9; }
    .hero-pill { display:inline-flex; align-items:center; gap:.5rem; margin-top:1.25rem; padding:.55rem .85rem; border-radius:999px; border:1px solid rgba(255,255,255,.13); background:rgba(255,255,255,.055); color:#e9e4ff; font-size:.82rem; }
    .section-kicker { color:#b8a5ff; font-size:.75rem; font-weight:700; text-transform:uppercase; letter-spacing:.17em; margin:1.35rem 0 .35rem; }
    .section-title { font-family:'Space Grotesk',sans-serif; font-weight:700; font-size:clamp(1.5rem,3vw,2.2rem); letter-spacing:-.035em; color:#fff; margin:.1rem 0 .35rem; }
    .section-copy { color:var(--muted); margin-bottom:1.1rem; }

    [data-testid="stTabs"] [data-baseweb="tab-list"] { gap:.5rem; border-bottom:1px solid var(--line); }
    [data-testid="stTabs"] button[role="tab"] { color:#b9b7cf; border-radius:12px 12px 0 0; padding:.75rem 1.1rem; }
    [data-testid="stTabs"] button[role="tab"][aria-selected="true"] { color:#fff; border-bottom:3px solid var(--pink); background:rgba(255,255,255,.045); }
    [data-testid="stSelectbox"], [data-testid="stMultiSelect"], [data-testid="stSlider"] { animation:riseIn .55s ease-out both; }
    [data-testid="stSelectbox"] label, [data-testid="stMultiSelect"] label, [data-testid="stSlider"] label { color:#e8e4ff !important; font-weight:600; }
    [data-baseweb="select"] > div { background:rgba(255,255,255,.055); border-color:rgba(255,255,255,.16); border-radius:12px; }
    [data-testid="stButton"] button { border-radius:12px; min-height:2.8rem; font-weight:700; transition:transform .2s ease, box-shadow .2s ease, border-color .2s ease; }
    [data-testid="stButton"] button[kind="primary"] { color:white; border:0; background:linear-gradient(100deg,#8058f5,#d9468a); box-shadow:0 8px 24px rgba(158,73,221,.24); }
    [data-testid="stButton"] button:hover { transform:translateY(-2px); box-shadow:0 12px 26px rgba(154,117,255,.25); }

    [data-testid="stVerticalBlockBorderWrapper"] { border:1px solid rgba(255,255,255,.11); border-radius:18px; background:linear-gradient(145deg,rgba(26,27,49,.82),rgba(17,18,34,.9)); box-shadow:0 10px 30px rgba(0,0,0,.12); transition:transform .25s ease,border-color .25s ease,box-shadow .25s ease; animation:riseIn .55s ease-out both; }
    [data-testid="stVerticalBlockBorderWrapper"]:hover { transform:translateY(-5px); border-color:rgba(189,157,255,.42); box-shadow:0 18px 42px rgba(0,0,0,.24); }
    [data-testid="stImage"] img { border-radius:12px; transition:transform .35s ease, filter .35s ease; }
    [data-testid="stImage"] img:hover { transform:scale(1.025); filter:saturate(1.12); }
    .poster-fallback { display:flex; aspect-ratio:2/3; width:100%; align-items:center; justify-content:center; flex-direction:column; gap:.6rem; border-radius:12px; background:radial-gradient(circle at 20% 15%,rgba(255,79,154,.45),transparent 35%),linear-gradient(145deg,#27204b,#101c36 65%,#451d47); color:white; text-align:center; padding:1rem; box-sizing:border-box; }
    .poster-fallback .clapper { font-size:2.4rem; animation:slowFloat 4s ease-in-out infinite; }
    .poster-fallback .poster-label { font-family:'Space Grotesk',sans-serif; font-size:1.05rem; font-weight:700; }
    .movie-name { font-family:'Space Grotesk',sans-serif; font-weight:700; font-size:1.04rem; line-height:1.3; color:#fff; margin:.7rem 0 .25rem; }
    .genre-line { color:#bcb8d5; font-size:.78rem; line-height:1.5; min-height:2.2rem; }
    .match-line { display:flex; justify-content:space-between; gap:.5rem; font-size:.75rem; color:#c9c5df; margin:.45rem 0 .25rem; }
    .tiny-tag { display:inline-block; border-radius:999px; padding:.25rem .55rem; color:#e4dcff; background:rgba(154,117,255,.14); border:1px solid rgba(154,117,255,.22); font-size:.7rem; }
    .stat-strip { display:flex; flex-wrap:wrap; gap:.6rem; margin-top:1.4rem; }
    .stat-chip { border:1px solid rgba(255,255,255,.12); border-radius:12px; background:rgba(255,255,255,.045); padding:.65rem .85rem; color:#d8d4ee; font-size:.83rem; }
    .footer-note { text-align:center; color:#777790; font-size:.76rem; padding:2.4rem 0 .4rem; }
    [data-testid="stAlert"] { border-radius:14px; }

    @media (prefers-reduced-motion: reduce) { *, *:before, *:after { animation:none !important; transition:none !important; scroll-behavior:auto !important; } }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <section class="hero">
      <div class="eyebrow">YOUR NEXT GREAT WATCH STARTS HERE</div>
      <h1 class="hero-title">Movie <span>Recommendation</span></h1>
      <p class="hero-copy">From mind-bending sci-fi to feel-good classics, discover films that fit your taste. Pick a movie you love or choose a mood through genres — we'll find your next watch.</p>
      <div class="hero-pill">✦ &nbsp; Personalized discovery &nbsp; · &nbsp; No sign-up needed</div>
      <div class="stat-strip">
        <div class="stat-chip">🎞️ &nbsp; Curated movie library</div>
        <div class="stat-chip">🧠 &nbsp; Content-based matching</div>
        <div class="stat-chip">⚡ &nbsp; Instant recommendations</div>
      </div>
    </section>
    """,
    unsafe_allow_html=True,
)

@st.cache_resource
def load_recommender():
    return MovieRecommender()

try:
    recommender = load_recommender()
except Exception as exc:
    st.error(f"Could not load the movie dataset: {exc}")
    st.stop()

movies = recommender.movies
movie_lookup = movies.set_index("title").to_dict(orient="index")
all_titles = recommender.list_movies()


def poster_url(title):
    filename = POSTERS.get(title)
    return f"{POSTER_BASE}{filename}" if filename else None


def show_poster(title, width=None):
    url = poster_url(title)
    if url:
        st.image(url, use_container_width=True)
    else:
        st.markdown(
            f'<div class="poster-fallback"><div class="clapper">🎬</div><div class="poster-label">{escape(title)}</div><div class="tiny-tag">MOVIE PICK</div></div>',
            unsafe_allow_html=True,
        )


def show_movie_card(movie, rank=None, score_label="Match"):
    title = str(movie.get("title", "Unknown title"))
    details = movie_lookup.get(title, {})
    with st.container(border=True):
        show_poster(title)
        if rank is not None:
            st.markdown(f'<span class="tiny-tag">#{rank} RECOMMENDED</span>', unsafe_allow_html=True)
        st.markdown(f'<div class="movie-name">{escape(title)}</div>', unsafe_allow_html=True)
        genres = escape(str(movie.get("genres", "")))
        st.markdown(f'<div class="genre-line">{genres}</div>', unsafe_allow_html=True)
        overview = str(details.get("overview", "")).strip()
        if overview:
            st.caption(overview)
        score = min(max(float(movie.get("score", 0.0)), 0.0), 1.0)
        st.markdown(
            f'<div class="match-line"><span>{escape(score_label)}</span><strong>{score:.0%}</strong></div>',
            unsafe_allow_html=True,
        )
        st.progress(score)


def show_results(results, score_label):
    if not results:
        st.info("No matching movies found. Try another title or genre.")
        return
    st.markdown('<div class="section-kicker">YOUR PICKS</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Recommended for you</div>', unsafe_allow_html=True)
    st.markdown("<div class=\"section-copy\">A few stories we think you'll enjoy next.</div>", unsafe_allow_html=True)
    columns = st.columns(3, gap="large")
    for index, movie in enumerate(results):
        with columns[index % 3]:
            show_movie_card(movie, rank=index + 1, score_label=score_label)


st.markdown('<div class="section-kicker">START EXPLORING</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">What are you in the mood for?</div>', unsafe_allow_html=True)
st.markdown('<div class="section-copy">Choose a starting point. Your results will appear below.</div>', unsafe_allow_html=True)

by_title_tab, by_genre_tab, library_tab = st.tabs(["🎬  By movie", "✦  By genre", "▦  Browse library"])

with by_title_tab:
    left, right = st.columns([1.25, 1], gap="large")
    with left:
        selected_title = st.selectbox("Choose a movie you already like", all_titles, key="selected_movie")
        count_title = st.slider("How many recommendations?", 1, 10, 5, key="title_count")
        if st.button("Find similar movies  →", type="primary", use_container_width=True, key="recommend_by_title"):
            st.session_state["movie_results"] = recommender.recommend(selected_title, count_title) or []
            st.session_state["movie_results_label"] = f"Because you chose {selected_title}"
            st.session_state["movie_score_label"] = "Content similarity"
    with right:
        st.markdown(
            '<div class="hero-pill">✦ &nbsp; Smart matching</div><h3 style="font-family:Space Grotesk,sans-serif;color:#fff;margin-top:1rem;">More movies. Same vibe.</h3><p style="color:#b9b6d0;line-height:1.7;">We compare each film’s genres and story description to find titles with similar themes — not just the same name or franchise.</p>',
            unsafe_allow_html=True,
        )
        show_poster(selected_title)

with by_genre_tab:
    genres = [
        "Action", "Adventure", "Animation", "Biography", "Comedy",
        "Crime", "Drama", "Family", "Romance", "Sci-Fi", "Thriller"
    ]
    selected_genres = st.multiselect("Pick one or more genres", genres, placeholder="Choose genres…", key="selected_genres")
    count_genre = st.slider("How many movies should we show?", 1, 10, 5, key="genre_count")
    if st.button("Explore these genres  →", type="primary", use_container_width=True, key="recommend_by_genre"):
        st.session_state["movie_results"] = recommender.recommend_by_genres(selected_genres, count_genre)
        st.session_state["movie_results_label"] = "Picked from your favorite genres"
        st.session_state["movie_score_label"] = "Genre match"

with library_tab:
    st.markdown('<div class="section-copy">Browse the movies in this demo library. Select a title in the “By movie” tab to discover similar stories.</div>', unsafe_allow_html=True)
    search_text = st.text_input("Search the library", placeholder="Try Interstellar, Coco, or Batman…", key="library_search")
    filtered_titles = [title for title in all_titles if search_text.casefold() in title.casefold()]
    st.caption(f"Showing {len(filtered_titles)} of {len(all_titles)} movies")
    catalog_columns = st.columns(4, gap="medium")
    for index, title in enumerate(filtered_titles):
        with catalog_columns[index % 4]:
            show_poster(title)
            st.markdown(f'<div class="movie-name">{escape(title)}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="genre-line">{escape(str(movie_lookup.get(title, {}).get("genres", "")))}</div>', unsafe_allow_html=True)

if st.session_state.get("movie_results") is not None:
    st.markdown("---")
    label = st.session_state.get("movie_results_label", "Your recommendations")
    st.caption(label)
    show_results(st.session_state["movie_results"], st.session_state.get("movie_score_label", "Match"))

st.markdown(
    '<div class="footer-note">Movie Recommendation · Poster images served from TMDB’s image CDN · Internet access is needed for poster artwork.</div>',
    unsafe_allow_html=True,
)
