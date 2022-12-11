import joblib
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from pages.Util import CombinedAttributesAdder
from sklearn.model_selection import cross_val_score

import streamlit as st
import pandas as pd

from hydralit import HydraHeadApp

#This will be useful for the encoding phase
housing = pd.read_csv('.\\CaliHousing\\housing.csv')
# Them column income_cat dung de chia data
housing["income_cat"] = pd.cut(housing["median_income"],
                            bins=[0., 1.5, 3.0, 4.5, 6., np.inf],
                            labels=[1, 2, 3, 4, 5])

split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
for train_index, test_index in split.split(housing, housing["income_cat"]):
    strat_train_set = housing.loc[train_index]
    strat_test_set = housing.loc[test_index]

# Chia xong thi delete column income_cat
for set_ in (strat_train_set, strat_test_set):
    set_.drop("income_cat", axis=1, inplace=True)

housing = strat_train_set.drop("median_house_value", axis=1)
housing_labels = strat_train_set["median_house_value"].copy()

housing_num = housing.drop("ocean_proximity", axis=1)

num_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy="median")),
        ('attribs_adder', CombinedAttributesAdder()),
        ('std_scaler', StandardScaler()),
    ])

num_attribs = list(housing_num)
cat_attribs = ["ocean_proximity"]
full_pipeline = ColumnTransformer([
        ("num", num_pipeline, num_attribs),
        ("cat", OneHotEncoder(), cat_attribs),
    ])

class PredictCaliHouse(HydraHeadApp):
    def run(self):
        select = st.selectbox("Model: ",("Linear Regression","Random Forest Regression","Random Forest Regression Grid Search CV","Random Forest Regression Random Search CV"),
        ) 
        container1 = st.empty()
        with container1:
            col1,col2,col3 = st.columns(3)
            with col1:
                longitude = st.number_input('Longitude',value=-122.23)
                latitude = st.number_input('Latitude',value=37.88)
                housingMedianAge = st.number_input('Housing Median Age',value=41)
            with col2:
                totalRooms = st.number_input('Total Rooms',value=880)
                totalBedrooms = st.number_input('Total Bedrooms',value=129)
                population = st.number_input('Population',value=322)
            with col3:
                households = st.number_input('Household',value=126)
                medianIncome = st.number_input('Median Income',value=8.3252)
                oceanProximity = st.selectbox('Ocean Proximity',('INLAND','<1H OCEAN','NEAR BAY','NEAR OCEAN','ISLAND'))
        data = {'longitude': longitude,
                'latitude': latitude,
                'housing_median_age': housingMedianAge,
                'total_rooms': totalRooms,
                'total_bedrooms': totalBedrooms,
                'population': population,
                'households': households,
                'median_income': medianIncome,
                'ocean_proximity': oceanProximity,
                }
        features = pd.DataFrame(data, index=[0])   

        df = features
        st.subheader('Dữ liệu đầu vào')
        st.write('Dữ liệu người dùng nhập vào: ',df)
        # Encoding of ordinal features
        df = pd.concat([features,housing],axis=0)
        df_prepared = full_pipeline.fit_transform(df)
        df_prepared = df_prepared[:1] # Selects only the first row (the user input data)
        st.write('Dữ liệu mã hóa cho input : ',df_prepared)

                
        # Reads in saved classification model
        if(select == "Linear Regression"):
            model = joblib.load('.\\pages\\CaliHousing\\lin_reg.pkl')
        elif(select == "Random Forest Regression"):
            model = joblib.load('.\\pages\\CaliHousing\\forest_reg.pkl')
        elif(select == "Random Forest Regression Grid Search CV"):
            model = joblib.load('.\\pages\\CaliHousing\\forest_reg_grid_search.pkl')
        elif(select == "Random Forest Regression Random Search CV"):
            model = joblib.load('.\\pages\\CaliHousing\\forest_reg_random_search.pkl')
        st.subheader('Dự đoán')
        st.write("Giá nhà dự đoán: $", model.predict(df_prepared)[0])
        
