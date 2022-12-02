import sqlite3 as sl
from sqlite3 import Error

class TaskgiverEmployeeDB:
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
        self.cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='TASKGIVER_EMPLOYEE_TABLE' ''')
        
        if self.cursor.fetchone()[0] != 1:
            self.cursor.execute(''' CREATE TABLE TASKGIVER_EMPLOYEE_TABLE
                                    (
                                    COMPANY_ID INT NOT NULL,
                                    TASKGIVER_ID INT NOT NULL,
                                    EMPLOYEE_ID INT NOT NULL,
                                    TASK_COUNT INT NOT NULL) ''')
    def closeDB(self):
        self.conn.close()
        
    def update(self, COMPANY_ID_, TASKGIVER_ID_, EMPLOYEE_ID_):
        self.cursor.execute("SELECT 1 FROM TASKGIVER_EMPLOYEE_TABLE WHERE COMPANY_ID = ? AND TASKGIVER_ID = ? AND EMPLOYEE_ID = ?",(COMPANY_ID_, TASKGIVER_ID_, EMPLOYEE_ID_,))
        if (self.cursor.fetchone() == None):
            self.cursor.execute("INSERT INTO TASKGIVER_EMPLOYEE_TABLE (COMPANY_ID ,TASKGIVER_ID, EMPLOYEE_ID, TASK_COUNT) VALUES (?,?,?,?)",(COMPANY_ID_, TASKGIVER_ID_, EMPLOYEE_ID_, 1))
            self.conn.commit()
        else:
            self.cursor.execute("UPDATE TASKGIVER_EMPLOYEE_TABLE SET TASK_COUNT = TASK_COUNT + 1 WHERE COMPANY_ID = ? AND TASKGIVER_ID = ? AND EMPLOYEE_ID = ?",(COMPANY_ID_, TASKGIVER_ID_, EMPLOYEE_ID_,))
            self.conn.commit()
    
    def remove(self, COMPANY_ID_, TASKGIVER_ID_, EMPLOYEE_ID_):
        self.cursor.execute("SELECT * FROM TASKGIVER_EMPLOYEE_TABLE WHERE COMPANY_ID = ? AND TASKGIVER_ID = ? AND EMPLOYEE_ID = ?",(COMPANY_ID_, TASKGIVER_ID_, EMPLOYEE_ID_,))
        data_tmp = self.cursor.fetchall()
        if (data_tmp[0][3] == 1):
            self.cursor.execute("DELETE FROM TASKGIVER_EMPLOYEE_TABLE WHERE COMPANY_ID = ? AND TASKGIVER_ID = ? AND EMPLOYEE_ID = ?",(COMPANY_ID_, TASKGIVER_ID_, EMPLOYEE_ID_,))
            self.conn.commit()
        else:
            self.cursor.execute("UPDATE TASKGIVER_EMPLOYEE_TABLE SET TASK_COUNT = TASK_COUNT - 1 WHERE COMPANY_ID = ? AND TASKGIVER_ID = ? AND EMPLOYEE_ID = ?",(COMPANY_ID_, TASKGIVER_ID_, EMPLOYEE_ID_,))
            self.conn.commit()
            