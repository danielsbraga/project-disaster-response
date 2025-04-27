import pandas as pd
import numpy as np
import re
from sqlalchemy import create_engine

def load_data(messages_filepath, categories_filepath):
    """
    Load and merge messages and categories datasets
    
    Args:
        messages_filepath: Path to messages CSV file
        categories_filepath: Path to categories CSV file
        
    Returns:
        df: Merged DataFrame
    """
    # In a real scenario, you would load data from CSV files
    # messages = pd.read_csv(messages_filepath)
    # categories = pd.read_csv(categories_filepath)
    
    # For demonstration, we'll create sample data
    messages = pd.DataFrame({
        'id': range(1, 11),
        'message': [
            "Water is running out in our village, need help!",
            "Earthquake hit our town, buildings collapsed, need medical assistance",
            "Selling new shoes, 50% discount today only",
            "Flood has destroyed our crops, need food and shelter",
            "New movie released this weekend, don't miss it",
            "Hurricane approaching, need evacuation assistance",
            "Looking for a new job in marketing",
            "Fire in the forest near our community, need firefighters",
            "Happy birthday to my best friend!",
            "Tsunami warning, moving to higher ground"
        ],
        'original': [
            "Water shortage in village",
            "Earthquake, buildings down, need medical",
            "Shoe sale 50% off",
            "Flood destroyed crops",
            "New movie this weekend",
            "Hurricane coming",
            "Job search marketing",
            "Forest fire",
            "Happy birthday",
            "Tsunami warning"
        ],
        'genre': ['direct', 'news', 'direct', 'news', 'direct', 'news', 'direct', 'news', 'direct', 'news']
    })
    
    categories = pd.DataFrame({
        'id': range(1, 11),
        'categories': [
            'water-1;earthquake-0;food-0;medical-0;weather-0',
            'water-0;earthquake-1;food-0;medical-1;weather-0',
            'water-0;earthquake-0;food-0;medical-0;weather-0',
            'water-1;earthquake-0;food-1;medical-0;weather-0',
            'water-0;earthquake-0;food-0;medical-0;weather-0',
            'water-0;earthquake-0;food-0;medical-0;weather-1',
            'water-0;earthquake-0;food-0;medical-0;weather-0',
            'water-0;earthquake-0;food-0;medical-0;weather-0',
            'water-0;earthquake-0;food-0;medical-0;weather-0',
            'water-0;earthquake-0;food-0;medical-0;weather-1'
        ]
    })
    
    # Merge datasets
    df = pd.merge(messages, categories, on='id')
    
    return df

def clean_data(df):
    """
    Clean the merged DataFrame
    
    Args:
        df: Merged DataFrame
        
    Returns:
        df: Cleaned DataFrame
    """
    # Create a dataframe of the individual category columns
    categories = df['categories'].str.split(';', expand=True)
    
    # Extract column names
    row = categories.iloc[0]
    category_colnames = row.apply(lambda x: x.split('-')[0])
    categories.columns = category_colnames
    
    # Convert category values to 0 or 1
    for column in categories:
        categories[column] = categories[column].str[-1]
        categories[column] = categories[column].astype(int)
    
    # Replace categories column with new category columns
    df = df.drop('categories', axis=1)
    df = pd.concat([df, categories], axis=1)
    
    # Remove duplicates
    df = df.drop_duplicates()
    
    return df

def save_data(df, database_filename):
    """
    Save DataFrame to SQLite database
    
    Args:
        df: Cleaned DataFrame
        database_filename: Path to SQLite database
    """
    engine = create_engine(f'sqlite:///{database_filename}')
    df.to_sql('DisasterResponse', engine, index=False, if_exists='replace')

def main():
    """
    Main function to run the ETL pipeline
    """
    print('Loading data...')
    df = load_data('messages.csv', 'categories.csv')
    
    print('Cleaning data...')
    df = clean_data(df)
    
    print('Saving data...')
    save_data(df, 'DisasterResponse.db')
    
    print('Cleaned data saved to database!')

if __name__ == '__main__':
    main()
