# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 14:55:12 2020

@author: Adam-22-26
"""
from PyQt5.QtWidgets import QDialog, QMessageBox
import csv
import os.path
from fcache.cache import FileCache


class User_Data(QDialog):
    '''
    Behavior: csv
    '''
    _link_writer = None
    __add_new = None
    def __init__(self,  title,save_link , parent=None):
        super(User_Data,self).__init__(parent=None)
        
        self._save_title = title
        self._save_link = save_link
        self.__add_new = [self._save_title,self._save_link]
                    
    def add_(self):
        if os.path.exists('.\data\My_favorites.csv'): # check if exists     
            with open('.\data\My_favorites.csv','a', encoding='utf-8', newline='') as add_fave, open('.\data\My_favorites.csv','r',newline='') as open_fave:
                
                file_reader = csv.reader(open_fave) #read   
                self._link_writer = csv.writer(add_fave)
                                        
                if self.__add_new not in file_reader:
                    self._link_writer.writerow(self.__add_new)    
                    self.informationBox_added_link(self._save_title)
                                       
        else: # create new file
            with open('.\data\My_favorites.csv','w') as add_fave:
                self._link_writer = csv.writer(add_fave,  delimiter=',')
                header = ['Titles', 'Links']
                self._link_writer.writerow(header)
      

    
    def informationBox_added_link(self,title):
        QMessageBox.information(self, "Added to favorite", "Title {}.".format(title))
     
class Cache:
    '''
    Behavior:  cache
    '''
    def __init__(self,link =None,thumb_bytes=None):
        self.save_link = link
        self.thumbnail_bytes = thumb_bytes
        self.thumbnail_cache = FileCache('appname', flag='cs') # change the cache location filename to AVplayer --------------
    
    def createCache(self):
        if self.save_link not in self.thumbnail_cache:
            self.thumbnail_cache[self.save_link] = self.thumbnail_bytes
    
    def getCache(self):
        return self.thumbnail_cache
        
