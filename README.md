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
In times of disaster, the ability to quickly and accurately communicate needs can mean the difference between life and death. People in emergency situations often turn to the internet to share their circumstances and seek humanitarian aid. However, **the overwhelming volume of messages can make it challenging for NGOs and relief organizations to identify and respond to urgent needs promptly**. This disconnect can delay critical assistance, exacerbating the suffering of those affected by disasters.

## Project Description
The Disaster Response Project leverages machine learning to classify disaster-related messages, ensuring that emergency response teams can quickly and accurately identify and act upon urgent needs. By bridging the gap between those in need and those able to help, this project aims to enhance the efficiency and effectiveness of disaster response efforts.

The project features a user-friendly web application that visualizes training data and provides an intuitive interface for classifying messages. This enables response teams to be activated more assertively and efficiently during emergencies, ultimately saving lives and reducing suffering.

## Objectives
The primary objective of this project is:
- **Provide a interface for response teams to evaluate if a message is related to disaster situations and of what type.**
  
The secondary objectives of this project are:
- **Create an ETL pipeline**: Process the dataset to ensure it is suitable for analysis and modeling.
- **Model Building and Evaluation**: Develop a multi-label classification ML model to identify the type of humanitarian support needed in Twitter messages from people in need.
- **Flask Web App**: Add data visualizations using Plotly in the web app.


## Model Structure

This project analyzes disaster data from [Appen](https://www.appen.com/) to build a model for an API that classifies disaster messages. The data comprises two separate datasets that together contain real messages sent during disaster events, comprising over a hundred columns. The key content regards messages categorized for multi-class classification: one column indicates if a message is disaster-related, and multiple columns categorize the type of disaster.

Considering the content in the data, this project was built in a two-part machine learning model:

### Part 1: Related Classification
- **Objective**: Determine if a given message is related to a disaster (binary classification: related or not related).
- **Components**:
  - `model_related.pkl`: A machine learning model that predicts if a message is related to a disaster.

### Part 2: Multi-Classification
- **Objective**: If the message is related to a disaster, classify it into specific categories (multi-label classification).
- **Components**:
  - `model_multi.pkl`: A machine learning model that predicts the specific disaster-related categories for a message.

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
    - `model_multi.pkl`: Model for multi-label classification of disaster-related messages.
    - `model_related.pkl`: Model for binary classification to determine if a message is related to a disaster.
      
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
   - The input message is first predicted using the `related_model.
   - If the message is related to a disaster, the message is further predicted using `multi_model` that inform the specific disaster-related categories.
   - If the message is not related to a disaster, than a text informs that "No relevant categories found for this message".

### `HTML Templates`
- **`master.html`**: The base template that includes the structure and common elements of the web pages.
- **`go.html`**: Extends `master.html` and displays the classification results. It includes blocks to display the input message, any error messages, and the classification results.

## How to Interact with the Project

### Prerequisites

Make sure you have Python and the necessary libraries installed. You can install the required libraries using `pip`:

```sh
pip install -r requirements.txt
cd path/to/project-directory
```
Run the python file `train_classifier.py` to create the models needed for the web application:
```sh
python train_classifier.py data/DisasterResponse.db models/best_models/related_model.pkl models/best_models/multi_model.pkl
```
Run the python file ` run.py ` to access web application:
```sh
python app\run.py
```

## Results and Discussion

### Results

Considering that this is a case where People in emergency situations need to be recognize, we want a model to be the best possible in predicting what messages are related to disasters, in technical language, we need to avoid the type 2 errors in a confusion matrix. Therefore, the metric that is considered to get the best model is the *Precision*.

With that in mind, these are the results founded in the project:

**Evaluating first model - Related Classification**
   - *Precision*: 0.8201
   - Recall: 0.6997
   - F1 Score: 0.7217
   - Accuracy: 0.6997

**Evaluating first model – Multi Classification**
   - *Macro Average Precision*: 0.9060
   - Macro Average Recall: 0.9148
   - Macro Average F1 Score: 0.8933
   - Overall Accuracy: 0.9148

Note: Macro Average is commonly used on Multi Class. It works by creating a median of all the results in every target column. For example, when evaluating the Macro Average Precision, we are getting the median of all precision values in every column in the target columns. Some may have bad values and others may have excellent results, but we use the median to simplify the evaluation and comparison between different models.

### Discussion

The evaluation showed good and grate results for prediction. Although I must point out some important analysis:
- The first model has low Recall value, even though the imbalanced data has been corrected. This could mean that more data is needed or other approaches to transform the message data should be tested.
 - As for the second model, the macro average for the evaluation metrics has high results, but it is good to point out that some class columns have terrible results. The project tried to overcome this problem by using a method called [MLSMOTE]( https://medium.com/thecyphy/handling-data-imbalance-in-multi-label-classification-mlsmote-531155416b87) to deal once again with the problem of imbalance data.
   
## Conclusion

In conclusion, the Disaster Response Project demonstrates the power of machine learning in addressing real-world problems. By effectively classifying disaster-related messages, the project aids emergency response teams in providing timely assistance, ultimately saving lives and reducing suffering.

More tests must be conducted to deal with the problems with imbalance data.

## Acknowledgements

I would like to express my gratitude to the following individuals and organizations for their invaluable support throughout the development of this project:

**Appen**: For providing the disaster-related message datasets used in this project.
**Udacity**: For the educational resources and support.
**Niteshsukhwani**: For providing a solution to deal with imbalanced data in a Multi-Class problem in his [github]( https://github.com/Prady029/LLSF_DL-MLSMOTE-Hybrid-for-handling-tail-labels)

## Contact

For any questions or further information, please contact:

**Name**: [Daniel S Braga]  
**Email**: [sindeauxdaniel@gmail.com]  
**LinkedIn**: [www.linkedin.com/in/danielsibraga]
