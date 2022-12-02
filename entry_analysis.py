import sqlite3 as sl
from sqlite3 import Error

from dbCodes.extract_keyword import KeywordExtractor

class TaskData:
    def __init__(self):
        self.company_id = 0
        self.task_code = 0
        self.task_giver = None
        self.task_reciever = None
        self.entry_title = None
        self.entry_description = None

class EntryAnalysis:
    def __init__(self, task_data, dbName_="employee_analysis"):
        self.conn = None
        self.cursor = None
        self.dbName = dbName_ + ".db"
        
        self.task_data = task_data
        self.title_list = []
        self.description_list = []
        self.fillKeywordList()
        
        employee_list = []
        max_id = self.getEmployeeNumber()
        for i in range(max_id):
            employee_list.append(0)
        
    def databaseConnector(self):
        try:
            self.conn = sl.connect(self.dbName)
            self.cursor = self.conn.cursor()
        except Error as e:
            print(e)
    
    def closeDB(self):
        self.conn.close()
     
    def getEmployeeNumber(self):
        self.databaseConnector()
        self.cursor.execute('''SELECT max(ID) FROM EMPLOYEE_ID_TABLE''')
        max_id = self.cursor.fetchone()[0]    
        self.closeDB()
        return max_id
    def fillKeywordList(self):
        extractor = KeywordExtractor(self.task_data.entry_title)
        self.title_list = extractor.extractKeywordList()
        
        extractor = KeywordExtractor(self.task_data.entry_description)
        self.description_list = extractor.extractKeywordList()
        
    def employeeFactor(self):
        
        matching_title_count = 0
        
        for title in self.title_list:
            self.cursor.execute('''SELECT * FROM KEYWORD_RECORDER_TABLE WHERE COMPANY_ID = ? AND KEYWORD = ?''',(self.task_data.company_id ,title))
            keyword_record = self.cursor.fetchone()
            if(keyword_record == None):
                continue
            keyword_id = keyword_record[1]
            self.cursor.execute('''SELECT * FROM EMPLOYEE_FACTOR_TABLE WHERE COMPANY_ID = ? AND KEYWORD_ID = ?''',(self.task_data.company_id , keyword_id))
            employee_factor_record = self.cursor.fetchall()    
            print(employee_factor_record)    
                
        
        
    

def main():
    task_data = TaskData()
    
    task_data.company_id = 3
    task_data.task_code = 45
    task_data.task_giver = 1
    task_data.task_reciever = 6
    task_data.entry_title = "İHA tabanlı savunma sistemi"
    task_data.entry_description = "ARM tabanlı mimari ile İHA savunma sisteminin yerleştirilmesi"
    
    analysis_object = EntryAnalysis(task_data, dbName_ = "employee_analysis")
    analysis_object.databaseConnector()
    analysis_object.employeeFactor()
    
        
if __name__ == "__main__":
    main()
    