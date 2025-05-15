import os
import sys
import json
import pandas as pd
import joblib
from sqlalchemy import create_engine
from flask import Flask, request, jsonify
from flask_cors import CORS

BASEDIR = os.path.abspath(os.path.dirname(__file__))

# Ajusta o path para encontrar as classes personalizadas
sys.path.append(os.path.join(BASEDIR, '..', 'models'))
from dataprocessor import TextProcessor, Resampler

# Cria o app Flask e habilita CORS para dev local
app = Flask(__name__)
CORS(app)

# dirname(__file__) é flask-api/app
DB_PATH = os.path.join(BASEDIR, '..', 'data', 'DisasterResponse.db')
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)

# pega o DB-API connection puro
raw_conn = engine.raw_connection()

# Carrega o dataframe de mensagens
try:
    df = pd.read_sql("SELECT * FROM messages", con=raw_conn)
    print("Colunas carregadas:", df.columns.tolist())
except Exception as e:
    print(f"Erro ao carregar tabela messages: {e}")
    df = pd.DataFrame()

print(df.head())

# Nomes das categorias na mesma ordem do multi_model
CATEGORY_NAMES = list(df.columns[5:]) if not df.empty else []

# Carrega os modelos de ML
related_model = joblib.load(os.path.join(BASEDIR, '..', 'models', 'best_models', 'related_model.pkl'))
multi_model   = joblib.load(os.path.join(BASEDIR, '..', 'models', 'best_models', 'multi_model.pkl'))

@app.route("/api/classify", methods=["POST"])
def api_classify():
    data = request.get_json(force=True)
    text = data.get("message", "")

    # Defaults
    is_related = False
    classification_results = {}
    error_message = None

    try:
        # Predição se relacionado
        is_related = bool(related_model.predict([text])[0])

        if is_related:
            # Predição multi-label
            labels = multi_model.predict([text])[0]
            classification_results = dict(zip(CATEGORY_NAMES, labels.tolist()))
            print("Classification results:", classification_results)
        else:
            print("Texto não relacionado a desastre:", text)

    except Exception as e:
        # Captura exceção corretamente
        error_message = str(e)
        print(f"Erro em api_classify: {error_message}")

    # Retorna JSON completo, incluindo error_message se houver
    return jsonify({
        "isRelated":  is_related,
        "categories": classification_results,
        "error":      error_message
    })

@app.route("/api/stats", methods=["GET"])
def api_stats():
    try:
        # Calculate total messages
        total_messages = len(df)
        
        # Calculate disaster related vs non-disaster related
        disaster_related = df[df.related == 1].shape[0]
        non_disaster_related = total_messages - disaster_related
        
        # Calculate category distribution (similar to original Graph 1)
        related_messages = df[df.related == 1]
        related_messages_features = related_messages.iloc[:, 5:]
        category_distribution = []
        for category, count in related_messages_features.sum().sort_values(ascending=False).items():
            if count > 0:  # Only include categories with messages
                category_distribution.append({
                    "name": category.replace('_', ' ').title(),
                    "count": int(count)
                })
        
        # Calculate genre distribution (similar to original Graph 2)
        genre_counts = df.genre.value_counts()
        genre_distribution = [
            {"name": genre, "value": int(count)}
            for genre, count in genre_counts.items()
        ]
        
        return jsonify({
            "totalMessages": total_messages,
            "disasterRelated": disaster_related,
            "nonDisasterRelated": non_disaster_related,
            "categoriesDistribution": category_distribution,
            "genreDistribution": genre_distribution
        })
        
    except Exception as e:
        print(f"Error in api_stats: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Roda o Flask na porta 5000
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
