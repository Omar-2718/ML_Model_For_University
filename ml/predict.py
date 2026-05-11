import sys
import json
import joblib
import pandas as pd
from pathlib import Path

def main():
    base_dir = Path(__file__).resolve().parent
    artifact_dir = base_dir / "model_artifacts"
    
    if len(sys.argv) > 1 and sys.argv[1] == "--features":
        with open(artifact_dir / "feature_schema.json") as f:
            feature_schema = json.load(f)
        print(json.dumps({"features": feature_schema["features"]}))
        return

    age = float(sys.argv[1].strip('"'))
    gender = sys.argv[2].strip('"')
    education_level = sys.argv[3].strip('"')
    job_title = sys.argv[4].strip('"')
    years_of_experience = float(sys.argv[5].strip('"'))

    model = joblib.load(artifact_dir / "salary_model.joblib")
    scaler = joblib.load(artifact_dir / "robust_scaler.joblib")
    with open(artifact_dir / "category_mappings.json") as f:
        mappings = json.load(f)
    with open(artifact_dir / "feature_schema.json") as f:
        feature_schema = json.load(f)

    gender_encoded = mappings["gender"][gender]
    education_encoded = mappings["education_level"][education_level]
    job_title_encoded = mappings["job_title"].get(job_title, mappings["global_salary_mean"])

    values_by_feature = {
        "Age": age,
        "Gender": gender_encoded,
        "Education Level": education_encoded,
        "Job Title": job_title_encoded,
        "Years of Experience": years_of_experience,
    }
    features = pd.DataFrame(
        [[values_by_feature[name] for name in feature_schema["features"]]],
        columns=feature_schema["features"]
    )
    features_scaled = scaler.transform(features)
    salary = float(model.predict(features_scaled)[0])

    print(json.dumps({
        "salary": round(salary, 2)
    }))

if __name__ == "__main__":
    main()
