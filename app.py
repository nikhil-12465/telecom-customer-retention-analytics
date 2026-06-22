
import pandas as pd
import pickle
from flask import Flask, render_template, request

app = Flask(__name__)

# Load Model

with open("model.sav", "rb") as f:
    model = pickle.load(f)

# Load training columns
model_cols = pd.read_csv(
    "tel_churn.csv",
    nrows=1
).columns.tolist()

# Remove unused columns
for col in ["Unnamed: 0", "Churn"]:
    if col in model_cols:
        model_cols.remove(col)


# Home Route

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        try:

        
            # Form Inputs
        

            senior_citizen = request.form.get("query1", "0")
            monthly_charges = request.form.get("query2", "0")
            total_charges = request.form.get("query3", "")

            gender = request.form.get("query4", "Female")
            partner = request.form.get("query5", "No")
            dependents = request.form.get("query6", "No")

            phone_service = request.form.get("query7", "Yes")
            multiple_lines = request.form.get("query8", "No")

            internet_service = request.form.get("query9", "DSL")

            online_security = request.form.get("query10", "No")
            online_backup = request.form.get("query11", "No")
            device_protection = request.form.get("query12", "No")
            tech_support = request.form.get("query13", "No")

            streaming_tv = request.form.get("query14", "No")
            streaming_movies = request.form.get("query15", "No")

            contract = request.form.get(
                "query16",
                "Month-to-month"
            )

            paperless_billing = request.form.get(
                "query17",
                "Yes"
            )

            payment_method = request.form.get(
                "query18",
                "Electronic check"
            )

            tenure = request.form.get("query19", "1")

        
            # Numeric Conversion
        

            senior_citizen = int(float(senior_citizen))
            monthly_charges = float(monthly_charges)

            tenure = int(float(tenure))

        
            # Tenure Validation
        

            if tenure < 1:
                tenure = 1

            if tenure > 72:
                tenure = 72

        
            # Total Charges
        

            try:
                total_charges = float(total_charges)

            except:
                total_charges = monthly_charges * tenure

        
            # Create Input DataFrame
        

            input_dict = {

                "SeniorCitizen": senior_citizen,
                "MonthlyCharges": monthly_charges,
                "TotalCharges": total_charges,

                "gender": gender,
                "Partner": partner,
                "Dependents": dependents,

                "PhoneService": phone_service,
                "MultipleLines": multiple_lines,

                "InternetService": internet_service,

                "OnlineSecurity": online_security,
                "OnlineBackup": online_backup,
                "DeviceProtection": device_protection,
                "TechSupport": tech_support,

                "StreamingTV": streaming_tv,
                "StreamingMovies": streaming_movies,

                "Contract": contract,

                "PaperlessBilling": paperless_billing,

                "PaymentMethod": payment_method,

                "tenure": tenure
            }

            new_df = pd.DataFrame([input_dict])

        
            # Create Tenure Group
        

            labels = [
                "1 - 12",
                "13 - 24",
                "25 - 36",
                "37 - 48",
                "49 - 60",
                "61 - 72"
            ]

            new_df["tenure_group"] = pd.cut(
                new_df["tenure"],
                bins=[1, 13, 25, 37, 49, 61, 73],
                labels=labels,
                right=False
            )

            new_df.drop(
                columns=["tenure"],
                inplace=True
            )

        
            # Dummy Encoding
        

            new_df_dummies = pd.get_dummies(new_df)

            final_df = new_df_dummies.reindex(
                columns=model_cols,
                fill_value=0
            )

        
            # Prediction
        

            prediction = model.predict(
                final_df
            )[0]

            probability = model.predict_proba(
                final_df
            )[0][1]

            churn_probability = round(
                probability * 100,
                2
            )

            retention_probability = round(
                (1 - probability) * 100,
                2
            )

        
            # Risk Level
        

            if probability >= 0.75:
                risk = "HIGH RISK"
                risk_class = "high-risk"

            elif probability >= 0.45:
                risk = "MEDIUM RISK"
                risk_class = "medium-risk"

            else:
                risk = "LOW RISK"
                risk_class = "low-risk"

        
            # Messages
        

            if prediction == 1:

                output1 = (
                    "Customer is likely to churn"
                )

                output2 = (
                    f"Churn Probability: "
                    f"{churn_probability}%"
                )

            else:

                output1 = (
                    "Customer is likely to stay"
                )

                output2 = (
                    f"Retention Probability: "
                    f"{retention_probability}%"
                )

            return render_template(
                "home.html",

                output1=output1,
                output2=output2,

                risk=risk,
                risk_class=risk_class,

                churn_probability=churn_probability,
                retention_probability=retention_probability,

                **request.form
            )

        except Exception as e:

            return render_template(
                "home.html",
                output1="Prediction Error",
                output2=str(e)
            )

    return render_template("home.html")


# Run Application

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=7860
    )

