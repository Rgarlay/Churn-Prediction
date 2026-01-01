# Customer Churn Prediction
Predict whether a customer will churn in the next 30 days using behavioral and demographic data.

## Problem Statement:- 
Analyse customer subscription details and listening behavior:
* identify key patterns and risk factors associated with churn.
* build a ML model to predict potential churn users to support retention strategies.

## Dataset
- __Source__: [Kaggle](https://www.kaggle.com/competitions/streaming-subscription-churn-model)
- __Rows__: 125,000
- __Features__: 21 (numerical + categorical)
- __Target__: `Churned` (binary)

## Tech Stack
* __Core Stack__: Python, SQL (MySQL), Pandas, NumPy
* __Machine Learning__: Scikit-learn
* __Visualization__ : Matplotlib, Seaborn
* __MLOps & Deployment__:Docker, MLflow, DagsHub, FastAPI, AWS
* __Automation__: GitHub Actions (CI/CD)

## Key Challenges
* Feature selection for seperating noisy features from useful signals. 
* Engineering most useful features from raw low-correlation features. 

## Methodology
* Ingest and analyze raw customer data in MySQL using SQL to uncover churn-related patterns.
* Perform visualization, feature engineering, and preprocessing in Jupyter to prepare model-ready data.
* Build structured pipelines to train and evaluate supervised machine learning models for churn prediction.
* Deploy the final model using FastAPI, containerized with Docker, and automated on AWS via CI/CD pipelines.

## Metrics

| Model | Recall Score | Accuracy Score | F1 Score |
|-------|--------------|----------------|----------|
| AdaBoostClassifier | 0.8221 | 0.8457 | 0.8455 |
| RandomForestClassifier | 0.8471 | 0.8445 | 0.8484 |
| XGBClassifier | 0.8351 | 0.8457 | 0.8476 |

## Future Prospects 
* Adding Test cases before model updation.
* Adding more models in training phase.
* Add more project oriented constraints to data to and fro from database.

Hi, if you have any further queries or suggestions, feel contact me at: - ravigarlay@outlook.com 
