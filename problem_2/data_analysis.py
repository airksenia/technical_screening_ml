import pandas as pd
import numpy as np
import pickle
import datetime
from talos.utils import lr_normalizer







def  main():
    data=pd.read_csv('data.csv')
    df=data
#start creating dict
    results={'number_of_orders_in_the_same_state': 0}
    for kk in range(len(df)):
        if df.loc[kk,'start_state_abr']==df.loc[kk, 'end_state_abr']:
            results['number_of_orders_in_the_same_state']=results['number_of_orders_in_the_same_state'] + 1
            
    results['number_of_orders_in_the_same_city']=0
    for kk in range(len(df)):
        if df.loc[kk, 'start_city']==df.loc[kk, 'end_city']:
            results['number_of_orders_in_the_same_city']=results['number_of_orders_in_the_same_city'] + 1
            
    results['number_of_orders_in_the_same_zipcode']=0
    for kk in range(len(df)):
        if df.loc[kk, 'start_zip']==df.loc[kk, 'end_zip']:
            results['number_of_orders_in_the_same_zipcode']=results['number_of_orders_in_the_same_zipcode'] + 1

    results['number_of_orders_in_different_state'] = 0
    for kk in range(len(df)):
        if df.loc[kk, 'start_state_abr']!=df.loc[kk, 'end_state_abr']:
            results['number_of_orders_in_different_state']=results['number_of_orders_in_different_state'] + 1
            
    results['number_of_orders_in_different_city']=0
    for kk in range(len(df)):
        if df.loc[kk, 'start_city']!=df.loc[kk, 'end_city']:
            results['number_of_orders_in_different_city']=results['number_of_orders_in_different_city'] + 1
            
    results['number_of_orders_in_different_zipcode']=0
    for kk in range(len(df)):
        if df.loc[kk, 'start_zip']!=df.loc[kk, 'end_zip']:
            results['number_of_orders_in_different_zipcode']=results['number_of_orders_in_different_zipcode'] + 1
    
    results['number_of_unique_cities']=0
    cities=[]
    for kk in range(len(df)):
        if df.loc[kk, 'start_city'] not in cities:
            cities.append(df.loc[kk, 'start_city'])
        if df.loc[kk, 'end_city'] not in cities:
            cities.append(df.loc[kk, 'end_city'])
    results['number_of_unique_cities']=len(cities)
    
    results['number_of_unique_zipcodes']=0
    cities=[]
    for kk in range(len(df)):
        if df.loc[kk, 'start_zip'] not in cities:
            cities.append(df.loc[kk, 'start_zip'])
        if df.loc[kk, 'end_zip'] not in cities:
            cities.append(df.loc[kk, 'end_zip'])
    results['number_of_unique_zipcodes']=len(cities)
    
    results['average_total_drive_miles']=0
    results['average_total_drive_miles']=np.mean(df['total_distance_miles'].values)
    
    results['order_id_of_the_heaviest_order']=0
    index=np.argmax(df['total_weight_lbs'])
    results['order_id_of_the_heaviest_order']=df['order_id'][index]
    
    results['features_ranked_by_importance']={}
    from sklearn.base import clone 
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    categorical_columns=['order_id',
        'start_state_abr',
            'end_state_abr',
        'start_city',
        'end_city',
        'start_zip','end_zip']
    continuous_columns=['total_volume_inches3', 'total_distance_miles', 'total_weight_lbs']
    response_column="total_predicted_hours"
    X=pd.get_dummies(df[categorical_columns + continuous_columns], columns=list(categorical_columns))
    y=df[response_column].values
    predictors={col: [col] for col in continuous_columns}
    for col in categorical_columns:
        predictors[col] = []
        for col_dum in X.columns:
            if col in col_dum:
                predictors[col].append(col_dum)
    random_state=222
    np.random.seed(seed=1913)
    #n_estimators=500
    n_estimators=250
    np.random.seed(seed=1913)
    X_train, X_valid, y_train, y_valid=train_test_split(X,
        y,
        test_size=0.2,
        random_state=1913)
    model=RandomForestRegressor(n_estimators=100,
        n_jobs=-1,
        random_state=1913)
    importances={}
    model_clone=clone(model)
    model_clone.random_state=1913
    model_clone.fit(X_train, y_train)
    benchmark_score=model_clone.score(X_train, y_train)
    print('\nStarting feature importance analysis...')
    for jj in range(len(predictors.keys())):
        model_clone=clone(model)
        model_clone.random_state=1913
        col=list(predictors.keys())[jj]
        model_clone.fit(X_train.drop(predictors[col], axis=1), y_train)
        drop_col_score=model_clone.score(X_train.drop(predictors[col], axis=1), y_train)
        importances[col]=benchmark_score - drop_col_score
        print('{} of {} completed: {}'.format(jj + 1,
                                              len(predictors.keys()),
                                              col))
    importances=dict(sorted(importances.items(), key=lambda item: item[1]))
    results['features_ranked_by_importance']=importances

    for key in results.keys():
        print(key, results[key])

if __name__=="__main__":
    main()
