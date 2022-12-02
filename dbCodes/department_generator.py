from department_identifier import DepartmentDB
from department_classifier import DepartmentClassifierDB


department_list = ["Yonetim",       # 1
                   "Hissedar",      # 2  
                   "Muhasebe",      # 3
                   "Arge",          # 4
                   "Bilgisayar",    # 5
                   "Simülasyon",    # 6
                   "Arayuz",        # 7
                   "Elektronik",    # 8
                   "Sensor",        # 9
                   "Gomulu",        # 10
                   "Mekanik",       # 11
                   "Tasarım",       # 12
                   "Analiz"]        # 13

department_descent_list = [[1,2,3],     # Yonetim
                           [2],         # Hissedar
                           [3],         # Muhasebe
                           [4,5,8,11],  # Arge
                           [5,6,7],     # Bilgisayar
                           [6],         # Simülasyon
                           [7],         # Arayuz
                           [8,9,10],    # Elektronik
                           [9],         # Sensor
                           [10],        # Gomulu
                           [11,12,13],  # Mekanik
                           [12],        # Tasarım
                           [13]]        # Analiz

COMPANY_ID = 3

def department_generator():
    global COMPANY_ID
    global department_list
    global department_descent_list

    department_db = DepartmentDB()
    department_classifier_db = DepartmentClassifierDB()

    for i in range(len(department_list)):
        department_db.databaseConnector()
        department_db.update(COMPANY_ID, department_list[i])
        department_db.closeDB()

        for j in department_descent_list[i]:
            department_classifier_db.databaseConnector()
            department_classifier_db.update(COMPANY_ID ,i+1, j)
            department_classifier_db.closeDB()
            
department_generator()