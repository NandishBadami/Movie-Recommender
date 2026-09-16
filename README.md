# Movie Recommender App

Live Website link: https://movierecommender.pythonanywhere.com/

This project is built using kaggle movie datasets https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata which contains hollywood movies released between 1916 to 2017 only. First the dataset is being loaded into the app and then based on the given input(movie name) the recommendation engine provies similar movies by calculating the cosine similarity based on movie genres, title, actor and director, keywords and cast.

## How to use the app

You have to enter movie name in the input box and have to select the movie in the dropdown menu so that correct spellings and case of the movie title will be matched and selected. If a movie is not showing up in the dropdown then the movie is just not present in the dataset.