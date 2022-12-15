import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import Icons
import sqlite3

database = sqlite3.connect('ClubArc.db')

class MainWindow(QMainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("HomePage.ui", self)
        self.clubButton.clicked.connect(self.gotoClubPage)
        self.membersButton.clicked.connect(self.gotoMembersPage)
        self.advisersButton.clicked.connect(self.gotoAdvisersPage)
        self.membershipButton.clicked.connect(self.gotoMembershipPage)
        self.settingsButton.clicked.connect(self.gotoSettingsPage)
        self.IMGBackground.setPixmap(QPixmap("BackgroundImage.png"))
    
    def gotoMembersPage(self):
        membersPage = MembersPage()
        widget.addWidget(membersPage)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def gotoClubPage(self):
        clubPage = ClubPage()
        widget.addWidget(clubPage)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def gotoAdvisersPage(self):
        advisersPage = AdvisersPage()
        widget.addWidget(advisersPage)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def gotoMembershipPage(self):
        membershipPage = MembershipPage()
        widget.addWidget(membershipPage)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def gotoSettingsPage(self):
        settingsPage = Settings()
        widget.addWidget(settingsPage)
        widget.setCurrentIndex(widget.currentIndex()+1)

class ClubPage(QMainWindow):
    def __init__(self):
        super(ClubPage, self).__init__()
        loadUi("Clubs.ui", self)
        self.homeButton.clicked.connect(self.gotoMainWindow)
        self.membersButton.clicked.connect(self.gotoMembersPage)
        self.advisersButton.clicked.connect(self.gotoAdvisersPage)
        self.membershipButton.clicked.connect(self.gotoMembershipPage)
        self.settingsButton.clicked.connect(self.gotoSettingsPage)
        self.IMGBackground.setPixmap(QPixmap("BackgroundImage.png"))
        self.IMGAddClub.setPixmap(QPixmap("Create Club.png"))
        self.IMGUpdateClub.setPixmap(QPixmap("Create Club 2.png"))
        
        #CRUD Methodology
        self.clrButtonAddClub.clicked.connect(self.clrButtonClub)
        self.insertClubButton.clicked.connect(self.insertClub)
        self.deleteClubButton.clicked.connect(self.deleteClub)
        self.updateClubButton.clicked.connect(self.updateClub)
        self.clubRefreshButton.clicked.connect(self.viewClubsTable)
        self.clubSortButton1.clicked.connect(self.sortClubName)
        self.clubSortButton2.clicked.connect(self.viewClubsTable)
        
        #Clubs Table
        self.clubsTable.setColumnWidth(0,100)
        self.clubsTable.setColumnWidth(1,200)
        self.clubsTable.setColumnWidth(2,364)
        self.clubsTable.setHorizontalHeaderLabels(["Club ID", "Club Name", "Club Description"])
        self.viewClubsTable()
    
    def gotoMembersPage(self):
        membersPage = MembersPage()
        widget.addWidget(membersPage)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def gotoMainWindow(self):
        mainwindow = MainWindow()
        widget.addWidget(mainwindow)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def gotoAdvisersPage(self):
        advisersPage = AdvisersPage()
        widget.addWidget(advisersPage)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def gotoMembershipPage(self):
        membershipPage = MembershipPage()
        widget.addWidget(membershipPage)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotoSettingsPage(self):
        settingsPage = Settings()
        widget.addWidget(settingsPage)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def clrButtonClub(self):
        self.addClubName.clear()
        self.addClubDescription.clear()
        
    #New Functions
    def insertClub(self):
        clubName = self.addClubName.text()
        clubDescription = self.addClubDescription.toPlainText()
        cursor = database.cursor()
        try:
            cursor.execute("SELECT COUNT(Club_Name) FROM Clubs WHERE Club_Name = ?", (clubName,))
            searchResult = cursor.fetchall()
            if clubName == "" or clubDescription == "":
                self.addClubResult.setStyleSheet("color: red")
                self.addClubResult.setText("Fill up all required information")
            else:
                if searchResult[-1][-1] == 1:
                    self.addClubResult.setStyleSheet("color: red")
                    self.addClubResult.setText("Similar Club Name already exists")
                else:
                    cursor.execute("INSERT INTO Clubs (Club_Name, Club_Description)\
                                    VALUES(?, ?)", (clubName, clubDescription))
                    self.addClubResult.setStyleSheet("color: green")
                    self.addClubResult.setText("Creation of " + clubName + " is Successful")
        except:
            database.rollback()
        database.commit()
        
    def deleteClub(self):
        clubID = self.deleteClubID.text()
        try:
            cursor.execute("SELECT COUNT(Club_ID) FROM Clubs WHERE Club_ID = ?", (clubID,))
            searchResult = cursor.fetchall()
            if searchResult[-1][-1] == 1:
                cursor.execute("DELETE FROM Memberships WHERE Club_ID = ?", (clubID,))
                cursor.execute("DELETE FROM Clubs WHERE Club_ID = ?", (clubID,))     
                self.deleteClubResult.setStyleSheet("color: green")
                self.deleteClubResult.setText("Deletion Successful. All Memberships under Club ID " + clubID + " are also Removed")
            else:
                self.deleteClubResult.setStyleSheet("color: red")
                self.deleteClubResult.setText("Deletion Unsuccessful. Club " + clubID + " does not exist")
        except:
            database.rollback()
        database.commit()
        
    def updateClub(self):
        clubID = self.updateClubID.text()
        clubName = self.updateCName.text()
        clubDescription = self.updateCDescription.toPlainText()
        nameCheck = self.UpdateCNameBox.isChecked()
        descriptionCheck = self.UpdateCDescriptionBox.isChecked()
        cursor = database.cursor()
        try:
            cursor.execute("SELECT COUNT(Club_ID) FROM Clubs WHERE Club_ID = ?", (clubID,))
            searchResult = cursor.fetchall()
            if searchResult[-1][-1] == 1:
                if nameCheck == True and descriptionCheck == False:
                    if clubName == "":
                        self.updateClubResult.setStyleSheet("color: red")
                        self.updateClubResult.setText("Update values 'Club Name' cannot be null")
                    else:
                        cursor.execute("UPDATE Clubs SET Club_Name = ? WHERE Club_ID = ?", (clubName, clubID))
                        self.updateClubResult.setStyleSheet("color: green")
                        self.updateClubResult.setText("Updating Club Name of Club ID " + clubID + " Successul")
                elif nameCheck == False and descriptionCheck == True:
                    if clubDescription == "":
                        self.updateClubResult.setStyleSheet("color: red")
                        self.updateClubResult.setText("Update values 'Club Description' cannot be null")
                    else:
                        cursor.execute("UPDATE Clubs SET Club_Description = ? WHERE Club_ID = ?", (clubDescription, clubID))
                        self.updateClubResult.setStyleSheet("color: green")
                        self.updateClubResult.setText("Updating Club Description of Club ID " + clubID + " Successul")
                elif nameCheck == True and descriptionCheck == True:
                    if clubDescription == "" or clubName == "":
                        self.updateClubResult.setStyleSheet("color: red")
                        self.updateClubResult.setText("Update values 'Club Name' and 'Club Description' cannot be null")
                    else:
                        cursor.execute("UPDATE Clubs SET Club_Name = ?, Club_Description = ? WHERE Club_ID = ?", (clubName, clubDescription, clubID))
                        self.updateClubResult.setStyleSheet("color: green")
                        self.updateClubResult.setText("Updating Information of Club ID " + clubID + " Successul")
            else:
                self.updateClubResult.setStyleSheet("color: red")
                self.updateClubResult.setText("Club ID " + clubID + " does not exist")
        except:
            database.rollback()
        database.commit()
    
    def viewClubsTable(self):
        cursor = database.cursor()
        query = "SELECT * FROM Clubs ORDER BY Club_ID"
        self.clubsTable.setRowCount(0)
        for row_number, row_data in enumerate(cursor.execute(query)):
            self.clubsTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.clubsTable.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        database.commit()
        
    def sortClubName(self):
        cursor = database.cursor()
        query = "SELECT * FROM Clubs ORDER BY Club_Name"
        self.clubsTable.setRowCount(0)
        for row_number, row_data in enumerate(cursor.execute(query)):
            self.clubsTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.clubsTable.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        database.commit()
        
class MembersPage(QMainWindow):
    def __init__(self):
        super(MembersPage, self).__init__()
        loadUi("Members.ui", self)
        self.homeButton.clicked.connect(self.gotoMainWindow)
        self.clubButton.clicked.connect(self.gotoClubPage)
        self.advisersButton.clicked.connect(self.gotoAdvisersPage)
        self.membershipButton.clicked.connect(self.gotoMembershipPage)
        self.settingsButton.clicked.connect(self.gotoSettingsPage)
        self.IMGBackground.setPixmap(QPixmap("BackgroundImage.png"))
        self.IMGAddPeople1.setPixmap(QPixmap("Avatar1.png"))
        self.IMGAddPeople2.setPixmap(QPixmap("Avatar2.png"))
        
        #CRUD Methodology
        self.insertButtonAddMember.clicked.connect(self.insertMembers)
        self.clrButtonAddMember.clicked.connect(self.clrButtonMembers)
        self.deleteMemberButton.clicked.connect(self.deleteMembers)
        self.updateMemberButton.clicked.connect(self.updateMembers)
        self.memberRefreshButton.clicked.connect(self.viewMembersTable)
        self.sortMembersByAge.clicked.connect(self.sortMembersTableByAge)
        self.sortByMemberFName.clicked.connect(self.sortMembersTableByFName)
        self.sortByMemberLName.clicked.connect(self.sortMembersTableByLName)
        
        #Members Table
        self.membersTable.setColumnWidth(0,20)
        self.membersTable.setColumnWidth(1,80)
        self.membersTable.setColumnWidth(2,80)
        self.membersTable.setColumnWidth(3,70)
        self.membersTable.setColumnWidth(4,35)
        self.membersTable.setColumnWidth(5,180)
        self.membersTable.setColumnWidth(6,300)
        self.membersTable.setColumnWidth(7,100)
        self.membersTable.setHorizontalHeaderLabels(["ID", "First Name", "Last Name", "BirthDate", "Age",
                                                     "E-mail", "Address", "Contact"])
        self.viewMembersTable()
    
    def gotoMainWindow(self):
        mainwindow = MainWindow()
        widget.addWidget(mainwindow)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def gotoClubPage(self):
        clubPage = ClubPage()
        widget.addWidget(clubPage)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def gotoMembershipPage(self):
        membershipPage = MembershipPage()
        widget.addWidget(membershipPage)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def gotoAdvisersPage(self):
        advisersPage = AdvisersPage()
        widget.addWidget(advisersPage)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def gotoSettingsPage(self):
        settingsPage = Settings()
        widget.addWidget(settingsPage)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def clrButtonMembers(self):
        self.addMemberFirstName.clear()
        self.addMemberLastName.clear()
        self.addMemberBirthDate.clear()
        self.addMemberAge.clear()
        self.addMemberEmail.clear()
        self.addMemberAddress.clear() 
        self.addMemberContactNumber.clear()
        
    def insertMembers(self):
        memberFirstName = self.addMemberFirstName.text()
        memberLastName = self.addMemberLastName.text()
        memberBirthDate = self.addMemberBirthDate.text()
        memberAge = self.addMemberAge.text()
        memberEmail = self.addMemberEmail.text()
        memberAddress = self.addMemberAddress.toPlainText()
        memberContact = self.addMemberContactNumber.text()
        cursor = database.cursor()
        if (memberFirstName == "" or memberLastName == "" or memberBirthDate == "" or memberAge == "" or 
            memberEmail == "" or memberAddress == "" or memberContact == ""):
            self.addMemberResult.setStyleSheet("color: red")
            self.addMemberResult.setText("Fill up all required information")
        else:
            try:
                cursor.execute("SELECT COUNT(Contact_Number) FROM Members WHERE Contact_Number = ?", (memberContact,))
                searchResult = cursor.fetchall()
                if searchResult[-1][-1] == 1:
                    self.addMemberResult.setStyleSheet("color: red")
                    self.addMemberResult.setText("Error: No same people have same contact number")
                else:
                    cursor.execute("INSERT INTO Members (First_Name, Last_Name, BirthDate, Age,\
                                    Email, Member_Address, Contact_Number)\
                                    VALUES(?, ?, ?, ?, ?, ?, ?)", (memberFirstName, memberLastName,
                                    memberBirthDate, memberAge, memberEmail, memberAddress, memberContact))
                    self.addMemberResult.setStyleSheet("color: green")
                    self.addMemberResult.setText("Information Complete. Addition of new People Successful")
            except:
                database.rollback()
        database.commit()
        
    def deleteMembers(self):
        memberID = self.deleteMemberID.text()
        cursor = database.cursor()
        try:
            cursor.execute("SELECT COUNT(Member_ID) FROM Members WHERE Member_ID = ?", (memberID,))
            searchResult = cursor.fetchall()
            if searchResult[-1][-1] == 1:
                cursor.execute("DELETE FROM Memberships WHERE Member_ID = ?", (memberID,))
                cursor.execute("DELETE FROM Members WHERE Member_ID = ?", (memberID,))
                self.deleteMemberResult.setStyleSheet("color: green")
                self.deleteMemberResult.setText("Deletion Successful. Membership related to the deleted person ID " + memberID + " also Removed")
            else:
                self.deleteMemberResult.setStyleSheet("color: red")
                self.deleteMemberResult.setText("Deletion Unsuccessful. Person ID " + memberID + " does not exist")
        except:
            database.rollback()
        database.commit()
        
    def updateMembers(self):
        memberID = self.updateMemberID.text()
        memberFirstName = self.updateMemberFirstName.text()
        memberLastName = self.updateMemberLastName.text()
        memberBirthDate = self.updateMemberBirthDate.text()
        memberAge = self.updateMemberAge.text()
        memberEmail = self.updateMemberEmail.text()
        memberAddress = self.updateMemberAddress.toPlainText()
        memberContact = self.updateMemberContact.text()
        FNameCheck = self.updateFNameBox.isChecked()
        LNameCheck = self.updateLNameBox.isChecked()
        BirthCheck = self.updateBirthDateBox.isChecked()
        AgeCheck = self.updateAgeBox.isChecked()
        EmailCheck = self.updateEmailBox.isChecked()
        AddressCheck = self.updateAddressBox.isChecked()
        ContactCheck = self.updateContactBox.isChecked()
        cursor = database.cursor()
        try:
            cursor.execute("SELECT COUNT(Member_ID) FROM Members WHERE Member_ID = ?", (memberID,))
            searchQuery = cursor.fetchall()
            if searchQuery[-1][-1] == 1:
                if (FNameCheck == True or LNameCheck == True or BirthCheck == True or AgeCheck == True or EmailCheck == True or 
                    AddressCheck == True or ContactCheck == True):
                    self.updateMemberResult.setText("")
                    if FNameCheck == True and memberFirstName != "":
                        cursor.execute("UPDATE Members SET First_Name = ? WHERE Member_ID = ?", (memberFirstName, memberID))
                        self.updateMemberResult.setStyleSheet("color: green")
                        self.updateMemberResult.setText("Updating Information of People ID " + memberID + " Successful")
                    if LNameCheck == True and memberLastName != "":
                        cursor.execute("UPDATE Members SET Last_Name = ? WHERE Member_ID = ?", (memberLastName, memberID))
                        self.updateMemberResult.setStyleSheet("color: green")
                        self.updateMemberResult.setText("Updating Information of People ID " + memberID + " Successful")
                    if BirthCheck == True and memberBirthDate != "":
                        cursor.execute("UPDATE Members SET BirthDate = ? WHERE Member_ID = ?", (memberBirthDate, memberID))
                        self.updateMemberResult.setStyleSheet("color: green")
                        self.updateMemberResult.setText("Updating Information of People ID " + memberID + " Successful")
                    if AgeCheck == True and memberAge != "":
                        cursor.execute("UPDATE Members SET Age = ? WHERE Member_ID = ?", (memberAge, memberID))
                        self.updateMemberResult.setStyleSheet("color: green")
                        self.updateMemberResult.setText("Updating Information of People ID " + memberID + " Successful")
                    if EmailCheck == True and memberEmail != "":
                        cursor.execute("UPDATE Members SET Email = ? WHERE Member_ID = ?", (memberEmail, memberID))
                        self.updateMemberResult.setStyleSheet("color: green")
                        self.updateMemberResult.setText("Updating Information of People ID " + memberID + " Successful")
                    if AddressCheck == True and memberAddress != "":
                        cursor.execute("UPDATE Members SET Member_Address = ? WHERE Member_ID = ?", (memberAddress, memberID))
                        self.updateMemberResult.setStyleSheet("color: green")
                        self.updateMemberResult.setText("Updating Information of People ID " + memberID + " Successful")
                    if ContactCheck == True and memberContact != "":
                        cursor.execute("UPDATE Members SET Contact_Number = ? WHERE Member_ID = ?", (memberContact, memberID))
                        self.updateMemberResult.setStyleSheet("color: green")
                        self.updateMemberResult.setText("Updating Information of People ID " + memberID + " Successful")
                elif (FNameCheck == False or LNameCheck == False or BirthCheck == False or AgeCheck == False or EmailCheck == False or 
                      AddressCheck == False or ContactCheck == False):
                    self.updateMemberResult.setStyleSheet("color: red")
                    self.updateMemberResult.setText("Check Box which information to update")
                else:
                    self.updateMemberResult.setStyleSheet("color: red")
                    self.updateMemberResult.setText("The information to update should not be null")
            else:
                self.updateMemberResult.setStyleSheet("color: red")
                self.updateMemberResult.setText("People ID given does not Exist")
        except:
            database.rollback()
        database.commit()
    
    def viewMembersTable(self):
        cursor = database.cursor()
        query = "SELECT Member_ID, First_Name, Last_Name, BirthDate, Age, Email,\
                 Member_Address, Contact_Number FROM Members ORDER BY Member_ID"
        self.membersTable.setRowCount(0)
        for row_number, row_data in enumerate(cursor.execute(query)):
            self.membersTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.membersTable.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        database.commit()
        
    def sortMembersTableByFName(self):
        cursor = database.cursor()
        query = "SELECT Member_ID, First_Name, Last_Name, BirthDate, Age, Email,\
                 Member_Address, Contact_Number FROM Members ORDER BY First_Name"
        self.membersTable.setRowCount(0)
        for row_number, row_data in enumerate(cursor.execute(query)):
            self.membersTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.membersTable.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        database.commit()
    
    def sortMembersTableByLName(self):
        cursor = database.cursor()
        query = "SELECT Member_ID, First_Name, Last_Name, BirthDate, Age, Email,\
                 Member_Address, Contact_Number FROM Members ORDER BY Last_Name"
        self.membersTable.setRowCount(0)
        for row_number, row_data in enumerate(cursor.execute(query)):
            self.membersTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.membersTable.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        database.commit()
        
    def sortMembersTableByAge(self):
        cursor = database.cursor()
        query = "SELECT Member_ID, First_Name, Last_Name, BirthDate, Age, Email,\
                 Member_Address, Contact_Number FROM Members ORDER BY Age"
        self.membersTable.setRowCount(0)
        for row_number, row_data in enumerate(cursor.execute(query)):
            self.membersTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.membersTable.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        database.commit()
        
class AdvisersPage(QMainWindow):
    def __init__(self):
        super(AdvisersPage, self).__init__()
        loadUi("Advisers.ui", self)
        self.homeButton.clicked.connect(self.gotoMainWindow)
        self.clubButton.clicked.connect(self.gotoClubPage)
        self.membersButton.clicked.connect(self.gotoMembersPage)
        self.membershipButton.clicked.connect(self.gotoMembershipPage)
        self.settingsButton.clicked.connect(self.gotoSettingsPage)
        self.IMGBackground.setPixmap(QPixmap("BackgroundImage.png"))
        self.IMGAddAdviser.setPixmap(QPixmap("Adviser.png"))
        
        #CRUD Methodology
        self.addAdviserButton.clicked.connect(self.addAdvisers)
        self.membershipRefresh.clicked.connect(self.viewAdvisersTable)
        self.deleteAdviserButton.clicked.connect(self.deleteAdvisers)
        self.adviserSort1.clicked.connect(self.viewAdvisersTable)
        self.adviserSort2.clicked.connect(self.sortAdviserName)
        self.adviserSort3.clicked.connect(self.sortAdviserClubID)
        self.adviserSort4.clicked.connect(self.sortAdviserClubName)
        
        #Advisers Table
        self.advisersTable.setColumnWidth(0,70)
        self.advisersTable.setColumnWidth(1,150)
        self.advisersTable.setColumnWidth(2,70)
        self.advisersTable.setColumnWidth(3,200)
        self.advisersTable.setHorizontalHeaderLabels(["Adviser ID", "Full Name", "Club ID", "Club Name"])
        self.viewAdvisersTable()
        
    def gotoMainWindow(self):
        mainwindow = MainWindow()
        widget.addWidget(mainwindow)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def gotoClubPage(self):
        clubPage = ClubPage()
        widget.addWidget(clubPage)
        widget.setCurrentIndex(widget.currentIndex()+1)  
    
    def gotoMembersPage(self):
        membersPage = MembersPage()
        widget.addWidget(membersPage)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def gotoMembershipPage(self):
        membershipPage = MembershipPage()
        widget.addWidget(membershipPage)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotoSettingsPage(self):
        settingsPage = Settings()
        widget.addWidget(settingsPage)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def addAdvisers(self):
        adviserFirstName = self.addAdviserFirstName.text()
        adviserLastName = self.addAdviserLastName.text()
        clubID = self.addMembershipClub.text()
        cursor = database.cursor()
        try:
            if adviserFirstName == "" or adviserLastName == "" or clubID == "":
                self.addAdviserResult.setStyleSheet("color: red")
                self.addAdviserResult.setText("Fill up the required information")
            else:
                cursor.execute("SELECT COUNT(Club_ID) FROM Clubs WHERE Club_ID = ?", (clubID,))
                searchClub = cursor.fetchall()
                if searchClub[-1][-1] == 1:
                    cursor.execute("SELECT COUNT(Adviser_ID) FROM Advisers WHERE Club_ID = ?", (clubID,))
                    searchAdviser = cursor.fetchall()
                    if searchAdviser[-1][-1] == 1:
                        self.addAdviserResult.setStyleSheet("color: red")
                        self.addAdviserResult.setText("Club ID " + clubID + " already has an adviser")
                    else:
                        cursor.execute("INSERT INTO Advisers(First_Name, Last_Name, Club_ID)\
                                        VALUES(?, ?, ?)", (adviserFirstName, adviserLastName, clubID))
                        self.addAdviserResult.setStyleSheet("color: green")
                        self.addAdviserResult.setText("Successfully added Adviser to Club ID " + clubID)
                else:
                    self.addAdviserResult.setStyleSheet("color: red")
                    self.addAdviserResult.setText("Club ID " + clubID + " does not exist")
        except:
            database.rollback()
        database.commit()
    
    def deleteAdvisers(self):
        adviserID = self.deleteAdviserID.text()
        cursor = database.cursor()
        try:
            if adviserID == "":
                self.removeAdviserResult.setStyleSheet("color: red")
                self.removeAdviserResult.setText("Fill up the required information")
            else:
                cursor.execute("SELECT COUNT(Adviser_ID) FROM Advisers WHERE Adviser_ID = ?", (adviserID,))
                searchClub = cursor.fetchall()
                if searchClub[-1][-1] == 1:
                    cursor.execute("DELETE FROM Advisers WHERE Adviser_ID = ?", (adviserID))
                    self.removeAdviserResult.setStyleSheet("color: green")
                    self.removeAdviserResult.setText("Adviser ID " + adviserID + " removed successfully")
                else:
                    self.removeAdviserResult.setStyleSheet("color: red")
                    self.removeAdviserResult.setText("Adviser ID " + adviserID + " does not exist")
        except:
            database.rollback()
        database.commit()
        
    def viewAdvisersTable(self):
        cursor = database.cursor()
        query = "SELECT a.Adviser_ID, a.First_Name || ' ' || a.Last_Name, a.Club_ID, b.Club_Name FROM Advisers a\
                 INNER JOIN Clubs b ON a.Club_ID = b.Club_ID ORDER BY a.Adviser_ID"
        self.advisersTable.setRowCount(0)
        for row_number, row_data in enumerate(cursor.execute(query)):
            self.advisersTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.advisersTable.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        database.commit()
    
    def sortAdviserName(self):
        cursor = database.cursor()
        query = "SELECT a.Adviser_ID, a.First_Name || ' ' || a.Last_Name AS 'FullName', a.Club_ID, b.Club_Name FROM Advisers a\
                 INNER JOIN Clubs b ON a.Club_ID = b.Club_ID ORDER BY FullName"
        self.advisersTable.setRowCount(0)
        for row_number, row_data in enumerate(cursor.execute(query)):
            self.advisersTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.advisersTable.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        database.commit()
    
    def sortAdviserClubID(self):
        cursor = database.cursor()
        query = "SELECT a.Adviser_ID, a.First_Name || ' ' || a.Last_Name, a.Club_ID, b.Club_Name FROM Advisers a\
                 INNER JOIN Clubs b ON a.Club_ID = b.Club_ID ORDER BY a.Club_ID"
        self.advisersTable.setRowCount(0)
        for row_number, row_data in enumerate(cursor.execute(query)):
            self.advisersTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.advisersTable.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        database.commit()
    
    def sortAdviserClubName(self):
        cursor = database.cursor()
        query = "SELECT a.Adviser_ID, a.First_Name || ' ' || a.Last_Name, a.Club_ID, b.Club_Name FROM Advisers a\
                 INNER JOIN Clubs b ON a.Club_ID = b.Club_ID ORDER BY b.Club_Name"
        self.advisersTable.setRowCount(0)
        for row_number, row_data in enumerate(cursor.execute(query)):
            self.advisersTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.advisersTable.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        database.commit()
        
class MembershipPage(QMainWindow):
    def __init__(self):
        super(MembershipPage, self).__init__()
        loadUi("Membership.ui", self)
        self.homeButton.clicked.connect(self.gotoMainWindow)
        self.clubButton.clicked.connect(self.gotoClubPage)
        self.membersButton.clicked.connect(self.gotoMembersPage)
        self.advisersButton.clicked.connect(self.gotoAdvisersPage)
        self.settingsButton.clicked.connect(self.gotoSettingsPage)
        self.IMGBackground.setPixmap(QPixmap("BackgroundImage.png"))
    
        #CRUD Methodology
        self.addMembershipButton.clicked.connect(self.addMembership)
        self.deleteMembership.clicked.connect(self.removeMembership)
        self.membershipClubRefresh.clicked.connect(self.viewClubMembersTable)
        self.membershipRefresh.clicked.connect(self.viewMembershipTable)
        self.membershipSort1.clicked.connect(self.sortMembershipTableMemID)  
        self.membershipSort2.clicked.connect(self.sortMembershipTableClubID)
        self.membershipSort3.clicked.connect(self.sortMembershipTableMemName)
        self.membershipSort4.clicked.connect(self.sortMembershipTableClubName)
        self.membershipSort5.clicked.connect(self.viewMembershipTable)
        
        #Memberships Table
        self.membershipTable.setColumnWidth(0,100)
        self.membershipTable.setColumnWidth(1,80)
        self.membershipTable.setColumnWidth(2,180)
        self.membershipTable.setColumnWidth(3,80)
        self.membershipTable.setColumnWidth(4,200)
        self.membershipTable.setColumnWidth(5,70)
        self.membershipTable.setHorizontalHeaderLabels(["Membership ID", "People ID", "Full Name",
                                                        "Club ID", "Club Name", "Date Joined"])
        self.viewMembershipTable()
        
        #ClubMembers Table
        self.clubMembersTable.setColumnWidth(0,100)
        self.clubMembersTable.setColumnWidth(1,50)
        self.clubMembersTable.setColumnWidth(2,70)
        self.clubMembersTable.setColumnWidth(3,150)
        self.clubMembersTable.setColumnWidth(4,30)
        self.clubMembersTable.setColumnWidth(5,200)
        self.clubMembersTable.setColumnWidth(6,70)
        self.clubMembersTable.setColumnWidth(7,80)
        self.clubMembersTable.setColumnWidth(8,70)
        self.clubMembersTable.setHorizontalHeaderLabels(["Membership ID", "Club ID", "People ID", "Full Name",
                                                         "Age", "Member Address", "Birth Date", "Contact", "Date Joined"])
        
    def gotoMainWindow(self):
        mainwindow = MainWindow()
        widget.addWidget(mainwindow)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def gotoClubPage(self):
        clubPage = ClubPage()
        widget.addWidget(clubPage)
        widget.setCurrentIndex(widget.currentIndex()+1)  
    
    def gotoMembersPage(self):
        membersPage = MembersPage()
        widget.addWidget(membersPage)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def gotoAdvisersPage(self):
        advisersPage = AdvisersPage()
        widget.addWidget(advisersPage)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def gotoSettingsPage(self):
        settingsPage = Settings()
        widget.addWidget(settingsPage)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    #New Functions    
    def addMembership(self):
        clubID = self.addMembershipClub.text()
        memberID = self.addMembershipMember.text()
        cursor = database.cursor()
        try:
            cursor.execute("SELECT COUNT(Club_ID) FROM Clubs WHERE Club_ID = ?", (clubID,))
            clubsfound = cursor.fetchall()
            if clubsfound[-1][-1] == 1:
                cursor.execute("SELECT COUNT(Member_ID) FROM Members WHERE Member_ID = ?", (memberID,))
                membersfound = cursor.fetchall()
                if membersfound[-1][-1] == 1:
                    cursor.execute("INSERT INTO Memberships(Member_ID, Club_ID, DateMembershipStarted)\
                                    VALUES(?, ?, DATE('now'))", (memberID, clubID))
                    cursor.execute("SELECT COUNT(*) FROM Memberships WHERE Member_ID = ? AND Club_ID = ?", (memberID, clubID))
                    membershipfound = cursor.fetchall()
                    if membershipfound[-1][-1] == 1:
                        self.addMembershipResult.setStyleSheet("color: green")
                        self.addMembershipResult.setText("Creation of Membership Successful. Member with ID " + memberID + " added to Club ID " + clubID + ".")
                    else:
                        self.addMembershipResult.setStyleSheet("color: red")
                        self.addMembershipResult.setText("Creation of Membership Unsuccessful. Member with ID " + memberID + " is already a member of Club " + clubID + ".")
                        database.rollback()
                else:
                    self.addMembershipResult.setStyleSheet("color: red")
                    self.addMembershipResult.setText("People with an ID of " + memberID + " does not exist")
            else:
                self.addMembershipResult.setStyleSheet("color: red")
                self.addMembershipResult.setText("Club with an ID of " + clubID + " does not exist")
        except:
            self.addMembershipResult.setStyleSheet("color: red")
            self.addMembershipResult.setText("Creation of Membership Unsuccessful. Check Member ID and Club ID if it exist.")
            database.rollback()
        database.commit()
    
    def removeMembership(self):
        memberID = self.deleteMembershipMemberID.text()
        clubID = self.deleteMembershipClubID.text()
        cursor = database.cursor()
        try:
            cursor.execute("SELECT COUNT(Membership_ID) FROM Memberships WHERE Club_ID = ? AND Member_ID = ?", (clubID, memberID))
            searchResult = cursor.fetchall()
            if searchResult[-1][-1] == 1:
                cursor.execute("DELETE FROM Memberships WHERE Club_ID = ? AND Member_ID = ?", (clubID, memberID))
                self.removeMembershipResult.setStyleSheet("color: green")
                self.removeMembershipResult.setText("Removal of Membership with Member ID " + memberID + " from Club ID " + clubID + " is successful")
            else:
                self.removeMembershipResult.setStyleSheet("color: red")
                self.removeMembershipResult.setText("There is no Membership with Member ID " + memberID + " from Club ID " + clubID)
        except:
            database.rollback()
        database.commit()
    
    def viewClubMembersTable(self):
        cursor = database.cursor()
        clubID = self.viewMembersInClub.text()     
        try:
            cursor.execute("SELECT COUNT(Club_ID) FROM Clubs WHERE Club_ID = ?", (clubID, ))
            obtainedClubID = cursor.fetchall()
            if obtainedClubID[-1][-1] == 1:
                cursor.execute("SELECT Club_Name FROM Clubs WHERE Club_ID = ?", (clubID, ))
                obtainedClub = cursor.fetchall() 
                self.ClubMembersLabel.setStyleSheet("color: green")
                self.ClubMembersLabel.setText("Viewing " + obtainedClub[-1][-1]) 
                query = "SELECT a.Membership_ID, b.Club_ID, c.Member_ID, c.First_Name ||' '|| c.Last_Name, c.Age, c.Member_Address,\
                         c.BirthDate, c.Contact_Number, a.DateMembershipStarted FROM Memberships a\
                         INNER JOIN Clubs b ON a.CLub_ID = b.Club_ID\
                         INNER JOIN Members c ON a.Member_ID = c.Member_ID\
                         WHERE b.Club_ID = ? ORDER BY c.Member_ID"
                self.clubMembersTable.setRowCount(0)
                for row_number, row_data in enumerate(cursor.execute(query, clubID)):
                    self.clubMembersTable.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.clubMembersTable.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
            else:
                self.ClubMembersLabel.setStyleSheet("color: red")
                self.ClubMembersLabel.setText("Club does not exist")
        except:
            database.rollback()
        database.commit()
        
    def viewMembershipTable(self):
        cursor = database.cursor()
        query = "SELECT a.Membership_ID, b.Member_ID, b.First_Name ||' '||b.Last_Name,\
                 c.Club_ID, c.Club_Name, a.DateMembershipStarted FROM Memberships a\
                 INNER JOIN Members b ON a.Member_ID = b.Member_ID\
                 INNER JOIN Clubs c ON a.Club_ID = c.Club_ID\
                 ORDER BY a.Membership_ID"
        self.membershipTable.setRowCount(0)
        for row_number, row_data in enumerate(cursor.execute(query)):
            self.membershipTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.membershipTable.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        database.commit()
        
    def sortMembershipTableMemID(self):
        cursor = database.cursor()
        query = "SELECT a.Membership_ID, b.Member_ID, b.First_Name ||' '||b.Last_Name,\
                 c.Club_ID, c.Club_Name, a.DateMembershipStarted FROM Memberships a\
                 INNER JOIN Members b ON a.Member_ID = b.Member_ID\
                 INNER JOIN Clubs c ON a.Club_ID = c.Club_ID\
                 ORDER BY b.Member_ID"
        self.membershipTable.setRowCount(0)
        for row_number, row_data in enumerate(cursor.execute(query)):
            self.membershipTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.membershipTable.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        database.commit()
    
    def sortMembershipTableClubID(self):
        cursor = database.cursor()
        query = "SELECT a.Membership_ID, b.Member_ID, b.First_Name ||' '||b.Last_Name,\
                 c.Club_ID, c.Club_Name, a.DateMembershipStarted FROM Memberships a\
                 INNER JOIN Members b ON a.Member_ID = b.Member_ID\
                 INNER JOIN Clubs c ON a.Club_ID = c.Club_ID\
                 ORDER BY c.Club_ID"
        self.membershipTable.setRowCount(0)
        for row_number, row_data in enumerate(cursor.execute(query)):
            self.membershipTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.membershipTable.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        database.commit()
    
    def sortMembershipTableMemName(self):
        cursor = database.cursor()
        query = "SELECT a.Membership_ID, b.Member_ID, b.First_Name ||' '||b.Last_Name AS Member_Name,\
                 c.Club_ID, c.Club_Name, a.DateMembershipStarted FROM Memberships a\
                 INNER JOIN Members b ON a.Member_ID = b.Member_ID\
                 INNER JOIN Clubs c ON a.Club_ID = c.Club_ID\
                 ORDER BY Member_Name"
        self.membershipTable.setRowCount(0)
        for row_number, row_data in enumerate(cursor.execute(query)):
            self.membershipTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.membershipTable.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        database.commit()
    
    def sortMembershipTableClubName(self):
        cursor = database.cursor()
        query = "SELECT a.Membership_ID, b.Member_ID, b.First_Name ||' '||b.Last_Name,\
                 c.Club_ID, c.Club_Name, a.DateMembershipStarted FROM Memberships a\
                 INNER JOIN Members b ON a.Member_ID = b.Member_ID\
                 INNER JOIN Clubs c ON a.Club_ID = c.Club_ID\
                 ORDER BY c.Club_Name"
        self.membershipTable.setRowCount(0)
        for row_number, row_data in enumerate(cursor.execute(query)):
            self.membershipTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.membershipTable.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        database.commit()
        
class Settings(QMainWindow):
    def __init__(self):
        super(Settings, self).__init__()
        loadUi("Settings.ui", self)
        self.homeButton.clicked.connect(self.gotoMainWindow)
        self.clubButton.clicked.connect(self.gotoClubPage)
        self.membersButton.clicked.connect(self.gotoMembersPage)
        self.advisersButton.clicked.connect(self.gotoAdvisersPage)
        self.membershipButton.clicked.connect(self.gotoMembershipPage)
        self.resetButton.clicked.connect(self.gotoWarning)
        self.IMGBackground.setPixmap(QPixmap("BackgroundImage.png"))
        
    def gotoMainWindow(self):
        mainwindow = MainWindow()
        widget.addWidget(mainwindow)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def gotoClubPage(self):
        clubPage = ClubPage()
        widget.addWidget(clubPage)
        widget.setCurrentIndex(widget.currentIndex()+1)  
    
    def gotoMembersPage(self):
        membersPage = MembersPage()
        widget.addWidget(membersPage)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def gotoAdvisersPage(self):
        advisersPage = AdvisersPage()
        widget.addWidget(advisersPage)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def gotoMembershipPage(self):
        membershipPage = MembershipPage()
        widget.addWidget(membershipPage)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def gotoWarning(self):
        warning = WarningWindow()
        widget.addWidget(warning)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
class WarningWindow(QMainWindow):
    def __init__(self):
        super(WarningWindow, self).__init__()
        loadUi("WarningPrompt.ui", self)
        self.YesButton.clicked.connect(self.resetDatabase)
        self.NoButton.clicked.connect(self.gotoSettingsPage)
        self.ExitButton.clicked.connect(self.gotoSettingsPage)
        self.IMGBackground.setPixmap(QPixmap("BackgroundImage.png"))
        self.ExitButton.hide()
        self.WarningResult.hide()
        
    def gotoSettingsPage(self):
        settingsPage = Settings()
        widget.addWidget(settingsPage)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def resetDatabase(self):
        cursor = database.cursor()
        cursor.execute("DROP TABLE IF EXISTS Memberships")
        cursor.execute("DROP TABLE IF EXISTS Advisers")
        cursor.execute("DROP TABLE IF EXISTS Members")
        cursor.execute("DROP TABLE IF EXISTS Clubs")
        cursor.execute("CREATE TABLE IF NOT EXISTS Clubs(\
                        Club_ID INTEGER PRIMARY KEY AUTOINCREMENT,\
                        Club_Name VARCHAR(50) NOT NULL,\
                        Club_Description TEXT NOT NULL)")     
        cursor.execute("CREATE TABLE IF NOT EXISTS Advisers(\
                        Adviser_ID INTEGER PRIMARY KEY AUTOINCREMENT,\
                    	First_Name VARCHAR(50) NOT NULL,\
                    	Last_Name VARCHAR(50) NOT NULL,\
                    	Club_ID INT,\
                    	FOREIGN KEY (Club_ID) REFERENCES Clubs(Club_ID))")
        cursor.execute("CREATE TABLE IF NOT EXISTS Members(\
                    	Member_ID INTEGER PRIMARY KEY AUTOINCREMENT,\
                    	First_Name VARCHAR(50) NOT NULL,\
                    	Last_Name VARCHAR(50) NOT NULL,\
                    	Member_Address TEXT NOT NULL,\
                    	BirthDate DATE NOT NULL,\
                    	Age INT NOT NULL,\
                    	Email VARCHAR(100) NOT NULL,\
                    	Contact_Number VARCHAR(11) NOT NULL)")
        cursor.execute("CREATE TABLE IF NOT EXISTS Memberships(\
                    	Membership_ID INTEGER PRIMARY KEY AUTOINCREMENT,\
                    	Member_ID INT NOT NULL,\
                    	Club_ID INT NOT NULL,\
                    	DateMembershipStarted DATETIME,\
                    	FOREIGN KEY (Member_ID) REFERENCES Members(Member_ID),\
                    	FOREIGN KEY (Club_ID) REFERENCES Clubs(Club_ID))")
        self.YesButton.hide()
        self.NoButton.hide()
        self.continueLabel.hide()
        self.WarningResult.show()
        self.ExitButton.show()
        self.WarningResult.setStyleSheet("color: green")   
        self.WarningResult.setText("Database has been cleared successfully")
        database.commit()

# main
app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
mainwindow = MainWindow()
widget.addWidget(mainwindow) 
widget.setFixedHeight(600)
widget.setFixedWidth(800)
title = "ClubArc"
widget.setWindowTitle(title)
widget.setWindowIcon(QIcon('club.ico'))
widget.show()

# creation of database and table if not exists
cursor = database.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS Clubs(\
                Club_ID INTEGER PRIMARY KEY AUTOINCREMENT,\
                Club_Name VARCHAR(50) NOT NULL,\
                Club_Description TEXT NOT NULL)")     

cursor.execute("CREATE TABLE IF NOT EXISTS Advisers(\
                Adviser_ID INTEGER PRIMARY KEY AUTOINCREMENT,\
            	First_Name VARCHAR(50) NOT NULL,\
            	Last_Name VARCHAR(50) NOT NULL,\
            	Club_ID INT,\
            	FOREIGN KEY (Club_ID) REFERENCES Clubs(Club_ID))")

cursor.execute("CREATE TABLE IF NOT EXISTS Members(\
            	Member_ID INTEGER PRIMARY KEY AUTOINCREMENT,\
            	First_Name VARCHAR(50) NOT NULL,\
            	Last_Name VARCHAR(50) NOT NULL,\
            	Member_Address TEXT NOT NULL,\
            	BirthDate DATE NOT NULL,\
            	Age INT NOT NULL,\
            	Email VARCHAR(100) NOT NULL,\
            	Contact_Number VARCHAR(11) NOT NULL)")

cursor.execute("CREATE TABLE IF NOT EXISTS Memberships(\
            	Membership_ID INTEGER PRIMARY KEY AUTOINCREMENT,\
            	Member_ID INT NOT NULL,\
            	Club_ID INT NOT NULL,\
            	DateMembershipStarted DATETIME,\
            	FOREIGN KEY (Member_ID) REFERENCES Members(Member_ID),\
            	FOREIGN KEY (Club_ID) REFERENCES Clubs(Club_ID))")
database.commit()

try:
    sys.exit(app.exec_())
except:
    print("Exiting")