import sqlite3 as sl
from sqlite3 import Error

class DepartmentDB:
    def __init__(self, dbName_="employee_analysis"):
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
        self.cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='DEPARTMENT_ID_TABLE' ''')
        
        if self.cursor.fetchone()[0] != 1:
            self.cursor.execute(''' CREATE TABLE DEPARTMENT_ID_TABLE
                                    (
                                    COMPANY_ID INT NOT NULL,
                                    ID INT PRIMARY KEY NOT NULL,
                                    DEPARTMENT TEXT NOT NULL) ''')
    def update(self, COMPANY_ID_, DEPARTMENT_):
        self.cursor.execute("SELECT 1 FROM DEPARTMENT_ID_TABLE WHERE COMPANY_ID = ? AND DEPARTMENT = ?",(COMPANY_ID_, DEPARTMENT_,))
        if (self.cursor.fetchone() == None):
            self.cursor.execute('SELECT max(ID) FROM DEPARTMENT_ID_TABLE')
            data_tmp = self.cursor.fetchone()
            if (data_tmp[0]):
                new_id = data_tmp[0] + 1
            else:
                new_id = 1
            self.cursor.execute("INSERT INTO DEPARTMENT_ID_TABLE (COMPANY_ID ,ID, DEPARTMENT) VALUES (?,?,?)",(COMPANY_ID_, new_id, DEPARTMENT_))
        self.conn.commit()
    
    def remove(self, COMPANY_ID_, DEPARTMENT_):
        self.cursor.execute("DELETE FROM DEPARTMENT_ID_TABLE WHERE COMPANY_ID = ? AND DEPARTMENT = ?",(COMPANY_ID_, DEPARTMENT_,))
        self.conn.commit()
        
def main():
    pass

if __name__ == "__main__":
    main()
