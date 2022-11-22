import imdb
import pandas as pd
from urllib.error import HTTPError
import time
import requests
import os
import re

ia = imdb.Cinemagoer()
data = pd.read_csv("../data/movieReplicationSet.csv").iloc[:, :400]
data.columns = data.columns.str.replace(":", "").str.replace("/", "")


def download_movie_cover(ia, movie, save_dir):
    try:
        similar_movies = ia.search_movie(movie)
    except:
        similar_movies = ia.search_movie(" ".join(re.findall("[a-zA-Z]+", movie)))
    try:
        url = similar_movies[0]["full-size cover url"]
    except:
        url = similar_movies[1]["full-size cover url"]
    print(url)
    save_path = os.path.join(save_dir, movie + ".png")
    r = requests.get(url)
    if r.status_code == 200:
        with open(save_path, "wb") as f:
            f.write(r.content)


def check_exist(movie, save_dir):
    return os.path.exists(os.path.join(save_dir, movie + ".png"))


while True:
    i = 0
    while i < len(data.columns):
        movie = data.columns[i]
        if check_exist(movie, '../image/'):
            i += 1
            continue
        print(i)
        print(movie)
        if i % 10 == 0:
            print("Downloaded Images:", i)

        try:
            download_movie_cover(ia, movie, "../image/")
        except:
            print("Error: ", movie)
            i -= 1
        time.sleep(10.3)
        i += 1