# Disaster Response ML project (under development)

## Table of Contents
- [Project Description](#project-description)
- [File Descriptions](#file-descriptions)
- [How to Interact with the Project](#how-to-interact-with-the-project)
- [Results and Discussion](#results-and-discussion)

## Project Description

### Objectives

The primary objectives of this project are:
- **Create an ETL pipeline**: Process the dataset to ensure it is suitable for analysis and modeling.
- **Model Building and Evaluation**: Develop Multiple label classification ML model to identify what kind of humanitarian supports are needed in Twitter messages of people in need.
- **Flask Web App**: Add data visualizations using Plotly in the web app.

## File Descriptions
Overview of the main files and directories in the repository:
- `README.md`: This file.
- `ETL Pipeline Preparation.ipynb`: The Jupyter Notebook with the ETL pipeline code preparing for a python code.
- `ML Pipeline Preparation.ipynb`: The Jupyter Notebook with the MKachine Learning pipeline code preparing for a python code (not ready).
- `dataset/`: Directory containing the dataset.

## How to Interact with the Project
This project is under development. I'm open to improvement tips

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
