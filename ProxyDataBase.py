#!usr/bin/python
#coding:utf-8

import sqlite3


class ProxyDataBase(object):
    
    
    def __init__(self):
        self.conn = sqlite3.connect("proxy.db")
    
    def save(self,iptype,ip,port,attr,type,date):
        
        cursor = self.conn.cursor()
        cursor.execute("create table IF NOT EXISTS ipInfo(_id INTEGER PRIMARY KEY,iptype VARCHAR(20),ip VARCHAR(20),port VARCHAR(20),attr VARCHAR(20),type VARCHAR(20),date VARCHAR(20)) ")
        self.conn.commit()
        cursor.execute("insert into ipInfo(iptype,ip,port,attr,type,date) values('"+iptype+"','"+ip+"','"+port+"','"+attr+"','"+type+"','"+date+"')")
        self.conn.commit()
        
    def close(self):
        self.conn.close()
