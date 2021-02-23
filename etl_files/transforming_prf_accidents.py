from pandas import DataFrame, read_csv, to_numeric, to_datetime, set_option
set_option('display.max_columns', None)

DATA_PATH = 'data/raw_accidents.csv.gz'

open_data = read_csv(DATA_PATH, sep=";", compression='gzip')
open_data.info()

open_data.head(2)

def remove_columns(dataset: DataFrame, columns) -> DataFrame:
    dataset = dataset.drop(columns=columns, axis=1)
    return dataset
    
open_data = remove_columns(open_data, columns=['id','ano','delegacia','uop'])

# optimization of the columns types
def data_types_optimization(dataset: DataFrame) -> DataFrame:
    
    list_types = ['int64','float64']
        
    int_cols, float_cols = [dataset.select_dtypes(t).columns.to_list() 
                            for t in list_types]
    dataset[int_cols] = dataset[int_cols].apply(to_numeric, downcast='integer')
    dataset[float_cols] = dataset[float_cols].apply(to_numeric, downcast='float')
    
    return dataset


data_transf = data_types_optimization(dataset=open_data)
data_transf.info()

data_transf.select_dtypes(include=['object']).columns.to_list()

data_transf['data_inversa'] = to_datetime(data_transf['data_inversa'])
data_transf['data_inversa'].max()
