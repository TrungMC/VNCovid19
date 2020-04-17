from urllib.request import urlopen
from bs4 import BeautifulSoup
import os.path
import re
from csv import writer
from datetime import datetime

def downloadInfographic():
    ''''
    URL: https://suckhoedoisong.vn/Covid-19-cap-nhat-moi-nhat-lien-tuc-n168210.html
    Sample ImageURL:https://media.suckhoedoisong.vn/Images/thutrang/2020/04/17/93411718_643264386237290_1218970645556101120_n.jpg
    '''

    html = urlopen('https://suckhoedoisong.vn/Covid-19-cap-nhat-moi-nhat-lien-tuc-n168210.html')
    bs = BeautifulSoup(html, 'html.parser')
    images = bs.find_all('img')
    dlimages = [image['src'] for image in images if image['src'].find('.vn/Images/') != -1]
    vninfographicUrl =dlimages[0]
    datestring = getFileDate(vninfographicUrl)
    filename = getFileName(vninfographicUrl)
    saveFileName = "data/"+datestring+"_"+filename+".jpg"
    downloadFile(vninfographicUrl, saveFileName)

    return
def getFileDate(url):
    regex = r"\/2020\/(.*)\/.*/"
    matches = re.search(regex, url)
    datestring = matches.group()
    datestring = datestring.replace('/', '_')[1:11]
    return datestring
def getFileName(url):
    regex = r"\/2020\/.*\/(.*).jpg"
    matches = re.search(regex, url)
    filename = matches.group(1)
    return filename
def downloadFile(url, filename):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    if not os.path.isfile(filename):
      f = open(filename, 'wb')
      f.write(urlopen(url).read())
      f.close()
      rowcontent=[dt_string, url]
      append_list_as_row(rowcontent)
    else:
        rowcontent = [dt_string, "Skipped. File Unchanged"]
        append_list_as_row(rowcontent)
    return

def append_list_as_row(list_of_elem):
    # Open file in append mode
    with open("data/download.log", 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)

downloadInfographic()
