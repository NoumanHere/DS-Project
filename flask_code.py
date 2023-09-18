from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from pycaret.regression import *
from sklearn.cluster import KMeans


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Handle file upload
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            # Save the uploaded file
            file_path = "uploads/" + uploaded_file.filename
            uploaded_file.save(file_path)

            # Read the uploaded CSV into a Pandas DataFrame
            df = pd.read_csv(file_path)

            # Perform data preprocessing (follow the preprocessing steps from your original code)
            columns_to_drop = ['ID', 'Customer Pay']
            df.drop(columns=columns_to_drop, inplace=True)

            # Calculate the 'Custom_Miles' feature
            #df['Customer RPM'] = df['Customer Pay'] / df['Miles']

            # Drop rows with 'Customer Pay' equal to 0
            #df = df[df[['Customer Pay', 'Customer RPM']] != 0]

            # Drop duplicates
            df.drop_duplicates(inplace=True)

            # Handle missing values (drop rows with missing values)
            df.dropna(inplace=True)

            # Filter the data to keep only rows where 'Miles' < 50, but check if there are rows to filter first

            #df = df[df['Miles'] > 50]

            """if df['Miles'].lt(50).any():
                df = df[df['Miles'] < 50]
            else:
                print("No rows with 'Miles' less than 50 found in the dataset.")"""

            # 4. Apply K-Means clustering to 'Miles' to create 'Miles_Cluster' (k=10)
            miles_data = df[['Miles']]
            kmeans = KMeans(n_clusters=10, random_state=0)
            df['Miles_Cluster'] = kmeans.fit_predict(miles_data)


            # 7. Calculate 'Miles_Range' based on custom ranges
            custom_ranges = [0, 100, 200, 300, 400, 500, 600, 700, 800, 1000, 2000, 4000, 10000]
            df['Miles_Range'] = pd.cut(df['Miles'], bins=custom_ranges, labels=False) + 1


            # Convert 'Pickup Date' to datetime data type
            df['Pickup Date'] = pd.to_datetime(df['Pickup Date'])

            # Define the function to extract date features
            def extract_date_features(df):
                df['Year'] = df['Pickup Date'].dt.year
                df['Month'] = df['Pickup Date'].dt.month
                df['Day'] = df['Pickup Date'].dt.day
                df['Dayofweek'] = df['Pickup Date'].dt.dayofweek
                df['DayOfyear'] = df['Pickup Date'].dt.dayofyear
                df['Week'] = df['Pickup Date'].dt.isocalendar().week
                df['Quarter'] = df['Pickup Date'].dt.quarter
                df['Is_month_start'] = df['Pickup Date'].dt.is_month_start
                df['Is_month_end'] = df['Pickup Date'].dt.is_month_end
                df['Is_quarter_start'] = df['Pickup Date'].dt.is_quarter_start
                df['Is_quarter_end'] = df['Pickup Date'].dt.is_quarter_end
                df['Is_year_start'] = df['Pickup Date'].dt.is_year_start
                df['Is_year_end'] = df['Pickup Date'].dt.is_year_end
                df['Semester'] = np.where(df['Quarter'].isin([1, 2]), 1, 2)
                df['Is_weekend'] = np.where(df['Dayofweek'].isin([5, 6]), 1, 0)
                df['Is_weekday'] = np.where(df['Dayofweek'].isin([0, 1, 2, 3, 4]), 1, 0)
                df['Days_in_month'] = df['Pickup Date'].dt.days_in_month
                return df

            # Extract date features
            df = extract_date_features(df)

            # Create new features: LANE and LANE_KMA
            df['LANE'] = df['Origin City'] + ', ' + df['Origin State'] + ' - ' + df['Delivery City'] + ', ' + df['Delivery State']

            # Convert 'LANE_KMA' to categorical data type
            #df['LANE'] = df['LANE'].astype('category')

            # Combine 'Origin KMA' and 'Delivery KMA' into 'LANE_KMA' and treat it as categorical
            df['LANE_KMA'] = df['Origin KMA'] + ' - ' + df['Delivery KMA']

            # Perform regression setup
            
            regression = setup(data=df, target='RPM', session_id=123, normalize=True, transformation=True, train_size=0.80, transformation_method='yeo-johnson')

            # Get regression results (you can use PyCaret functions for this)
            
            best_model = compare_models()
            model=create_model(best_model)
            final_model=finalize_model(model)
            print(final_model)
            save_model(final_model, model_name='Main_Model_sept1')
            # Render the results template with the relevant data
            return render_template('result.html', results=final_model)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
