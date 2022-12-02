import sqlite3 as sl
from sqlite3 import Error

class GeneralCounterDB:
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
        self.cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='GENERAL_COUNTER_TABLE' ''')
        
        if self.cursor.fetchone()[0] != 1:
            self.cursor.execute(''' CREATE TABLE GENERAL_COUNTER_TABLE
                                    (
                                    COMPANY_ID INT NOT NULL,
                                    KEYWORD_COUNT INT NOT NULL,
                                    TOTAL_USAGE_COUNT INT NOT NULL) ''')


    def update(self, call_option, COMPANY_ID_):
        self.cursor.execute('''SELECT 1 FROM GENERAL_COUNTER_TABLE WHERE COMPANY_ID = ?''',(COMPANY_ID_,))
        if self.cursor.fetchone() == None:
            self.cursor.execute('''INSERT INTO GENERAL_COUNTER_TABLE (COMPANY_ID, KEYWORD_COUNT, TOTAL_USAGE_COUNT) VALUES (?,?,?)''',(COMPANY_ID_,1,1))
            self.conn.commit()
            return

       
        #Options:
        #1. call_option = "Increase keyword count & total usage count"
        #2. call_option = "Increase total usage count"
        #3. call_option = "Decrease keyword count & total usage count"
        #4. call_option = "Decrease total usage count"
    
        if(call_option == 1):
            self.cursor.execute('''UPDATE GENERAL_COUNTER_TABLE SET TOTAL_USAGE_COUNT = TOTAL_USAGE_COUNT + 1 WHERE COMPANY_ID =?''',(COMPANY_ID_,))
            self.cursor.execute('''UPDATE GENERAL_COUNTER_TABLE SET KEYWORD_COUNT = KEYWORD_COUNT + 1 WHERE COMPANY_ID =?''',(COMPANY_ID_,))
            
        elif(call_option == 2):
            self.cursor.execute('''UPDATE GENERAL_COUNTER_TABLE SET TOTAL_USAGE_COUNT = TOTAL_USAGE_COUNT + 1 WHERE COMPANY_ID =?''',(COMPANY_ID_,))
        
        elif(call_option == 3):
            self.cursor.execute('''UPDATE GENERAL_COUNTER_TABLE SET TOTAL_USAGE_COUNT = TOTAL_USAGE_COUNT - 1 WHERE COMPANY_ID =?''',(COMPANY_ID_,))
            self.cursor.execute('''UPDATE GENERAL_COUNTER_TABLE SET KEYWORD_COUNT = KEYWORD_COUNT - 1 WHERE COMPANY_ID =?''',(COMPANY_ID_,))
            
        elif(call_option == 4):
            self.cursor.execute('''UPDATE GENERAL_COUNTER_TABLE SET TOTAL_USAGE_COUNT = TOTAL_USAGE_COUNT - 1 WHERE COMPANY_ID =?''',(COMPANY_ID_,))
        
        else:
            print("Invalid call option")
            
        self.conn.commit()
    
    def closeDB(self):
        self.conn.close()
        
def main():
    pass

if __name__ == "__main__":
    main()
