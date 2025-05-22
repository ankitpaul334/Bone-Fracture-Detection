#  Bone Fracture Detection System

An AI-powered medical imaging project that uses deep learning models (ResNet50) to automatically detect bone fractures from X-ray and MRI scans. This system assists radiologists by improving diagnostic accuracy, reducing diagnosis time, and increasing accessibility to quality healthcare diagnostics.

##  Project Overview

This project leverages Convolutional Neural Networks (CNNs) for:
- Bone Type Classification (Hand, Elbow, Shoulder)
- Fracture Detection based on classified bone type
- Severity Estimation to assist in clinical decision-making

The system is trained on the MURA dataset, one of the largest public musculoskeletal radiograph datasets.

##  Features

- Image preprocessing: noise reduction, augmentation, and resizing
- ResNet50-based bone classification and fracture detection
- Heatmap-based output visualization
- Functional test case validation
- Privacy-preserving data handling

##  Folder Structure

- `/data` – Contains processed/raw images
- `/models` – Trained deep learning models
- `/notebooks` – Model training/evaluation notebooks
- `/src` – Core code for preprocessing, model training, and inference
- `/app` – Flask-based UI for predictions
- `/docs` – Project documentation and reports
- `/tests` – Functional test cases and results

##  Models Used

- ResNet50 (Main architecture)
- Optional: DenseNet & VGG16 (for comparison)

##  Installation

1. Clone the repository:

git clone https://github.com/yourusername/bone-fracture-detection.git
cd bone-fracture-detection


2. Install required packages:

pip install -r requirements.txt


3. Download the MURA dataset and place it in `/data`.

##  Running the Project

To run the web interface:

cd app
python app.py


To train the model:

python src/train_model.py


To make predictions:

python src/predict.py


##  Functional Test Coverage

- Image preprocessing validation
- Bone classification accuracy
- Fracture detection precision
- Handling of invalid image inputs
- Logging and report generation

##  Target Users

- Radiologists & Orthopedic Experts
- Medical AI Researchers
- Healthcare Institutions

##  Contributors

- Astha Jaiswal  
- Ankit Paul  
- Dhawal Sahu  
- Anushka Sharma  

## 📜 License

This repository is intended for academic and research use only.
