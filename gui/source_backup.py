import pafy
import urllib.request
import os
os.add_dll_directory(r'C:\Program Files\VideoLAN\VLC')
import vlc
import time
import sys
import threading
# import _thread
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QTimer, QRunnable , pyqtSignal
from PyQt5.QtGui import QIcon, QPalette, QColor, QPixmap, QFont, QImage

from PyQt5.QtWidgets import  (QWidget, QStatusBar, QApplication,
                             QScrollArea, QPushButton, QHBoxLayout, QGroupBox,
                            QVBoxLayout,QLabel, QFrame,QLineEdit,
                              QSlider , QAction,QProgressBar,
                              QMainWindow, QGridLayout)
###################################################################
#import selenium
from selenium import webdriver
PATH = ".\pre-requisties\chromedriver.exe"


from selenium.webdriver.chrome.options import Options

from gui.downloadWin import DownloadWindow
###############################################################################################
###############################################################################################

# making clickable Qlabel 

class ClickQLable(QLabel):
    clicked = pyqtSignal(str)
    def __init__(self, parent=None):
        super(ClickQLable, self).__init__(parent)

    def mousePressEvent(self, event):
        self.now_click = "Click"
    
    def mouseReleaseEvent(self, event):
        if self.now_click == "Click":
            QTimer.singleShot(QApplication.instance().doubleClickInterval(),
                              self.performSingleClickAction)
        else:
            # Realizar acción de doble clic.
            self.clicked.emit(self.now_click)
    
    def mouseDoubleClickEvent(self, event):
        self.now_click = "Doble Click"
    
    def performSingleClickAction(self):
        if self.now_click == "Click":
            self.clicked.emit(self.now_click)


class MainWindow(QMainWindow,QRunnable):
    def __init__(self):
        QMainWindow.__init__(self)
############################################################################################
# %%%%%%%%%%%%%%%%%%%%%%%%% Instances  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   
    # WEBDRIVER
        option = Options()
        option.headless = True
        option.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(PATH, options=option)           
        
        self._player = vlc.Instance(['--video-on-top','--loop','--input-repeat=-1'])
        self.mediaplayer = self._player.media_player_new()
        self.mediaplayer.set_fullscreen(True)
    # menu bar -------------------------------------------------------------------
        self.menu = self.menuBar()
        self.file = self.menu.addMenu("File")
        self.options = self.menu.addMenu("Options")
        self.about = self.menu.addMenu("About")


    # exit Action
        exitAction = QAction("Exit", self) #exit
        exitAction.setShortcut("Ctrl+Q")
        exitAction.triggered.connect(self.exit_)# slot
    # add action
        self.file.addAction(exitAction)
        
        #----------------------------------------------------------------------------
        
        self.setWindowTitle("AV - Player")
        self.setWindowIcon(QIcon(".\Images\LU.png"))
        
        self.initWidgets()
        self.isPaused = False
        self.littlewindow = None # kapag wala pang window 
        
#         self.GroupBox()
    # threadpool - -----------------------------------------------------------------------    
        

############################################################################################
# %%%%%%%%%%%%%%%%%%%%%%%%% USER INTERFACE  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    def initWidgets(self):
        self.setWindowOpacity(0.95) 
        winpalette = self.palette()
        winpalette.setColor(QPalette.Window, QColor("DarkSlateBlue"))
        self.setPalette(winpalette)
        
        #----------------------
        self.widget = QWidget(self)                                #.widget = QWidget
        self.setCentralWidget(self.widget)
        
        
##################################################################################################
        self.welcome = QLabel("Welcome to YouTube Player  ")
        self.welcome.setFont(QFont("Noto Sans", 16))
        self.searchBtn = QPushButton("Search")
        self.searchBtn.setFont(QFont("Noto Sans", 16,QFont.Bold))
        self.searchBtn.setFixedSize(90,30)
        self.searchBtn.clicked.connect(self.GroupBox)
        self.searchBtn.setAutoDefault(True)
        

        self.searchBar = QLineEdit(self)
        self.searchBar.setFixedSize(250,30)
        self.font = self.searchBar.font()
        self.font.setPointSize(1)
        self.searchBar.returnPressed.connect(self.searchBtn.click)
        
        self.searchBox =QHBoxLayout()
        self.searchBox.addWidget(self.welcome)
        self.searchBox.addWidget(self.searchBar)
        self.searchBox.addWidget(self.searchBtn)
        self.searchBox.addStretch(1)
        
        
        
        self.VboxGrid = QVBoxLayout(self)

##########################################################################################################
        
    #  frame video  -right side
        
        self.videoframe = QFrame()
        self.vpalette = self.videoframe.palette()
        self.vpalette.setColor(QPalette.Window, QColor(120,120,120))
        
        self.videoframe.setPalette(self.vpalette)
        self.videoframe.setAutoFillBackground(True)

    # slider
        self.videoposition = QSlider(Qt.Horizontal, self)             
        self.videoposition.setMaximum(1000)
        self.videoposition.sliderMoved.connect(self.setPosition)
    # Volume Slider
        self.volume = QSlider(Qt.Horizontal)
        self.volume.setMaximum(120)
        self.volume.setValue(self.mediaplayer.audio_get_volume())
        self.volume.valueChanged.connect(self.setVolume)
       
        #self.volume.setValue(self.mediaplayer.audio_get_volume())
        
    # BUTTON
        self.pauseBtn = QPushButton("Pause") # it mush be hbox
        self.stopBtn = QPushButton("Stop") # it mush be hbox
        self.openbtn = QPushButton("Open") # it mush be hbox
        self.nextBtn = QPushButton("Next") # it mush be hbox
        self.removeList = QPushButton("ReMove ThIs LiSt") # sa ilalim ng gridlayout
        self.favorites = QPushButton("My Favorites ⭐")
        self.dislike = QPushButton("Send Dislike 👎")
        self.statusBar = QStatusBar()
        self.statusBar.setFont(QFont("Noto Sans", 7))
        self.statusBar.setFixedHeight(14)
    
    # Toggle buttons
        self.pauseBtn.clicked.connect(self.PlayPause)
        self.pauseBtn.setEnabled(False)
        self.stopBtn.clicked.connect(self.stop_)
        self.stopBtn.setEnabled(False)
        self.nextBtn.clicked.connect(self.next_)
        self.nextBtn.setEnabled(False)
        self.openbtn.clicked.connect(self.OpenMedia)
        self.favorites.setEnabled(True)
        self.dislike.setEnabled(False)
        
    # timer
        self.timer = QTimer(self)
        self.timer.setInterval(200)
        self.timer.timeout.connect(self.updatevideoposition)
        
    # Tooltip
        self.videoposition.setToolTip("media running time position")
        self.volume.setToolTip("Drag the Handle to change volume")
        self.pauseBtn.setToolTip("Play or Pause")
        self.stopBtn.setToolTip("Stop Playing")
        self.openbtn.setToolTip("Open video from local folder")
        self.nextBtn.setToolTip("Next video/media")
        self.volume.setToolTip("Volume")
        self.removeList.setToolTip("remove list from group box")
        self.favorites.setToolTip("Open Your favorites") # open a small window
    
        
    # Horizonal layout for buttons
        self.Hbutton = QHBoxLayout()
        self.Hbutton.addWidget(self.pauseBtn)
        self.Hbutton.addWidget(self.stopBtn)
        self.Hbutton.addWidget(self.nextBtn)
        self.Hbutton.addWidget(self.openbtn)
        self.Hbutton.addWidget(self.volume)
        self.Hbutton.addWidget(self.favorites)
        self.Hbutton.addWidget(self.dislike)
        self.Hbutton.addStretch(1)
    
    # vertical layout objects for video and sliders
        self.Vbox = QVBoxLayout()
        self.Vbox.addLayout(self.searchBox)
        self.Vbox.addWidget(self.videoframe)
        self.Vbox.addWidget(self.videoposition)
        self.Vbox.addLayout(self.Hbutton)
        self.Vbox.addWidget(self.statusBar)
        self.statusBar.showMessage("Ready")
        
    # Final Layout        
        self.mainlayout = QHBoxLayout()
        self.mainlayout.addLayout(self.Vbox)   
        self.mainlayout.addLayout(self.VboxGrid)
             
    
    # add to central widget
        self.widget.setLayout(self.mainlayout)
        
        
        
############################################################################################
# %%%%%%%%%%%%%%%%%%%%%%%%%  GroupBox %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    def GroupBox(self):
        
        self.searchtext = self.searchBar.text().replace(' ', '+')
        
        
        if self.searchtext == ' ' and self.searchtext == '':
            return
        else:
            self.openbtn.setEnabled(False)

            self.myurl = f"https://www.youtube.com/results?search_query={self.searchtext}"

            self.driver.get(self.myurl)

            self.GridLayout = QGridLayout()

            self.videoTitle = self.driver.find_elements_by_xpath('//*[@id="video-title"]')
        #lists
            self.hrefs = []
            self.titles = []

        # search data id=video-title
            for attributes in self.videoTitle[0:55]:            
                if attributes.get_attribute("href") is not None:
                    self.href = attributes.get_attribute("href")
                    self.title = attributes.text
                    self.hrefs.append(self.href)
                    self.titles.append(self.title)

            self.HGroupBox = QGroupBox(f"SEARCHED: {self.searchBar.text()} RESULTS: {len(self.titles)}") # len of results

        # make dictionary for titles and href ####################################################
            self.collectiontitles = {}
            for number, ttl in enumerate(self.titles):
                self.collectiontitles["title_%s" %number] = ttl

            self.collectionhref = {}
            for num_atr, atr in enumerate(self.hrefs):
                self.collectionhref["link_%s" %num_atr] = atr
         ##############################################################################
         
         
            for num_atr, atrkey in enumerate(self.collectionhref):
                ''' Thumbnail '''
                
                self.thumbs = self.collectionhref[atrkey]
                self.Vthumbs = pafy.new(self.thumbs) 
                
                Turl = self.Vthumbs.thumb
                data = urllib.request.urlopen(Turl).read()
                
                self.img = QImage()
                self.img.loadFromData(data)
                
                self.thumbclickable = ClickQLable(self)
                self.thumbclickable.setCursor(Qt.PointingHandCursor)
                
                self.thumbclickable.setStyleSheet('min-height:30px;max-width:100px;')
                self.thumbpixmap = QPixmap(self.img)  #.\Images\thumb.png      
                self.thumbclickable.setPixmap(self.thumbpixmap)
                self.GridLayout.addWidget(self.thumbclickable,num_atr,0)
                self.thumbclickable.clicked.connect(lambda state, x= self.collectionhref[atrkey]: self.playvideo(x))
                
                #--------------------------------------------------
                ''' Label'''
                
                self.label_link = pafy.new(self.collectionhref[atrkey]) 
                self.label_title = ClickQLable((f"{self.label_link.title[:55]}-\n{self.label_link.title[55:]}  \n Author: {self.label_link.author} ||  VIEWS:{self.label_link.viewcount} ||: {self.label_link.duration}")) #
                self.label_title.setFont(QFont("Noto Sans",10))  
                self.label_title.setCursor(Qt.PointingHandCursor)
                
                if (num_atr % 2) == 0:
                    self.label_title.setStyleSheet("border: 1px solid green; background-color: Gainsboro;color: black;border-radius: 3px;max-height:60px;") 
                else:
                    self.label_title.setStyleSheet("border: 1px solid green; background-color: DarkGray;color:black;border-radius: 3px;max-height:60px;") 
                
                self.label_title.clicked.connect(lambda state, x= self.collectionhref[atrkey]: self.playvideo(x))
                self.GridLayout.addWidget(self.label_title,num_atr,1)
                
                #--------------------------------------------------
                ''' Star button '''
                self.keybutton = atrkey     
                self.keybutton  = QPushButton(QIcon('.\Images\star.png'),"",self)
                if (num_atr % 2) == 0:
                    self.keybutton.setStyleSheet("background-color: DodgerBlue;color:white;border-color:rgb(218, 165, 32);font:  16px;max-width: 30px; min-height:30px; ")
                else:
                    self.keybutton.setStyleSheet("background-color: DodgerBlue;color:white;border-color:rgb(218, 165, 32);font:  16px;max-width: 60px;min-height:30px;") 
                
                self.GridLayout.addWidget(self.keybutton,num_atr,2)
                self.keybutton.clicked.connect(lambda state, save_link= self.collectionhref[atrkey]: self.addFavorites(save_link)) # connect to href 
                self.keybutton.setToolTip(self.collectionhref[atrkey])
                
                #--------------------------------------------------
                ''' Download button '''
                self.d_link = atrkey
                self.d_link = QPushButton(QIcon(".\Images\download.png"),"",self)
                
                if (num_atr % 2) == 0:
                    self.d_link.setStyleSheet("background-color: rgb(220, 20, 60);color:white;border-color:beige;font: 20px;max-width: 40px;min-height:30px;")
                else:
                    self.d_link.setStyleSheet("background-color: rgb(220, 20, 60);color:white;border-color:beige;font:  20px;max-width: 40px;min-height:30px;") 
                
                self.GridLayout.addWidget(self.d_link, num_atr,3)
                self.d_link.clicked.connect(lambda state, x= self.collectionhref[atrkey]: self.download_(x)) # self.timer.start()
                self.d_link.setToolTip(self.collectionhref[atrkey])


                self.next_atr = num_atr
                self.next_key = atrkey            
                                

        ##############################################################################

            self.HGroupBox.setLayout(self.GridLayout)
            #self.HGroupBox.setLayout(self.removeList)
            
            self.scroll = QScrollArea()
            self.scroll.setWidget(self.HGroupBox)
            #self.scroll.setWidget(self.removeList)
            self.scroll.setWidgetResizable(True)

            self.VboxGrid.addWidget(self.scroll)
            
            #self.VboxGrid.addWidget(self.HGroupBox)
            #self.VboxGrid.addStretch(1)
           

############################################################################################
# %%%%%%%%%%%%%%%%%%%%%%%%%  SLOTS  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    def exit_(self):
        self.driver.close()
        sys.exit()
        
        
    def setVolume(self, Volume):
        self.mediaplayer.audio_set_volume(Volume)
        
    def setPosition(self, position):
        self.mediaplayer.set_position(position / 1000)
        
    def updatevideoposition(self):
        self.videoposition.setValue(self.mediaplayer.get_position() * 1000)
        if not self.mediaplayer.is_playing():
            self.timer.stop()
            if not self.isPaused:
                self.stop_()
   
    def PlayPause(self):
        if self.mediaplayer.is_playing():
            self.mediaplayer.pause()
            self.pauseBtn.setText("Play")
            self.isPaused = True
        else:
            if self.mediaplayer.play() == -1:
                self.mediaplayer.play()
                self.pauseBtn.setText("Pause")
                return
            self.pauseBtn.setText("Pause")
            self.timer.start()
            self.isPaused = False

    def stop_(self): 
        self.mediaplayer.stop()
        self.pauseBtn.setEnabled(False)
        self.stopBtn.setEnabled(False)
        
            
    def next_(self): # kailangan ko gumawa ng media player list :)  
        print(self.collectionhref)
        
    def previous(self): # same as next_()
        pass
    
    
    def OpenMedia(self):
        """Open a media file in a MediaPlayer
        """
        #filename = r'C:\Users\Adam-22-26\OneDrive\PlayerProject\Demon_Slayer.mp4'
        
        #filename = QFileDialog.getOpenFileName(self, "Open File", [os.path('.','media')])  #os.path.expandvars

      #  if sys.version < '3':
       #     filename = unicode(filename)
       # self.media = self._player.media_new(filename)
       # self.mediaplayer.set_media(self.media)
       # self.media.parse()
       # if sys.platform == "win32": # for Windows
       #     self.mediaplayer.set_hwnd(self.videoframe.winId())
       
       
        #self.PlayPause()
        self.pauseBtn.setEnabled(True)
        self.stopBtn.setEnabled(True)
        self.nextBtn.setEnabled(True)
            
    def addFavorites(self, save_link):
        ''' there you can add your favorites link/youtube videos to a local storage (csv)'''
        self.save_link = save_link
        
    def OpenFavorites(self):
        '''Open your favorite list'''
        pass
    
    def playvideo(self, url ): # connected to play now buttons
        self.url = url
        video = pafy.new(self.url)

        self.best = video.streams[0]
        self.best = video.getbest()

        self.best.resolution      
        # creating vlc media player object 
        media = self._player.media_new(self.best.url) # the actual video source
        self.mediaplayer.set_media(media)
        self.setWindowTitle(video.title)

        self.mediaplayer.play()
        
        if sys.platform.startswith("linux"):  # for Linux using the X Server
            self.mediaplayer.set_xwindow(self.videoframe.winId())
        elif sys.platform == "win32":  # for Windows
            self.mediaplayer.set_hwnd(self.videoframe.winId())

        elif sys.platform == "darwin":  # for MacOS
            self.mediaplayer.set_nsobject(self.videoframe.winId())
        self.PlayPause()
        
        time.sleep(3)
        if self.mediaplayer.is_playing():
            self.timer.start()
            self.favorites.setEnabled(True)
            self.pauseBtn.setEnabled(True)
            self.stopBtn.setEnabled(True)
            self.nextBtn.setEnabled(True)
            
            #-------------------------------
            self.statusBar.showMessage("time for videoposition ")
            
    
    def download_(self,url):
        urlD = url
        if self.littlewindow is None:
            self.littlewindow = DownloadWindow(urlD)
            self.littlewindow.show()
        else:
            self.littlewindow.close()
            self.littlewindow = None

        

            

        
