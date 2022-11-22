from sklearn.impute import KNNImputer
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from PIL import Image
import os


print(os.curdir)
print(os.listdir(os.curdir))


@st.cache
def load_data(file):
    data = pd.read_csv(file)
    data.columns = data.columns.str.replace(":", "").str.replace("/", "")
    data_movie = data.iloc[:, :400].dropna(how='all').reset_index(drop=True)
    return data_movie


@st.cache
def KNN_fill(data_movie):
    data_complete = KNNImputer(n_neighbors=10).fit_transform(data_movie)
    data_complete = pd.DataFrame(data_complete, columns=data_movie.columns)

    # Set already watched movies' rating to -1 so will not be recommended again
    data_recommend = data_complete.mask(~data_movie.isna().values, -1)
    return data_recommend


def favorite(data_movie):
    data_taste = data_movie.fillna(-1)
    return pd.DataFrame(data_taste.values.argsort(axis=1)[:, -5:]).applymap(lambda idx: data_taste.columns[idx])


def recommend(data_recommend):
    return pd.DataFrame(data_recommend.values.argsort(axis=1)[:, -5:]).applymap(lambda idx: data_recommend.columns[idx])


def get_movie_list(df, user_no):
    print()
    return df.iloc[user_no, :]


def show_movies(movie_lst, save_dir):
    for idx, col in enumerate(st.columns(len(movie_lst))):
        movie = movie_lst[idx]
        save_path = os.path.join(save_dir, movie + ".png")
        with col:
            with open(save_path, 'rb') as f:
                image = Image.open(f)
                st.image(image)
                st.write(movie)


# Data preperation
df_movie = load_data('.../data/movieReplicationSet.csv')
df_movie_filled = KNN_fill(df_movie)
df_favorite_movies = favorite(df_movie)
df_recommend_movies = recommend(df_movie_filled)

# Web page layout

st.write('''
    # KNN Movie Recommendation

    Created by [*Nuo Lei*](https://github.com/NuoLeiNYU)

    Highlights: **KNN**, **Recommendation System**, **Data Visualization**

    ## 1.Introduction

    Movie recommendation is an exciting topic closely related to our daily lives.
    It saves our precious time and energy to choose from millions of movies.
    But no one could ever go through all millions of movies so as to make a good recommendation.
    So this is the time when data science techniques such as **K Nearest Neighbor (KNN)** can help.

    ## 2. KNN Model 
    The idea of KNN model is quite intuitive. 
    Imagine that you are in a movie lover's club at NYC.
    You have fun and meet a bunch of friends who are eager to share you their favorite movies.
    Who's recommendation should you take? 
    The one who have the same taste just like you, or the one who disagree with your opinion on every single movie?
    Well, of course it is important sometimes to be open to different opinions. 
    But as for a movie to relax after a day of tiring work, I would go with the recommendation from my like-minded friends.

    KNN model just follows this intuition and asks for the opinion of $K$ like-minded 'friends'.
    With a similar taste, it is reasonable to assume that I would have a similar rating like my 'friends' though I haven't seen the movie yet.
    In this way, we successfully estimate the rating of movies by the average rating of like-minded people. 

    The following is a easy demo of 1097 people (one is missing) and their ratings for 400 movies (movies haven't seen are rated as NaN).
    Based on KNN, we can recommend movies for each of them!

    ## 3. Movie recommendation demo 
''')

# option to display raw data
if st.checkbox('Show raw rating data (with 1096 rows and 400 columns)'):
    st.subheader('Raw data')
    st.write(df_movie)

# choose user number
user_no = st.selectbox(
    'Recommend movies to user No. (0 to 1095)',
    df_movie.index)

favorite_movies = get_movie_list(df_favorite_movies, user_no)
recommend_movies = get_movie_list(df_recommend_movies, user_no)

st.write("### User {}'s result is as follow:".format(user_no))
col1, col2 = st.columns(2)


st.write("#### Favorite movies:")
show_movies(favorite_movies, '.../image/')
st.write("#### Recommendations:")
show_movies(recommend_movies, '.../image/')


st.write('''
    ## Conclusion
    
    Here we employed KNN model to complete the rating matrix.
    Therefore we can recommend movies for users by sorted rating.
    This method ensures that the recommendations are movies highly rated by like-mined people.
    
    But since it is a easy demo for KNN, here we do not consider other factors such as preferred **genres** and **staring actors**.
    So it is possible that we make further improvement and make better recommendations considering these factors.

    ## Thank you for exploring!
    More on my [github](https://github.com/NuoLeiNYU).
''')
