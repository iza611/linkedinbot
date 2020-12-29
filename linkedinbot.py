from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import urllib.request
import os

allEpisodes = []
courseLink = 'https://www.linkedin.com/learning/blockchain-basics/welcome-and-introduction'
parentDirectory = '/Users/ozogiz01/OneDrive - StepStone Group/Documents/LinkedIn Premium/test/'


# 1. prep

# open course to be downloaded
browser = webdriver.Chrome('/Users/ozogiz01/chromedriver')
browser.get((courseLink))

# sign in
signinButton = browser.find_element_by_class_name('nav__button-secondary')
signinButton.click()

# type email
email = browser.find_element_by_id('auth-id-input')
email.send_keys('fotoluminescencja@gmail.com')
continueButton = browser.find_element_by_id('auth-id-button')
continueButton.click()

# wait until I type password and course page is open
element = WebDriverWait(browser, 1000).until(
    EC.presence_of_element_located((By.CLASS_NAME, "vjs-tech"))
)

# change quality
settings = browser.find_element_by_class_name('vjs-settings-menu-button')
settings.click()
quality = browser.find_element_by_class_name('vjs-quality-setting')
quality.click()
qualityOptions = browser.find_elements_by_class_name('vjs-quality-setting-level')
qualityOptions[len(qualityOptions)-1].click()


# 2. collect data into allEpisodes array

# create folders 
contentsListNames = browser.find_elements_by_class_name('classroom-toc-chapter__toggle-title')
directories = []
for x in range (len(contentsListNames)):
    directories.insert(len(directories), contentsListNames[x].text)
for x in range (len(directories)):
    path = parentDirectory + directories[x]
    os.mkdir(path)
    print("\'" + directories[x] + "\'" + ' folder created')

# open each chapter and save (links & titles & folder num) for each episodes
def getEpisodesFromCurrentlyOpenedChapter(chapter):
    episodesLinks = browser.find_elements_by_class_name('classroom-toc-item__link')
    episodesTitles = browser.find_elements_by_class_name('classroom-toc-item__title')
    quiz = 'quiz'
    Quiz = 'Quiz'
    for x in range (len(episodesLinks)):
        episodeLink = episodesLinks[x].get_attribute('href')
        episodeTitle = episodesTitles[x].text
        if episodeTitle.endswith('(Viewed)'):
            episodeTitle = episodeTitle[:-8]
        episodeTitle = episodeTitle.replace('\n','')
        if quiz not in episodeLink and Quiz not in episodeTitle:
            allEpisodes.insert(len(allEpisodes), [episodeLink, str(x+1) + '. ' + episodeTitle + '.mp4', chapter, 'null'])
    

def openNextChapterContent():
    contentsList = browser.find_elements_by_class_name('btn-inverse-link')
    for x in range (len(contentsList)-1):
        if contentsList[x].get_attribute('aria-expanded') == 'true':
            contentsList[x].click()
            contentsList[x+1].click()
            return x+1

getEpisodesFromCurrentlyOpenedChapter(0)
for x in range (len(contentsListNames)-1):
    chapter = openNextChapterContent()
    getEpisodesFromCurrentlyOpenedChapter(chapter)

# save api for all videos that will be used for downloading 
def saveSingleVideoApi(x):
    video = browser.find_element_by_class_name('vjs-tech')
    src = video.get_attribute('src')
    allEpisodes[x][3] = src

def saveAllVideosApis():
    for x in range (len(allEpisodes)):
        browser.get(allEpisodes[x][0])
        saveSingleVideoApi(x)

saveAllVideosApis()
print(allEpisodes)


# 3. download

# download videos to proper folders
def pickFolder(folderNum):
    folder = directories[folderNum] + '/'
    return folder

def downloadSingleVideo(episode):
    dwn_link = episode[3]
    file_name = episode[1]
    folder = pickFolder(episode[2])
    urllib.request.urlretrieve(dwn_link, parentDirectory + folder + file_name)
    print('downloaded ' + file_name + ' into folder: ' + folder)

for x in range (len(allEpisodes)):
    downloadSingleVideo(allEpisodes[x])

