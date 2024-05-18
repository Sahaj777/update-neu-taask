import os
import stat
import datetime
import sqlite3



class gen_folder:
    def __init__(self, user, sel):
        self.user = user
        self.path3_1 = "None"
        self.sel = sel
        project = None
        
        # Generate the path from the first folder. This will be processed further at the bottom (folder creation)
        dir_name = datetime.datetime.now()
        dir_name2 = dir_name.strftime("%d%m%y_")
        dir_name3 = dir_name2 + str(user)
        
        
        # Check which project the user has chosen? Based on the HTML select tag. Read out the database and send the information
        # back to the object in the /upload route. (In which folder should the file be saved?)
        con =sqlite3.connect('/home/sahaj/Downloads/Neu/datenbank/user_data.db')
        c = con.cursor()
        
        if self.sel == "project1":
            c.execute("SELECT project1 FROM users WHERE name =?", [self.user])
            result = c.fetchall()
            
            for res in result:
                project = res[0]
                   
        if self.sel == "project2":
            c.execute("SELECT project2 FROM users WHERE name =?", [self.user])
            result = c.fetchall()
            
            for res in result:
                project = res[0]
                
        if self.sel == "project3":
            c.execute("SELECT project3 FROM users WHERE name =?", [self.user])
            result = c.fetchall()
            
            for res in result:
                project = res[0]
        
        if self.sel == "project4":
            c.execute("SELECT project4 FROM users WHERE name =?", [self.user])
            result = c.fetchall()
            
            for res in result:
                project = res[0]
                
        if self.sel == "project5":
            c.execute("SELECT project5 FROM users WHERE name =?", [self.user])
            result = c.fetchall()
            
            for res in result:
                project = res[0]
                
        if self.sel == None:
            project = "-"       
            
        c.close()   
  
        # Create two folders, if are not already exist (uploads/user/project name)
        self.path3 = "/home/sahaj/Downloads/Neu/datenbank/" + dir_name3 + "/"
        mkdirs = os.makedirs(self.path3, exist_ok=True)
        
        # Second folder with information from the choosen project
        self.path3_1 = self.path3 + str(project)
        mkdirs = os.makedirs(self.path3_1, exist_ok=True)
        
        # Permission
        path4 = self.path3_1
        path4_1 = "/home/sahaj/Downloads/Neu/uploads"
        path4_check = os.path.isdir(path4)
        print(path4_check)
        if path4_check == True:
            
            permission = 0o777
            os.chmod(str(path4), permission)
        
        else:      
            permission = 0o777
            os.chmod(str(path4_1), permission)
            
            permission = 0o777
            os.chmod(str(path4), permission)
            
            
#gen_folder("1", "project1")      
       