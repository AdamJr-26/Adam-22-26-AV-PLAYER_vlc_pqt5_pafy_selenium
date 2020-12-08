# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 14:55:12 2020

@author: Adam-22-26
"""
from PyQt5.QtWidgets import QDialog, QMessageBox
import csv
import pafy
import urllib.request
import requests
import os.path
from fcache.cache import FileCache
import codecs

class User_Data(QDialog):
    '''
    Behavior: Storage, cache
    '''
    link_writer = None
    __add_new = None
    def __init__(self,title, save_link, parent=None):
        super(User_Data,self).__init__(parent=None)
        
        self.save_title = title
        self.save_link = save_link
        self.__add_new = [self.save_title,self.save_link]
        
            
    def add_(self):
        if os.path.exists('My_favorites.csv'): # check if exists
        
            with open('My_favorites.csv','a',newline='') as add_fave, open('My_favorites.csv','r',newline='') as open_fave:
                
                file_reader = csv.reader(open_fave) #read   
                
                self.link_writer = csv.writer(add_fave,  delimiter=',')
                                        
                if self.__add_new not in file_reader:
                    self.link_writer.writerow(self.__add_new)    
                    self.informationBox_added_link(self.save_title)
                    
                    
        else: # create new file
            with open('My_favorites.csv','w') as add_fave:
                self.link_writer = csv.writer(add_fave,  delimiter=',')
                header = ['Titles', 'Links','thumbnail directory']
                self.link_writer.writerow(header)
      
    def _getThumb(self):        
        self.Vthumbs = pafy.new(self.save_link)         
        Turl = self.Vthumbs.thumb
        data = urllib.request.urlopen(Turl).read()
        print(data)
        links = requests.get(Turl)
        #with open('site.text') as csvfile:
           # reader = csv.DictReader(csvfile)
           # for row in reader:
             #   print(row)
                
class Cache:
        '''
    Behavior:  cache
    '''
    def __init__(self,title, save_link):
        self.save_title = title
        self.save_link = save_link
        
    def createCache(self):
        self.mycache = FileCache('appname', flag='cs')
        self.mycache[]
    
    def getCache(self):
        pass
        
        
        
        '''
        print(data)
        rawThumb = requests.get(Turl,stream=True)
        
        with open('new.csv', 'wb') as fd:
            writer = csv.writer(fd,delimiter=',')
            
            for chunk in rawThumb.iter_content(chunk_size = 1024):
                
                fd.write(chunk)
                '''
    
    def informationBox_added_link(self,accion):
        QMessageBox.information(self, "Added to favorite", "Title {}.".format(accion))
                    
        
        
        

data = User_Data('no title2','https://www.youtube.com/watch?v=IEEhzQoKtQU&ab_channel=CoreySchafer')
data.add_()
data._getThumb()

class ImageTitleLink:
    '''
    Storage of thumbnail and label
    '''


        