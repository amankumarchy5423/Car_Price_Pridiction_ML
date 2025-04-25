#  Vehicle Price Prediction

This project is a machine learning-based web application that predicts the resale price of a vehicle based on its details such as brand, engine size, mileage, year of manufacture, fuel type, and more.

The aim of this project is to help users or businesses estimate the market value of used vehicles. It's especially useful for second-hand car platforms, dealerships, or individuals looking to buy or sell a car with more confidence.

The app is built using Python and Flask for the web interface, and the machine learning pipeline is carefully designed with cloud integration using AWS for real-time model loading.

---

##  Tools & Technologies Used

1.Python - Core programming language
2.Flask - Web framework to create the application UI
3.Scikit-learn - For preprocessing and building ML models
4.Git and Github - For code tracking and code versioning
5.MLflow - To track model training and versions
6.DVC - uses for data versioning and data tracking
7.Dagshub - used for collaborative version control with mlflow , dvc and github
8.AWS S3 - To store trained models and load them during inference
9.EC2 - For hosting the application in the cloud
10.ECR - AWS Elastic Container Registry -> For storing Docker images of the application
11.joblib - For saving and loading ML models
12.Docker - For containerizing the app in production
13.Kubernetes - For runing multipule microservices on cloud
13.Github Action - Continuous Integration and Continuous Deployment (CI/CD) tools like GitHub Actions are utilized for automating the deployment process.
14.AWS Elastic Load Balancer - To distribute incoming application traffic across multiple targets, ensuring high availability and reliability.
15.AWS Auto Scaling Group - To automatically adjust the number of EC2 instances based on traffic demands, ensuring optimal performance and cost efficiency.



##  Project Workflow

### 1. Data Ingestion
- The raw data is collected from historical vehicle listings.
- The data is loaded into the project using Python.
- Logging is set up to track this step.

### 2. Data Transformation
- Preprocessing includes:
  - Handling missing values
  - Encoding categorical variables
  - Scaling numerical features
- This transformation is saved using `joblib` for reuse in production.

### 3. Model Training
- A regression model (like Linear Regression or Random Forest) is trained on the preprocessed data.
- Multiple experiments can be tracked using **MLflow**.
- The best model is saved and registered.

### 4. Model Evaluation
- The trained model is evaluated on a validation set.
- Metrics like RMSE and R² score are used to assess accuracy.
- If the model performs well, it's pushed to production.

### 5. Model Push to Cloud
- The trained model and preprocessor are uploaded to **AWS S3**.
- This allows the app to fetch and use the model directly from the cloud when deployed on **EC2**.
- This keeps the Docker image or deployment lightweight.

### 6. Prediction Pipeline (test_pipe.py)
- When the app receives user input, the pipeline:
  - Loads the model and preprocessor from S3
  - Transforms the user input
  - Predicts the estimated price
  - Displays the result on the web interface

---

##  Web Application

- The app has a clean UI with a form to enter car details.
- Upon submission, the predicted price is shown.
- The backend handles data preprocessing, prediction, and logging.

---

##  Cloud Deployment

- The app is deployed on an **AWS EC2 instance**.
- It is accessible through the server's public IP.
- The model is **not stored locally** on EC2; it's dynamically downloaded from **S3** at runtime.

---

##  Final Thoughts

This project demonstrates the full ML lifecycle:
- From data preprocessing to model deployment
- Integration with real cloud services
- Usable and clean web interface

It reflects real-world scenarios and is built with scalability and modularity in mind.

---

