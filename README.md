Word:
# Disaster Response Project: Classifying Disaster-Related Messages to Aid Emergency Response Teams

## Table of Contents
- [Project Description](#project-description)
- [Model Structure](#model-structure)
- [Web Application](#web-application)
- [File Descriptions](#file-descriptions)
- [Code Explanation](#code-explanation)
- [How to Interact with the Project](#how-to-interact-with-the-project)
- [Results and Discussion](#results-and-discussion)

## Project Description

The Disaster Response Project is designed to classify disaster-related messages to aid emergency response teams.
The web application features a homepage that visualizes training data and provides an input form for message classification, and a results page that displays the classification outcomes.

### Objectives

The primary objectives of this project are:
- **Create an ETL pipeline**: Process the dataset to ensure it is suitable for analysis and modeling.
- **Model Building and Evaluation**: Develop Multiple label classification ML model to identify what kind of humanitarian supports are needed in Twitter messages of people in need.
- **Flask Web App**: Add data visualizations using Plotly in the web app.

## Model Structure

To manage the multi-class classification problem, implemented a two-part machine learning model:

### Part 1: Related Classification

- **Objective**: Determine if a given message is related to a disaster (binary classification: related or not related).
- **Components**:
  - `related_model.pkl`: A machine learning model that predicts if a message is related to a disaster.
  - `count_vec_related.pkl`: A `CountVectorizer` that transforms text data into token counts.
  - `tfidf_trans_related.pkl`: A `TfidfTransformer` that converts the token counts into TF-IDF features.

### Part 2: Multi-Classification

- **Objective**: If the message is related to a disaster, classify it into specific categories (multi-label classification).
- **Components**:
  - `multi_model.pkl`: A machine learning model that predicts the specific disaster-related categories for a message.
  - `count_vec_multi.pkl`: A `CountVectorizer` that transforms text data into token counts.
  - `tfidf_trans_multi.pkl`: A `TfidfTransformer` that converts the token counts into TF-IDF features.

## Web Application

The web application is built using Flask and provides the following functionalities:

1. **Homepage**:
   - Displays visualizations of the training data (e.g., feature counts, genre counts).
   - Provides an input form for users to enter a message to classify.

2. **Results Page**:
   - Displays the classification results for the input message.
   - If the message is related to a disaster, it shows the relevant categories.
   - If the message is not related, it indicates that no relevant categories were found.

## File Descriptions
Overview of the main files and directories in the repository:
- `README.md`: This file.
- `ETL Pipeline Preparation.ipynb`: The Jupyter Notebook with the ETL pipeline code preparing for a python code.
- `ML Pipeline Preparation.ipynb`: The Jupyter Notebook with the MKachine Learning pipeline code preparing for a python code (not ready).
- `dataset/`: Directory containing the dataset.

## Code Explanation

### `run.py`

This script contains the Flask application setup and the logic for loading the models and handling user input:

1. **Loading Models**:
   - The models and transformers are loaded from the `models/best_models/` directory.

2. **Routes**:
   - **`/index`**: Renders the homepage with visualizations.
   - **`/go`**: Handles the user input and displays the classification results.

3. **Model Prediction**:
   - The input message is first vectorized using the `count_vec_related` and `tfidf_trans_related` transformers.
   - The `related_model` predicts if the message is related to a disaster.
   - If related, the message is further vectorized using `count_vec_multi` and `tfidf_trans_multi` transformers.
   - The `multi_model` predicts the specific disaster-related categories.

### HTML Templates

- **`master.html`**: The base template that includes the structure and common elements of the web pages.
- **`go.html`**: Extends `master.html` and displays the classification results. It includes blocks to display the input message, any error messages, and the classification results.

## How to Interact with the Project

### Prerequisites

Make sure you have Python and the necessary libraries installed. You can install the required libraries using `pip`:

```sh
pip install -r requirements.txt
cd path/to/project-directory
python app\run.py
```

## Results and Discussion
The questions I have encountered so far are:
1. **What is the best metric to validate a Multi Label Classifier model?**: Considering that it is a recommendation problem for what humanitarian aid a person needs considering this person twitter message, the important thing here is to bring the most relevant classifications, that is, reducing false positives. Therefore, precision is more relevant then recall and accuracy. What do you think?
2. **My ML resulted has conflicting precision and recall metrics**: Using sklearn's MultiOutputClassifier and classification_report methods, I found some classification labels with precision greater than 0 and recall equal to 0, this should be impossible. What could have happened?
   
##### Example: Classification Report for infrastructure_related
| Class       | Precision | Recall | F1-Score | Support |
|-------------|-----------|--------|----------|---------|
| 0           | 0.94      | 1.00   | 0.97     | 7360    |
| 1           | 0.33      | 0.00   | 0.00     | 505     |
| **Avg/Total** | **0.90** | **0.94** | **0.90** | **7865** |


