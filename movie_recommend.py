from sklearn.impute import KNNImputer
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from PIL import Image
import os
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import normalize


class MovieRecommender:
    def __init__(self, rec_num=5, n_neighbors=10):
        self.rec_num = rec_num
        self.n_neighbors = n_neighbors

        self.df_raw = None
        self.df_filled = None

        self.df_favorite = None
        self.df_recommend_overall = None
        self.df_recommend_genres = []

        self.genres_label = None

    def _get_movie_list(self, df, user_no):
        return df.iloc[user_no, :]

    def _mask_raw_pos(self, df):
        return df.mask(~self.df_raw.isna().values, -1)

    @st.cache
    def _knn_fill(self):
        df_complete = KNNImputer(n_neighbors=self.n_neighbors).fit_transform(self.df_raw)
        df_complete = pd.DataFrame(df_complete, columns=self.df_raw.columns)
        return df_complete

    @st.cache
    def _pca_kmeans(self, k):
        df_normalized = normalize(self.df_filled.T, norm='l2')
        df_pca = PCA(n_components=3).fit_transform(df_normalized)

        clusterer = KMeans(n_clusters=k, random_state=30).fit(df_pca)
        preds = clusterer.predict(df_pca)
        return preds

    def load_data(self, file_path):
        df_raw = pd.read_csv(file_path)
        df_raw.columns = df_raw.columns.str.replace(":", "").str.replace("/", "")
        df_raw = df_raw.iloc[:, :400].dropna(how='all').reset_index(drop=True)
        self.df_raw = df_raw
        self.df_filled = self._knn_fill()

    def watched_movie_list(self, user_no):
        return self.df_raw.iloc[user_no, :].dropna().index

    @st.cache
    def favorite_overall(self, user_no):
        if not self.df_favorite:
            df_favorite_movie = self.df_raw.fillna(-1)
            self.df_favorite = pd.DataFrame(df_favorite_movie.values.argsort(axis=1)[:, -self.rec_num:]).applymap(
                lambda idx: df_favorite_movie.columns[idx])
        favorite_movies = self._get_movie_list(self.df_favorite, user_no)
        return favorite_movies

    @st.cache
    def recommend_overall(self, user_no):
        if not self.df_recommend_overall:
            df_filled_masked = self._mask_raw_pos(self.df_filled)
            self.df_recommend_overall = pd.DataFrame(
                df_filled_masked.values.argsort(axis=1)[:, -self.rec_num:]).applymap(
                lambda idx: df_filled_masked.columns[idx])
        recommended_movies = self._get_movie_list(self.df_recommend_overall, user_no)
        return recommended_movies


    def recommend_by_genres(self, user_no=None, movie_name=None, movie_no=None, k=3):
        if movie_name:
            movie_no = self.df_raw.columns.to_list().index(movie_name)

        if self.genres_label is None:
            self.genres_label = self._pca_kmeans(k)
        if len(self.df_recommend_genres) == 0:
            for label in range(k):
                df_filled_masked = self._mask_raw_pos(self.df_filled)
                df_within_cluster = df_filled_masked.loc[:, label == self.genres_label]
                df_within_cluster = pd.DataFrame(df_within_cluster.values.argsort(axis=1)[:, -self.rec_num:]).applymap(
                    lambda idx: df_within_cluster.columns[idx])
                self.df_recommend_genres.append(df_within_cluster)
        label = self.genres_label[movie_no]
        recommend_movies = self._get_movie_list(self.df_recommend_genres[label], user_no)
        return recommend_movies, label


def show_movies(movie_lst, save_dir):
    for idx, col in enumerate(st.columns(len(movie_lst))):
        movie = movie_lst[idx]
        save_path = os.path.join(save_dir, movie + ".png")
        with col:
            with open(save_path, 'rb') as f:
                image = Image.open(f)
                st.image(image)
                st.write(movie)


# Web page layout
st.write('''
    # Movie Recommender

    Created by [*Nuo Lei*](https://github.com/NuoLeiNYU)

    Highlights: **KNN**, **K-means**, **PCA**, **Data visualization**
    
    _*This demo focuses on showing my movie recommender's results. 
    Full data analysis and modeling notebook is uploaded on my 
    [github](https://github.com/NuoLeiNYU/movie-recommendation-system) 
    if you want more details!_
    ## 1.Introduction

    Movie recommendation is an exciting topic closely related to our daily lives.
    It saves our precious time and energy to choose from millions of movies.
    But no one could ever go through all millions of movies so as to make a good recommendation.
    So this is the time when data science techniques such as **K Nearest Neighbor (KNN)** and **K-means** can help.
    Here we will first use KNN model and then improve it with K-means clustering. Fun!
    
    ## 2. How does KNN work here?
    ### _A user-user approach_
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

    ## 3. Recommendation based on KNN
''')

movieRecommender = MovieRecommender()
movieRecommender.load_data('data/movieReplicationSet.csv')

# option to display raw data
if st.checkbox('Show raw rating data (with 1096 rows and 400 columns)'):
    st.subheader('Raw data')
    st.write(movieRecommender.df_raw)

st.write('### 👇 Explore here!')

# choose user number
user_no = st.selectbox(
    'Recommend movies to user No. (0 to 1095)',
    movieRecommender.df_raw.index)

favorite_movies = movieRecommender.favorite_overall(user_no)
recommend_movies = movieRecommender.recommend_overall(user_no)

col1, col2 = st.columns(2)

st.write("#### User {}'s favorite movies:".format(user_no))
show_movies(favorite_movies, 'image/')
st.write("#### Overall recommendations:")
show_movies(recommend_movies, 'image/')

st.write('''
    ## 4. Can we do more?
    
    ### What we have done
    
    Here we employed KNN model to complete the rating matrix.
    Therefore we can recommend movies for users by sorted rating.
    This method ensures that the recommendations are movies highly rated by like-mined people.
    
    ### Where to improve?
    Except for overall recommendation, we have a lot of other real-world scenarios!
    When I just finished a great movie, chances are that I would want more movies of the same kind.
    Well, clustering model can help us do that!
    
    In the next part, we will deploy the basic clustering model **K-means** to recommend movies in the same genre.

    ## 5. How does K-means work here
    
    ### _A item-item approach_
    
    The idea of K-means is quite similar to KNN with a little bit difference. 
    In the KNN part we want the average rating from K like-minded friends.
    But here we want more than that. We not only want to find similar movies, 
    but also want to further group them up and give each groups **meaningful interpretation**!
    
    In short by Silhouette score, our clustering result shows that there are **three** possible movie clusters. 
    We further take mean average and take a look at the top 10 movies in each group.
''')


st.write("### 🔍 Cluster visualiztion")
if st.checkbox('Show Clustering '):
    st.write("#### Determine parameter K with Silhouette score")
    with open('readme/silhouette_score.png', 'rb') as f:
        image = Image.open(f)
        st.image(image)
    with open('readme/inertia.png', 'rb') as f:
        image = Image.open(f)
        st.image(image)

    st.write("#### Clustering visualization in lower dimensions")
    with open('readme/kmeans_3d.png', 'rb') as f:
        image = Image.open(f)
        st.image(image)
    with open('readme/kmeans_2d.png', 'rb') as f:
        image = Image.open(f)
        st.image(image)


st.write('''
    Finally by observing the top 10 movies with the highest average rating, we can have a sense of what each cluster is made of.
    And they contains mainly:
    
    1. **Adventure and action movies**
    2. **Drama movies**
    3. **Horror and thriller**
    
''')

group_name = ['Adventure/Action', 'Drama','Horror/Thriller']
st.write("### 👇 Cluster result")
if st.checkbox('Show top 10 movies in each cluster'):
    movieRecommender.recommend_by_genres(user_no=0, movie_no=0)

    for idx in range(3):
        st.write('#### Top 10 movies in Group {}: ({})'.format(idx+1, group_name[idx]))
        series_top10 = movieRecommender.df_filled.loc[:, idx == movieRecommender.genres_label].T.mean(axis=1).nlargest(10)
        series_top10.name = 'ave_rating'
        st.table(series_top10)



####################### New part ######################

st.write('## 6. Recommendation based on KNN & K-means')
st.write('### 👇 Explore here')

user_no = st.selectbox(
    'Choose user No. (0 to 1095):',
    movieRecommender.df_raw.index)

watched_movie_list = movieRecommender.watched_movie_list(user_no)

movie_name = st.selectbox(
    'Choose one from the {} movies that the user has watched:'.format(len(watched_movie_list)),
    watched_movie_list)

recommend_movies, label = movieRecommender.recommend_by_genres(user_no = user_no, movie_name=movie_name)

dt = {0: 'Adventure/Action/Comedy', 1: 'Drama and more', 2: 'Horror/Thriller'}

st.write('''
    By kmeans clustering, this movie may belong to **{}** movies!
    
    Here are more top rated **{}** movies for you :smile:
'''.format(dt[label], dt[label]))

show_movies(recommend_movies, 'image/')

# movie_just_watched = st.selectbox(
#     'Recommend movies to user No. (0 to 1095)',
#     movieRecommender.df_raw.index)

# r = movieRecommender.recommend_by_genres(3, 5)
# st.write(r)


st.write('''
    ## 7. To do even better?
    ### More features!
    We can take into account many other factors such as **staring actors**, **director**, **language**, **area**, **length**, etc. 
    We can even employ NLP methods to analyse audiences' **movie reviews** and construct our own features!
    
    ### More samples!
    Our sample size 1097 is a big number. 
    But considering the huge user amount in movie companies database, we can of course simply do better by having a larger sample (With far more movies and more users!).
    
    ### More powerful models!
    We adopt KNN and K-means model because of their **simplicity** and good **interpretability**.
    But in industrial applications we may have much more to worry about, 
    like in model performance and speed in real-time recommendation and so on.
    So it is a discretionary call and we may employ more SOTA models in that case.
    
''')

st.write('''
    ## Thank you for exploring!
    
    Again, this website is for demonstration.
    
    A full data analysis notebook with source code is published [here](https://github.com/NuoLeiNYU/movie-recommendation-system).
    
    More on my [github](https://github.com/NuoLeiNYU).
''')
