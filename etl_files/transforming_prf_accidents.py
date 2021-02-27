from pandas import (
    DataFrame, read_csv, to_numeric, to_datetime, set_option
)
set_option('display.max_columns', None)

DATA_PATH = 'data/raw_accidents.csv.gz'

open_data = read_csv(DATA_PATH, sep=";", compression='gzip')
open_data.info()

def remove_columns(dataset: DataFrame, columns) -> DataFrame:
    dataset = dataset.drop(columns=columns, axis=1)
    return dataset
    
def data_types_optimization(dataset: DataFrame) -> DataFrame:
    
    list_types = ['int64','float64']
        
    int_cols, float_cols = [dataset.select_dtypes(t).columns.to_list() 
                            for t in list_types]
    dataset[int_cols] = dataset[int_cols].apply(to_numeric, downcast='integer')
    dataset[float_cols] = dataset[float_cols].apply(to_numeric, downcast='float')
    
    return dataset

def filter_not_null_str(dataset: DataFrame, column: str) -> DataFrame:    
    
    query_template = "{} != '(null)' ".format(column)
    
    dataset = dataset.query(query_template) 
    return dataset   

def convert_to_datetime(dataset: DataFrame, column: str) -> DataFrame:
    dataset[column] = to_datetime(dataset[column])
    return dataset

def unite_two_columns(dataset: DataFrame, 
                  first_column: str, 
                  second_column: str,
                  new_column: str) -> DataFrame:
    dataset[new_column] = dataset[first_column] +'-'+ dataset[second_column] 
    return dataset

def replace_repeated_values(dataset: DataFrame, column:str)-> DataFrame:
    
    day_of_week_new = ['Segunda','Terça','Quarta','Quinta','Sexta','Sábado','Domingo']
    day_of_week_old =  ['segunda-feira','terça-feira','quarta-feira','quinta-feira','sexta-feira','sábado','domingo']
    
    day_of_week = dict(zip(day_of_week_old,day_of_week_new))

    dataset[column] = dataset[column].replace(day_of_week)
    return dataset

def extract_hour_from_time(dataset: DataFrame, new_column:str) -> DataFrame:
    data_transf[new_column] = to_datetime(data_transf['horario'], format="%H:%M:%S").dt.hour
    return dataset
    
open_data = remove_columns(dataset=open_data, 
                           columns=['id','ano','br','km','delegacia','uop'])
data_transf = data_types_optimization(dataset=open_data)

data_transf = filter_not_null_str(data_transf, column='uf')
data_transf = filter_not_null_str(data_transf, column='causa_acidente')
data_transf = filter_not_null_str(data_transf, column='classificacao_acidente')
data_transf = filter_not_null_str(data_transf, column='fase_dia')
data_transf = filter_not_null_str(data_transf, column='condicao_metereologica')
data_transf = filter_not_null_str(data_transf, column='tipo_pista')


data_transf = convert_to_datetime(dataset=data_transf, column='data_inversa')
data_transf = unite_two_columns(dataset=data_transf, 
                                first_column='municipio',
                                second_column='uf',
                                new_column='cidade_uf')
data_transf = replace_repeated_values(dataset=data_transf, column='dia_semana')
data_transf = extract_hour_from_time(dataset=data_transf, new_column='hour')