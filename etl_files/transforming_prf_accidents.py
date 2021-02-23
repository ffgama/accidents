from pandas import read_csv, to_numeric

DATA_PATH = 'data/raw_accidents.csv.gz'

open_data = read_csv(DATA_PATH, sep=";", compression='gzip')
open_data.head()
open_data.info()


# optimization of the columns types

types = ['int64','float64']
int_cols, float_cols = [open_data.select_dtypes(t).columns.to_list() for t in types]

open_data[int_cols] = open_data[int_cols].apply(to_numeric, downcast='integer')
open_data[float_cols] = open_data[float_cols].apply(to_numeric, downcast='float')
