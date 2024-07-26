# Disaster Response Project: Classifying Disaster-Related Messages to Aid Emergency Response Teams

## Table of Contents
- [Introduction](#introduction)
- [Project Description](#project-description)
- [Objectives](#objectives)
- [Model Structure](#model-structure)
- [Web Application](#web-application)
- [File Descriptions](#file-descriptions)
- [Code Explanation](#code-explanation)
- [How to Interact with the Project](#how-to-interact-with-the-project)
- [Results and Discussion](#results-and-discussion)
- [Conclusion](#conclusion)
- [Acknowledgements](#acknowledgements)
- [Contact](#contact)

## Introduction
In times of disaster, the ability to quickly and accurately communicate needs can mean the difference between life and death. People in emergency situations often turn to the internet to share their circumstances and seek humanitarian aid. However, the overwhelming volume of messages can make it challenging for NGOs and relief organizations to identify and respond to urgent needs promptly. This disconnect can delay critical assistance, exacerbating the suffering of those affected by disasters.

## Project Description
The Disaster Response Project leverages machine learning to classify disaster-related messages, ensuring that emergency response teams can quickly and accurately identify and act upon urgent needs. By bridging the gap between those in need and those able to help, this project aims to enhance the efficiency and effectiveness of disaster response efforts.

The project features a user-friendly web application that visualizes training data and provides an intuitive interface for classifying messages. This enables response teams to be activated more assertively and efficiently during emergencies, ultimately saving lives and reducing suffering.

## Objectives
The primary objectives of this project are:
- **Create an ETL pipeline**: Process the dataset to ensure it is suitable for analysis and modeling.
- **Model Building and Evaluation**: Develop a multi-label classification ML model to identify the type of humanitarian support needed in Twitter messages from people in need.
- **Flask Web App**: Add data visualizations using Plotly in the web app.

## Model Structure
To manage the multi-class classification problem, a two-part machine learning model was implemented:

### Part 1: Related Classification
- **Objective**: Determine if a given message is related to a disaster (binary classification: related or not related).
- **Components**:
  - `best_model_related.pkl`: A machine learning model that predicts if a message is related to a disaster.
  - `count_vectorizer_related.pkl`: A `CountVectorizer` that transforms text data into token counts.
  - `tfidf_transformer_related.pkl`: A `TfidfTransformer` that converts the token counts into TF-IDF features.

### Part 2: Multi-Classification
- **Objective**: If the message is related to a disaster, classify it into specific categories (multi-label classification).
- **Components**:
  - `best_model_multi.pkl`: A machine learning model that predicts the specific disaster-related categories for a message.
  - `count_vectorizer_multi.pkl`: A `CountVectorizer` that transforms text data into token counts.
  - `tfidf_transformer_multi.pkl`: A `TfidfTransformer` that converts the token counts into TF-IDF features.

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

## File Descriptions
Overview of the main files and directories in the repository:

- `README.md`: Provides an overview of the project, including its objectives, structure, and instructions for interaction.
- `app/`: Directory containing the Flask web application files.
  - `run.py`: Script to start the Flask web application. It includes the logic for loading models and handling user input for message classification.
  - `templates/`: Directory containing HTML templates for the web application.
    - `master.html`: Base template that includes the structure and common elements of the web pages.
    - `go.html`: Template for displaying the classification results.

- `data/`: Directory containing the dataset and any additional data files used in the project.
  - `categories.csv`: CSV file containing categories of disaster messages.
  - `messages.csv`: CSV file containing the disaster messages.
  - `DisasterResponse.db`: SQLite database created from the dataset.
  - `process_data.py`: Script for processing the data and creating the database.
    
- `models/`: Directory containing the trained machine learning models and their components:
  - `dataprocessor.py`: Script containing additional data processing utilities.
  - `train_classifier.py`: Script for training the machine learning models.
  - `best_models/`: Subdirectory intended for storing the best performing models and their components. (Note: The files in this directory are empty in the GitHub repository because they are very large and exceed GitHub's size limits).
    - `best_model_multi.pkl`: Model for multi-label classification of disaster-related messages.
    - `best_model_related.pkl`: Model for binary classification to determine if a message is related to a disaster.
    - `count_vectorizer_multi.pkl`: CountVectorizer object for text preprocessing for multi-class classification.
    - `count_vectorizer_related.pkl`: CountVectorizer object for text preprocessing for binary classification.
    - `tfidf_transformer_multi.pkl`: TfidfTransformer object for converting token counts into TF-IDF features for multi-class classification.
    - `tfidf_transformer_related.pkl`: TfidfTransformer object for converting token counts into TF-IDF features for binary classification.
      
- `training/`: Directory containing Jupyter Notebook files and datasets for the training process.
  - `dataset/`: Subdirectory containing datasets used for training.
  - `EDA.ipynb`: Jupyter Notebook for Exploratory Data Analysis on the dataset.
  - `ETL Pipeline Preparation.ipynb`: Jupyter Notebook for data processing and ETL pipeline.
  - `ML Pipeline Preparation.ipynb`: Jupyter Notebook for training and evaluating the machine learning models.
    
- `requirements.txt`: A list of Python libraries required to run the project, which can be installed using `pip`.
- `LICENSE`: The license under which the project is distributed.

This updated section provides a comprehensive overview of the project's structure, making it easier for others to understand and navigate the repository.

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

## Conclusion
In conclusion, the Disaster Response Project demonstrates the power of machine learning in addressing real-world problems. By effectively classifying disaster-related messages, the project aids emergency response teams in providing timely assistance, ultimately saving lives and reducing suffering.

## Contact
For any questions or further information, please contact:

**Name**: [Daniel S Braga]  
**Email**: [sindeauxdaniel@gmail.com]  
**LinkedIn**: [www.linkedin.com/in/danielsibraga]
