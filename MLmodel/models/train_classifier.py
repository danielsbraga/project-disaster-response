# import libraries
from imblearn.over_sampling import RandomOverSampler
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import joblib
import sys

# import sklearn libraries
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.multioutput import MultiOutputClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline

# import custom classes
from dataprocessor import TextProcessor, Resampler

def load_data(database_filepath):
    """
    Load data from the SQLite database.
    
    Args:
        database_filepath (str): Filepath of the SQLite database.
    
    Returns:
        tuple: Tuple containing feature and target data for related and multi-label classification.
    """
    engine = create_engine(f'sqlite:///{database_filepath}')
    with engine.connect() as connection:
        df = pd.read_sql("SELECT * FROM messages", connection)
    engine.dispose()
    
    # Split data into feature and target for related classification
    X_related = df['message']
    Y_related = df['related']

    # Split data into feature and target for multi-label classification
    df_related = df[df['related'] == 1]
    target_columns = [col for col in df.columns if col not in ['message', 'related', 'id', 'original', 'genre']]
    columns_to_drop = df_related[target_columns].sum() == 0
    columns_to_drop = columns_to_drop[columns_to_drop].index

    X_multi = df_related['message']
    Y_multi = df_related[target_columns]
    Y_multi = Y_multi.drop(columns=columns_to_drop, axis=1)

    return X_related, Y_related, X_multi, Y_multi

# First part functions - related classification
def balance_data_related(X, y):
    """
    Balance the data for related classification using RandomOverSampler.
    
    Args:
        X (pd.Series): Feature data.
        y (pd.Series): Target data.
    
    Returns:
        tuple: Tuple containing balanced feature and target data.
    """
    ros = RandomOverSampler(random_state=42)
    X_balanced, y_balanced = ros.fit_resample(X.to_frame(), y)
    X_train_balanced = X_balanced.squeeze()
    y_train_balanced = y_balanced
    return X_train_balanced, y_train_balanced

def build_model_related():
    """
    Build a model pipeline for related classification.
    
    Returns:
        GridSearchCV: Grid search model for related classification.
    """
    # Define the pipeline for related classification using FeatureUnion
    pipeline_related = Pipeline([
        ('vect', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('clf', RandomForestClassifier())
    ])

    # Define the parameter grid for related classification
    param_grid_related = {
        'clf__n_estimators': [100, 200],
        'clf__min_samples_split': [2, 5]
    }

    # Perform grid search for related classification
    cv_related = GridSearchCV(pipeline_related, param_grid_related, cv=2, scoring='precision_weighted', n_jobs=1, verbose=2)

    return cv_related

def evaluate_model_related(y_test, y_pred):
    """
    Evaluate the related classification model.
    
    Args:
        y_test (pd.Series): True target values.
        y_pred (pd.Series): Predicted target values.
    """
    related_precision = precision_score(y_test, y_pred, average='weighted')
    related_recall = recall_score(y_test, y_pred, average='weighted')
    related_f1 = f1_score(y_test, y_pred, average='weighted')
    related_accuracy = accuracy_score(y_test, y_pred)

    print(f'Related Classification - Precision: {related_precision:.4f}')
    print(f'Related Classification - Recall: {related_recall:.4f}')
    print(f'Related Classification - F1 Score: {related_f1:.4f}')
    print(f'Related Classification - Accuracy: {related_accuracy:.4f}')

def save_model_related(model, model_filepath):
    """
    Save the related classification model.
    
    Args:
        model (GridSearchCV): Trained model.
        model_filepath (str): Filepath to save the model.
    """
    # Print the best parameters and best score for related classification
    print(f'Best parameters found for related classification: {model.best_params_}')
    print(f'Best Precision score for related classification: {model.best_score_}')

    # Save the model and other files in the specified directory
    joblib.dump(model.best_estimator_, model_filepath)

# Second part functions - multi-label classification
def build_model_multi():
    """
    Build a model pipeline for multi-label classification.
    
    Returns:
        GridSearchCV: Grid search model for multi-label classification.
    """
    # Define the pipeline for multi-label classification
    pipeline_multi = Pipeline([
        ('text_processor', TextProcessor()),
        ('resample', Resampler()),
        ('clf', MultiOutputClassifier(estimator=RandomForestClassifier()))
    ])

    # Define the parameter grid for multi-label classification
    param_grid_multi = [
        {
            'clf__estimator__n_estimators': [100, 200],
            'clf__estimator__min_samples_split': [2, 5]
        },
        {
            'clf__estimator': [LogisticRegression(max_iter=1000)],
            'clf__estimator__C': [0.1, 1, 10],
            'clf__estimator__solver': ['liblinear', 'saga']
        }
    ]

    # Perform grid search for multi-label classification
    grid_search_multi = GridSearchCV(pipeline_multi, param_grid_multi, cv=2, scoring='precision_weighted', n_jobs=1, verbose=2)

    return grid_search_multi

def evaluate_model_multi(y_test, y_pred):
    """
    Evaluate the multi-label classification model.
    
    Args:
        y_test (pd.DataFrame): True target values.
        y_pred (np.ndarray): Predicted target values.
    """
    # Initialize lists to store the precision, recall, and f1-score for each label
    precision_list = []
    recall_list = []
    f1_list = []

    # Calculate precision, recall, and f1-score for each label
    for i, column in enumerate(y_test.columns):
        precision = precision_score(y_test[column], y_pred[:, i], average='weighted', zero_division=0)
        recall = recall_score(y_test[column], y_pred[:, i], average='weighted', zero_division=0)
        f1 = f1_score(y_test[column], y_pred[:, i], average='weighted', zero_division=0)

        precision_list.append(precision)
        recall_list.append(recall)
        f1_list.append(f1)

    # Compute macro averages
    precision_macro = np.mean(precision_list)
    recall_macro = np.mean(recall_list)
    f1_macro = np.mean(f1_list)

    # Overall metrics
    overall_accuracy = (y_pred == y_test).mean().mean()

    print(f'Overall Accuracy: {overall_accuracy:.4f}')
    print(f'Macro Average Precision: {precision_macro:.4f}')
    print(f'Macro Average Recall: {recall_macro:.4f}')
    print(f'Macro Average F1 Score: {f1_macro:.4f}')

def save_model_multi(model, model_filepath):
    """
    Save the multi-label classification model.
    
    Args:
        model (GridSearchCV): Trained model.
        model_filepath (str): Filepath to save the model.
    """
    # Print the best parameters and best score for multi-label classification
    print(f'Best parameters found for multi-label classification: {model.best_params_}')
    print(f'Best Precision score for multi-label classification: {model.best_score_}')

    # Save the model and other files in the specified directory
    joblib.dump(model.best_estimator_, model_filepath)

def main():
    """
    Main function to load data, build models, train, evaluate, and save models.
    """
    if len(sys.argv) == 4:
        database_filepath, model_filepath_related, model_filepath_multi = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X_related, Y_related, X_multi, Y_multi = load_data(database_filepath)

        # First part - related classification
        print('Splitting data from first model...')
        X_train_related, X_test_related, y_train_related, y_test_related = train_test_split(X_related, Y_related, test_size=0.3, random_state=42)
        X_train_related_balanced, y_train_related_balanced = balance_data_related(X_train_related, y_train_related)

        print('Building first model...')
        model_related = build_model_related()

        print('Training first model...')
        model_related.fit(X_train_related_balanced, y_train_related_balanced)

        print('Predicting first model...')
        y_pred_related = model_related.predict(X_test_related)
        
        print('Evaluating first model...')
        evaluate_model_related(y_test_related, y_pred_related)

        print('Saving first model...\n    MODEL: {}'.format(model_filepath_related))
        save_model_related(model_related, model_filepath_related)

        print('Trained first model saved!')

        # Second part - multi-label classification
        print('Splitting data from second model...')
        X_train_multi, X_test_multi, y_train_multi, y_test_multi = train_test_split(X_multi, Y_multi, test_size=0.3, random_state=42)

        print('Building second model...')
        model_multi = build_model_multi()
        
        print('Training second model...')
        model_multi.fit(X_train_multi, y_train_multi)

        print('Predicting second model...')
        y_pred_multi = model_multi.predict(X_test_multi)
        
        print('Evaluating second model...')
        evaluate_model_multi(y_test_multi, y_pred_multi)

        print('Saving second model...\n    MODEL: {}'.format(model_filepath_multi))
        save_model_multi(model_multi, model_filepath_multi)

        print('All trained models saved!')

    else:
        print('Please provide the filepath of the disaster messages database, the filepaths for the related and multi models, '
              'the filepaths for the vectorizers and transformers as arguments.\n'
              'Example: python train_classifier.py data/DisasterResponse.db models/best_models/related_model.pkl models/best_models/multi_model.pkl')

if __name__ == '__main__':
    main()