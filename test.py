from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import word_tokenize
import pygsheets

class Connect:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.titles = []
        self.urls = []
        self.corpus = []
        self.keyword=""

    def runsrc(self):
        self.keyword=input('輸入你想查的字: ')
        self.driver.get('https://www.google.com')
        search_box = self.driver.find_element('xpath', '//*[@id="APjFqb"]')
        search_box.send_keys(self.keyword)
        search_box.send_keys(Keys.ENTER)
        time.sleep(3)
        results = self.driver.find_elements('xpath', '//div[@class="yuRUbf"]/a')
        for result in results:
            title = result.get_attribute('text')
            url = result.get_attribute('href')
            self.titles.append(title)
            self.urls.append(url)
            self.corpus.append(title)

            print('標題:', title)
            print('網址:', url)
            print('---')
        self.driver.quit()

    def connect_pygsheets(self):
        gc = pygsheets.authorize(service_file='./auth.json')
        spreadsheet = gc.open_by_key('1Ymi5GT_nydUbPc--vuFh9tXSEPKnEMKjOPJzJrfTqSw') 
        worksheet = spreadsheet.sheet1
        for i in range(len(self.corpus)):
            title = self.corpus[i]
            url = self.urls[i]
            
            worksheet.update_value((i+2, 1), title)  
            worksheet.update_value((i+2, 2), url)  
        
            
            words = self.tokenizer(title)
            keywords = [word for word in words if word.isalnum()]
            worksheet.update_value((i+2, 3), ', '.join(keywords))  
        print('資料已儲存到 Google Sheets 中。')

    def tf_idf(self):
        self.tokenizer = word_tokenize
        vectorizer = TfidfVectorizer(tokenizer=self.tokenizer)
        # tfidf_matrix = vectorizer.fit_transform(self.corpus)
        # features = vectorizer.get_feature_names()
        
        

if __name__ == '__main__':
    connect = Connect()
    connect.runsrc()
    connect.tf_idf()
    connect.connect_pygsheets()
    
