# 01 - Introduction
## ML Ops
- ML Ops: Putting machine learning to production
- Stages in MLOps
![alt text](<Screenshot 2025-05-05 at 22.14.40.png>)

### Example Case
Green Taxi duration model training: [notebook link](https://github.com/DataTalksClub/mlops-zoomcamp/blob/main/01-intro/duration-prediction.ipynb)
Problems without MLOps:
- No tracker for every model training with different algorithms --> solved with **Experiment Tracking**
- No proper model registration --> solved with **Model Registry**
- Cannot be reexecuted easily if there is different dataset to run solved with **ML Training Pipeline**

### Best Practice
1. Include **experiment tracking**
2. Create **training pipeline** to automate generating model using pre-defined scripts.
3. Store model in **model registry**
4. **Deploy** model to be accessed by users, for example using web services.
5. Create **monitoring** system to alert user if there is performance drop or *automatically trigger training* pipeline to produce new model and deploy the new model automatically
6. Scripts should be well-maintained, clean and well-documented

### MLOps Maturity model
| Level    | Characteristics | 
| -------- | ------- |
| 0  | **No MLOps**<br>No automation, All code in Jupyter Notebook   |
| 1 | **DevOps, But No MLOps** <br> - Release are automated, Unit test, CI/CD, Ops Metrics <br> - DS separated from engineers, no reproducibility, no experiment tracking    |
| 2    | **Automated Training**<br> - Training pipeline, experiment tracking, model registry, low friction deployment, DS work with engineers |
| 3    | **Automated Deployment**<br> - Deployment is done without user intervention <br> - A/B Test, Model Monitoring
| 4    | **Full MLOps Automation**<br> Automatic training, automatic retraining and automatic deployment in one place

### Setting Up Anaconda
1. Open github code space
2. Get Anaconda
```
wget https://repo.anaconda.com/archive/Anaconda3-2022.05-Linux-x86_64.sh
bash Anaconda3-2022.05-Linux-x86_64.sh
```
