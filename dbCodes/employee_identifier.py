import sqlite3 as sl
from sqlite3 import Error

class EmployeeIdentifierDB:
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
        self.cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='EMPLOYEE_ID_TABLE' ''')
        
        if self.cursor.fetchone()[0] != 1:
            self.cursor.execute(''' CREATE TABLE EMPLOYEE_ID_TABLE
                                    (
                                    COMPANY_ID INT NOT NULL,
                                    ID INT PRIMARY KEY NOT NULL,
                                    EMPLOYEE TEXT NOT NULL,
                                    DEPARTMENT_ID NOT NULL,
                                    SALARY REAL NOT NULL) ''')
     
    def closeDB(self):
        self.conn.close()
            
    def update(self, COMPANY_ID_, EMPLOYEE_, DEPARTMENT_ID_, SALARY_):
        self.cursor.execute("SELECT 1 FROM EMPLOYEE_ID_TABLE WHERE COMPANY_ID = ? AND EMPLOYEE = ?",(COMPANY_ID_, EMPLOYEE_,))
        if (self.cursor.fetchone() == None):
            self.cursor.execute('SELECT max(ID) FROM EMPLOYEE_ID_TABLE')
            data_tmp = self.cursor.fetchone()
            if (data_tmp[0]):
                new_id = data_tmp[0] + 1
            else:
                new_id = 1
            self.cursor.execute("INSERT INTO EMPLOYEE_ID_TABLE (COMPANY_ID ,ID, EMPLOYEE, DEPARTMENT_ID, SALARY) VALUES (?,?,?,?,?)",(COMPANY_ID_, new_id, EMPLOYEE_, DEPARTMENT_ID_, SALARY_))
        self.conn.commit()
        
    def remove(self, COMPANY_ID_, EMPLOYEE_):
        self.cursor.execute("DELETE FROM EMPLOYEE_ID_TABLE WHERE COMPANY_ID = ? AND EMPLOYEE = ?",(COMPANY_ID_, EMPLOYEE_,))
        self.conn.commit()
        
def main():
    pass

if __name__ == "__main__":
    main()
    
    