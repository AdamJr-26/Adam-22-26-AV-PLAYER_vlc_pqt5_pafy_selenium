# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 08:48:26 2020

@author: Adam-22-26
"""

import pafy
import os
os.add_dll_directory(r'C:\Program Files\VideoLAN\VLC')
import threading
# import _thread
from PyQt5 import QtCore
from PyQt5.QtCore import  pyqtSignal
from PyQt5.QtWidgets import  (QWidget,
                             QPushButton, QHBoxLayout, 
                            QVBoxLayout,QLabel, QLineEdit, QProgressBar,
                              QMainWindow)

###################################################################

class DownloadWindow(QMainWindow):
    
    progressChanged = pyqtSignal(int)
    def __init__(self, url,parent=None):
        super(DownloadWindow, self).__init__(parent)
        
        QMainWindow.__init__(self)        
        self.urlD = url
        self.videoD = pafy.new(self.urlD) 
        
        self.audioD = pafy.new(self.urlD)
        
        
        self.bestD = self.videoD.streams[0]
        self.bestD = self.videoD.getbest()
        
        self.audiobest = self.audioD.streams[0]
        self.audiobest = self.audioD.getbestaudio(preftype ="m4a")
                
        self.widgetD = QWidget(self)                                
        self.setCentralWidget(self.widgetD)
        
        self.video_size = QLabel(f" MP4 SIZE: {self.bestD.get_filesize()} Bytes\n MP3 SIZE: {self.audiobest.get_filesize()}\n {self.audiobest.title}")
        self.video_size.setStyleSheet("font: bold 13px")
        
        
        self.setWindowTitle("Choose Format")
        
        self.exitD = QPushButton("Exit")
        self.exitD.setStyleSheet("max-width: 50px;")
        self.exitD.clicked.connect(self.exitd)
        
        self.mp3 = QPushButton("MP3")
        self.mp3.setStyleSheet("max-width: 50px;")
        self.mp3.clicked.connect(self.mp3F)
        
        self.mp4 = QPushButton("MP4")
        self.mp4.setStyleSheet("max-width: 50px;")
        self.mp4.clicked.connect(self.mp4F)

        
        self.layoutFormat = QHBoxLayout()
        self.layoutFormat.addStretch(50)
        self.VdownloadLayout = QVBoxLayout()
        self.layoutFormat.addWidget(self.mp3)
        self.layoutFormat.addWidget(self.mp4)
        self.layoutFormat.addWidget(self.exitD)
        
        self.pbar = QProgressBar(maximum=100)
        self.pbar.setGeometry(30, 40, 200, 25)
        self.progressChanged.connect(self.pbar.setValue)
                
        path = QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.DownloadLocation)
        self.le_output = QLineEdit(path)

        self.VdownloadLayout.addWidget(self.video_size)
        self.VdownloadLayout.addLayout(self.layoutFormat)
        
        self.VdownloadLayout.addWidget(self.le_output)
        
        
        self.widgetD.setLayout(self.VdownloadLayout)
        self.show()
        
    
    def download_info(self, total, recvd, ratio, rate, eta): # pafy callback for pafy.download
        self.setWindowTitle(f"downloading {self.videoD.title}")
        val = int(ratio * 100)
        self.progressChanged.emit(val)
        if val == 100:
            self.close()
            
            # add condition if it's not receiving or inter connection timeout
        

    def mp3F(self):        
        video_save = self.le_output.text()
        self.audiobest = self.audioD.streams[0]
        self.audiobest = self.audioD.getbestaudio(preftype ="m4a")
        threading.Thread(target=self.audiobest.download, kwargs={'filepath' : video_save, 'callback': self.download_info}, daemon=True).start()
        self.VdownloadLayout.addWidget(self.pbar)
        

    def mp4F(self):
        
        video_save = self.le_output.text()
        self.bestD = self.videoD.streams[0]
        self.bestD = self.videoD.getbest(preftype ="mp4")
        threading.Thread(target=self.bestD.download, kwargs={'filepath' : video_save, 'callback': self.download_info}, daemon=True).start()
        self.VdownloadLayout.addWidget(self.pbar)
    
    def exitd(self):
        self.close()