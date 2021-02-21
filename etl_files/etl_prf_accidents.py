from os import getcwd
from settings import *
from bs4 import BeautifulSoup
import requests
from pandas import read_csv, DataFrame
from rarfile import RarFile
from shutil import rmtree
from glob import glob
from mimetypes import guess_extension

def extract_url_files(url):
    """
    As from skeleton from the home page we can extracting the urls that containing  csv files desired.

    Args:
        url ([string]): home page containing csv files.

    Returns:
        [dataframe]: dataset with 2 columns: year and the url corresponding.
    """    
        
    response = requests.get(MAIN_URL)
    
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
    
    END_PATH = '/download'
    TARGET_PATH = getcwd()+'/data/compress_data/'
    FILENAME_SAVED = 'data_'
     
    for index, row in links_df.iterrows():
        
        select_url = row['url'] 
        response = requests.get(select_url+END_PATH)
        print(response)
                
        content_type = response.headers['content-type']
        ext = guess_extension(content_type)
        print(ext)
        
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
    rar = RarFile(path_zipped_file)
    temp = tmp_dir
    rar.extractall(path=temp)
    
rar_files = glob(pathname='data/'+'*.rar')
csv_temp_files = list(map(unrar_files, rar_files))

def open_data_files(tmp_dir, format_compress):
    
    if format_compress=='rar':
        temp_files = glob(tmp_dir+"*.csv")[0]
        open = read_csv(temp_files, sep=";", encoding="iso-8859-1")
        print(open.head(2))
    elif format_compress=='zip':
        zip_files = glob('data/'+'*.zip')[0]
        open = read_csv(zip_files, sep=";", compression='zip', encoding="iso-8859-1")
        print(open.head(2))
        
open_data_files(tmp_dir=TEMP_DIR, format_compress='zip')

# rmtree(TEMP_DIR)

