import streamlit as st
import pickle
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(
    page_title="CineMa - Movie Recommendations",
    page_icon="🎬",
    layout="wide"
)

# Custom CSS for beautiful styling
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
        color: white;
        border: none;
        padding: 0.75rem;
        font-size: 1.1rem;
        font-weight: bold;
        border-radius: 10px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    .movie-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 2px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s;
    }
    .movie-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
    }
    h1, h2, h3 {
        color: white !important;
    }
    .stSelectbox label, .stRadio label {
        color: white !important;
        font-size: 1.2rem !important;
        font-weight: bold !important;
    }
    .metric-container {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Load data from pickle files
new = pickle.load(open("movie_data.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))
    
# Recommendation function
def recommend(movie):
    index = new[new["title"] == movie].index[0]
    dist = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommendations = []
    for i in dist[1:11]:
        recommendations.append({
            'title': new.iloc[i[0]]['title'],
            'rating': new.iloc[i[0]]['rating'],
            'genre': new.iloc[i[0]]['genres'],
            'similarity': i[1]
        })
    return recommendations
    
# Top rated movies function
def get_top_rated():
    dist = sorted(list(enumerate(new['rating'])), reverse=True, key=lambda x: x[1])
    top_movies = []
    for i in dist[:50]:
        top_movies.append({
            'title': new.iloc[i[0]]['title'],
            'rating': new.iloc[i[0]]['rating'],
            'genre': new.iloc[i[0]]['genres']
        })
    return top_movies

# Header
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("<h1 style='text-align: center;'>🎬 CineMa</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #ffecd2; font-size: 1.3rem;'>Discover Your Next Favorite Movie</p>", unsafe_allow_html=True)

st.markdown("---")

# Sidebar for navigation
with st.sidebar:
    st.markdown("## 🎯 Navigation")
    page = st.radio("", ["🔍 Similar Movies", "⭐ Top Rated Movies"])
    
    st.markdown("---")
    st.markdown("### 📊 Statistics")
    st.metric("Total Movies", len(new))
    st.metric("Avg Rating", f"{new['rating'].mean():.1f}")
    st.metric("Genres", new['genres'].nunique())

# Main content
if page == "🔍 Similar Movies":
    st.markdown("<h2>🔍 Find Similar Movies</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        selected_movie = st.selectbox(
            "Select a movie to get recommendations:",
            options=new['title'].tolist()
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        search_button = st.button("🚀 Get Recommendations")
    
    if search_button or selected_movie:
        st.markdown(f"### Movies Similar to *{selected_movie}*")
        recommendations = recommend(selected_movie)
        
        if recommendations:
            for idx, movie in enumerate(recommendations, 1):
                col1, col2, col3, col4 = st.columns([0.5, 3, 1, 1])
                
                with col1:
                    st.markdown(f"<div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); border-radius: 50%; width: 50px; height: 50px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 1.5rem;'>{idx}</div>", unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"### {movie['title']}")
                    st.markdown(f"**Genre:** {movie['genre']}")
                
                with col3:
                    st.markdown(f"<div class='metric-container'><h3>⭐ {movie['rating']:.2f}</h3><p>Rating</p></div>", unsafe_allow_html=True)
                
                with col4:
                    match_percent = int(movie['similarity'] * 100)
                    st.markdown(f"<div class='metric-container'><h3>🎯 {match_percent}%</h3><p>Match</p></div>", unsafe_allow_html=True)
                
                st.markdown("---")

elif page == "⭐ Top Rated Movies":
    st.markdown("<h2>⭐ Top 50 Movies by Their Rating</h2>", unsafe_allow_html=True)
    
    top_movies = get_top_rated()
    
    for idx, movie in enumerate(top_movies, 1):
        col1, col2, col3 = st.columns([0.5, 3, 1])
        
        with col1:
            st.markdown(f"<div style='background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); border-radius: 50%; width: 50px; height: 50px; display: flex; align-items: center; justify-content: center; color: #333; font-weight: bold; font-size: 1.5rem;'>{idx}</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"### {movie['title']}")
            st.markdown(f"**Genre:** {movie['genre']}")
        
        with col3:
            st.markdown(f"<div class='metric-container'><h2>⭐ {movie['rating']:.2f}</h2></div>", unsafe_allow_html=True)
        
        st.markdown("---")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #ffecd2;'>Made with ❤️ using Streamlit | Roman</p>", unsafe_allow_html=True)