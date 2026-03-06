# ![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)


# Analysis and Forecasting of ADHD Assessment Demand and Service Strain in England (2019–2024)

![Dashboard Overview](images/dashboard_overview.png)

This project applies statistical analysis and forecasting techniques to NHS ADHD referral data to identify demand trends and visualise service pressures through an interactive Streamlit dashboard.


## Table of Contents

- [Project Overview](#project-overview)
- [Objectives](#objectives)
- [Project Workflow](#project-workflow)
- [Dataset](#dataset)
- [Business Requirements](#business-requirements)
- [Hypothesis Validation](#hypothesis-validation)
- [Tools & Technologies](#tools--technologies)
- [Use of Generative Artificial Intelligence](#use-of-generative-artificial-intelligence-genai-in-this-project)
- [How to Run the Project](#how-to-run-the-project)
- [Dashboard](#dashboard)
- [Ethical Considerations](#ethical-considerations)
- [Limitations](#limitations)
- [Future Improvements](#future-improvements)
- [Project Structure](#project-structure)
- [Key Project Outputs](#key-project-outputs)
- [Author](#author)
- [References](#references)


## Project Overview

This project analyses national ADHD referral data from NHS England to examine trends in assessment demand, evaluate indicators of service strain, and develop an interpretable forecasting model for future referral volumes.

Statistical hypothesis testing and regression modelling are used to determine whether referral demand has increased significantly over time, whether referral levels differ across age groups, and whether long-wait referral proportions indicate increasing pressure on services.

An interactive Streamlit dashboard was developed to communicate the analytical findings through stakeholder-focused visualisations.


## Objectives

The primary objective of this project is to analyse ADHD referral demand trends in England and evaluate indicators of service strain within NHS assessment pathways.

Specific objectives include:

- Determining whether ADHD referral demand has increased significantly over time.
- Identifying differences in referral patterns across age groups.
- Evaluating long-wait referral proportions as an indicator of service strain.
- Developing a forecasting model to estimate future referral demand.
- Communicating insights through an interactive Streamlit dashboard.


## Project Workflow

The project follows a structured analytics pipeline:

1. **Data Collection**
   - NHS ADHD referral statistics were obtained from NHS England MHSDS reports.

2. **Data Preparation**
   - Raw datasets were cleaned and structured into time-series datasets.

3. **Statistical Analysis**
   - Regression and ANOVA tests were used to evaluate referral trends and demographic differences.

4. **Forecast Modelling**
   - A linear regression model was used to forecast future referral demand.

5. **Dashboard Development**
   - Results were communicated through an interactive Streamlit dashboard.


## Dataset

The dataset used in this project is derived from **NHS England Mental Health Services Monthly Statistics (MHSDS)**.

It contains national-level indicators relating to ADHD referrals and waiting times across England.

Key variables analysed include:

- Total open ADHD referrals
- Age-group referral counts
- Referrals waiting longer than 52 weeks
- Monthly reporting periods

Raw data is stored in: data/raw/MHSDS_historic.csv

Processed datasets used for modelling and dashboard visualisation are stored in: data/processed/


## Business Requirements

This project addresses the following analytical questions:

1. Has ADHD referral demand increased significantly over time in England between 2019 and 2024?
2. Do mean referral counts differ significantly across age groups?
3. Has the proportion of referrals waiting longer than 52 weeks increased over time?
4. Can future ADHD referral demand be predicted with acceptable accuracy using supervised machine learning?


## Hypothesis Validation

Three statistical hypotheses were tested.

### H1 – Growth Trend in ADHD Referrals

**Null hypothesis (H₀)**  
There is no statistically significant relationship between reporting month and open ADHD referral counts.

**Alternative hypothesis (H₁)**  
There is a statistically significant positive relationship between reporting month and open ADHD referral counts.

Test used: Linear regression

Result: **Reject H₀ (p < 0.001)**


### H2 – Age Group Differences

**Null hypothesis (H₀)**  
There is no statistically significant difference in mean open ADHD referral counts across age groups.

**Alternative hypothesis (H₁)**  
There is a statistically significant difference in mean open ADHD referral counts across age groups.

Test used: One-way ANOVA

Result: **Reject H₀ (p < 0.05)**


### H3 – Long Wait Service Strain

**Null hypothesis (H₀)**  
There is no statistically significant relationship between reporting month and the proportion of ADHD referrals waiting more than 52 weeks.

**Alternative hypothesis (H₁)**  
There is a statistically significant relationship between reporting month and the long-wait referral proportion.

Test used: Linear regression

Result: **Fail to reject H₀ (p = 0.561)**


## Tools & Technologies

The project was implemented using the following tools and technologies:

- Data cleaning and preprocessing
- Time-series structuring
- Descriptive statistical analysis
- Linear regression trend testing
- One-way ANOVA hypothesis testing
- Forecast modelling using linear regression
- Model evaluation using MAE, RMSE and MAPE

Python libraries used include:

- pandas
- numpy
- scipy
- statsmodels
- matplotlib
- plotly
- streamlit

Development environment: VS Code
Version control: Git & GitHub


## Use of Generative Artificial Intelligence (GenAI) 

GenAI (Microsoft Copilot) was used to support the workflow:

- Code support: assisting with debugging. 
- Data storytelling and communication: refining text such as the project title, motivation, and objectives. Helping to write interpretations of each chart for a non-technical audience. 


## How to Run the Project

1. Clone the repository: 

git clone <repo-url>

2. Navigate to the project folder.

3. Install dependencies:

 pip install -r requirements.txt

4. Run the Streamlit dashboard:

 streamlit run app.py

The analysis notebook can be found in: jupyter_notebooks/adhd_demand_analysis_and_forecasting.ipynb


## Dashboard

An interactive dashboard was developed using **Streamlit** to present the analytical findings.

The dashboard includes four analytical views:

1. **Overview**
   - National referral demand trends
   - Key performance indicators

2. **Age Analysis**
   - Referral comparisons across age groups
   - Statistical insight from ANOVA testing

3. **Service Strain**
   - Long-wait referral trends (>52 weeks)

4. **Forecast**
   - Predicted vs actual referrals
   - Model accuracy metrics

To run the dashboard locally: 

streamlit run app.py


Example dashboard views:

![Overview](images/dashboard_overview.png)

![Age Analysis](images/dashboard_age_analysis.png)

![Service Strain](images/dashboard_service_strain.png)

![Forecast](images/dashboard_forecast.png)


## Ethical Considerations

The project uses publicly available aggregated NHS statistics.  
No personally identifiable data is included.

Analysis was conducted responsibly and results are interpreted cautiously to avoid overgeneralisation.


## Limitations

Several limitations should be considered when interpreting the results:

- The dataset contains aggregated national-level statistics, preventing regional analysis.
- Referral data reflects service activity rather than underlying ADHD prevalence.
- The forecasting model assumes continuation of historical trends.
- External factors such as policy changes or service capacity expansions may influence future referral demand.


## Future Improvements

Potential improvements include:

- Incorporating regional-level referral data
- Testing more advanced forecasting models
- Automating data updates for the dashboard
- Extending the dashboard with additional service indicators


## Project Structure

adhd-demand-forecast-england/
│
├── data
│ ├── raw
│ │ └── MHSDS_historic.csv
│ └── processed
│ ├── referrals_timeseries.csv
│ ├── age_group_referrals.csv
│ ├── service_strain.csv
│ └── forecast_results.csv
│
├── images
│ ├── dashboard_overview.png
│ ├── dashboard_age_analysis.png
│ ├── dashboard_service_strain.png
│ ├── dashboard_forecast.png
│ └── dashboard_wireframe.drawio.png
│
├── jupyter_notebooks
│ └── adhd_demand_analysis_and_forecasting.ipynb
│
├── app.py
├── requirements.txt
└── README.md


## Key Project Outputs

The main outputs of the project include:

- **Analysis notebook**  
  `jupyter_notebooks/adhd_demand_analysis_and_forecasting.ipynb`

- **Processed datasets used for modelling**  
  `data/processed/`

- **Interactive Streamlit dashboard**  
  `app.py`

- **Dashboard screenshots used in documentation**  
  `images/`


## Author

Shazia  

Data Analytics Capstone Project 2 - March 2026 


## References

NHS Digital (2025) *Mental Health Services Monthly Statistics – ADHD Waiting Times and Referrals.*

NICE (2018) *Attention Deficit Hyperactivity Disorder: Diagnosis and Management.*

NHS England (2024) *Independent ADHD Taskforce Report.*

UK Parliament Commons Library (2025) *ADHD in the UK: Prevalence and Services.*

