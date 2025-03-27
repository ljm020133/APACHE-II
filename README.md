# APACHE II, IV, and IVa Scoring System (ICU Patient Severity Prediction)

This project implements a full pipeline to calculate **APACHE II**, **APACHE IV**, and **APACHE IVa** scores based on ICU patient data. These scores help assess the severity of illness and predict outcomes such as ICU and hospital mortality.

## What Is APACHE?

APACHE (Acute Physiology And Chronic Health Evaluation) is a scoring system widely used in ICUs to evaluate how critically ill a patient is, using a combination of physiological variables, lab values, and chronic health indicators.

---

## Project Structure

apache_scoring_project/ ├── data/ │ ├── physicalExam.csv │ ├── lab.csv │ ├── patient.csv │ ├── diagnosis.csv │ ├── ... │ └── updated_APACHE_data.csv # Final merged dataset ├── apache_scoring.py # Scoring functions (modular) ├── preprocessing/ # Data cleaning scripts ├── fileMerger.py # Merges physical/lab/patient data └── README.md


---

## Features

- **APACHE II scoring** (implemented so far):
  - Heart Rate
  - Mean Arterial Pressure (MAP)
  - Respiratory Rate
  - Oxygenation (PaO2, FiO2, PaCO2)
  - Temperature
  - White Blood Cell Count (WBC)
  - Sodium
  - Creatinine
  - BUN (Blood Urea Nitrogen)
  - Hematocrit
  - Glucose
  - GCS (Glasgow Coma Scale)

- **Score accuracy tracking** per patient based on data availability
- Extensive data cleaning for:
  - Merging inconsistent labels (e.g. `pco2` vs `paCO2`)
  - One-hot GCS fields into structured scores
  - Fixing `FiO2` inconsistencies from physical exam notes

---

## How It Works

1. **Raw data is preprocessed** from multiple CSVs (lab, physicalExam, patient)
2. **Filtered and cleaned** into `updated_APACHE_data.csv`
3. **Modular scoring functions** are applied to calculate each APACHE II component
4. Total APACHE score is calculated, along with accuracy (% of available components)

---

## How to Run

1. Place all raw `.csv` files in the `data/` directory
2. Run the preprocessing scripts to clean and merge:
   ```bash
   python fileMerger.py


