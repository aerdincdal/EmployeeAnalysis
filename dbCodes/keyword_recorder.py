import sqlite3 as sl
from sqlite3 import Error

from general_counter import GeneralCounterDB
from employee_factor import EmployeeFactorDB

class KeywordRecorderDB:
    def __init__(self, dbName_="employee_analysis"):
        self.general_counter = GeneralCounterDB(dbName_)
        self.employee_factor = EmployeeFactorDB(dbName_)
        
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
        self.cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='KEYWORD_RECORDER_TABLE' ''')
        
        if self.cursor.fetchone()[0] != 1:
            self.cursor.execute(''' CREATE TABLE KEYWORD_RECORDER_TABLE
                                    (
                                    COMPANY_ID INT NOT NULL,
                                    ID INT PRIMARY KEY NOT NULL,
                                    KEYWORD TEXT NOT NULL,
                                    USAGE_COUNT INT NOT NULL) ''')
    def update(self, COMPANY_ID_, KEYWORD_, EMPLOYEE_ID_, isTitle_):
        self.cursor.execute("SELECT 1 FROM KEYWORD_RECORDER_TABLE WHERE COMPANY_ID = ? AND KEYWORD = ?",(COMPANY_ID_, KEYWORD_,))
        if (self.cursor.fetchone() == None):
            self.cursor.execute('SELECT max(ID) FROM KEYWORD_RECORDER_TABLE')
            data_tmp = self.cursor.fetchone()
            if (data_tmp[0]):
                new_id = data_tmp[0] + 1
            else:
                new_id = 1
            self.cursor.execute("INSERT INTO KEYWORD_RECORDER_TABLE (COMPANY_ID ,ID, KEYWORD, USAGE_COUNT) VALUES (?,?,?,?)",(COMPANY_ID_, new_id, KEYWORD_, 1))
            self.conn.commit()
            #ADD TO GENERAL_COUNTER_TABLE
            try:
                self.closeDB()
                self.general_counter.databaseConnector()
                self.general_counter.update(1, COMPANY_ID_)
                self.general_counter.closeDB()
                self.databaseConnector()
            except:
                self.closeDB()
                self.general_counter.databaseConnector()
                self.general_counter.update(1, COMPANY_ID_)
                self.general_counter.closeDB()
                self.databaseConnector()
                
            #ADD TO EMPLOYEE_FACTOR_TABLE
            try:
                self.closeDB()
                self.employee_factor.databaseConnector()
                self.employee_factor.update(1, isTitle_, COMPANY_ID_, new_id, EMPLOYEE_ID_)
                self.employee_factor.closeDB()
                self.databaseConnector()
            except:
                self.closeDB()
                self.employee_factor.databaseConnector()
                self.employee_factor.update(1, isTitle_, COMPANY_ID_, new_id, EMPLOYEE_ID_)
                self.employee_factor.closeDB()
                self.databaseConnector()
        else:
            self.cursor.execute("UPDATE KEYWORD_RECORDER_TABLE SET USAGE_COUNT = USAGE_COUNT + 1 WHERE COMPANY_ID = ? AND KEYWORD = ?",(COMPANY_ID_, KEYWORD_,))
            self.conn.commit()
            self.cursor.execute("SELECT * FROM KEYWORD_RECORDER_TABLE WHERE COMPANY_ID = ? AND KEYWORD = ?",(COMPANY_ID_, KEYWORD_,))
            data_tmp = self.cursor.fetchall()
            # ADD TO GENERAL_COUNTER_TABLE
            try:
                self.closeDB()
                self.general_counter.databaseConnector()
                self.general_counter.update(2, COMPANY_ID_)
                self.general_counter.closeDB()
                self.databaseConnector()
            except:
                self.closeDB()
                self.general_counter.databaseConnector()
                self.general_counter.update(2, COMPANY_ID_)
                self.general_counter.closeDB()
                self.databaseConnector()
            
            #ADD TO EMPLOYEE_FACTOR_TABLE
            try:
                self.closeDB()
                self.employee_factor.databaseConnector()
                self.employee_factor.update(2, isTitle_, COMPANY_ID_, data_tmp[0][1], EMPLOYEE_ID_)
                self.employee_factor.closeDB()
                self.databaseConnector()
            except:
                self.closeDB()
                self.employee_factor.databaseConnector()
                self.employee_factor.update(2, isTitle_, COMPANY_ID_, data_tmp[0][1], EMPLOYEE_ID_)
                self.employee_factor.closeDB()
                self.databaseConnector()

    def remove(self, COMPANY_ID_, KEYWORD_, EMPLOYEE_ID_, isTitle_):
        self.cursor.execute("SELECT 1 FROM KEYWORD_RECORDER_TABLE WHERE COMPANY_ID =? AND KEYWORD =?",(COMPANY_ID_, KEYWORD_,))
        if (self.cursor.fetchone() == None):
            print("Keyword not found")
            return
        
        self.cursor.execute("SELECT * FROM KEYWORD_RECORDER_TABLE WHERE COMPANY_ID = ? AND KEYWORD = ?",(COMPANY_ID_, KEYWORD_,))
        data_tmp = self.cursor.fetchall()
        if (data_tmp[0][3] == 1):
            self.cursor.execute("DELETE FROM KEYWORD_RECORDER_TABLE WHERE COMPANY_ID = ? AND KEYWORD = ?",(COMPANY_ID_, KEYWORD_,))
            self.conn.commit()
            #GENERAL_COUNTER_TABLE
            try:
                self.closeDB()
                self.general_counter.databaseConnector()
                self.general_counter.update(3, COMPANY_ID_)
                self.general_counter.closeDB()
                self.databaseConnector()
            except:
                self.closeDB()
                self.general_counter.databaseConnector()
                self.general_counter.update(3, COMPANY_ID_)
                self.general_counter.closeDB()
                self.databaseConnector()
            #EMPLOYEE_FACTOR_TABLE
            try:
                self.closeDB()
                self.employee_factor.databaseConnector()
                self.employee_factor.update(3, isTitle_, COMPANY_ID_, data_tmp[0][1], EMPLOYEE_ID_)
                self.employee_factor.closeDB()
                self.databaseConnector()
            except:
                self.closeDB()
                self.employee_factor.databaseConnector()
                self.employee_factor.update(3, isTitle_, COMPANY_ID_, data_tmp[0][1], EMPLOYEE_ID_)
                self.employee_factor.closeDB()
                self.databaseConnector()
        else:
            self.cursor.execute("UPDATE KEYWORD_RECORDER_TABLE SET USAGE_COUNT = USAGE_COUNT - 1 WHERE COMPANY_ID = ? AND KEYWORD = ?",(COMPANY_ID_, KEYWORD_,))
            self.conn.commit()
            #GENERAL_COUNTER_TABLE
            try:
                self.closeDB()
                self.general_counter.databaseConnector()
                self.general_counter.update(4, COMPANY_ID_)
                self.general_counter.closeDB()
                self.databaseConnector()
            except:
                self.closeDB()
                self.general_counter.databaseConnector()
                self.general_counter.update(4, COMPANY_ID_)
                self.general_counter.closeDB()
                self.databaseConnector()
            
            #EMPLOYEE_FACTOR_TABLE
            try:
                self.closeDB()
                self.employee_factor.databaseConnector()
                self.employee_factor.update(4, isTitle_, COMPANY_ID_, data_tmp[0][1], EMPLOYEE_ID_)
                self.employee_factor.closeDB()
                self.databaseConnector()
            except:
                self.closeDB()
                self.employee_factor.databaseConnector()
                self.employee_factor.update(4, isTitle_, COMPANY_ID_, data_tmp[0][1], EMPLOYEE_ID_)
                self.employee_factor.closeDB()
                self.databaseConnector()


def main():
    pass

if __name__ == "__main__":
    main()
