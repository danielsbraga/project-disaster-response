# import libraries
import pandas as pd
import numpy as np
import random

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.neighbors import NearestNeighbors

from scipy.sparse import csr_matrix

from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk
nltk.download(['punkt', 'wordnet'])

class DataProcessor:
    """
    DataProcessor class to handle data preprocessing, tokenization, vectorization, and resampling for imbalance handling.
    """
    def __init__(self):
        self.count_vectorizer = None
        self.tfidf_transformer = None
    
    def tokenize(self, text_data):
        """
        Tokenize and lemmatize text data.
        
        Args:
            text_data (str): Text data to tokenize.
        
        Returns:
            list: List of tokenized and lemmatized words.
        """
        tokens = word_tokenize(text_data)
        lemmatizer = WordNetLemmatizer()
        return [lemmatizer.lemmatize(tok).lower().strip() for tok in tokens]
    
    def vectorize_transform(self, df):
        """
        Vectorize and transform text data using CountVectorizer and TfidfTransformer.
        
        Args:
            df (pd.Series): Series of text data.
        
        Returns:
            tuple: Tuple containing transformed text data, CountVectorizer, and TfidfTransformer.
        """
        self.count_vectorizer = CountVectorizer(tokenizer=self.tokenize, token_pattern=None, ngram_range=(1, 3))
        self.tfidf_transformer = TfidfTransformer()
        text_data_counts = self.count_vectorizer.fit_transform(df)
        text_data_tfidf = self.tfidf_transformer.fit_transform(text_data_counts)
        return text_data_tfidf, self.count_vectorizer, self.tfidf_transformer
    
    def get_tail_label(self, df):
        """
        Identify tail labels (minority class) in the dataframe based on imbalance ratio.
        
        Args:
            df (pd.DataFrame): DataFrame containing target labels.
        
        Returns:
            list: List of tail labels.
        """
        columns = df.columns
        n = len(columns)
        irpl = np.zeros(n)
        for column in range(n):
            irpl[column] = df[columns[column]].value_counts()[1]
        irpl = max(irpl) / irpl
        mir = np.average(irpl)
        tail_label = [columns[i] for i in range(n) if irpl[i] > mir]
        return tail_label
    
    def get_index(self, df):
        """
        Get indices of minority instances based on tail labels.
        
        Args:
            df (pd.DataFrame): DataFrame containing target labels.
        
        Returns:
            list: List of indices for minority instances.
        """
        tail_labels = self.get_tail_label(df)
        index = set()
        for tail_label in tail_labels:
            sub_index = set(df[df[tail_label] == 1].index)
            index = index.union(sub_index)
        return list(index)
    
    def get_minority_instance(self, X, y):
        """
        Get minority instances from the feature and target data.
        
        Args:
            X (pd.DataFrame): Feature data.
            y (pd.DataFrame): Target data.
        
        Returns:
            tuple: Tuple containing minority feature and target data.
        """
        index = self.get_index(y)
        X_sub = X[X.index.isin(index)].reset_index(drop=True)
        y_sub = y[y.index.isin(index)].reset_index(drop=True)
        return X_sub, y_sub
    
    def nearest_neighbour(self, X):
        """
        Find nearest neighbors for the given data.
        
        Args:
            X (pd.DataFrame): Feature data.
        
        Returns:
            ndarray: Indices of nearest neighbors.
        """
        nbs = NearestNeighbors(n_neighbors=5, metric='euclidean', algorithm='kd_tree').fit(X)
        _, indices = nbs.kneighbors(X)
        return indices
    
    def MLSMOTE(self, X, y, n_sample, indices):
        """
        Apply Multi-label Synthetic Minority Over-sampling Technique (MLSMOTE) to the data.
        
        Args:
            X (pd.DataFrame): Feature data.
            y (pd.DataFrame): Target data.
            n_sample (int): Number of samples to generate.
            indices (ndarray): Indices of nearest neighbors.
        
        Returns:
            tuple: Tuple containing resampled feature and target data.
        """
        X = pd.DataFrame(X.toarray())
        n = len(indices)
        new_X = np.zeros((n_sample, X.shape[1]))
        target = np.zeros((n_sample, y.shape[1]))

        for i in range(n_sample):
            reference = random.randint(0, n - 1)
            neighbour = random.choice(indices[reference, 1:])
            all_point = indices[reference]
            nn_df = y[y.index.isin(all_point)]
            ser = nn_df.sum(axis=0, skipna=True)
            target[i] = np.array([1 if val > 2 else 0 for val in ser])
            ratio = random.random()
            gap = X.loc[reference, :] - X.loc[neighbour, :]
            new_X[i] = np.array(X.loc[reference, :] + ratio * gap)

        new_X = pd.DataFrame(new_X, columns=X.columns)
        target = pd.DataFrame(target, columns=y.columns)
        target = pd.concat([y, target], axis=0)
        new_X = pd.concat([X, new_X], axis=0)
        new_X = csr_matrix(new_X.values)
        return new_X, target
    
    def vectorize_test(self, text_data):
        """
        Vectorize and transform test text data using fitted CountVectorizer and TfidfTransformer.
        
        Args:
            text_data (pd.Series): Series of text data.
        
        Returns:
            csr_matrix: Transformed text data.
        """
        text_data_counts = self.count_vectorizer.transform(text_data)
        text_data_tfidf = self.tfidf_transformer.transform(text_data_counts)
        return text_data_tfidf
    
    def fit_resample(self, X, y):
        """
        Fit and resample the data using MLSMOTE.
        
        Args:
            X (pd.DataFrame): Feature data.
            y (pd.DataFrame): Target data.
        
        Returns:
            tuple: Tuple containing resampled feature and target data.
        """
        X_sub, y_sub = self.get_minority_instance(X, y)
        indices = self.nearest_neighbour(X_sub)
        n_sample = len(y) - len(y_sub)
        return self.MLSMOTE(X_sub, y_sub, n_sample, indices)

class Resampler(BaseEstimator, TransformerMixin):
    """
    Custom transformer to apply the MLSMOTE resampling technique.
    """
    def __init__(self):
        self.processor = DataProcessor()
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        """
        Transform the data by applying MLSMOTE resampling.
        
        Args:
            X (pd.DataFrame): Feature data.
            y (pd.DataFrame): Target data.
        
        Returns:
            tuple: Tuple containing resampled feature and target data.
        """
        if y is None:
            return X
        return self.processor.fit_resample(X, y)

class TextProcessor(BaseEstimator, TransformerMixin):
    """
    Custom transformer to handle text vectorization using CountVectorizer and TfidfTransformer.
    """
    def __init__(self):
        self.count_vectorizer = CountVectorizer(tokenizer=DataProcessor().tokenize, token_pattern=None, ngram_range=(1, 3))
        self.tfidf_transformer = TfidfTransformer()
    
    def fit(self, X, y=None):
        """
        Fit the vectorizer and transformer on the text data.
        
        Args:
            X (pd.Series): Series of text data.
            y (pd.DataFrame, optional): Target data. Defaults to None.
        
        Returns:
            self: Fitted transformer.
        """
        text_data_counts = self.count_vectorizer.fit_transform(X)
        self.tfidf_transformer.fit(text_data_counts)
        return self

    def transform(self, X, y=None):
        """
        Transform the text data using the fitted vectorizer and transformer.
        
        Args:
            X (pd.Series): Series of text data.
            y (pd.DataFrame, optional): Target data. Defaults to None.
        
        Returns:
            csr_matrix: Transformed text data.
        """
        text_data_counts = self.count_vectorizer.transform(X)
        text_data_tfidf = self.tfidf_transformer.transform(text_data_counts)
        return text_data_tfidf