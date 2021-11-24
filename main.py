from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window #might not be needed for app on android
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import OneLineListItem
from kivymd.uix.snackbar import Snackbar
import mysql.connector
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color
from kivymd.toast import toast

from kivy.properties import ObjectProperty  #for working with ids
from kivy.utils import platform
import os
from datetime import datetime, date as date_only

if platform ==  'android':
    from android.storage import primary_external_storage_path
    dir = primary_external_storage_path()
    document_dir_path = os.path.join(dir, 'Documents')
#----------for nfc------------
##from derver import DefaultSnepServer as Dss
##import nfc



class LoginScreen(MDScreen):
    
    def menu_action(self):
        #show option for close and exit
        Snackbar(text="close and exit", font_size='25sp').open()
        
    def login_button_action(self):   
        in_class = ObjectProperty(None)
        in_class1 = ObjectProperty(None)
        lect_id_input = self.in_class.text
        lect_passwrd_input = self.in_class1.text  
        if lect_id_input=='' or lect_passwrd_input=='':
            toast('required field cannot be left empty')
            self.manager.current = 'Login'
        else:
            try:
               #establish connection to db
               conn = mysql.connector.connect(user='<user>',password='<password>', host='<host>', database='<db>')
               #create a cursor object using the cursor() method
               cursor = conn.cursor()

               #retrieving data from table
               cursor.execute("SELECT * from lecturer_tbl")

               result = cursor.fetchall();
               print("Connected to DB::\n") #verify connection to DB was successful

               #closing the conection
               conn.close()

               #validate lecturer credentials

               for i in range(len(result)):
                   if lect_id_input == result[i][0] and lect_passwrd_input == result[i][1]:
                       toast('ACCESS GRANTED\nwelcome {}'.format(result[i][2]))
                       global instructor
                       instructor=result[i][2]
                       self.manager.current = 'Home'#'CourseSelet'
                       break
                   else:
                       if i == len(result)-1:  #program done scanning
                           toast('ACCESS DENIED\nUsername or password incorrect')
                       self.manager.current = 'Login'
            except:
               #when noconnection established
               toast("problems connecting to server, check internet connection...")
               self.manager.current = 'Login'

#---------------------------------------------           
#create object of CourseSelect to access the attributes for making the button
    #for courses in lecturer define button and fill text be the code

#might be an improvement
class CourseSelectScreen(MDScreen):
    #define functions of the buttons in the screen
    pass
#---------------------------------------------

class HomeScreen(MDScreen):
    #menu 
    def menu_action(self):  #must show option for logout
        Snackbar(text="Logout", font_size='25sp').open()

    in_class2 = ObjectProperty(None)

##    def startup(llc):
##        global my_snep_server
##        my_snep_server = Dss(llc)
##        return llc
##    
##    def connected(llc):
##        my_snep_server.start()
##        return True
        
    def beam_button_action(self):
        #----nfc sect.
##        my_snep_server = None  
##    
##        clf = nfc.ContactlessFrontend("udp")
##        clf.connect(llcp={'on-startup': self.startup(), 'on-connect': self.connected()})
        global course_code
        course_code = self.in_class2.text.upper()
        if course_code != '':
            #check if course is in the system
            try:
                conn = mysql.connector.connect(user='<user>',password='<password>', host='<host>', database='<db>')
                print("connected!")
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM course_tbl")
                courses = cursor.fetchall()
                conn.close()
                for i in range(len(courses)):
                    if course_code.upper() == str(courses[i][0]) and courses[i][2]==instructor:
                        self.manager.current = 'Attendance'
                        break
                    elif i == len(courses)-1:
                        toast('Check if YOUR code was entered, or\nContact system admin::course not registered')
                        self.manager.current = 'Home'
            except:
                toast('CHECK INTERNET CONNECTION...')
                self.manager.current = 'Home'              
        else:
            self.manager.current = 'Home'
            toast('Course code required')
        #update attendance db

    def report_button_action(self):
        global course_code
        course_code = self.in_class2.text.upper()
        if course_code != '':
            #check if course is in the system
            try:
                conn = mysql.connector.connect(user='<user>',password='<password>', host='<host>', database='<db>')
                print("connected!")
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM course_tbl")
                courses = cursor.fetchall()
                conn.close()
                for i in range(len(courses)):
                    if course_code.upper() == str(courses[i][0]) and courses[i][2]==instructor:
                        self.manager.current = 'ReportHome'
                        break
                    elif i == len(courses)-1:
                        toast('Check if YOUR code was entered, or\nContact system admin::course not registered')
                        self.manager.current = 'Home'
            except:
                toast('CHECK INTERNET CONNECTION...')
                self.manager.current = 'Home' 
            
        else:
            self.manager.current = 'Home'
            toast('Course code required')
        # self.manager.current = 'ReportHome'

class AttendanceScreen(MDScreen):
    #menu and back arrow
    def menu_action(self):  #menu 

        self.manager.current = 'Home'

    def backbtn(self): 

        self.manager.current = 'Home'
    #--------
    
    #define functions to receive data
    #upload it in relevant dbs
    #define function to display relevant msg to student
    
            
class ReportHomeScreen(MDScreen):
    #menu and back arrow
    def menu_action(self):  #menu 

        self.manager.current = 'Home'

    def backbtn(self): 

        self.manager.current = 'Home'
    #--------
    
    def classAtt_button_action(self):
        self.manager.current = 'ClassAttendance'

    def covContacts_button_action(self):
        self.manager.current = 'CovidContacts'

class CovidContactsScreen(MDScreen):
    #menu and back arrow
    def menu_action(self):  #menu 
        self.manager.current = 'Home'

    def backbtn(self): 
        self.manager.current = 'ReportHome'
    
    def go_button_action(self):
    #start here!!!
        in_class3 = ObjectProperty(None)
        in_class4 = ObjectProperty(None)
        cov_date = self.in_class3.text
        stu_id = self.in_class4.text

        if cov_date=='' or stu_id=='':
            toast('please fill in all the information')
            self.manager.current = 'CovidContacts'
        else:
            # try:
            conn = mysql.connector.connect(user='<user>',password='<password>', host='<host>', database='<db>')
            cursor = conn.cursor()

            #get name and surname of the student whose contacts we want
            sql = "SELECT ST_NAME,ST_SURNAME FROM student_tbl WHERE ST_ID=%s"
            data = (stu_id,)
            cursor.execute(sql,data)
            this_student = cursor.fetchall()
            print(this_student)
            f = open(os.path.join(document_dir_path,str(stu_id)+'-contacts'+str(date_only.today())+'.csv'),'w') 
            # f = open(str(stu_id)+'-contacts.csv','w')

            #get student ids for other students on that day, that went to same course(s) as this student
            #get courses this student went to 
            sql1 = "SELECT COURSE_CODE FROM attendance_tbl WHERE STUDENT_ID=%s AND DATE='"+cov_date+"'"
            cursor.execute(sql1,data)
            this_courses = cursor.fetchall()
            print(this_courses)
            f.write('COVID CONTACTS OF:,'+str(this_student[0][0])+' '+str(this_student[0][1])+'\nDATE:,'+cov_date+'\n\n')

            for course in this_courses:
                print('list of students in {} on {} is: '.format(course[0],cov_date))
                f.write('LIST OF CONTACTS IN:, {} CLASS\n\n'.format(course[0]))
                f.write('ID,SURNAME,NAME,PHONE NUMBER\n')
                sql2 = "SELECT STUDENT_ID FROM attendance_tbl WHERE DATE=%s AND COURSE_CODE=%s"
                data2 = (cov_date,course[0],)
                cursor.execute(sql2,data2)
                st = cursor.fetchall() #student ids 
                for s in st:
                    print('ID is: ',str(s),end=" ")
                    #find the name and surname of the student with this id
                    sql3 = "SELECT ST_NAME,ST_SURNAME,PHONE_NUM FROM student_tbl WHERE ST_ID=%s"
                    data3 = (s[0],)
                    cursor.execute(sql3,data3)
                    details = cursor.fetchall()
                    print(details) #display student name and surname
                    if s[0]==stu_id: #exclude this student from the list
                        continue
                    try: 
                        f.write(str(s[0])+','+details[0][1]+','+details[0][0]+','+str(details[0][2])+'\n')
                    except:
                        toast('The list is empty.')   
            f.close()
            #close db connection
            conn.close()

            # access DB search for the date and bring back data
            #if date in db is same as entered date
            #fetch where course and date match with the courses attended
            #by the student on that day
            # data to be output in a file (*.csv or *.txt) or as a list
            toast('Report saved to covid_contacts'+str(date_only.today())+'.csv')
            # except:
            #     toast('solve possible problems:\nCheck connection and format of information\nthen try again...')
            #     self.manager.current = 'CovidContacts'
        
class ClassAttScreen(MDScreen):
    #menu and back arrow
    def menu_action(self):  #menu 

        self.manager.current = 'Home'

    def backbtn(self): 

        self.manager.current = 'ReportHome'
    #--------
    
    def classList_button_action(self):
        # file with details on the class attendacne
        # conn to db-----------
        try:

            conn = mysql.connector.connect(user='<user>',password='<password>', host='<host>', database='<db>')
            print("connected:....")

            #create a cursor object using the cursor() method
            cursor = conn.cursor()
            
            # fetch info and store in respective memory
            cursor.execute("SELECT * FROM course_tbl")
            courses = cursor.fetchall() # holding the course code, name and instructor
            
            sql = "SELECT STUDENT_ID,DATE,COURSE_CODE FROM attendance_tbl WHERE COURSE_CODE= '"+course_code+"'"
            cursor.execute(sql)
            attend = cursor.fetchall() # holding the attendance info to use for class list
            
            print(attend)

            cursor.execute("SELECT * FROM student_tbl")
            students = cursor.fetchall()      

            dates_head=[] #hold dates headers(list of tuples)
            dates = []  #to hold actual date for checking if student was available on that day
            for j in range(len(attend)):
                #for one entry in DB 
                dat = attend[j][1]
                dates.append(dat)
                if j == 0:
                    dates_head.append(str(attend[j][1]))
                if j>0 and str(attend[j][1]) != dates_head[-1]:
                    dates_head.append(str(attend[j][1]))

            print(dates_head) 
            
            # ---------write into the text file-------
            try:
                for i in range(len(courses)):
                    if course_code.upper() == str(courses[i][0]):
                        #write header in the classlist defining the course details
                        print(courses[i][0]+'\t'+courses[i][1]+'\t'+courses[i][2])
                        f = open(os.path.join(document_dir_path,'classlist'+str(date_only.today())+'.csv'),'w') 
                        # f = open('classlist13.csv','w')
                        f.write('ATTENDANCE SHEET\nCOURSE CODE:\t'+courses[i][0]+'\nCOURSE NAME:\t'+courses[i][1]+'\nINSTRUCTOR:\t'+courses[i][2]+'\n\n')
                        break
                    
                    elif i==len(courses):
                        toast("no match for course")
                
                #-----------print in table format-----
                print('ID\tSURNAME\t        NAME\t\t'+str(attend[0][1]),end =" ")
                f.write('ID,SURNAME,NAME')
                
                for y in range(len(dates_head)):
                    f.write(','+str(dates_head[y]))
                f.write('\n')

                #start body--------------
                status = ''
                msg2 = ' '
                shortlist = [] #holds 'scanned' or 'processed' student Ids
                orlist =[] #holds ids from db
                for i in range(len(attend)):
                    #list 1 (list of all ids)
                    orlist=[attend[i][0]] 
                    #list 2 is shortlist

                    check = any(item in shortlist for item in orlist)

                    if check is True:#element found action
                        continue 

                    else:#no element found
                        shortlist.append(attend[i][0])

                    msg0 = str(attend[i][0])
                    #print info from student table
                    for j in range(len(students)):
                        if attend[i][0] == students[j][0]:
                            msg1 = students[j][2]+','+students[j][1]
                            break
                               
                    #after checking if id has been scanned before
                    print('attend[i][0]: ',attend[i][0])
                    stid = (attend[i][0],)
                    sql2 ="SELECT STUDENT_ID,DATE,COURSE_CODE FROM attendance_tbl WHERE STUDENT_ID =%s AND COURSE_CODE='"+course_code+"'"
                    cursor.execute(sql2,stid)
                    
                    dates_present = cursor.fetchall()

                    print('dates_present: '+str(dates_present))

                    for s in range(len(dates_head)):
                        res = 0 #no match in dates
                        print('Length of dates_present: ',len(dates_present))
                        for t in range(len(dates_present)):
                            if dates_head[s] == str(dates_present[t][1]):
                                res =1 #true for match
                        if res == 1:
                            status += ',X'
                        else:
                            status += ',-'
                    msg2 += status
                    print('shortlist: ',shortlist)
                    print(msg0+msg1+msg2)
                    f.write(msg0+','+msg1+msg2+'\n')
                    
                    #reset memories
                    status = ''
                    msg2 = ' '
                self.manager.current = 'Home'
                
                #close file
                f.close()
                # close conn
                conn.close()

                toast('class list saved to classlist'+str(date_only.today())+'.csv')
            except:
                toast('File already exists in destination folder')
                self.manager.current = 'ClassAttendance'
        except:
            toast('POSSIBLE CONNECTION PROBLEMS\nTRY::checking your connection...')
            self.manager.current = 'Home'        
        #------done writing-------

    def individualList_button_action(self):
        self.manager.current = 'IndividualRep'

class IndividualRepScreen(MDScreen):
    #menu and back arrow
    def menu_action(self):  #menu 

        self.manager.current = 'Home'

    def backbtn(self): 

        self.manager.current = 'ClassAttendance'
    #--------
    
    def vwrpt_button_action(self):
    #Then come here!!!
        #brings screen with detailed report in individual
        #have option for exporting report into a file
        #file may be used by instructor in the student file
        toast("snackbar with information displayed\nwith two buttons\nclose and save")

class MainApp(MDApp):
    # Window.size = (400,600)
    def close_action(self):
        MainApp().stop()
        
    def build(self):
        self.title = "Lecturer App"
        sm = ScreenManager();
        sm.add_widget(LoginScreen(name='Login'))
        sm.add_widget(HomeScreen(name='Home'))
        sm.add_widget(AttendanceScreen(name='Attendance'))
        sm.add_widget(ReportHomeScreen(name='ReportHome'))
        sm.add_widget(CovidContactsScreen(name='CovidContacts'))
        sm.add_widget(ClassAttScreen(name='ClassAttendance'))
        sm.add_widget(IndividualRepScreen(name='IndividualRep'))        

        return sm


if __name__ == '__main__':
    MainApp().run()
