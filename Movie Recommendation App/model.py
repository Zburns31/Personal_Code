#! usr/bin/env python3

""" This module is for containing the logic for the recommendation models. It includes the Popularity based recommender,
    Content based recommender, Collaborative filtering recommender and hybrid recommendaiton system

    Model Builder Class: Primary Responsibilities:
    - Ingest Clean, Pre-processed data
    - Feature Engineering
    - Providing Recommendations
    - Find similar users to the curent user to be able to do collaborative filtering

    TODO:
    https://medium.com/project-obhave/obhave-bayesian-front-end-game-of-user-stereotypes-902dd718c0a3#.lt35pfkx9
    clustering similar users to reduce very sparse matrix
    https://blog.codecentric.de/en/2019/07/recommender-system-movie-lens-dataset/
"""

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity

from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer as wnl
from nltk.corpus import wordnet
from stop_words import get_stop_words

stop_words = list(get_stop_words('en'))

import string
import pandas as pd
import numpy as np
from ast import literal_eval

# TODO: Decide whether to use taglines or not
feat_cols = ['genres', 'id', 'title', 'overview', 'popularity', 'year', 'keywords', #tagline
                'vote_average', 'vote_count', 'director', 'top_10_cast']

class ModelBuilder():

    def __init__(self,
                 model_type,
                 save_similarity_matrix = True,
                 data = './pre-processed.csv'
                 ):

        self.model_type = model_type
        self.save_similarity_matrix = save_similarity_matrix
        self.data = data

    def read_and_prep_data(self, data, columns, dtype_map = None, seperator = ','):
        return pd.read_csv(data, sep = seperator, usecols = columns, dtype = None)


    def explode_col_lis_to_feats(self, df, target_col):
        unique_values = df[target_col].apply(pd.Series).stack().value_counts().index.tolist()
        
        # add a prefix to each element
        new_cols = ["genre_" + i for i in unique_values]
        # fill in the column values
        for column in new_cols:
            df[column] = np.nan

        for col in new_cols:
            df.loc[:, col] = df.apply(lambda x: 1 if col[6:] in x["genres"] else 0, 1)
        
        return df.drop(target_col, axis=1)

    def remove_stop_words(self, df, cols):
        """ Helper function for removing stop words and punctuation
        """ 
        for col in cols:
            
            df[col] = df[col].astype('str') 
            df[col] = df[col].apply(lambda x: [word for word in x.split() if word not in stop_words])
            df[col] = df[col].apply(lambda x: [''.join(c for c in s if c not in string.punctuation) for s in x])
            df[col] = df[col].apply(lambda x: list(filter(None, x)))

        return df


    def run(self, model_type, save_sim_matrix, data):


        df = self.read_and_prep_data(data, columns = feat_cols)

        # Lists and other object types (not primitive) are loaded as string representations in csv format
        str_rep_cols = ['genres', 'director', 'top_10_cast', 'keywords']
        for col in str_rep_cols:
            df[col] = df[col].fillna('[]').apply(lambda x: literal_eval(x))

        new_df = self.explode_col_lis_to_feats(df, 'genres')
        cleaned_df = self.remove_stop_words(new_df, cols = ['overview', 'keywords'])



        return cleaned_df





if __name__ == '__main__':

    pop_recommender = ModelBuilder(model_type = 'popularity_rec')
    df = pop_recommender.run(model_type = pop_recommender.model_type, 
                             save_sim_matrix = pop_recommender.save_similarity_matrix, 
                             data = pop_recommender.data)



