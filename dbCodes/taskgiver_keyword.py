import sqlite3 as sl
from sqlite3 import Error

class TaskgiverKeywordDB:
    def __init__(self, dbName_="employee_analysis"):
        self.conn = None
        self.cursor = None
        self.dbName = dbName_ + ".db"
    
    def databaseConnector(self):
        try:
            self.conn = sl.connect(self.dbName)
        except Error as e:
            print(e)
        
        self.cursor = self.conn.cursor()
        self.cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='TASKGIVER_KEYWORD_TABLE' ''')
        
        if self.cursor.fetchone()[0] != 1:
            self.cursor.execute(''' CREATE TABLE TASKGIVER_KEYWORD_TABLE
                                    (
                                    COMPANY_ID INT NOT NULL,
                                    KEYWORD_ID INT NOT NULL,
                                    TASKGIVER_ID INT NOT NULL,
                                    UCT INT NOT NULL,
                                    UCD INT NOT NULL) ''')
    
    def closeDB(self):
        self.conn.close()
    
    def update(self, COMPANY_ID_, KEYWORD_ID_, TASKGIVER_ID_, isTitle_):
        self.cursor.execute("SELECT 1 FROM TASGIVER_KEYWORD_TABLE WHERE COMPANY_ID = ? AND KEYWORD_ID = ? AND TASKGIVER_ID = ?",(COMPANY_ID_, KEYWORD_ID_, TASKGIVER_ID_,))
        if self.cursor.fetchone() == None:
            if isTitle_:
                self.cursor.execute("INSERT INTO TASKGIVER_KEYWORD_TABLE (COMPANY_ID, KEYWORD_ID, TASKGIVER_ID, UCT, UCD) VALUES (?,?,?,?,?)",(COMPANY_ID_, KEYWORD_ID_, TASKGIVER_ID_, 1, 0))
            else:
                self.cursor.execute("INSERT INTO TASKGIVER_KEYWORD_TABLE (COMPANY_ID, KEYWORD_ID, TASKGIVER_ID, UCT, UCD) VALUES (?,?,?,?,?)",(COMPANY_ID_, KEYWORD_ID_, TASKGIVER_ID_, 0, 1))
                
        else:
            if isTitle_:
                self.cursor.execute("UPDATE TASKGIVER_KEYWORD_TABLE SET UCT = UCT + 1 WHERE COMPANY_ID = ? AND KEYWORD_ID = ? AND TASKGIVER_ID = ?",(COMPANY_ID_, KEYWORD_ID_, TASKGIVER_ID_,))
            else:
                self.cursor.execute("UPDATE TASKGIVER_KEYWORD_TABLE SET UCD = UCD + 1 WHERE COMPANY_ID = ? AND KEYWORD_ID = ? AND TASKGIVER_ID = ?",(COMPANY_ID_, KEYWORD_ID_, TASKGIVER_ID_,))
        
        self.conn.commit()
    
    def remove(self, COMPANY_ID_, KEYWORD_ID_, TASKGIVER_ID_, isTitle_):
        self.cursor.execute("SELECT * FROM TASKGIVER_KEYWORD_TABLE WHERE COMPANY_ID = ? AND KEYWORD_ID = ? AND TASKGIVER_ID = ?",(COMPANY_ID_, KEYWORD_ID_, TASKGIVER_ID_,))
        data_tmp = self.cursor.fetchall()
        if (data_tmp[0][3] == 1 and data_tmp[0][4] == 0 and  isTitle_):
            self.cursor.execute("DELETE FROM TASKGIVER_KEYWORD_TABLE WHERE COMPANY_ID = ? AND KEYWORD_ID = ? AND TASKGIVER_ID = ?",(COMPANY_ID_, KEYWORD_ID_, TASKGIVER_ID_,))
            
        elif (data_tmp[0][3] == 0 and data_tmp[0][4] == 1 and  not isTitle_):
            self.cursor.execute("DELETE FROM TASKGIVER_KEYWORD_TABLE WHERE COMPANY_ID = ? AND KEYWORD_ID = ? AND TASKGIVER_ID = ?",(COMPANY_ID_, KEYWORD_ID_, TASKGIVER_ID_,))
            
        elif (isTitle_):
            self.cursor.execute("UPDATE TASKGIVER_KEYWORD_TABLE SET UCT = UCT - 1 WHERE COMPANY_ID = ? AND KEYWORD_ID = ? AND TASKGIVER_ID = ?",(COMPANY_ID_, KEYWORD_ID_, TASKGIVER_ID_,))
        
        else:
            self.cursor.execute("UPDATE TASKGIVER_KEYWORD_TABLE SET UCD = UCD - 1 WHERE COMPANY_ID = ? AND KEYWORD_ID = ? AND TASKGIVER_ID = ?",(COMPANY_ID_, KEYWORD_ID_, TASKGIVER_ID_,))
                
        self.conn.commit()
