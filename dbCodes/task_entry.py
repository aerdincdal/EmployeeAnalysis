import sqlite3 as sl
from sqlite3 import Error
from datetime import datetime

from department_keyword import DepartmentKeywordDB
from keyword_recorder import KeywordRecorderDB
from employee_identifier import EmployeeIdentifierDB
from extract_keyword import KeywordExtractor

class TaskEntryDB:
    def __init__(self, dbName_="employee_analysis"):
        self.department_keyword = DepartmentKeywordDB(dbName_)
        
        self.keyword_recorder = KeywordRecorderDB(dbName_)
        self.employee_identifier = EmployeeIdentifierDB(dbName_)
        
        self.conn = None
        self.cursor = None
        self.dbName = dbName_ + ".db"
        
    def closeDB(self):
        self.conn.close()
    
    def databaseConnector(self):
        try:
            self.conn = sl.connect(self.dbName)
        except Error as e:
            print(e)
        
        self.cursor = self.conn.cursor()
        self.cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='TASKENTRY_TABLE' ''')
        
        if self.cursor.fetchone()[0] != 1: 
            self.cursor.execute(''' CREATE TABLE TASKENTRY_TABLE
                            ( COMPANY_ID INT NOT NULL,
                            ID INT PRIMARY KEY NOT NULL,
                            TASK_CODE INT NOT NULL,  
                            TASKGIVER_ID INT NOT NULL,
                            TASKRECIEVER_ID INT NOT NULL,
                            ENTRY_TITLE TEXT NOT NULL,
                            ENTRY_DESCRIPTION TEXT,
                            TASK_START_TIME TEXT NOT NULL,
                            TASK_END_TIME TEXT) ''')
   
    def keywordExtractor(self, entry):
        extractor = KeywordExtractor(entry)
        return extractor.extractKeywordList()
        
    
    def update(self, COMPANY_ID, TASK_CODE, TASKGIVER_ID, TASKRECIEVER_ID, ENTRY_TITLE, ENTRY_DESCRIPTION, ID = None, TASK_START_TIME = None, TASK_END_TIME = None):
        if (ID != None):
            self.cursor.execute(''' SELECT * FROM TASKENTRY_TABLE WHERE ID = ? ''', (ID,))
            data_tmp = self.cursor.fetchall()
            
            self.cursor.execute(''' UPDATE TASKENTRY_TABLE
                            SET COMPANY_ID =?,
                            ID =?,
                            TASK_CODE =?,
                            TASKGIVER_ID =?,
                            TASKRECIEVER_ID =?,
                            ENTRY_TITLE =?,
                            ENTRY_DESCRIPTION =?,
                            TASK_START_TIME =?,
                            TASK_END_TIME =?
                            WHERE COMPANY_ID =? AND ID =?''', (COMPANY_ID, ID, TASK_CODE, TASKGIVER_ID, TASKRECIEVER_ID, ENTRY_TITLE, ENTRY_DESCRIPTION, TASK_START_TIME, TASK_END_TIME, COMPANY_ID, ID))
            
            ### UPDATE THE DATABASE ###
            
            # 1. REMOVE FROM DATABASE SECTION
            
            self.cursor.execute(''' SELECT * FROM EMPLOYEE_ID_TABLE WHERE ID = ?''', (data_tmp[0][4],))
            department_id_tmp = self.cursor.fetchall()[0][3]
            
                # Remove Titles
            
            extractor = KeywordExtractor(data_tmp[0][5])
            title_list = extractor.extractKeywordList()
            
            for title in title_list:
                
                try:
                    self.department_keyword.closeDB()
                    self.databaseConnector()
                    self.cursor.execute("SELECT * FROM KEYWORD_RECORDER_TABLE WHERE KEYWORD = ?",(title,))
                    keyword_id_tmp = self.cursor.fetchall()[0][1]
                except:
                    self.department_keyword.closeDB()
                    self.databaseConnector()
                    self.cursor.execute("SELECT * FROM KEYWORD_RECORDER_TABLE WHERE KEYWORD = ?",(title,))
                    keyword_id_tmp = self.cursor.fetchall()[0][1]
                
                try:
                    self.closeDB()
                    self.department_keyword.closeDB()
                    self.keyword_recorder.databaseConnector()
                    self.keyword_recorder.remove(data_tmp[0][0], title, data_tmp[0][4], True)
                    self.keyword_recorder.closeDB()
                
                except:
                    self.closeDB()
                    self.department_keyword.closeDB()
                    self.keyword_recorder.databaseConnector()
                    self.keyword_recorder.remove(data_tmp[0][0], title, data_tmp[0][4], True)
                    self.keyword_recorder.closeDB()
                try:
                    self.closeDB()
                    self.keyword_recorder.closeDB()
                    self.department_keyword.dwoatabaseConnector()
                    self.department_keyword.remove(data_tmp[0][0], keyword_id_tmp, department_id_tmp, True)
                    self.department_keyword.closeDB()
                except:
                    self.closeDB()
                    self.keyword_recorder.closeDB()
                    self.department_keyword.databaseConnector()
                    self.department_keyword.remove(data_tmp[0][0], keyword_id_tmp, department_id_tmp, True)
                    self.department_keyword.closeDB()
                
                # Remove Descriptions
            extractor = KeywordExtractor(data_tmp[0][6])
            description_list = extractor.extractKeywordList()
            
            self.closeDB()
            for description in description_list:
                try:
                    self.department_keyword.closeDB()
                    self.databaseConnector()
                    self.cursor.execute("SELECT * FROM KEYWORD_RECORDER_TABLE WHERE KEYWORD = ?",(description,))
                    keyword_id_tmp = self.cursor.fetchall()[0][1]
                except:
                    self.department_keyword.closeDB()
                    self.databaseConnector()
                    self.cursor.execute("SELECT * FROM KEYWORD_RECORDER_TABLE WHERE KEYWORD = ?",(description,))
                    keyword_id_tmp = self.cursor.fetchall()[0][1]
                
                try:
                    self.closeDB()
                    self.department_keyword.closeDB()
                    self.keyword_recorder.databaseConnector()
                    self.keyword_recorder.remove(data_tmp[0][0], description, data_tmp[0][4], False)
                    self.keyword_recorder.closeDB()
                
                except:
                    self.closeDB()
                    self.department_keyword.closeDB()
                    self.keyword_recorder.databaseConnector()
                    self.keyword_recorder.remove(data_tmp[0][0], description, data_tmp[0][4], False)
                    self.keyword_recorder.closeDB()
                try:
                    self.closeDB()
                    self.keyword_recorder.closeDB()
                    self.department_keyword.dwoatabaseConnector()
                    self.department_keyword.remove(data_tmp[0][0], keyword_id_tmp, department_id_tmp, False)
                    self.department_keyword.closeDB()
                except:
                    self.closeDB()
                    self.keyword_recorder.closeDB()
                    self.department_keyword.databaseConnector()
                    self.department_keyword.remove(data_tmp[0][0], keyword_id_tmp, department_id_tmp, False)
                    self.department_keyword.closeDB()
        
            # 2. ADD TO DATABASE SECTION
            
                # Add Titles
            extractor = KeywordExtractor(data_tmp[0][5])
            title_list = extractor.extractKeywordList()    
            
            for title in title_list:
                try:
                    self.closeDB()
                    self.department_keyword.closeDB()
                    self.keyword_recorder.databaseConnector()
                    self.keyword_recorder.update(COMPANY_ID, title, TASKRECIEVER_ID, True)
                    self.keyword_recorder.closeDB()
                except:
                    self.closeDB()
                    self.department_keyword.closeDB()
                    self.keyword_recorder.databaseConnector()
                    self.keyword_recorder.update(COMPANY_ID, title, TASKRECIEVER_ID, True)
                    self.keyword_recorder.closeDB()
                
                try:
                    self.keyword_recorder.closeDB()
                    self.databaseConnector()
                    self.cursor.execute("SELECT * FROM KEYWORD_RECORDER_TABLE WHERE KEYWORD = ?",(title,))
                    keyword_id_tmp = self.cursor.fetchall()[0][1]
                except:
                    self.keyword_recorder.closeDB()
                    self.databaseConnector()
                    self.cursor.execute("SELECT * FROM KEYWORD_RECORDER_TABLE WHERE KEYWORD = ?",(title,))
                    keyword_id_tmp = self.cursor.fetchall()[0][1]
                    
                try:
                    self.closeDB()
                    self.department_keyword.databaseConnector()
                    self.department_keyword.update(COMPANY_ID, keyword_id_tmp, department_id_tmp, True)
                    self.department_keyword.closeDB()
                except:
                    self.closeDB()
                    self.department_keyword.databaseConnector()
                    self.department_keyword.update(COMPANY_ID, keyword_id_tmp, department_id_tmp, True)
                    self.department_keyword.closeDB()
            
                # Add Descriptions
            extractor = KeywordExtractor(data_tmp[0][6])
            description_list = extractor.extractKeywordList()
            
            for description in description_list:
                try:
                    self.closeDB()
                    self.department_keyword.closeDB()
                    self.keyword_recorder.databaseConnector()
                    self.keyword_recorder.update(COMPANY_ID, description, TASKRECIEVER_ID, False)
                    self.keyword_recorder.closeDB()
                except:
                    self.closeDB()
                    self.department_keyword.closeDB()
                    self.keyword_recorder.databaseConnector()
                    self.keyword_recorder.update(COMPANY_ID, description, TASKRECIEVER_ID, False)
                    self.keyword_recorder.closeDB()
                
                try:
                    self.keyword_recorder.closeDB()
                    self.databaseConnector()
                    self.cursor.execute("SELECT * FROM KEYWORD_RECORDER_TABLE WHERE KEYWORD = ?",(description,))
                    keyword_id_tmp = self.cursor.fetchall()[0][1]
                except:
                    self.keyword_recorder.closeDB()
                    self.databaseConnector()
                    self.cursor.execute("SELECT * FROM KEYWORD_RECORDER_TABLE WHERE KEYWORD = ?",(description,))
                    keyword_id_tmp = self.cursor.fetchall()[0][1]
                    
                try:
                    self.closeDB()
                    self.department_keyword.databaseConnector()
                    self.department_keyword.update(COMPANY_ID, keyword_id_tmp, department_id_tmp, False)
                    self.department_keyword.closeDB()
                except:
                    self.closeDB()
                    self.department_keyword.databaseConnector()
                    self.department_keyword.update(COMPANY_ID, keyword_id_tmp, department_id_tmp, False)
                    self.department_keyword.closeDB()

        else:
            self.databaseConnector()
            self.cursor.execute("SELECT max(id) FROM TASKENTRY_TABLE")
            data_tmp = self.cursor.fetchone()
            
            if(data_tmp[0]):
                ID = data_tmp[0] + 1
            else:
                ID = 1
                        
            if(TASK_START_TIME == None):
                TASK_START_TIME = datetime.now()
                self.cursor.execute("""INSERT INTO TASKENTRY_TABLE
                                    (COMPANY_ID, ID, TASK_CODE, TASKGIVER_ID, TASKRECIEVER_ID, ENTRY_TITLE, ENTRY_DESCRIPTION, TASK_START_TIME, TASK_END_TIME) 
                                    VALUES (?,?,?,?,?,?,?,?,?)""", (COMPANY_ID, ID, TASK_CODE, TASKGIVER_ID, TASKRECIEVER_ID, ENTRY_TITLE, ENTRY_DESCRIPTION, TASK_START_TIME, TASK_END_TIME))
                self.conn.commit()
            else:
                if(TASK_END_TIME == None):
                    self.cursor.execute("""INSERT INTO TASKENTRY_TABLE
                                        (COMPANY_ID, ID, TASK_CODE, TASKGIVER_ID, TASKRECIEVER_ID, ENTRY_TITLE, ENTRY_DESCRIPTION, TASK_START_TIME, TASK_END_TIME)  VALUES (?,?,?,?,?,?,?,?)""", (COMPANY_ID, ID, TASK_CODE, TASKGIVER_ID, TASKRECIEVER_ID, ENTRY_TITLE, ENTRY_DESCRIPTION, TASK_START_TIME))
                else:
                    self.cursor.execute("""INSERT INTO TASKENTRY_TABLE
                                        (COMPANY_ID, ID, TASK_CODE, TASKGIVER_ID, TASKRECIEVER_ID, ENTRY_TITLE, ENTRY_DESCRIPTION, TASK_START_TIME, TASK_END_TIME)  VALUES (?,?,?,?,?,?,?,?,?)""", (COMPANY_ID, ID, TASK_CODE, TASKGIVER_ID, TASKRECIEVER_ID, ENTRY_TITLE, ENTRY_DESCRIPTION, TASK_START_TIME, TASK_END_TIME))
                self.conn.commit()
            ### ADD TO DATABASE ###
            self.cursor.execute("SELECT * FROM TASKENTRY_TABLE WHERE ID = ?",(ID,))
            data_tmp = self.cursor.fetchall()
                # Add Titles
                
            self.cursor.execute(''' SELECT * FROM EMPLOYEE_ID_TABLE WHERE ID = ?''', (data_tmp[0][4],))
            department_id_tmp = self.cursor.fetchall()[0][3]
            
            extractor = KeywordExtractor(data_tmp[0][5])
            title_list = extractor.extractKeywordList()    
            
            for title in title_list:
                try:
                    self.closeDB()
                    self.keyword_recorder.databaseConnector()
                    self.keyword_recorder.update(COMPANY_ID, title, TASKRECIEVER_ID, True)
                    self.keyword_recorder.closeDB()
                except:
                    self.closeDB()
                    self.keyword_recorder.databaseConnector()
                    self.keyword_recorder.update(COMPANY_ID, title, TASKRECIEVER_ID, True)
                    self.keyword_recorder.closeDB()
                
                try:
                    self.keyword_recorder.closeDB()
                    self.databaseConnector()
                    self.cursor.execute("SELECT * FROM KEYWORD_RECORDER_TABLE WHERE KEYWORD = ?",(title,))
                    keyword_id_tmp = self.cursor.fetchall()[0][1]
                except:
                    self.keyword_recorder.closeDB()
                    self.databaseConnector()
                    self.cursor.execute("SELECT * FROM KEYWORD_RECORDER_TABLE WHERE KEYWORD = ?",(title,))
                    keyword_id_tmp = self.cursor.fetchall()[0][1]
                    
                try:
                    self.closeDB()
                    self.department_keyword.databaseConnector()
                    self.department_keyword.update(COMPANY_ID, keyword_id_tmp, department_id_tmp, True)
                    self.department_keyword.closeDB()
                except:
                    self.closeDB()
                    self.department_keyword.databaseConnector()
                    self.department_keyword.update(COMPANY_ID, keyword_id_tmp, department_id_tmp, True)
                    self.department_keyword.closeDB()
            
                # Add Descriptions
            extractor = KeywordExtractor(data_tmp[0][6])
            description_list = extractor.extractKeywordList()
            
            for description in description_list:
                try:
                    self.closeDB()
                    self.department_keyword.closeDB()
                    self.keyword_recorder.databaseConnector()
                    self.keyword_recorder.update(COMPANY_ID, description, TASKRECIEVER_ID, False)
                    self.keyword_recorder.closeDB()
                except:
                    self.closeDB()
                    self.department_keyword.closeDB()
                    self.keyword_recorder.databaseConnector()
                    self.keyword_recorder.update(COMPANY_ID, description, TASKRECIEVER_ID, False)
                    self.keyword_recorder.closeDB()
                
                try:
                    self.keyword_recorder.closeDB()
                    self.databaseConnector()
                    self.cursor.execute("SELECT * FROM KEYWORD_RECORDER_TABLE WHERE KEYWORD = ?",(description,))
                    keyword_id_tmp = self.cursor.fetchall()[0][1]
                except:
                    self.keyword_recorder.closeDB()
                    self.databaseConnector()
                    self.cursor.execute("SELECT * FROM KEYWORD_RECORDER_TABLE WHERE KEYWORD = ?",(description,))
                    keyword_id_tmp = self.cursor.fetchall()[0][1]
                    
                try:
                    self.closeDB()
                    self.department_keyword.databaseConnector()
                    self.department_keyword.update(COMPANY_ID, keyword_id_tmp, department_id_tmp, False)
                    self.department_keyword.closeDB()
                except:
                    self.closeDB()
                    self.department_keyword.databaseConnector()
                    self.department_keyword.update(COMPANY_ID, keyword_id_tmp, department_id_tmp, False)
                    self.department_keyword.closeDB()
        
        self.databaseConnector()
            
    def remove(self, ID):
        
        self.cursor.execute("SELECT * FROM TASKENTRY_TABLE WHERE ID = ?",(ID,))
        data_tmp = self.cursor.fetchall()
        
        self.cursor.execute(''' SELECT * FROM EMPLOYEE_ID_TABLE WHERE ID = ?''', (data_tmp[0][4],))
        department_id_tmp = self.cursor.fetchall()[0][3]
        
        ### REMOVE FROM DATABASE ###
        
            # Remove Titles
        
        extractor = KeywordExtractor(data_tmp[0][5])
        title_list = extractor.extractKeywordList()
        
        for title in title_list:
            
            try:
                self.department_keyword.closeDB()
                self.databaseConnector()
                self.cursor.execute("SELECT * FROM KEYWORD_RECORDER_TABLE WHERE KEYWORD = ?",(title,))
                keyword_id_tmp = self.cursor.fetchall()[0][1]
            except:
                self.department_keyword.closeDB()
                self.databaseConnector()
                self.cursor.execute("SELECT * FROM KEYWORD_RECORDER_TABLE WHERE KEYWORD = ?",(title,))
                keyword_id_tmp = self.cursor.fetchall()[0][1]
            
            try:
                self.closeDB()
                self.department_keyword.closeDB()
                self.keyword_recorder.databaseConnector()
                self.keyword_recorder.remove(data_tmp[0][0], title, data_tmp[0][4], True)
                self.keyword_recorder.closeDB()
            
            except:
                self.closeDB()
                self.department_keyword.closeDB()
                self.keyword_recorder.databaseConnector()
                self.keyword_recorder.remove(data_tmp[0][0], title, data_tmp[0][4], True)
                self.keyword_recorder.closeDB()
            try:
                self.closeDB()
                self.keyword_recorder.closeDB()
                self.department_keyword.dwoatabaseConnector()
                self.department_keyword.remove(data_tmp[0][0], keyword_id_tmp, department_id_tmp, True)
                self.department_keyword.closeDB()
            except:
                self.closeDB()
                self.keyword_recorder.closeDB()
                self.department_keyword.databaseConnector()
                self.department_keyword.remove(data_tmp[0][0], keyword_id_tmp, department_id_tmp, True)
                self.department_keyword.closeDB()
            
            # Remove Descriptions
        extractor = KeywordExtractor(data_tmp[0][6])
        description_list = extractor.extractKeywordList()
        
        self.closeDB()
        for description in description_list:
            try:
                self.department_keyword.closeDB()
                self.databaseConnector()
                self.cursor.execute("SELECT * FROM KEYWORD_RECORDER_TABLE WHERE KEYWORD = ?",(description,))
                keyword_id_tmp = self.cursor.fetchall()[0][1]
            except:
                self.department_keyword.closeDB()
                self.databaseConnector()
                self.cursor.execute("SELECT * FROM KEYWORD_RECORDER_TABLE WHERE KEYWORD = ?",(description,))
                keyword_id_tmp = self.cursor.fetchall()[0][1]
            
            try:
                self.closeDB()
                self.department_keyword.closeDB()
                self.keyword_recorder.databaseConnector()
                self.keyword_recorder.remove(data_tmp[0][0], description, data_tmp[0][4], False)
                self.keyword_recorder.closeDB()
            
            except:
                self.closeDB()
                self.department_keyword.closeDB()
                self.keyword_recorder.databaseConnector()
                self.keyword_recorder.remove(data_tmp[0][0], description, data_tmp[0][4], False)
                self.keyword_recorder.closeDB()
            try:
                self.closeDB()
                self.keyword_recorder.closeDB()
                self.department_keyword.dwoatabaseConnector()
                self.department_keyword.remove(data_tmp[0][0], keyword_id_tmp, department_id_tmp, False)
                self.department_keyword.closeDB()
            except:
                self.closeDB()
                self.keyword_recorder.closeDB()
                self.department_keyword.databaseConnector()
                self.department_keyword.remove(data_tmp[0][0], keyword_id_tmp, department_id_tmp, False)
                self.department_keyword.closeDB()
        
        self.databaseConnector()
        self.cursor.execute(''' DELETE FROM TASKENTRY_TABLE WHERE ID =?''', (ID,))
        
        
        
        