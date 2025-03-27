import pandas as pd
import os

# === File Paths ===
base_dir = r"C:\Users\gigm2\OneDrive - Iowa State University\Desktop\work\data\APACH II\APACHE 2, 4, 4a\data"
input_file = os.path.join(base_dir, "updated_APACHE_data.csv")
output_file = os.path.join(base_dir, "updated_APACHE_data.csv")

# === Load Dataset ===
df = pd.read_csv(input_file)
# === Clean up duplicate BUN columns ===
if "BUN" in df.columns and "bun" in df.columns:
    # Prefer the one with more non-null values
    if df["bun"].isna().sum() > df["BUN"].isna().sum():
        df["bun"] = df["BUN"]  # Replace with more complete version

    # Drop the redundant column
    df.drop(columns=["BUN"], inplace=True)

# === APACHE II Scoring Functions ===

def apache_heart_rate_score(hr):
    if pd.isna(hr): return None
    if hr < 40 or hr >= 180: return 4
    elif 40 <= hr <= 54 or 140 <= hr <= 179: return 3
    elif 55 <= hr <= 69 or 110 <= hr <= 139: return 2
    elif 70 <= hr <= 109: return 0
    return None

def apache_map_score(map_value):
    if pd.isna(map_value): return None
    if map_value < 50 or map_value >= 160: return 4
    elif 130 <= map_value <= 159: return 3
    elif 50 <= map_value <= 69 or 110 <= map_value <= 129: return 2
    elif 70 <= map_value <= 109: return 0
    return None

def apache_rr_score(rr):
    if pd.isna(rr): return None
    if rr < 6 or rr >= 50: return 4
    elif 6 <= rr <= 9 or 35 <= rr <= 49: return 2
    elif 10 <= rr <= 11 or 25 <= rr <= 34: return 1
    elif 12 <= rr <= 24: return 0
    return None

def apache_oxygenation_score(row):
    pao2 = row.get("PaO2_combined")
    paco2 = row.get("PaCO2_combined")
    fio2 = row.get("FiO2_clean")

    if pd.isna(pao2) or pd.isna(fio2): return None
    fio2_frac = fio2 / 100.0

    if fio2_frac >= 0.5 and not pd.isna(paco2):
        aa_gradient = (713 * fio2_frac) - (paco2 / 0.8) - pao2
        if aa_gradient > 500: return 4
        elif aa_gradient > 350: return 3
        elif aa_gradient > 200: return 2
        else: return 0
    else:
        if fio2_frac == 0: return None
        ratio = pao2 / fio2_frac
        if ratio < 55: return 4
        elif ratio <= 60: return 3
        elif ratio <= 70: return 2
        elif ratio <= 200: return 1
        else: return 0

def apache_temp_score(temp_c):
    if pd.isna(temp_c):
        return None
    if temp_c >= 41 or temp_c < 29.9:
        return 4
    elif 39 <= temp_c < 41:
        return 3
    elif 38.5 <= temp_c < 39:
        return 1
    elif 36 <= temp_c < 38.5:
        return 0
    elif 34 <= temp_c < 36:
        return 1
    elif 32 <= temp_c < 34:
        return 2
    elif 30 <= temp_c < 32:
        return 3
    elif 29.9 <= temp_c < 30:
        return 4
    return None

def apache_wbc_score(wbc):
    if pd.isna(wbc):
        return None
    if wbc < 1 or wbc >= 40:
        return 4
    elif 1 <= wbc < 3:
        return 2
    elif 3 <= wbc < 15:
        return 0
    elif 15 <= wbc < 20:
        return 1
    elif 20 <= wbc < 40:
        return 2
    return None

def apache_sodium_score(na):
    if pd.isna(na):
        return None
    if na <= 110 or na >= 180:
        return 4
    elif 111 <= na <= 119 or 160 <= na <= 179:
        return 3
    elif 120 <= na <= 129 or 155 <= na <= 159:
        return 2
    elif 150 <= na <= 154:
        return 1
    elif 130 <= na <= 149:
        return 0
    return None

# potassium score but current dataset does not have potassium
def apache_potassium_score(k):
    if pd.isna(k):
        return None
    if k >= 7.0:
        return 4
    elif 6.0 <= k < 7.0:
        return 3
    elif 5.5 <= k < 6.0:
        return 1
    elif 3.5 <= k < 5.5:
        return 0
    elif 3.0 <= k < 3.5:
        return 1
    elif 2.5 <= k < 3.0:
        return 2
    elif k < 2.5:
        return 4
    return None

def apache_creatinine_score(row):
    creat = row.get("creatinine")
    dialysis = row.get("dialysis")

    if pd.isna(creat):
        return None

    # If on dialysis and Cr ≥ 3.5, score is 0
    if dialysis == 1 and creat >= 3.5:
        return 0
    elif creat >= 3.5:
        return 4
    elif 2.0 <= creat < 3.5:
        return 3
    elif 1.5 <= creat < 2.0:
        return 2
    elif 0.6 <= creat < 1.5:
        return 0
    elif creat < 0.6:
        return 2
    return None


def apache_bun_score(bun):
    if pd.isna(bun):
        return None
    if bun >= 96:
        return 4
    elif 70 <= bun < 96:
        return 3
    elif 50 <= bun < 70:
        return 2
    elif 40 <= bun < 50:
        return 1
    elif 18 <= bun < 40:
        return 0
    elif bun < 18:
        return 2
    return None

def apache_glucose_score(glucose):
    if pd.isna(glucose):
        return None
    if glucose >= 500:
        return 4
    elif 200 <= glucose < 500:
        return 2
    elif 70 <= glucose < 200:
        return 0
    elif glucose < 70:
        return 2
    return None

def apache_hematocrit_score(hct):
    if pd.isna(hct):
        return None
    if hct >= 60:
        return 4
    elif 50 <= hct < 60:
        return 2
    elif 46 <= hct < 50:
        return 1
    elif 30 <= hct < 46:
        return 0
    elif 20 <= hct < 30:
        return 2
    elif hct < 20:
        return 4
    return None

def apache_ph_score(ph):
    if pd.isna(ph):
        return None
    if ph >= 7.7:
        return 4
    elif 7.6 <= ph < 7.7:
        return 3
    elif 7.5 <= ph < 7.6:
        return 1
    elif 7.33 <= ph < 7.5:
        return 0
    elif 7.25 <= ph < 7.33:
        return 2
    elif 7.15 <= ph < 7.25:
        return 3
    elif ph < 7.15:
        return 4
    return None

def apache_albumin_score(albumin):
    if pd.isna(albumin):
        return None
    if albumin >= 3.5:
        return 0
    elif 2.5 <= albumin < 3.5:
        return 1
    elif albumin < 2.5:
        return 2
    return None

def apache_bilirubin_score(bili):
    if pd.isna(bili):
        return None
    if bili < 2.0:
        return 0
    elif 2.0 <= bili < 5.0:
        return 1
    elif 5.0 <= bili < 10.0:
        return 2
    elif bili >= 10.0:
        return 4
    return None



# === Find columns ===
eye_cols = [col for col in df.columns if "gcs/eyes" in col.lower()]
motor_cols = [col for col in df.columns if "gcs/motor" in col.lower()]
verbal_cols = [col for col in df.columns if "gcs/verbal" in col.lower()]

# Replace NaNs with 0 temporarily if needed (optional)
df["gcs_eye"] = df["gcs_eye"].fillna(0)
df["gcs_motor"] = df["gcs_motor"].fillna(0)
df["gcs_verbal"] = df["gcs_verbal"].fillna(0)

# === Get max (assumes binary 0/1s indicating score presence) ===
df["gcs_eye"] = df[eye_cols].mul([int(col.split("/")[-1]) for col in eye_cols], axis=1).max(axis=1)
df["gcs_motor"] = df[motor_cols].mul([int(col.split("/")[-1]) for col in motor_cols], axis=1).max(axis=1)
df["gcs_verbal"] = df[verbal_cols].mul([int(col.split("/")[-1]) for col in verbal_cols], axis=1).max(axis=1)

# === Total GCS ===
# Compute GCS total (should be in range 3–15)
df["gcs_total"] = df["gcs_eye"] + df["gcs_motor"] + df["gcs_verbal"]
df["gcs_total"] = df["gcs_total"].clip(lower=3, upper=15)

# Now subtract from 15
df["apache_gcs_score"] = 15 - df["gcs_total"]

# === List of APACHE II score component columns you've calculated ===
apache_score_columns = [
    "apache_temp_score",
    "apache_map_score",
    "apache_hr_score",
    "apache_rr_score",
    "apache_oxygenation_score",
    "apache_ph_score",
    "apache_sodium_score",      
    "apache_potassium_score",    # skip if not yet added
    "apache_creatinine_score",
    "apache_hematocrit_score",
    "apache_wbc_score",
    "apache_gcs_score",
    "apache_glucose_score",
    "apache_bun_score"
]

# === Filter out score columns that aren't in your dataset
apache_score_columns = [col for col in apache_score_columns if col in df.columns]

# === Total APACHE II score
df["apache2_score_total"] = df[apache_score_columns].sum(axis=1, skipna=True)

# === Count how many score components are present
df["apache2_score_components_count"] = df[apache_score_columns].notna().sum(axis=1)

# === Calculate % completeness (accuracy)
df["apache2_score_accuracy"] = df["apache2_score_components_count"] / len(apache_score_columns)


# === Apply Scoring ===
df["apache_hr_score"] = df["heartrate"].apply(apache_heart_rate_score)
df["apache_map_score"] = df["meanbp"].apply(apache_map_score)
df["apache_rr_score"] = df["respiratoryrate"].apply(apache_rr_score)
df["apache_oxygenation_score"] = df.apply(apache_oxygenation_score, axis=1)
df["apache_temp_score"] = df["temperature"].apply(apache_temp_score)
df["apache_wbc_score"] = df["wbc"].apply(apache_wbc_score)
df["apache_sodium_score"] = df["sodium"].apply(apache_sodium_score)
df["apache_creatinine_score"] = df.apply(apache_creatinine_score, axis=1)
df["apache_bun_score"] = df["bun"].apply(apache_bun_score)
df["apache_glucose_score"] = df["glucose"].apply(apache_glucose_score)
df["apache_hematocrit_score"] = df["hematocrit"].apply(apache_hematocrit_score)
df["apache_ph_score"] = df["ph"].apply(apache_ph_score)
df["apache_albumin_score"] = df["albumin"].apply(apache_albumin_score)
df["apache_bilirubin_score"] = df["bilirubin"].apply(apache_bilirubin_score)

# potassium score but current dataset does not have potassium
df["apache_potassium_score"] = df["potassium"].apply(apache_potassium_score)


# === Save Updated Dataset ===
df.to_csv(output_file, index=False)
print(f"Updated APACHE dataset saved to: {output_file}")
