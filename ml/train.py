import pandas as pd
import json
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, RobustScaler
from sklearn.ensemble import GradientBoostingRegressor

base_dir = Path(__file__).resolve().parent
data_file = base_dir / "data" / "Salary_Data[1].csv"
output_dir = base_dir / "model_artifacts"
output_dir.mkdir(exist_ok=True)

df = pd.read_csv(data_file)
df = df.drop_duplicates()

df = df[df['Gender'].notna()]
df = df[df['Gender'].isin(['Male', 'Female'])]
df = df[df['Years of Experience'].notna()]
df = df[df['Education Level'].notna()]

df["Salary"] = df.groupby("Years of Experience")["Salary"].transform(
    lambda x: x.fillna(x.median())
)
df = df[df['Salary'].notna()]

X = df.drop("Salary", axis=1)
y = df["Salary"]
feature_names = X.columns.tolist()

x_train, x_test, y_train, y_test = train_test_split(
    X, y, train_size=0.8, random_state=42, shuffle=True
)

le_gender = LabelEncoder()
gender_encoded_train = le_gender.fit_transform(x_train["Gender"])
gender_mapping = {label: int(code) for label, code in zip(le_gender.classes_, le_gender.transform(le_gender.classes_))}

x_train["Gender"] = gender_encoded_train
x_test["Gender"] = le_gender.transform(x_test["Gender"])

education_normalize = {
    "Bachelor's Degree": "Bachelor's",
    "Master's Degree": "Master's",
    "phD": "PhD"
}
x_train["Education Level"] = x_train["Education Level"].replace(education_normalize)
x_test["Education Level"] = x_test["Education Level"].replace(education_normalize)

education_ordinal_map = {"High School": 0, "Bachelor's": 1, "Master's": 2, "PhD": 3}
x_train["Education Level"] = x_train["Education Level"].map(education_ordinal_map)
x_test["Education Level"] = x_test["Education Level"].map(education_ordinal_map)

train_data_with_salary = x_train.copy()
train_data_with_salary["Salary"] = y_train
job_title_mean = train_data_with_salary.groupby("Job Title")["Salary"].mean().to_dict()

x_train["Job Title"] = x_train["Job Title"].map(job_title_mean)
x_test["Job Title"] = x_test["Job Title"].map(job_title_mean)
x_test["Job Title"] = x_test["Job Title"].fillna(y_train.mean())

scaler = RobustScaler()
x_train_scaled = scaler.fit_transform(x_train)
x_test_scaled = scaler.transform(x_test)

model = GradientBoostingRegressor(
    n_estimators=300,
    learning_rate=0.1,
    max_depth=5,
    random_state=33
)
model.fit(x_train_scaled, y_train)

joblib.dump(model, output_dir / "salary_model.joblib")
joblib.dump(scaler, output_dir / "robust_scaler.joblib")

mappings = {
    "gender": gender_mapping,
    "education_level": education_ordinal_map,
    "job_title": job_title_mean,
    "global_salary_mean": float(y_train.mean()),
}
with open(output_dir / "category_mappings.json", "w") as f:
    json.dump(mappings, f, indent=2)

feature_schema = {
    "features": feature_names,
    "feature_count": len(feature_names)
}
with open(output_dir / "feature_schema.json", "w") as f:
    json.dump(feature_schema, f, indent=2)
