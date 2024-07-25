import os
import sys
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.multioutput import MultiOutputClassifier
from scipy.sparse import vstack
from sklearn.utils import resample
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
import joblib
from dataprocessor import DataProcessor

processor = DataProcessor()

def load_data(database_filepath):
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

def build_model_related(X, Y):
    # Vectorize the features for related classification
    X_tfidf, count_vectorizer_related, tfidf_transformer_related = processor.vectorize_transform(X)

    # Split the data into training and testing sets for related classification
    X_train_related, X_test_related, y_train_related, y_test_related = train_test_split(X_tfidf, Y, test_size=0.3, random_state=42)

    # Balance the training dataset for related classification
    X_train_majority = X_train_related[y_train_related == 0]
    y_train_majority = y_train_related[y_train_related == 0]
    X_train_minority = X_train_related[y_train_related == 1]
    y_train_minority = y_train_related[y_train_related == 1]

    X_train_minority_resampled, y_train_minority_resampled = resample(X_train_minority, y_train_minority,
                                                                      replace=True,
                                                                      n_samples=len(y_train_majority),
                                                                      random_state=42)

    X_train_balanced = vstack((X_train_majority, X_train_minority_resampled))
    y_train_balanced = np.hstack((y_train_majority, y_train_minority_resampled))

    # Define the pipeline for related classification
    pipeline_related = Pipeline([
        ('clf', RandomForestClassifier())
    ])

    # Define the parameter grid for related classification
    param_grid_related = {
        'clf__n_estimators': [100, 200],
        'clf__min_samples_split': [2, 5]
    }

    # Perform grid search for related classification
    grid_search_related = GridSearchCV(pipeline_related, param_grid_related, cv=2, scoring='precision_weighted', n_jobs=1, verbose=2)

    return {
        'grid_search_related': grid_search_related,
        'X_train_related': X_train_balanced,
        'y_train_related': y_train_balanced,
        'X_test_related': X_test_related,
        'y_test_related': y_test_related,
        'count_vectorizer_related': count_vectorizer_related,
        'tfidf_transformer_related': tfidf_transformer_related
    }

def evaluate_model_related(model, X_test, y_test):
    # Evaluate the related classification model
    y_pred = model.best_estimator_.predict(X_test)
    related_precision = precision_score(y_test, y_pred, average='weighted')
    related_recall = recall_score(y_test, y_pred, average='weighted')
    related_f1 = f1_score(y_test, y_pred, average='weighted')
    related_accuracy = accuracy_score(y_test, y_pred)

    print(f'Related Classification - Precision: {related_precision:.4f}')
    print(f'Related Classification - Recall: {related_recall:.4f}')
    print(f'Related Classification - F1 Score: {related_f1:.4f}')
    print(f'Related Classification - Accuracy: {related_accuracy:.4f}')

def save_model_related(model, count_vectorizer, tfidf_transformer, model_filepath):
    # Print the best parameters and best score for related classification
    print(f'Best parameters found for related classification: {model.best_params_}')
    print(f'Best Precision score for related classification: {model.best_score_}')

    # file_path to save the model
    model_filepath = 'best_models'

    # Create the directory if it doesn't exist
    os.makedirs(model_filepath, exist_ok=True)

    # Save the model and other files in the specified directory
    joblib.dump(model.best_estimator_, os.path.join(model_filepath, 'best_model_related.pkl'))
    joblib.dump(count_vectorizer, os.path.join(model_filepath, 'count_vectorizer_related.pkl'))
    joblib.dump(tfidf_transformer, os.path.join(model_filepath, 'tfidf_transformer_related.pkl'))

def build_model_multi(X, Y):
    # Split the dataset into training and testing sets for multi-label classification
    X_train_multi, X_test_multi, y_train_multi, y_test_multi = train_test_split(X, Y, test_size=0.3, random_state=42)

    # Get minority instance (tail labels) of that dataframe
    X_sub, y_sub = processor.get_minority_instance(X_train_multi, y_train_multi)

    # Vectorize the features for multi-label classification
    X_tfidf_multi, count_vectorizer_multi, tfidf_transformer_multi = processor.vectorize_transform(X_sub)

    # Get index of 5 nearest neighbors of all the instances
    indices = processor.nearest_neighbour(X_tfidf_multi)

    # Apply MLSMOTE to augment the dataframe
    X_res, y_res = processor.MLSMOTE(X_tfidf_multi, y_sub, 100, indices)

    # Transform the test set for multi-label classification
    X_test_tfidf_multi = processor.vectorize_test(X_test_multi)

    # Define the pipeline for multi-label classification
    pipeline_multi = Pipeline([
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

    return {
        'grid_search_multi': grid_search_multi,
        'X_res': X_res,
        'y_res': y_res,
        'X_test_tfidf_multi': X_test_tfidf_multi,
        'y_test_multi': y_test_multi,
        'count_vectorizer_multi': count_vectorizer_multi,
        'tfidf_transformer_multi': tfidf_transformer_multi
    }

def evaluate_model_multi(model, X_test, y_test):
    # Predict on test data for multi-label classification
    Y_pred = model.best_estimator_.predict(X_test)

    # Initialize lists to store the precision, recall, and f1-score for each label
    precision_list = []
    recall_list = []
    f1_list = []

    # Calculate precision, recall, and f1-score for each label
    for i, column in enumerate(y_test.columns):
        precision = precision_score(y_test[column], Y_pred[:, i], average='weighted', zero_division=0)
        recall = recall_score(y_test[column], Y_pred[:, i], average='weighted', zero_division=0)
        f1 = f1_score(y_test[column], Y_pred[:, i], average='weighted', zero_division=0)

        precision_list.append(precision)
        recall_list.append(recall)
        f1_list.append(f1)

    # Compute macro averages
    precision_macro = np.mean(precision_list)
    recall_macro = np.mean(recall_list)
    f1_macro = np.mean(f1_list)

    # Overall metrics
    overall_accuracy = (Y_pred == y_test).mean().mean()

    print(f'Overall Accuracy: {overall_accuracy:.4f}')
    print(f'Macro Average Precision: {precision_macro:.4f}')
    print(f'Macro Average Recall: {recall_macro:.4f}')
    print(f'Macro Average F1 Score: {f1_macro:.4f}')

def save_model_multi(model, count_vectorizer, tfidf_transformer, model_filepath):
    # Print the best parameters and best score for multi-label classification
    print(f'Best parameters found for multi-label classification: {model.best_params_}')
    print(f'Best Precision score for multi-label classification: {model.best_score_}')

    # file_path to save the model
    model_filepath = 'best_models'

    # Create the directory if it doesn't exist
    os.makedirs(model_filepath, exist_ok=True)

    # Save the best model for multi-label classification
    joblib.dump(model.best_estimator_, os.path.join(model_filepath, 'best_model_multi.pkl'))
    joblib.dump(count_vectorizer, os.path.join(model_filepath, 'count_vectorizer_multi.pkl'))
    joblib.dump(tfidf_transformer, os.path.join(model_filepath, 'tfidf_transformer_multi.pkl'))

def main():
    if len(sys.argv) == 8:
        database_filepath, model_filepath_related, model_filepath_multi, vec_filepath_related, tfidf_filepath_related, vec_filepath_multi, tfidf_filepath_multi = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X_related, Y_related, X_multi, Y_multi = load_data(database_filepath)

        print('Building first model...')
        model_related = build_model_related(X_related, Y_related)

        print('Training first model...')
        model_r = model_related['grid_search_related']
        X_train_related = model_related['X_train_related']
        y_train_related = model_related['y_train_related']
        model_r.fit(X_train_related, y_train_related)
        
        print('Evaluating first model...')
        X_test_related = model_related['X_test_related']
        y_test_related = model_related['y_test_related']
        evaluate_model_related(model_r, X_test_related, y_test_related)

        print('Saving first model...\n    MODEL: {}'.format(model_filepath_related))
        count_vectorizer_related = model_related['count_vectorizer_related']
        tfidf_transformer_related = model_related['tfidf_transformer_related']
        save_model_related(model_r, count_vectorizer_related, tfidf_transformer_related, model_filepath_related)

        print('Trained first model saved!')

        print('Building second model...')
        model_multi = build_model_multi(X_multi, Y_multi)
        
        print('Training second model...')
        model_m = model_multi['grid_search_multi']
        X_train_multi = model_multi['X_res']
        y_train_multi = model_multi['y_res']
        model_m.fit(X_train_multi, y_train_multi)
        
        print('Evaluating second model...')
        X_test_multi = model_multi['X_test_tfidf_multi']
        y_test_multi = model_multi['y_test_multi']
        evaluate_model_multi(model_m, X_test_multi, y_test_multi)

        print('Saving second model...\n    MODEL: {}'.format(model_filepath_multi))
        count_vectorizer_multi = model_multi['count_vectorizer_multi']
        tfidf_transformer_multi = model_multi['tfidf_transformer_multi']
        save_model_multi(model_m, count_vectorizer_multi, tfidf_transformer_multi, model_filepath_multi)

        print('All trained models saved!')

    else:
        print('Please provide the filepath of the disaster messages database, the filepaths for the related and multi models, '
              'the filepaths for the vectorizers and transformers as arguments.\n'
              'Go to the "models/" directory and use the example bellow\n'
              'Example: python train_classifier.py ../data/DisasterResponse.db related_model.pkl multi_model.pkl '
              'count_vec_related.pkl tfidf_trans_related.pkl count_vec_multi.pkl tfidf_trans_multi.pkl')

if __name__ == '__main__':
    main()
