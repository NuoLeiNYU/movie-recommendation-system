# KNN Movie Recommendation

Project highlights: **KNN**, **Recommendation System**, **Data Visualization**

_!!!Explore this project on our [online demo](http://nuolei-movie.streamlit.app) in one click !!!_

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

_!!!Explore this [online demo](http://nuolei-movie.streamlit.app) in one click!!!_

## 4. Conclusion

Here we employed KNN model to complete the rating matrix.
Therefore we can recommend movies for users by sorted rating.
This method ensures that the recommendations are movies highly rated by like-mined people.

But since it is a easy demo for KNN, here we do not consider other factors such as preferred **genres** and **staring actors**.
So it is possible that we make further improvement and make better recommendations considering these factors.

## Thank you for exploring!
Source code is published [here](https://github.com/NuoLeiNYU/movie-recommendation-system).

More on my [github](https://github.com/NuoLeiNYU).