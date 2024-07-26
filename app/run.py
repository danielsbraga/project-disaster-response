import os
import sys
import json
import plotly
import pandas as pd
import joblib
from plotly.graph_objs import Bar
from sqlalchemy import create_engine
from flask import Flask, render_template, request

app = Flask(__name__)

# Add the path to the dataprocessor module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../models')))

# Define the directory for the best models
best_models_dir = "models/best_models/"

# Load model files
related_model = joblib.load(os.path.join(best_models_dir, "best_model_related.pkl"))
count_vec_related = joblib.load(os.path.join(best_models_dir, "count_vectorizer_related.pkl"))
tfidf_trans_related = joblib.load(os.path.join(best_models_dir, "tfidf_transformer_related.pkl"))
multi_model = joblib.load(os.path.join(best_models_dir, "best_model_multi.pkl"))
count_vec_multi = joblib.load(os.path.join(best_models_dir, "count_vectorizer_multi.pkl"))
tfidf_trans_multi = joblib.load(os.path.join(best_models_dir, "tfidf_transformer_multi.pkl"))

# Print the type of loaded models for debugging
print("related_model type:", type(related_model))
print("count_vec_related type:", type(count_vec_related))
print("tfidf_trans_related type:", type(tfidf_trans_related))
print("multi_model type:", type(multi_model))
print("count_vec_multi type:", type(count_vec_multi))
print("tfidf_trans_multi type:", type(tfidf_trans_multi))

# Load data
engine = create_engine('sqlite:///data/DisasterResponse.db')
df = pd.read_sql_table("messages", engine)


@app.route('/')
@app.route('/index')
def index():
    # GRAPH 1
    related_messages = df[df.related == 1]
    related_messages_features = related_messages.iloc[:, 5:]
    count_features = related_messages_features.sum().sort_values() / related_messages_features.shape[0]

    print("Graph 1 data:", count_features)  # Debug print

    graph1 = {
        'data': [
            Bar(
                x=count_features.values,
                y=count_features.index,
                orientation='h'
            )
        ],
        'layout': {
            'title': 'Feature Counts for Related Text',
            'xaxis': {'title': "Count"},
            'yaxis': {'title': "Features"}
        }
    }

    # GRAPH 2
    genre_count = df.genre.value_counts()

    print("Graph 2 data:", genre_count)  # Debug print

    graph2 = {
        'data': [
            Bar(
                x=genre_count.index,
                y=genre_count.values,
                text=genre_count.values,
                textposition='auto'
            )
        ],
        'layout': {
            'title': 'Genre Counts',
            'xaxis': {'title': "Genre"},
            'yaxis': {'title': "Count"}
        }
    }

    # GRAPH 3
    pivot_table = df[df.related != 2].pivot_table(index='related', columns='genre', aggfunc='size', fill_value=0)
    percentage_table = (pivot_table.div(pivot_table.sum(axis=1), axis=0) * 100).round(2)

    print("Graph 3 data:", percentage_table)  # Debug print

    graph3 = {
        'data': [
            {
                'type': 'bar',
                'x': percentage_table.index,
                'y': percentage_table[genre],
                'name': genre
            } for genre in percentage_table.columns
        ],
        'layout': {
            'title': '100% Stacked Bar Chart of Genre by Related',
            'barmode': 'stack',
            'xaxis': {'title': "Related"},
            'yaxis': {'title': "Percentage"},
            'legend': {'title': 'Genre'}
        }
    }

    graphs = [graph1, graph2, graph3]
    ids = ["graph-{}".format(i) for i, _ in enumerate(graphs)]
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    print("Graph JSON:", graphJSON)  # Debug print

    return render_template('master.html', ids=ids, graphJSON=graphJSON)

@app.route('/go')
def go():
    query = request.args.get('query', '')

    # Debug print to check if the query is empty
    if query:
        print("Query is not empty")
    else:
        print("Query is empty")

    error_message = None

    try:
        # Ensure the correct sequence of transformations
        query_vectorized = count_vec_related.transform([query])
        query_vectorized = tfidf_trans_related.transform(query_vectorized)
        is_related = related_model.predict(query_vectorized)[0]

        # Debug print to check if the text is related
        print("Is related:", is_related)

        if is_related:
            query_vectorized = count_vec_multi.transform([query])
            query_vectorized = tfidf_trans_multi.transform(query_vectorized)
            
            # Debug print to check the vectorized query for multi_model
            print("Vectorized query for multi_model:", query_vectorized)
            
            classification_labels = multi_model.predict(query_vectorized)[0]
            classification_results = dict(zip(df.columns[5:], classification_labels))

            # Debug print to check classification results
            print("Classification results:", classification_results)
        else:
            classification_results = {}
            # Debug print to confirm non-related text handling
            print("Classification results for non-related text:", classification_results)

    except Exception as e:
        error_message = str(e)
        classification_results = {}

    return render_template('go.html', query=query, classification_result=classification_results, error_message=error_message)

def main():
    app.run(host='0.0.0.0', port=3001, debug=True, use_reloader=False)

if __name__ == '__main__':
    main()
