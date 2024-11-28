import pickle
import streamlit as st
import numpy as np

# Load artifacts
model = pickle.load(open('artifacts/model.pkl', 'rb'))
book_names = pickle.load(open('artifacts/book_names.pkl', 'rb'))
final_rating = pickle.load(open('artifacts/final_rating.pkl', 'rb'))
book_pivot = pickle.load(open('artifacts/book_pivot.pkl', 'rb'))

# Function to fetch poster URLs
def fetch_poster(suggestion):
    book_name = []
    ids_index = []
    poster_url = []

    for book_id in suggestion:
        book_name.append(book_pivot.index[book_id])

    for name in book_name[0]:
        ids = np.where(final_rating['title'] == name)[0][0]
        ids_index.append(ids)

    for idx in ids_index:
        url = final_rating.iloc[idx]['image_url']
        poster_url.append(url)

    return poster_url

# Function to recommend books
def recommend_book(book_name):
    books_list = []
    book_id = np.where(book_pivot.index == book_name)[0][0]
    distance, suggestion = model.kneighbors(book_pivot.iloc[book_id, :].values.reshape(1, -1), n_neighbors=4)

    poster_url = fetch_poster(suggestion)
    
    for i in range(len(suggestion[0])):
        book = book_pivot.index[suggestion[0][i]]
        books_list.append(book)
    
    return books_list[1:], poster_url[1:]  # Skip the input book itself

# Apply custom CSS for glassmorphism
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Page configuration
st.set_page_config(page_title='Book Recommendation System', layout='centered')

# Load CSS for styling
local_css("style.css")

# Add a fancy header with emojis
st.markdown("""
    <div class="glass">
        <h1>📚Book Finder📚</h1>
        <p>Let AI find your perfect book match.</p>
    </div>
""", unsafe_allow_html=True)

# Centered dropdown for book selection with glass effect
st.markdown("""
    <div class="glass">
        <p>🔎 Type or select a book from the dropdown</p>
    </div>
""", unsafe_allow_html=True)

# Dropdown for book selection
selected_books = st.selectbox("", book_names)

# Apply custom button styling to Streamlit's default button using CSS
st.markdown("""
    <style>
        .stButton > button {
            background: linear-gradient(135deg, #8B5E3C, #B8860B); /* Warm vintage gold-brown gradient */
            border: none;
            color: white; /* White text */
            padding: 12px 24px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 10px 5px;
            cursor: pointer;
            border-radius: 12px; /* Rounded corners for a soft vintage touch */
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.25); /* Soft, deep shadow for antique feel */
            font-family: 'Georgia', serif; /* Classic serif font for the button */
            text-transform: uppercase; /* Uppercase text for a formal touch */
        }

        .stButton > button:hover {
            background: linear-gradient(135deg, #704214, #B8860B); /* Slightly darker gold-brown */
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3); /* Stronger shadow for depth on hover */
            transform: translateY(-2px); /* Lift effect */
        }
    </style>
""", unsafe_allow_html=True)

# Streamlit button with custom styling applied
if st.button('Show Recommendation', key='show_recommendation_button'):
    recommended_books, poster_url = recommend_book(selected_books)

    # Display recommendations in a grid
    st.markdown("<h3>Recommended Books:</h3>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div class='glass'><p>{recommended_books[0]}</p></div>", unsafe_allow_html=True)
        st.image(poster_url[0])
    with col2:
        st.markdown(f"<div class='glass'><p>{recommended_books[1]}</p></div>", unsafe_allow_html=True)
        st.image(poster_url[1])
    with col3:
        st.markdown(f"<div class='glass'><p>{recommended_books[2]}</p></div>", unsafe_allow_html=True)
        st.image(poster_url[2])
