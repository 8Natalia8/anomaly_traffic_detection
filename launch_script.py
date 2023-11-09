import platform; 
import sys; 

import pandas as pd
from joblib import load
from sklearn.preprocessing import StandardScaler, LabelEncoder
import ipaddress

def ip_to_int(ip):
    try:
        ip_version = ipaddress.ip_address(ip).version
        if ip_version == 4:  # IPv4
            return int(ipaddress.IPv4Address(ip))
        elif ip_version == 6:  # IPv6
            return int(ipaddress.IPv6Address(ip))
    except ValueError:
        return None  
    
def preprocessing(data):
    assert ('MATCHED_VARIABLE_VALUE' in data.columns) and ('EVENT_ID' in data.columns), 'Columns missing'
    #print("Columns 'MATCHED_VARIABLE_VALUE' and 'EVENT_ID' are existing in the DataFrame")
    # todo: проверку всех ост колонок
    data.dropna(how='all',axis=0, inplace=True)
    data.reset_index(inplace=True)
    data.rename(columns={'index': 'orig_orig_idx'}, inplace=True)
    data.drop_duplicates(inplace=True)
    print(f'Df shape with unique and Non Nan rows: {data.shape} ')
    cols2drop = ['MATCHED_VARIABLE_VALUE','EVENT_ID']
    #df_clean = data.copy(deep=True)
    df_clean = data.drop(cols2drop, axis=1)
    # preprocessing
    df_clean['REQUEST_SIZE'] = pd.to_numeric(df_clean['REQUEST_SIZE'], errors='coerce')
    df_clean['RESPONSE_CODE'] = pd.to_numeric(df_clean['RESPONSE_CODE'], errors='coerce')
    # только после заменять NaN значения, тк errors='coerce' их снова создаст
    df_clean['REQUEST_SIZE'] = df_clean['REQUEST_SIZE'].fillna(0)
    df_clean['RESPONSE_CODE'] = df_clean['RESPONSE_CODE'].fillna(0)
    df_clean['CLIENT_USERAGENT'] = df_clean['CLIENT_USERAGENT'].fillna('Unknown')
    df_clean['MATCHED_VARIABLE_NAME'] = df_clean['MATCHED_VARIABLE_NAME'].fillna('NonDefined')
    df_clean['MATCHED_VARIABLE_SRC'] = df_clean['MATCHED_VARIABLE_SRC'].fillna('NonDefined')
    
    userag_list=[''.join(i.split()) for i in df_clean['CLIENT_USERAGENT'].values.tolist()]
    df_clean['CLIENT_USERAGENT'] = userag_list
    df_clean['CLIENT_USERAGENT'] = df_clean['CLIENT_USERAGENT'].str.replace(r'[^a-zA-Z0-9]+','')
    le = LabelEncoder()
    df_clean['CLIENT_USERAGENT'] = le.fit_transform(df_clean['CLIENT_USERAGENT'])
    
    scaler1 = StandardScaler()
    df_clean[['REQUEST_SIZE','RESPONSE_CODE']] = scaler1.fit_transform(df_clean[['REQUEST_SIZE', 'RESPONSE_CODE']])
    
    userag_list2=[''.join(i.split()) for i in df_clean['MATCHED_VARIABLE_SRC'].values.tolist()]
    df_clean['MATCHED_VARIABLE_SRC'] = userag_list2
    df_clean['MATCHED_VARIABLE_SRC'] = df_clean['MATCHED_VARIABLE_SRC'].str.replace(r'[^a-zA-Z0-9]+','')
    df_clean['MATCHED_VARIABLE_SRC'] = le.fit_transform(df_clean['MATCHED_VARIABLE_SRC'])
    
    userag_list3=[''.join(i.split()) for i in df_clean['MATCHED_VARIABLE_NAME'].values.tolist()]
    df_clean['MATCHED_VARIABLE_NAME'] = userag_list3
    df_clean['MATCHED_VARIABLE_NAME'] = df_clean['MATCHED_VARIABLE_NAME'].str.replace(r'[^a-zA-Z0-9]+','')
    df_clean['MATCHED_VARIABLE_NAME'] = le.fit_transform(df_clean['MATCHED_VARIABLE_NAME'])
    scaler2 = StandardScaler()
    df_clean[['CLIENT_USERAGENT', 'MATCHED_VARIABLE_SRC', 'MATCHED_VARIABLE_NAME']] = scaler2.fit_transform(df_clean[['CLIENT_USERAGENT', 'MATCHED_VARIABLE_SRC', 'MATCHED_VARIABLE_NAME']])
    
    df_clean['CLIENT_IP_INT'] = df_clean['CLIENT_IP'].apply(ip_to_int)


    print(df_clean.columns)
    #df_clean = df_clean.drop(['CLIENT_IP', 'orig_orig_idx'], axis=1)
    df_clean_train = df_clean.copy(deep=True)
    assert data['orig_orig_idx'].equals(df_clean_train['orig_orig_idx']), 'orig indexes are different!'
    df_clean_train.drop(['CLIENT_IP', 'orig_orig_idx'], axis=1, inplace=True)
    scaler3 = StandardScaler()
    df_clean_train['CLIENT_IP_INT'] = scaler3.fit_transform(df_clean_train[['CLIENT_IP_INT']])
    df_clean_train['CLIENT_IP_INT'] = df_clean_train['CLIENT_IP_INT'].fillna(0)

    return df_clean_train

def inference():

    # Load, read and normalize training data
    testing = "./test.csv"
    data_test = pd.read_csv(testing)
    print("Shape of the test data")
    print(data_test.shape)
    assert len(data_test.columns)==8, 'data_train and data_test have different shapes!'
    preprocessed_data_test = preprocessing(data_test)
    print(f'Data_test.columns total: {preprocessed_data_test.columns}')

    classifier = load('dbscan_orig_model.joblib')
    cluster_labels = classifier.fit_predict(preprocessed_data_test)
    print(f'Num of clusters: {len(set(cluster_labels)) - (1 if -1 in cluster_labels else 0)}')
    preprocessed_data_test['Cluster_Label_dbscan'] = cluster_labels

    df_result = pd.concat([data_test['orig_orig_idx'], preprocessed_data_test['Cluster_Label_dbscan']], axis=1)
    df_result = pd.concat([df_result, data_test.loc[data_test['orig_orig_idx'] == df_result['orig_orig_idx']]], axis=1)
    df_result = df_result[['CLIENT_IP', 'CLIENT_USERAGENT', 'REQUEST_SIZE', 'RESPONSE_CODE', 'MATCHED_VARIABLE_SRC',
                           'MATCHED_VARIABLE_NAME', 'MATCHED_VARIABLE_VALUE', 'EVENT_ID', 'Cluster_Label_dbscan']]

    return preprocessed_data_test.to_csv('Test_preprocessed_result.csv', index=False), df_result.to_csv('Test_original_result.csv', index_label='original_idx')

if __name__=='__main__':
    print(platform.platform())
    print("Python", sys.version)

    
    inference()