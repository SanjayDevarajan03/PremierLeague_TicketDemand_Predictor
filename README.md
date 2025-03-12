# Premier League Ticket Demand Prediction Service

## Project Overview  
This project presents an end-to-end, production-ready ticket demand forecasting system designed to ticket pricing and availibility for **Premier League matches**. Utilizing MLOps best practices. The solution is fully automated, integrating data collection, feature engineering, model training, inference, and continuous monitoring into a seamless ML pipeline.
access the app [here]() .

#
![GIF](vid.gif)


## Business Problem  
 The Premier League faces several challenges in managing ticket sales across various stadiums in the UK:
- **Underpricing or Overpricing**: Setting ticket prices inaccurately, leading to revenue loss or unsold tickets.  
- **Inconsistent Attendance**: Failing to anticipate fluctuations in match attendance, impacting stadium atmosphere and revenue.  
- **Demand Forecasting**: Difficulty in predciting ticket demand due to external factors scuh as weather, team performance, and competing events.  

These issues lead to lost revenue, inefficient ticket allocation, and a poor fan experience.  

## ML Problem  
Accurately predict ticket demand for the upcoming Premier League matches to optimize pricing, ensure optimal seat allocation, and maximize revenue while improving fan engagement.  

## Data Sources
To ensure accurate predictions, we use multiple data sources:

- **Historical Ticket Sales Data**: Fetched from **[TicketMaster API](https://app.ticketmaster.com/discovery/v2/)**. 
- **Weather Data**: Historical weather information retrieved from **[Openmeteo Weather API](https://open-meteo.com/)**.
- **Match Schedule & Team Performance**: Retrieved from Football-Data.org and TheSportsDB.
- **Competing Events**: Other major events happening near stadiums fetched from Ticketmaster API
  
## Project methodalgy 
Our methodalgy features three-stage ML pipelines, leveraging modern MLOps principles such as feature stores, model registries, and automated inference to ensure scalability and reliability.

### **1. Feature Pipeline**

This pipeline fetches and preprocesses the required data, transforms it into a time-series format, and stores it in the **Hopsworks Feature Store**.

#### **Steps:**

1. Fetch historical ticket sales data from the **Ticketmaster API**.  
2. Fetch historical and forecasted weather data (temperature) from **Open-Meteo API**.
3. Fetch match scehdules and team statistics from Football-Data.org and TheSportsDB
4. Fetch competing event data from Ticketmaster API.
5. Merge data sources based on timestamps and stadium locations.
4. transform data into time series format
5. Store transformed data in the Hopsworks Feature Store.

### **2. Training Pipeline**

This pipeline fetches data from the feature store, processes it into feature-target format, trains a machine learning model, and evaluates it before saving the trained model in the **Hopsworks Model Registry**.

#### **Steps:**

1. Load preprocessed time series data from the feature store.
2.  Transform data into features and target:
   - **Prediction Target**: Number of tickets sold per match.
   - **Features**:
     - Historical ticket sales trends
     - Weather conditions on match day
     - Team performance and league standings
     - Type of match (e.g. rivalry, final, mid-season)
     - Competing events near the stadium
3. Train a **LightGBM model** with hyperparameter tuning using **Optuna** with 5-fold cross-validation.
4. Implement **feature engineering**:
   - Adding weekend/weekday and public holidays.
   - Incorporating time-series features (lags, rolling statistics).
5. Evaluate the model using **Mean Absolute Error (MAE)**.
6. Store the trained model in the **Hopsworks Model Registry**.


### **3. Inference Pipeline**

This pipeline is responsible for generating ticket demand predictions using the trained model from the model registory and the features from the feature store.

#### **Steps:**

1. Fetch the latest feature set from the Hopsworks Feature Store.
2. Load the trained model from the **Hopsworks Model Registry**.
3. Generate ticket demand predictions for upcoming matches.
4. Compare predictions against actual ticket sales to compute **Mean Absolute Error (MAE)**.
5. The pipeline runs as a **serverless function in `inference_pipeline.py`**, scheduled via **GitHub Actions** to execute every hour.


## Deployment & Monitoring

We developed **two interactive Streamlit applications** for ticket demand forecasting and model performance monitoring.

### **batch demand forecasting app**

- A **Streamlit application** visualizes forecasted ticket demand for Premier League matches. 
- The application features an interactive **stadium map** where the size of circles represents demand at specific venues.
- Users can explore electricity demand variations across locations in real-time,
- you can access the app [here]() 

### **Monitoring Dashboard**
- A separate **Streamlit dashboard** monitors model performance on an hourly basis.
- The dashboard includes:
  - A real-time chart of **MAE trends**
  - Historical performance records
  - Comparison of predicted vs. actual ticket demand
- you can access the dashbored [here]() 


## summery
This project successfully implements prediction system for ticket demand forecasting. By leveraging machine learning, ticket vendors and clubs can optimize pricing strategies, improve stadium attendance, maximize revenue by achieiving the following:

 - **Automated ML Pipeline** → Fully automated process from data collection to inference.

 - **Feature Store & Model Registry** → Efficient feature storage & model versioning.

 - **batch Demand Forecasting** → Predicts hourly electricity demand across locations.

 - **Interactive app** → Provides easy-to-interpret forecasts & model insights.

 - **Production-Ready** → Scheduled batch inference, model monitoring and retrainning & scalable architecture. 


  ## Contact
If you have any questions or would like to discuss this project further, feel free to reach out!
* [LinkedIn](https://www.linkedin.com/in/sanjay-devarajan-605127191/) 
* [Email](sanjay.jbsh02@gmail.com) 
