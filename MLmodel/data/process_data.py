import sys

from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import re

def load_data(messages_filepath, categories_filepath):
    # import datsets
    messages = pd.read_csv(messages_filepath).reset_index()
    categories = pd.read_csv(categories_filepath).reset_index()
    # merge datasets
    keepcol = ['id','index','message', 'original', 'genre', 'categories']
    df = pd.merge(messages,categories,on='index',suffixes=('', '_1'))[keepcol]\
        .set_index('index')
    return df

def clean_data(df):    
    # create a dataframe of the 36 individual category columns
    categories = df['categories'].str.split(';',expand=True)
    
    # extract a list of new column names for categories.
    row = categories.iloc[0]
    category_colnames = [re.sub(r'-\d+', '', i) for i in row]
    
    # rename the columns of `categories`
    categories.columns = category_colnames
    
    for column in categories:
        # set each value to be the last character of the string
        categories[column] = categories[column].apply(lambda x: x[-1])

        # convert column from string to numeric
        categories[column] = pd.to_numeric(categories[column])
        
    # drop the original categories column from `df`
    df.drop('categories',axis=1,inplace=True)

    # concatenate the original dataframe with the new `categories` dataframe
    df = pd.concat([df,categories],axis=1)
    
    # drop duplicates
    if df.duplicated().sum() > 0:
        df = df.drop_duplicates()

    #remove possible erros in related column
    df = df[df['related'] != 2]
    return df

def save_data(df, database_filename):
    # convert DataFrame to SQL DataSet 
    engine = create_engine(f'sqlite:///{database_filename}')
    # If there already is a message table, it will be removed
    df.to_sql('messages', engine, index=False, if_exists='replace')


def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)
        
        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__':
    main()