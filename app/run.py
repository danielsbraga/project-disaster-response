import os
import sys
import json
import plotly
import pandas as pd
import joblib
from plotly.graph_objs import Bar
from sqlalchemy import create_engine
from flask import Flask, render_template, request

# import custom classes
sys.path.append('models/')
from dataprocessor import TextProcessor, Resampler

app = Flask(__name__)

# Load data
engine = create_engine('sqlite:///data/DisasterResponse.db')
df = pd.read_sql_table("messages", engine)

# Load models
related_model = joblib.load("models/best_models/related_model.pkl")
multi_model = joblib.load("models/best_models/multi_model.pkl")

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
        # Use related classification model to predict query
        is_related = related_model.predict([query])[0]

        # Debug print to check if the text is related
        print("Is related:", is_related)

        if is_related:  
            # If query is related, check which labels                 
            classification_labels = multi_model.predict([query])[0]
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
