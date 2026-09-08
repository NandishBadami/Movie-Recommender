from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import numpy as np
from ast import literal_eval
from django.conf import settings
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Create your views here.

credits_path = settings.BASE_DIR / 'recommender' / 'datasets' / 'tmdb_5000_credits.csv'
movies_path = settings.BASE_DIR / 'recommender' / 'datasets' / 'tmdb_5000_movies.csv'

movie_credits = pd.read_csv(credits_path)
movies = pd.read_csv(movies_path)

movie_credits.drop(['title'], axis=1, inplace=True)
movies_data = pd.merge(movies, movie_credits, left_on='id', right_on='movie_id')

movies_data = movies_data[~pd.isnull(movies_data['overview'])]

movies_data = movies_data.reset_index(drop=True)
movies_data['index']=movies_data.index

features = ['cast', 'crew', 'keywords', 'genres']
for __feature__ in features:
    movies_data[__feature__] = movies_data[__feature__].apply(literal_eval)

movies_data.head()

def get_keywords_list(keywords, is_cast=False):
    key_list = []
    if is_cast == True:
        count = 0
        for keyword_dict in keywords:
            if count == 3:
                break
            if 'name' in keyword_dict:
                key_list.append(keyword_dict['name'].lower().replace(" ", ''))
                count += 1
    else:
        for keyword_dict in keywords:
            if 'name' in keyword_dict:
                key_list.append(keyword_dict['name'].lower().replace(' ', ''))
    return key_list

movies_data['keywords_list'] = movies_data['keywords'].apply(lambda x: get_keywords_list(x))
movies_data['genres_list'] = movies_data['genres'].apply(lambda x:get_keywords_list(x))
movies_data['cast_list'] = movies_data['cast'].apply(lambda x: get_keywords_list(x, True))

def get_director(crew):
    for crew_dict in crew:
        if crew_dict['job'].lower() == 'director':
            return crew_dict['name'].lower().replace(" ", '')
        
    return 'no director'

movies_data['director'] = movies_data['crew'].apply(lambda x: get_director(x))

movies_data['keywords_string'] = movies_data['keywords_list'].apply(lambda x: ','.join(x))
movies_data['genres_string'] = movies_data['genres_list'].apply(lambda x: ','.join(x))
movies_data['cast_string'] = movies_data['cast_list'].apply(lambda x: ','.join(x))

movies_data['features_text'] = movies_data['keywords_string'] + ' ' + movies_data['genres_string'] + ' ' + movies_data['cast_string'] + ' ' + movies_data['director']

count_vectoriser = CountVectorizer(stop_words='english')
count_vectoriser_matrix = count_vectoriser.fit_transform(movies_data['features_text'])

cosine_sim = cosine_similarity(count_vectoriser_matrix)

title_index_mapping = movies_data[['title', 'index']]

def get_recommendation(title, cosine_sim=cosine_sim, top_n=10, title_index_map=title_index_mapping):
    title_idx = title_index_map.loc[title_index_map['title'] == title, 'index'].tolist()
    
    if title_idx:
        sim_scores = list(enumerate(cosine_sim[title_idx[0]]))

        sim_scores = sorted(sim_scores, key = lambda score: score[1], reverse=True)

        sim_scores = [(score[0], score[1]) for score in sim_scores if score[0] != title_idx[0]]

        top_scores = sim_scores[:top_n]

        top_movies = [title_index_map.loc[title_index_map['index'] == scores[0], 'title'].tolist()[0] for scores in top_scores]

        return top_movies
    else:
        return 'Movie is not present in the dataset or movie name has not been entered properly'

def home(request):
    if(request.GET.get('name')):
        movies = get_recommendation(request.GET.get('name'))
        if type(movies) == list:
            return render(request, 'index.html', {'movies': movies, 'name': request.GET.get('name')})
        else:
            return render(request, 'index.html', {'error': movies})
    return render(request, 'index.html')