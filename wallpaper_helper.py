# ----------------------------------------------------------------------------------------------------------------------
# Kyle Haston
# December 3rd, 2017
# I built a new rig and wanted some wallpapers.
# Decided it was time to throw together a script to scrape them from a site that has decent wallpapers.
# ----------------------------------------------------------------------------------------------------------------------

import requests
from bs4 import BeautifulSoup
import urllib
import time
import os

# use requests to get a text version of the webpage we want.
# feed it into BeautifulSoup and specify an HTML parser
URL = 'https://wallpaperfx.com'
subDir1 = '/nature'
keyword = 'wallpaper'
skipTo = 'wallpaperfx'  # in this case, we want to skip past this string in each link (contains keyword of interest)

for i in range(40):

    if i == 1:
        URL = 'https://wallpaperfx.com'
    else:
        # Phase two: see link below. There are 90+ pages.
        # URL2 = 'https://wallpaperfx.com/nature/page-2'
        URL = 'https://wallpaperfx.com/nature/page-' + i.__str__()

    searchURL = URL + subDir1
    soup = BeautifulSoup(requests.get(searchURL).text, 'html.parser')

    # some forbidden links (found after a little tinkering)
    forbidden = ['https://wallpaperfx.com/tags/nature-wallpapers']

    # find all anchors (links)
    tags = soup.find_all('a')

    # matrix to hold good links
    goodLinks = []

    for tag in tags:
        # print('\n-------href-----')
        # if we find the subDir in the link AND the keyword, then we're interested in it
        if subDir1 in tag.attrs['href']:

            # now check for keyword, observing the skipTo behaviour
            link = tag.attrs['href']
            index1 = link.find(skipTo)
            if keyword in link:

                fullLink = URL + link

                # if we don't already have the link,
                # and the link is not in the forbidden list,
                # append it to the array of good links
                if fullLink not in goodLinks:
                    if fullLink not in forbidden:
                        goodLinks.append(fullLink)
                        # print(fullLink)
    print(goodLinks)

    # now massage the links so we can directly download the image

    # here is an example of a good link that we farmed
    temp = 'https://wallpaperfx.com/nature/grand-canyon-cave-wallpaper-18580.htm'

    # here is a good link to an image that we want.
    goal = 'https://wallpaperfx.com/view_image/grand-canyon-cave-1920x1080-wallpaper-18580.jpg'
    # we're going to make the assumption that we can use a prefix, some info specific to the image, then a .jpg suffix.
    stripThis = 'https://wallpaperfx.com/nature/'
    prefix = 'https://wallpaperfx.com/view_image/'
    suffix = '.jpg'
    insertThis = '-1920x1080'  # need to insert this into the filename
    here = '-wallpaper'  # insert it before this keyword

    # array to hold modified good links
    newGoodLinks = []

    # now filter out the guts of our 'goodLink'
    for link in goodLinks:
        # print(link)
        guts = link[stripThis.__len__():(link.__len__()-4)]  # -4 to shed the '.htm'

        # strip away any more directories which preclude the actual guts we want
        while '/' in guts:
            indexSlash = guts.find('/')
            guts = guts[indexSlash+1:]

        index = guts.find(here)
        newLink = prefix + guts[:index] + insertThis + guts[index:] + suffix
        # print(newLink)
        newGoodLinks.append(newLink)

    # now retrieve the images
    for link in newGoodLinks:
        filename = link[prefix.__len__():link.__len__()]

        # check if the filename already exists (don't try to download it twice)
        if not os.path.isfile(filename):
            print('downloading: ' + link)

            try:
                print()
                # uncomment the following 2 lines to download files.
                # keep them commented to "practice"
                urllib.request.urlretrieve(link, filename)
                time.sleep(2)  # sleep for some amount of time, so we don't get banned from the server
            except:
                pass
        else:
            print('skipping: ' + filename + ' because we already have it')