import requests
from bs4 import BeautifulSoup
import sys

def turnToSoup(url):
    
    # turns url into soup object
    
    res = requests.get(url)
    contents = res.text
    
    soup = BeautifulSoup(contents, 'lxml')
    
    return soup


def findtotalPages(soup):
    container = soup.find('div', class_='pager')
    
    totalPages = int(container.find_all('a')[2]['href'][-2:])
    
    return totalPages
    

def findImageLinks(soup):
    
    # finds all the image links 
        
    container = soup.find('div', class_='wallpapers wallpapers_zoom wallpapers_main')
    
    sub_container = container.find_all('img', class_='wallpapers__image')
    
    listOfImageLinks = []
    
    for img in sub_container:
        listOfImageLinks.append(img['src'].replace('300x168', '1280x720'))
        
    return listOfImageLinks
        
    

def writeImagesToFile(listOfImageLinks):
    
    # Write images to directory 
    
    for image in listOfImageLinks:
        with open(image[41:], 'wb') as f:
            f.write(requests.get(image).content)
            

def main(pagesToScrape=1):
    
    soup = turnToSoup('https://wallpaperscraft.com/tag/kitten')
    
    totalPages = findtotalPages(soup)
    
    if pagesToScrape > totalPages:
        print(f"Sorry there aren't that many pages available for me to scrape.\nPlease choose a number smaller than {totalPages} and try again.\n")
        sys.exit()
        
    for i in range(pagesToScrape):
        
        soup = turnToSoup(f'https://wallpaperscraft.com/tag/kitten/page{i+1}')

        listOfImageLinks = findImageLinks(soup)
        
        writeImagesToFile(listOfImageLinks)


#Please specify how many pages you'd like to scrape inside the (). Default set to 1.
main()





