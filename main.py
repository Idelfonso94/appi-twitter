import sys,tweepy,csv,re
from tkinter import *
from textblob import TextBlob
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize 
import matplotlib.pyplot as plt


class SentimentAnalysis(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        
        self.setMinimumSize(QSize(320, 140))    
        self.setWindowTitle("Proyecto de Tendencias de Twitter") 

        self.nameLabel = QLabel(self)
        self.nameLabel.setText('Nombre:')
        self.line = QLineEdit(self)  
        
        self.line.move(80, 20)
        self.line.resize(200, 32)
        self.nameLabel.move(20, 20)
		
        self.nameLabel1 = QLabel(self)
        self.nameLabel1.setText('Twiters')
        self.numero = QLineEdit(self)
		
        self.numero.move(80, 60)
        self.numero.resize(200, 32)
        self.nameLabel1.move(20, 50)
		
        pybutton = QPushButton('Buscar1', self)
        pybutton.clicked.connect(self.clickMethod)
        pybutton.resize(200,32)
        pybutton.move(80, 100)        
        self.tweets = []
        self.tweetText = []
		
    def clickMethod(self):
        self.DownloadData(self.line.text())
        self.DownloadData(self.numero.text())
		

    def DownloadData(self):
        #authenticating
        consumerKey = 'wHA7FJhTLAsKdqAS3Iuq66y8k'
        consumerSecret = '0qQebyVvxMXNgXHklE9gEM3OUNKNoaVM51yiXXBn8EIRuaBsPl'
        accessTokenSecret = 'UCHIhwP37qjCsJksJm493HgJoEOBauqoOOGpBn0LjWACD'
        auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        auth.set_access_token(accessToken, accessTokenSecret)
        api = tweepy.API(auth)

        # input for term to be searched and how many tweets to search
        #searchTerm = input("Enter Keyword/Tag to search about: ")
        searchTerm = self.line.text()
        		
        #NoOfTerms = int(input("Enter how many tweets to search: "))
        NoOfTerms = self.numero.text()
        
        # searching for tweets
        self.tweets = tweepy.Cursor(api.search, q=searchTerm, lang = "en").items(NoOfTerms)

        # Open/create a file to append data to
        csvFile = open('result.csv', 'a')

        # Use csv writer
        csvWriter = csv.writer(csvFile)


        # creating some variables to store info
        polarity = 0
        positive = 0
        wpositive = 0
        spositive = 0
        negative = 0
        wnegative = 0
        snegative = 0
        neutral = 0


        # iterating through tweets fetched
        for tweet in self.tweets:
            #Append to temp so that we can store in csv later. I use encode UTF-8
            self.tweetText.append(self.cleanTweet(tweet.text).encode('utf-8'))
            # print (tweet.text.translate(non_bmp_map))    #print tweet's text
            analysis = TextBlob(tweet.text)
            # print(analysis.sentiment)  # print tweet's polarity
            polarity += analysis.sentiment.polarity  # adding up polarities to find the average later

            if (analysis.sentiment.polarity == 0):  # adding reaction of how people are reacting to find average later
                neutral += 1
				# agregar el tweet.text al qlabel de polarity
            elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 0.3):
                wpositive += 1
            elif (analysis.sentiment.polarity > 0.3 and analysis.sentiment.polarity <= 0.6):
                positive += 1
            elif (analysis.sentiment.polarity > 0.6 and analysis.sentiment.polarity <= 1):
                spositive += 1
            elif (analysis.sentiment.polarity > -0.3 and analysis.sentiment.polarity <= 0):
                wnegative += 1
            elif (analysis.sentiment.polarity > -0.6 and analysis.sentiment.polarity <= -0.3):
                negative += 1
            elif (analysis.sentiment.polarity > -1 and analysis.sentiment.polarity <= -0.6):
                snegative += 1


        # Write to csv and close csv file
        csvWriter.writerow(self.tweetText)
        csvFile.close()

        # finding average of how people are reacting
        positive = self.percentage(positive, NoOfTerms)
        wpositive = self.percentage(wpositive, NoOfTerms)
        spositive = self.percentage(spositive, NoOfTerms)
        negative = self.percentage(negative, NoOfTerms)
        wnegative = self.percentage(wnegative, NoOfTerms)
        snegative = self.percentage(snegative, NoOfTerms)
        neutral = self.percentage(neutral, NoOfTerms)

        # finding average reaction
        polarity = polarity / NoOfTerms

        # printing out data
        


    def cleanTweet(self, tweet):
        # Remove Links, Special Characters etc from tweet
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

    # function to calculate percentage
    def percentage(self, part, whole):
        temp = 100 * float(part) / float(whole)
        return format(temp, '.2f')

    def plotPieChart(self, positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, noOfSearchTerms):
        labels = ['Positivo [' + str(positive) + '%]', 'Debilmente Positivo [' + str(wpositive) + '%]','Fuertemente Positivo [' + str(spositive) + '%]', 'Neutral [' + str(neutral) + '%]',
                  'Negativo [' + str(negative) + '%]', 'Debilmente Negativo [' + str(wnegative) + '%]', 'Fuertemente Negativo [' + str(snegative) + '%]']
        sizes = [positive, wpositive, spositive, neutral, negative, wnegative, snegative]
        colors = ['yellowgreen','lightgreen','darkgreen', 'gold', 'red','lightsalmon','darkred']
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.title('Como las personas estan Reaccionando en ' + searchTerm + ' analizando ' + str(noOfSearchTerms) + ' Tweets.')
        plt.axis('equal')
        plt.tight_layout()
        plt.show()


		
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = SentimentAnalysis()
    mainWin.show()
    #mainWin.DownloadData()
    sys.exit( app.exec_() )


class conteo (QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(320, 140))    
        self.setWindowTitle("Conteo") 


		
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = conteo()
    mainWin.show()
    #mainWin.DownloadData()
    sys.exit( app.exec_() )