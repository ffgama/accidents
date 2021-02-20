from settings import *
from bs4 import BeautifulSoup
import requests
from pandas import read_csv, DataFrame

def extract_url_files(url):
    """
    As from skeleton from the home page we can extracting the urls that containing  csv files desired.

    Args:
        url ([string]): home page containing csv files.

    Returns:
        [dataframe]: dataset with 2 columns: year and the url corresponding.
    """    
        
    r = requests.get(MAIN_URL)
    
    loading_soup = BeautifulSoup(r.text)

    # catching the first group from <ul>
    tag_lists = loading_soup.select('div.content ul:nth-of-type(1) li a')

    data_url = (
        DataFrame([tag_lists[i].string ,tag_lists[i].get('href')] 
            for i in range(0, len(tag_lists)))
    )

    data_url = data_url.rename(columns={0:'year', 1:'url'})
    
    return data_url

data_urls = extract_url_files(url=MAIN_URL)
data_urls