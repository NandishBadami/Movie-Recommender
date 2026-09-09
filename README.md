# Movie Recommender App

Live Website link: https://movierecommender.pythonanywhere.com/

This project is built using kaggle movie datasets https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata which contains hollywood movies released between 1916 to 2017 only. First the dataset is being loaded into the app and then based on the given input(movie name) the recommendation engine provies similar movies by calculating the cosine similarity based on movie genres, title, actor and director, keywords and cast.

## How to use the app

You have to enter movie name in the input box with correct spellings and with correct case to match the movie that is present in the datasets. Example: Writing "spider man" is wrong ❌ because the correct name of the movie which was released in 2002 was "Spider-Man" ✅. You might have to google the movie name and then copy paste from google to get the correct recommendations(suggestions) for similar movies.