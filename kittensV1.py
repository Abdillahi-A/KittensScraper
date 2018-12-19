import requests
from bs4 import BeautifulSoup

def turnToSoup(url):
    res = requests.get(url)
    contents = res.text
    soup = BeautifulSoup(contents, 'lxml')
    
    return soup

# =============================================================================
# 1. Get all the images
# =============================================================================

soup = turnToSoup('https://wallpaperscraft.com/tag/kitten')

container = soup.find('div', class_='wallpapers wallpapers_zoom wallpapers_main')

images = container.findAll('img', class_='wallpapers__image')

#print(images[0]['src'])

imagesList = []

for image in images:
    imagesList.append(image['src'])
    


# =============================================================================
# 2. Get all the images but with their original file size
# =============================================================================

nextPageUrls = []
originalDimensions = []

for i in imagesList:
    nextUrl = 'https://wallpaperscraft.com/wallpaper{}'.format(i[40:-12])
    soup = turnToSoup(nextUrl)
    container = soup.find('div', class_='wallpaper-table__row').findAll('span',class_="wallpaper-table__cell")[1].find('a')['href']
    originalDimensions.append(container[-9:])

fullSizeImages = []
    
for i in range(len(imagesList)):
    fullSizeImages.append(imagesList[i][:-11]+originalDimensions[i]+'.jpg')



# =============================================================================
# 3. Save images to a file
# =============================================================================

for imageLink in fullSizeImages:
    img = requests.get(imageLink).content
    imageName = imageLink[41:-14]+'.jpg'
    file = open(imageName,'wb')
    file.write(img)
    file.close()



