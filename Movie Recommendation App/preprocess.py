""" This file is used for ingesting, cleaning and preprocessing data before it can be used to provide recommendations

    TODO: The script should download the files from MovieLen's dataset into the current directory so they can be used
    - The option should be given to use a pre-trained file for the user if they want a quick recommendation
"""
import os
import pandas as pd
import numpy as np

from datetime import datetime as dt
from ast import literal_eval

from nltk import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer

current_date = str(dt.now())[0:10]

###############################################################################
# Data Files to be used

# final_df_loc = './clean_and_joined_movies.csv'
final_df_loc = None

###############################################################################

class DatasetCleaner():
    """ This class is to help with data ingestion, cleaning and pre-processing before passing the data
        onto the pre-features class for feature engineering
        TODO: Movies and tags datasets are not being used currently. Tags is missing tags for lots of movies
         - Will need to come back to this to see if there are other options
    """

    def __init__(self,
                 name,
                 metadata = './ml-latest-small/movies_metadata.csv',
                 credits = './ml-latest-small/credits.csv',
                 keywords = './ml-latest-small/keywords.csv',
                 ratings = './ml-latest-small/ratings.csv',
                 tags = './ml-latest-small/tags.csv',
                 movies = './ml-latest-small/movies.csv'):

        self.name = name
        self.metadata = metadata
        self.credits = credits
        self.keywords = keywords
        self.ratings = ratings
        self.tags = tags
        self.movies = movies


    def read_data(self, df_loc, columns_to_drop=[], seperator = ','):

        return pd.read_csv(df_loc, sep = seperator).drop(columns = columns_to_drop)


    def join_tables(self, left_table, right_table, on_col, type_of_join=None):

        if not type_of_join:
            return left_table.merge(right_table, on = on_col)
        
        return left_table.merge(right_table, on = on_col, how = type_of_join)

    
    def fix_str_repr_cols(self, df, col_to_fix, func = literal_eval, default_null_value = '[]'):
        """ This function is to help with fixing columns which are read into the DF
            as a string representation. E.g. When reading in the metadata.csv file, genres are
            loaded as a string representation of a list
        """

        return df[col_to_fix].fillna(default_null_value).apply(lambda x: func(x))

    # Todo: need to fix this
    def fix_bad_num_cols(self, df, col, cast_type=None):
        """ This function is to help with finding bad records
        """

        try:
            print('Trying to convert column {col} to numeric type')
            if not cast_type:
                df[col] = pd.to_numeric(df[col], errors = 'coerce')
                print('Column {col} successfully changed')
                return df
            
            df[col] = df[col].astype(cast_type)
            print('Column {col} successfully changed')
            return df
            
        except ValueError:
            print('Error raised, trying to correct')
            mask = pd.to_numeric(df[col], errors = 'coerce').isnull()
            bad_values = df.loc[mask, 'id'].tolist()
            
            print(f'Records not converted are: {bad_values}')
            bad_records = df.index[df[col].isin(bad_values)]
            clean_table = df.drop(bad_records, axis =0)
            clean_table[col] = clean_table[col].astype(cast_type)

            print('Column {col} successfully changed')
            return clean_table


    def run(self, time_stamp = current_date, save_output = True, output_loc = final_df_loc):

        ###############################################################################
        # data Ingestion

        metadata_df = self.read_data(self.metadata, 
                                     columns_to_drop = ['belongs_to_collection', 'poster_path', 'homepage',
                                                        'production_companies', 'production_countries',
                                                        'revenue', 'runtime', 'spoken_languages', 'budget',
                                                        'status', 'video', 'imdb_id'])

        credits_df = self.read_data(self.credits)

        keywords_df = self.read_data(self.keywords)

        ratings_df = self.read_data(self.ratings, columns_to_drop = ['timestamp'])

        tags_df = self.read_data(self.tags, columns_to_drop = ['timestamp'])

        ###############################################################################
        # Processing & Cleaning

        # A few columns need to be fixed before we can move on. Genres in metadata_df is a list of dictionaries,
        # so we need to extract the genres into a list
        metadata_df['genres'] = self.fix_str_repr_cols(metadata_df, 'genres', func=literal_eval)
        metadata_df['genres'] = metadata_df['genres'].apply(lambda x: [elem['name'] for elem in x])
        # return metadata_df

        metadata_df['year'] = pd.to_numeric(metadata_df['release_date'].apply(
                                                lambda x: str(x).split('-')[0] if x != np.nan else np.nan),
                                            errors = 'coerce').fillna(0)
        
        # Need to convert to numeric/float to handle NaN's first, fill the null values with 0 and then convert to int
        metadata_df['year'] = metadata_df['year'].astype('int')
                                                    
        tags_df = tags_df.rename(columns = {'movieId': 'id'})

        # need to make sure ID columns are of all type INT before joining into 1 table
        # TODO:  This wont work for some reason
        # for df in [metadata_df, credits_df, keywords_df, tags_df]:
        #     df = self.fix_bad_num_cols(df, 'id', 'int')

        clean_meta_df = self.fix_bad_num_cols(metadata_df, 'id', 'int')
        clean_credits_df = self.fix_bad_num_cols(credits_df, 'id', 'int')
        clean_keywords_df = self.fix_bad_num_cols(keywords_df, 'id', 'int')
        # clean_tags_df = self.fix_bad_num_cols(tags_df, 'id', 'int')

        # Tags are done on a user basis. So we need to collect all the tags per movie
        # clean_tags_df = clean_tags_df.groupby('id').agg({'tag': lambda x: list(set(x))})

        # return clean_meta_df, clean_credits_df, clean_keywords_df, clean_tags_df

        # Now we need to join all the extra columns into one merged DF so it can be used for feature engineering
        joined_df = clean_meta_df.merge(clean_credits_df, on = 'id', how = 'left')\
                                 .merge(clean_keywords_df, on = 'id', how = 'left')

        

        joined_df['keywords'] = self.fix_str_repr_cols(joined_df, 'keywords')
        joined_df['crew'] = self.fix_str_repr_cols(joined_df, 'crew')
        joined_df['cast'] = self.fix_str_repr_cols(joined_df, 'cast')

        joined_df['keywords'] = joined_df['keywords'].apply(lambda x: [i['name'] for i in x])
        joined_df['director'] = joined_df['crew'].apply(lambda x: [i['name'] for i in x if i['job'] == 'Director'])
        joined_df['cast'] = joined_df['cast'].apply(lambda x: [i['name'] for i in x])
        joined_df['top_10_cast'] = joined_df['cast'].apply(lambda x: x[0:11] if len(x) > 10 else x)


        joined_df['cast'] = joined_df['cast'].apply(lambda x: [str.lower(i.replace(' ', '')) for i in x])
        joined_df['director'] = joined_df['director'].apply(lambda x: [str.lower(i.replace(' ', '')) for i in x])
        # We want to lemmatize only the single words and keep the phrases together in the keywords
        
        if save_output:
            if final_df_loc:
                joined_df.to_csv(final_df_loc)
            else:
                joined_df.csv_path = 'pre-processed.csv'
                current_directory = os.getcwd()
                joined_df.to_csv(joined_df.csv_path)



if __name__ == '__main__':

    clean_data = DatasetCleaner(name='movie_data')
    df = clean_data.run(save_output=True)