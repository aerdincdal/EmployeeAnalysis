import sys
from task_entry import TaskEntryDB
from employee_identifier import EmployeeIdentifierDB
from department_generator import department_generator

class FileReader:
    def __init__(self) -> None:
        self.employee_db = EmployeeIdentifierDB()
        self.task_db = TaskEntryDB()
        self._inputFile = None

    # This method opens the file including ogrenci info
    # @params dosyaYolu for file path
    def open(self, dosyaYolu):
        self._inputFile = open(dosyaYolu, 'r', encoding="utf8")

    def close(self):
        self._inputFile.close()
        self._inputFile = None

    # extract only one record every step
    def fetchEmployee(self):
        line = self._inputFile.readline()
        if line == "":
            return None
        employee = EmployeeData()
        employee.company_id = int(line.split('=')[-1].rstrip())
        employee.employee = self._inputFile.readline().split('=')[-1].rstrip().split('"')[1] + " " + self._inputFile.readline().split('=')[-1].rstrip().split('"')[1]
        employee.employee_department = int(self._inputFile.readline().split('=')[-1].rstrip())
        employee.employee_salary = int(self._inputFile.readline().split('=')[-1].rstrip())

        self.employee_db.databaseConnector()
        self.employee_db.update(employee.company_id, employee.employee, employee.employee_department, employee.employee_salary)
        self.employee_db.closeDB()
                
        return employee

    def fetchAllEmployees(self):
        record = self.fetchEmployee()
        self._inputFile.readline()
        while record != None:
            record = self.fetchEmployee()
            self._inputFile.readline()
            

    def fetchTask(self):
        line = self._inputFile.readline()
        if line == "":
            return None
        
        task = TaskData()
        task.company_id = int(line.split('=')[-1].rstrip())
        task.task_code = int(self._inputFile.readline().split('=')[-1].rstrip())
        task.task_giver = int(self._inputFile.readline().split('=')[-1].rstrip())
        task.task_reciever = int(self._inputFile.readline().split('=')[-1].rstrip())
        task.entry_title = self._inputFile.readline().split('=')[-1].rstrip().split('"')[1]
        task.entry_description = self._inputFile.readline().split('=')[-1].rstrip().split('"')[1]

        self.task_db.databaseConnector()
        self.task_db.update(task.company_id, task.task_code, task.task_giver, task.task_reciever, task.entry_title, task.entry_description)
        self.task_db.closeDB()

        return task

    def fetchAllTasks(self):
        record = self.fetchTask()
        self._inputFile.readline()
        while record != None:
            record = self.fetchTask()
            self._inputFile.readline()

class TaskData:
    def __init__(self):
        self.company_id = 0
        self.task_code = 0
        self.task_giver = None
        self.task_reciever = None
        self.entry_title = None
        self.entry_description = None
        
class EmployeeData:
    def __init__(self):
        self.company_id = 0
        self.employee = None
        self.employee_department = None
        self.employee_salary = 0
        
def main():
        
    department_generator()        

    file_reader = FileReader()
    file_reader.open("dbCodes/employee_list.txt")
    file_reader.fetchAllEmployees()
    file_reader.close()

    file_reader = FileReader()
    file_reader.open("dbCodes/task_list.txt")
    file_reader.fetchAllTasks()
    file_reader.close()
    
if __name__ == "__main__":
    main()  