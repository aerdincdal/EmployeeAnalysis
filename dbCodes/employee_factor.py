import sqlite3 as sl
from sqlite3 import Error

class EmployeeFactorDB:
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
        self.cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='EMPLOYEE_FACTOR_TABLE' ''')
        
        if self.cursor.fetchone()[0] != 1:
            self.cursor.execute(''' CREATE TABLE EMPLOYEE_FACTOR_TABLE
                                    (
                                    COMPANY_ID INT NOT NULL,
                                    KEYWORD_ID INT NOT NULL,
                                    EMPLOYEE_ID INT NOT NULL,
                                    UCT INT NOT NULL,
                                    UCD INT NOT NULL,
                                    TASK_COUNT INT NOT NULL,
                                    AVARAGE_HOURS REAL) ''')
    def closeDB(self):
        self.conn.close()
    
    def update(self, call_option, isTitle_, COMPANY_ID_, KEYWORD_ID_, EMPLOYEE_ID_):
        
        #Options:
        #1. call_option = "Add keyword and set UCT or UCD to one"
        #2. call_option = "Increase UCT or UCD"
        #3. call_option = "Delete keyword"
        #4. call_option = "Decrease UCT or UCD"
        if(call_option == 1):
            if(isTitle_):
                self.cursor.execute('''INSERT INTO EMPLOYEE_FACTOR_TABLE (COMPANY_ID, KEYWORD_ID, EMPLOYEE_ID, UCT, UCD, TASK_COUNT, AVARAGE_HOURS) VALUES (?,?,?,?,?,?,?)''',(COMPANY_ID_, KEYWORD_ID_, EMPLOYEE_ID_, 1, 0, 0,0))
                self.conn.commit()
            else:
                self.cursor.execute('''INSERT INTO EMPLOYEE_FACTOR_TABLE (COMPANY_ID, KEYWORD_ID, EMPLOYEE_ID, UCT, UCD, TASK_COUNT, AVARAGE_HOURS) VALUES (?,?,?,?,?,?,?)''',(COMPANY_ID_, KEYWORD_ID_, EMPLOYEE_ID_, 0, 1, 0,0))
                self.conn.commit()
        elif(call_option == 2):
            if(isTitle_):
                self.cursor.execute('''UPDATE EMPLOYEE_FACTOR_TABLE SET UCT = UCT + 1 WHERE COMPANY_ID = ? AND KEYWORD_ID = ? AND EMPLOYEE_ID = ?''',(COMPANY_ID_, KEYWORD_ID_, EMPLOYEE_ID_))
                self.conn.commit()
            else:
                self.cursor.execute('''UPDATE EMPLOYEE_FACTOR_TABLE SET UCD = UCD + 1 WHERE COMPANY_ID = ? AND KEYWORD_ID = ? AND EMPLOYEE_ID = ?''',(COMPANY_ID_, KEYWORD_ID_, EMPLOYEE_ID_))
                self.conn.commit()
        elif(call_option == 3):
            self.cursor.execute('''DELETE FROM EMPLOYEE_FACTOR_TABLE WHERE COMPANY_ID = ? AND KEYWORD_ID = ? AND EMPLOYEE_ID = ?''',(COMPANY_ID_, KEYWORD_ID_, EMPLOYEE_ID_))
            self.conn.commit()
        elif(call_option == 4):
            if(isTitle_):
                self.cursor.execute('''UPDATE EMPLOYEE_FACTOR_TABLE SET UCT = UCT - 1 WHERE COMPANY_ID = ? AND KEYWORD_ID = ? AND EMPLOYEE_ID = ?''',(COMPANY_ID_, KEYWORD_ID_, EMPLOYEE_ID_))
                self.conn.commit()
            else:
                self.cursor.execute('''UPDATE EMPLOYEE_FACTOR_TABLE SET UCD = UCD - 1 WHERE COMPANY_ID = ? AND KEYWORD_ID = ? AND EMPLOYEE_ID = ?''',(COMPANY_ID_, KEYWORD_ID_, EMPLOYEE_ID_))
                self.conn.commit()
                
        else:
            print("Wrong call option")
        
    
    def updateTime(self, COMPANY_ID_, KEYWORD_ID_, EMPLOYEE_ID_, TIME_SPENT_):
        self.cursor.execute("SELECT * FROM COMPANY_TABLE WHERE COMPANY_ID = ? AND KEYWORD_ID = ? AND EMPLOYEE_ID = ?",(COMPANY_ID_, KEYWORD_ID_, EMPLOYEE_ID_))
        data_tmp = self.cursor.fetchall()
        time_avarage = (data_tmp[0][5] * data_tmp[0][6] + TIME_SPENT_) / data_tmp[0][5] + 1
        self.cursor.execute("UPDATE COMPANY_TABLE SET TIME_SPENT =? WHERE COMPANY_ID = ? AND KEYWORD_ID = ? AND EMPLOYEE_ID = ?",(time_avarage, COMPANY_ID_, KEYWORD_ID_, EMPLOYEE_ID_))
        self.cursor.execute("UPDATE COMPANY_TABLE SET TASK_COUNT = TASK_COUNT + 1 WHERE COMPANY_ID = ? AND KEYWORD_ID = ? AND EMPLOYEE_ID = ?",(COMPANY_ID_, KEYWORD_ID_, EMPLOYEE_ID_))
        self.conn.commit()
        
    def removeTime(self, COMPANY_ID_, KEYWORD_ID_, EMPLOYEE_ID_, TIME_SPENT_):
        self.cursor.execute("SELECT * FROM COMPANY_TABLE WHERE COMPANY_ID = ? AND KEYWORD_ID = ? AND EMPLOYEE_ID = ?",(COMPANY_ID_, KEYWORD_ID_, EMPLOYEE_ID_))
        data_tmp = self.cursor.fetchall()
        time_avarage = (data_tmp[0][5] * data_tmp[0][6] - TIME_SPENT_) / data_tmp[0][5] - 1
        self.cursor.execute("UPDATE COMPANY_TABLE SET TIME_SPENT =? WHERE COMPANY_ID = ? AND KEYWORD_ID = ? AND EMPLOYEE_ID = ?",(time_avarage, COMPANY_ID_, KEYWORD_ID_, EMPLOYEE_ID_))
        self.cursor.execute("UPDATE COMPANY_TABLE SET TASK_COUNT = TASK_COUNT - 1 WHERE COMPANY_ID = ? AND KEYWORD_ID = ? AND EMPLOYEE_ID = ?",(COMPANY_ID_, KEYWORD_ID_, EMPLOYEE_ID_))
        self.conn.commit()
        
