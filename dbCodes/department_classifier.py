import sqlite3 as sl
from sqlite3 import Error

class DepartmentClassifierDB:
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
        self.cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='DEPARTMENT_CLASSIFIER_TABLE' ''')
        
        if self.cursor.fetchone()[0] != 1:
            self.cursor.execute(''' CREATE TABLE DEPARTMENT_CLASSIFIER_TABLE
                                    (
                                    COMPANY_ID INT NOT NULL,
                                    ANCESTOR_ID INT NOT NULL,
                                    DESCENDANT_ID INT NOT NULL) ''')
    def update(self, COMPANY_ID_, ANCESTOR_ID_, DESCENDANT_ID_):
        self.cursor.execute("SELECT 1 FROM DEPARTMENT_CLASSIFIER_TABLE WHERE COMPANY_ID = ? AND ANCESTOR_ID = ? AND DESCENDANT_ID = ?",(COMPANY_ID_, ANCESTOR_ID_, DESCENDANT_ID_,))
        if (self.cursor.fetchone() == None):
            self.cursor.execute("INSERT INTO DEPARTMENT_CLASSIFIER_TABLE (COMPANY_ID ,ANCESTOR_ID, DESCENDANT_ID) VALUES (?,?,?)",(COMPANY_ID_, ANCESTOR_ID_, DESCENDANT_ID_))
        self.conn.commit()
    
    def remove(self, COMPANY_ID_, ANCESTOR_ID_, DESCENDANT_ID_):
        self.cursor.execute("DELETE FROM DEPARTMENT_CLASSIFIER_TABLE WHERE COMPANY_ID = ? AND ANCESTOR_ID = ? AND DESCENDANT_ID = ?",(COMPANY_ID_, ANCESTOR_ID_, DESCENDANT_ID_,))
        self.conn.commit()
    
def main():
    pass

if __name__ == "__main__":
    main()
    