import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import StringProperty,OptionProperty,ListProperty,ObjectProperty #while using db conn
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import OneLineListItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.snackbar import Snackbar
from kivymd.toast import toast
from kivy.graphics import Color

#for connecting to database (must be commented out)
import mysql.connector
from datetime import datetime, date
#---------------------------

#remove comments for nfc
##import nfc
##import nfc.snep
##import threading

Builder.load_string("""
<homeScreen>:
    orientation: 'vertical'
    in_class: studentid
    in_classa: coursecode
    MDToolbar:
        pos_hint: {'top':1.0}
        title: 'Home'
        right_action_items: [["close",lambda x: app.menu_callback()]]
    MDLabel:
        text: "WELCOME!! Please Enter: "
        theme_text_color: "Custom"
        text_color: 0, 0, 1, 1
        halign: "center"
        pos_hint: {'center_x': .5, 'center_y': .8}
  
    MDTextField:
        size_hint_x: .5
        hint_text: "Student_ID"
        id: studentid
        pos_hint: {'center_x': .5, 'center_y': .7}
    MDTextField:
        size_hint_x: .5
        hint_text: "Course Code"
        helper_text: "e.g EEE555"
        helper_text_mode: "on_focus"
        id: coursecode
        pos_hint: {'center_x': .5, 'center_y': .6}
    MDFillRoundFlatButton:
        text: 'Attendance'
        on_release: root.att_button_action()
        pos_hint: {'center_x': .5, 'center_y': .4}
    MDFillRoundFlatButton:
        text: 'Register'
        on_release: root.register_button_action()
        pos_hint: {'center_x': .5, 'center_y': .3}

<registerScreen>:
    orientation: 'vertical'
    in_class2: studentname
    in_class3: studentsurname
    MDToolbar:
        pos_hint: {'top':1.0}
        title: 'Register'
        left_action_items: [["arrow-left",lambda x: root.backbtn()]]
        right_action_items: [["close",lambda x: app.menu_callback()]]
    MDLabel:
        text: 'Enter Your Registration Info...'
        theme_text_color: "Custom"
        text_color: 0, 0, 1, 1
        halign: 'center'
        pos_hint: {'center_x': .5, 'center_y': .8}
    MDLabel:

        text: 'To prevent issues: Make sure you have entered the correct student ID,name and surname'

        font_style: 'Body2'

        theme_text_color: 'Secondary'

        halign: 'center'

        pos_hint: {'center_x': .5, 'center_y': .75}
    MDTextField:
        hint_text: "Enter Name"
        id: studentname
        size_hint_x: .9
        pos_hint:{'center_x': .5, 'center_y': .6}
    MDTextField:
        hint_text: "Enter Surname"
        id: studentsurname
        size_hint_x: .9
        pos_hint:{'center_x': .5, 'center_y': .5}
    MDFillRoundFlatButton:
        text: 'Done'
        on_release: root.regDone_button_action()
        pos_hint:{'center_x': .5, 'center_y': .3}
                
<attendanceScreen>:
    orientation: 'vertical'
    MDToolbar:
        pos_hint: {'top':1.0}
        title: 'Attendance'
        left_action_items: [["arrow-left",lambda x: root.backbtn()]]
        right_action_items: [["close",lambda x: app.menu_callback()]]
    MDLabel:
        text: 'How do you feel today?...'
        theme_text_color: "Custom"
        text_color: 0, 0, 1, 1
        halign: 'center'
        pos_hint: {'center_x': .5, 'center_y': .85}
        font_style: 'H5'
    MDLabel:
        text: 'check boxes if you feel any of the following: '
        font_style: 'Body1'
        theme_text_color: 'Secondary'
        halign: 'center'
        pos_hint: {'center_x': .5, 'center_y': .8}
    MDList:
        pos_hint: {'top':0.76}
        size_hint: (1,1)
        OneLineListItem:
            text: 'Fever'
            MDCheckbox:
                size: '48dp', '48dp'
                pos_hint: {'center_x': .9,'center_y': .5}
                on_active: root.fever_checkbox_active()
        OneLineListItem:
            text: 'Breathing difficulty'
            MDCheckbox:
                size: '48dp', '48dp'
                pos_hint: {'center_x': .9,'center_y': .5}
                on_active: root.brdiff_checkbox_active()
        OneLineListItem:
            text: 'Chest pains'
            MDCheckbox:
                size: '48dp', '48dp'
                pos_hint: {'center_x': .9,'center_y': .5}
                on_active: root.chpns_checkbox_active()
        OneLineListItem:
            text: 'Headache'
            MDCheckbox:
                size: '48dp', '48dp'
                pos_hint: {'center_x': .9,'center_y': .5}
                on_active: root.headache_checkbox_active()
        OneLineListItem:
            text: 'Loss of appetite'
            MDCheckbox:
                size: '48dp', '48dp'
                pos_hint: {'center_x': .9,'center_y': .5}
                on_active: root.lossApp_checkbox_active()
        OneLineListItem:
            text: 'Anxiety'
            MDCheckbox:
                size: '48dp', '48dp'
                pos_hint: {'center_x': .9,'center_y': .5}
                on_active: root.anxiety_checkbox_active()
    MDFillRoundFlatButton:
        text: 'Done'
        on_release: root.attDone_button_action()
        pos_hint: {'center_x':.5,'center_y': .08}

<startBeamScreen>:
    orientation: 'vertical'
    MDToolbar:
        pos_hint: {'top':1.0}
        title: ''
        left_action_items: [["arrow-left",lambda x: root.backbtn()]]
        right_action_items: [["close",lambda x: app.menu_callback()]]
    MDLabel:
        text: "Touch device with target to finish"
        halign: "center"

""")
class HomeScreen(MDScreen):
    def menu_action(self):
        self.snackbar = Snackbar(text=" ",button_text="Close&Exit",font_size='10sp',duration=5,button_callback=MDApp().stop())
        self.snackbar.open()
        
    #use student id and code from entered value
    in_class = ObjectProperty(None)
    in_classa = ObjectProperty(None)
        
    def att_button_action(self):
        global bflag #to be used in back button
        bflag = 0

        #to be able to use course code when creating NDEF message
        global course_code_input
        course_code_input = self.in_classa.text.upper()
        #str(course_code_input).upper() #cater for small letters
        
        #ensuring st id is not empty **also add other restrictions**
        global st_id_input
        st_id_input = self.in_class.text
        if st_id_input == '':  #if st id field is empty
            self.snackbar = Snackbar(text="Student ID cannot be empty!!", font_size='15sp')
            self.snackbar.open()
            self.manager.current = 'Home'
        else:
            self.manager.current = 'Attendance'

    def register_button_action(self):
        global bflag #to be used in back button
        bflag = 1

        global course_code_input
        course_code_input = self.in_classa.text
        #str(course_code_input).upper() #cater for small letters
         
        global st_id_input
        st_id_input = self.in_class.text
        if st_id_input != '':
            self.manager.current = 'Register'
        else:
            self.snackbar = Snackbar(text="Student ID cannot be empty!!", font_size='15sp')
            self.snackbar.open()
            self.manager.current = 'Home'


class RegisterScreen(MDScreen):   
    def menu_action(self):  #menu 
        self.snackbar = Snackbar(text="Close & Exit", font_size='25sp')
        self.snackbar.open()
        
    in_class2 = ObjectProperty(None)
    in_class3 = ObjectProperty(None)
    
    def regDone_button_action(self):
        global bbflag
        bbflag = 1

        #name and surname to be used when adding student to database
        global name_input
        name_input = self.in_class2.text,upper()

        global surname_input
        surname_input = self.in_class3.text.upper()
        
        self.manager.current = 'Attendance'
        #validate details and if correct (if wrong start afresh after beaming)
            #go to covid sypmtoms recording and start beaming
            #else reenter details (use snackbar)
        #goto screen displaying message for student to

    def backbtn(self): #find a way to use just 1 fuction in in class MainApp
        self.manager.current = 'Home'
           
# make tuple to hold covid sysmptoms
#tuple used for updating db during beaming
covid_symptoms = [0,0,0,0,0,0]
class AttendanceScreen(MDScreen):
    
    def backbtn(self): #find a way to use just 1 fuction in in class MainApp
        if bflag == 0:
            self.manager.current = 'Home'
        else: self.manager.current = 'Register'

    #for menu button
    def menu_action(self):
        Snackbar(text=" ",button_text="Close&Exit",font_size='25sp').open()

    #--------covid sysmptoms checkboxes-----------
    def fever_checkbox_active(self):
        #cater for a mistaken press!!!
        if covid_symptoms[0] == 0:
            covid_symptoms[0] = 1
        else:
            covid_symptoms[0] = 0
        
    def brdiff_checkbox_active(self):
        if covid_symptoms[1] == 0:
            covid_symptoms[1] = 1
        else:
            covid_symptoms[1] = 0

    def chpns_checkbox_active(self):
        if covid_symptoms[2] == 0:
            covid_symptoms[2] = 1
        else:
            covid_symptoms[2] = 0

    def headache_checkbox_active(self):
        if covid_symptoms[3] == 0:
            covid_symptoms[3] = 1
        else:
            covid_symptoms[3] = 0

    def lossApp_checkbox_active(self):
        if covid_symptoms[4] == 0:
            covid_symptoms[4] = 1
        else:
            covid_symptoms[4] = 0

    def anxiety_checkbox_active(self):
        if covid_symptoms[5] == 0:
            covid_symptoms[5] = 1
        else:
            covid_symptoms[5] = 0
    #-------------------------------------------------
            
    def attDone_button_action(self):
        global bbflag #for back button
        bbflag = 0

        #-----------nfc section----------------
       server = None
       
       def send_ndef_message(llc):
           txt_record = ndef.TextRecord('hello world')
           nfc.snep.SnepClient(llc).put_records( [txt_record] )
           
       def startup(clf, llc): #create server to accept and discard put requests from peer
           global server
           server = nfc.snep.SnepServer(llc, "urn:nfc:sn:snep")
           return llc
       
       def connected(llc):
           server.start()
           threading.Thread(target=send_ndef_message, args=(llc,)).start()
           return True
       
       clf = nfc.ContactlessFrontend("udp")
       clf.connect(llcp={'on-startup': startup, 'on-connect': connected})
       self.manager.current = 'StartBeam'       #may go to beaming screen or use snackbar(s)

       except:
           self.manager.current='Attendance'
           Snackbar(text="TypeError: startup() missing 1 required positional argument: 'llc'", font_size='10sp').show()

        #-----------end nfc section------------
##------------test attendance db----------------------------------------
#         try: #for handling case of connection problems
#             conn = mysql.connector.connect(user='<username>',password='<password>', host='<host address>', database='<db name>')

#             print("connected:....")

#             #create a cursor object using the cursor() method

#             cursor = conn.cursor()


#             today = date.today()
#             now = datetime.now().time()
#             #insert data into db (if register way was taken)
#             sql = '''INSERT INTO eee599.attendance_tbl(DATE,TIME,STUDENT_ID,COURSE_CODE,FEVER,DIFF_BREATHING,HEADACHE,CHEST_PAINS,ANXIETY,LOSS_APPETITE)
#                      VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
#             data = (today,now,st_id_input,course_code_input,covid_symptoms[0],covid_symptoms[1],covid_symptoms[3],covid_symptoms[2],covid_symptoms[5],covid_symptoms[4])

#             #retrieving data from table
#             cursor.execute("SELECT ST_ID FROM student_tbl")
#             result1 = cursor.fetchall();
                        
#             try:
#                 for j in range(len(result1)):
#                     if st_id_input == str(result1[j][0]):
#                         # Executing the SQL command
#                         cursor.execute(sql,data)
#                         print('Data inserted to attendance DB...')
#                         toast('Attendance taken')
#                         self.manager.current = 'StartBeam'
#                         break
                        
#                 if st_id_input != str(result1[j][0]):
#                     if bflag!=1:
#                         toast('Not Registered, Please select Register')
#                     self.manager.current = 'Home'                                         
#                 # Commit your changes in the database
#                 conn.commit()
# ##                if bflag == 0:
# ##                    self.manager.current = 'StartBeam'
                
                    
#             except:
#             # Rolling back in case of error
#                 conn.rollback()
#                 print('Data NOT inserted to DB...')

#             if bflag == 1: #register selected    
#                 try:
#                     print('trying conn to student_tbl')
#                     sql1 = '''INSERT INTO eee599.student_tbl(ST_ID,ST_NAME,ST_SURNAME)
#                         VALUES(%s,%s,%s)'''
#                     data1 = (st_id_input,name_input,surname_input)
                    
#                     cursor.execute(sql1,data1)
#                     conn.commit()
#                     print('data inserted to student tbl')
#                     toast('Registration Successful!!\nAttendance taken...')
#                     self.manager.current = 'StartBeam'

#                 except mysql.connector.Error as err:
#                     print('except mode')
#                     message = err.msg
#                     conn.rollback()
#                     self.manager.current = 'Home'
#                     toast(message+"\nCheck info again or\nSelect different option")
                        
#             #execute comands for adding student to course database if first time
                
#             #closing the conection

#             conn.close()
            
#         except:
#             toast("CHECK CONNECTION....")
#             self.manager.current = 'Home'
##------------end test of db (delete once able to send using NFC)-------    
        
        
class StartBeamScreen(MDScreen):
    def backbtn(self): #find a way to use just 1 fuction in in class MainApp
        if bbflag == 0:
            self.manager.current = 'Attendance'
        else:
            self.manager.current = 'Register'

    def menu_action(self):
        self.snackbar = Snackbar(text="Close & Exit", font_size='25sp')
        self.snackbar.open()
        
    

class MainApp(MDApp):
    def menu_callback(self):
        #toast('closing app')
        MainApp().stop()    
    
    def build(self):
        sm = ScreenManager();
        sm.add_widget(HomeScreen(name='Home'))
        sm.add_widget(AttendanceScreen(name='Attendance'))
        sm.add_widget(RegisterScreen(name='Register'))
        sm.add_widget(StartBeamScreen(name='StartBeam'))

        return sm
        
        #use sm and the name of the current widget in defining the funtion of the back button


if __name__ == '__main__':
    MainApp().run()
