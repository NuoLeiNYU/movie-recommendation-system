# KNN Movie Recommendation

Project highlights: **KNN**, **Recommendation System**, **Data Visualization**

_!!!Explore this project on our [online demo](http://nuolei-movie.streamlit.app) in one click !!!_


## File tree

```bash
├─ data 
│  └─ movieReplicationSet.csv # 1097 people's rating of 400 movies.
├─ image # 400 movie posters for result visualization.
│  ├─ 10 Things I Hate About You (1999).png
│  ├─ 10000 BC (2008).png
│  ├─ 12 Monkeys (1995).png
   ...
│  ├─ Wing Commander (1999).png
│  ├─ X-Men (2000).png
│  ├─ X-Men 2 (2003).png
│  ├─ You're Next (2011).png
│  └─ Zoolander (2001).png
├─ readme
│  └─ demo_screenshot.png
├─ tools # web crawler for movie posters.
│  └─ get_movie_cover.py
├─ README.md
├─ movie_recommend.py # main py file for KNN recommendation and webpage rendering.
└─ requirements.txt

```

## 1. Introduction

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

_!!!Explore this [online demo](http://nuolei-movie.streamlit.app) in one click!!!_

![Example](readme/demo_screenshot.png)

## 4. Conclusion

Here we employed KNN model to complete the rating matrix.
Therefore we can recommend movies for users by sorted rating.
This method ensures that the recommendations are movies highly rated by like-mined people.

But since it is a easy demo for KNN, here we do not consider other factors such as preferred **genres** and **staring actors**.
So it is possible that we make further improvement and make better recommendations considering these factors.

## Thank you for exploring!
Source code is published [here](https://github.com/NuoLeiNYU/movie-recommendation-system).

More on my [github](https://github.com/NuoLeiNYU).