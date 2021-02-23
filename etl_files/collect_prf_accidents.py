import requests
from os import getcwd
from rarfile import RarFile
from shutil import rmtree
from glob import glob
from mimetypes import guess_extension
from bs4 import BeautifulSoup
from pandas import read_csv, DataFrame, concat
from functools import reduce

from settings import *

def extract_url_files(url):
    """
    As from skeleton from the home page we can extracting the urls that containing  csv files desired.

    Args:
        url ([str]): home page containing csv files.

    Returns:
        [dataframe]: dataset with 2 columns: year and the url corresponding.
    """    
        
    try:
        response = requests.get(MAIN_URL)
        response.raise_for_status()
        
    except requests.exceptions.HTTPError as e:
        return "Error: " + str(e)
    
    loading_soup = BeautifulSoup(response.text)

    # catching the first group from <ul>
    tag_lists = loading_soup.select('div.content ul:nth-of-type(1) li a')

    data_url = (
        DataFrame([tag_lists[i].string ,tag_lists[i].get('href')] 
            for i in range(0, len(tag_lists)))
    )

    data_url = data_url.rename(columns={0:'year', 1:'url'})
    
    return data_url

data_urls = extract_url_files(url=MAIN_URL)

def download_all_files(links_df):
    """
    Download all files and save them according with their compression format.
    
    Args:
        links_df ([str]): specific url of the file that will downloaded.
    """   
    END_PATH = '/download'
    TARGET_PATH = getcwd()+'/data/external/'
    FILENAME_SAVED = 'data_'
     
    for index, row in links_df.iterrows():
        
        select_url = row['url'] 
            
        try:
            response = requests.get(select_url+END_PATH)
            response.raise_for_status()
            
        except requests.exceptions.HTTPError as e:
            return "Error: " + str(e)
        
        content_type = response.headers['content-type']
        ext = guess_extension(content_type)
        
        if ext is None:            
            full_path = TARGET_PATH+FILENAME_SAVED+row['year']+'.rar'
            with open(full_path, 'wb') as saved_data:
                saved_data.write(response.content)
        else:
            full_path = TARGET_PATH+FILENAME_SAVED+row['year']+'.zip'
            with open(full_path, 'wb') as saved_data:
                saved_data.write(response.content)
   

download_all_files(links_df=data_urls)

TEMP_DIR = '/tmp/data/'
def unrar_files(path_zipped_file, tmp_dir=TEMP_DIR):
    """
    Uncompress zipped file (rar extension) by saving in a temporary file.
    
    Args:
        path_zipped_file ([str]): respective file path in a rar format.
        tmp_dir ([str], optional): temporary file path.
    """        
    rar = RarFile(path_zipped_file)
    temp = tmp_dir
    rar.extractall(path=temp)
    
list_rar_files = glob(pathname='data/external/'+'*.rar')
# persistance on local disk /tmp
csv_temp_files = list(map(unrar_files, list_rar_files))

dfs_data = []
def open_data_files(format_compress, tmp_dir=TEMP_DIR):
    
    """
    Find and read the file according its location and compression format extension. 
    In the end, for each dataset save them into a list.
    
    Returns:
        [list]: list of dataframes that have been read.
    """    
    
    temp_files = glob(tmp_dir+"*.csv")
    zip_files = glob('data/external/'+'*.zip')

    if format_compress=='rar':    
        for i in range(0, len(temp_files)):
            open_data = read_csv(temp_files[i], sep=";", encoding="iso-8859-1")        
            dfs_data.append(open_data)
        return dfs_data
    
    elif format_compress=='zip':
        for i in range(0, len(zip_files)):
            open_data = read_csv(zip_files[i], sep=";", compression='zip', encoding="iso-8859-1")
            dfs_data.append(open_data)
        return dfs_data
    
dfs_data = [open_data_files(item) for item in ['zip','rar']][0]

data_accidents = reduce(lambda left, right: concat([left, right]), dfs_data)
data_accidents

# removing local temporary files
rmtree(TEMP_DIR)

data_accidents.to_csv('data/'+'raw_accidents.csv.gz', sep=";", index=False, compression='gzip')