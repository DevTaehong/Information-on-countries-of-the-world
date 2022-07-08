import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtGui import QPixmap
import csv

#ADD IMPORT STATEMENT FOR YOUR GENERATED UI.PY FILE HERE
import Ui_FinalProject
#      ^^^^^^^^^^^ Change this!

#CHANGE THE SECOND PARAMETER (Ui_ChangeMe) TO MATCH YOUR GENERATED UI.PY FILE
class MyForm(QMainWindow, Ui_FinalProject.Ui_MainWindow):
#                         ^^^^^^^^^^   Change this!
    #Initializing variables
    countries = []
    listPopulation = []
    listTotalArea = []
    unsaved_changes = False

    # DO NOT MODIFY THIS CODE
    def __init__(self, parent=None):
        super(MyForm, self).__init__(parent)
        self.setupUi(self)
    # END DO NOT MODIFY

        self.area_units = True # True stands for sq. miles - False stands for Sq. Km
        self.density_units = True # True stands for per sq miles - False stands for per Sq. Km
        self.selectedCountryIndex = 0
        
        #action save to file disabled
        self.actionSave_To_File.setEnabled(False)

        #At startup, with country details area hidden 
        self.labelPopulation.setVisible(False)
        self.labelTotalAreaIn.setVisible(False)
        self.comboBoxMilesOrKilometers.setVisible(False)
        self.groupBoxPopulationDensity.setVisible(False)
        self.labelPercentageText.setVisible(False)
        self.pushButtonUpdatePopulation.setVisible(False)
        self.lineEditInputUserUpdate.setVisible(False)
        
        # ADD SLOTS HERE, indented to this level (ie. inside def __init__)
        self.actionLoad_Countries.triggered.connect(self.LoadCountriesFromFile)
        self.listCountries.currentRowChanged.connect(self.DisplayCountryData)
        self.comboBoxMilesOrKilometers.currentIndexChanged.connect(self.setAreaUnits)
        self.radioButtonPerSqMile.clicked.connect(self.setDensityMiles)
        self.radioButtonPerSqKM.clicked.connect(self.setDensityKilometers)
        self.pushButtonUpdatePopulation.clicked.connect(self.pushedUpdate)
        self.actionSave_To_File.triggered.connect(self.save_action_clicked)
        self.actionExit_2.triggered.connect(self.exit_program)
        
    # ADD SLOT FUNCTIONS HERE
    # These are the functions your slots will point to
    # Indent to this level (ie. inside the class, at same level as def __init__)
    def LoadCountriesFromFile(self):
        self.actionLoad_Countries.setEnabled(False) #After user clicked Load countries, the action is disabled
        self.LoadCountriesListBox()

    def DisplayCountryData(self, selectedCountryIndex): #Index parameter to indentify which index we will use
        #After user clicked a country, display all data
        self.labelPopulation.setVisible(True)
        self.labelTotalAreaIn.setVisible(True)
        self.comboBoxMilesOrKilometers.setVisible(True)
        self.groupBoxPopulationDensity.setVisible(True)
        self.labelPercentageText.setVisible(True)
        self.pushButtonUpdatePopulation.setVisible(True)
        self.lineEditInputUserUpdate.setVisible(True)

        self.Display_theData(selectedCountryIndex)


    def pushedUpdate(self):
        selected_index = self.listCountries.currentRow()
        try:
            self.countries[selected_index][1] = self.lineEditInputUserUpdate.text() #Update the countries list
            self.LoadCountriesListBox() #Reload countries list box
            self.actionSave_To_File.setEnabled(True) 
            self.showMessageBox()
            self.unsaved_changes = True
        except Exception:
            QMessageBox.information(self, "Invalid", "Data is invalid so not updated in memory", QMessageBox.Ok)
            self.countries.clear()
            self.LoadCountriesListBox()
            self.Display_theData(selected_index)
            pass
    
    def save_action_clicked(self):
        self.save_changes_to_file()
        QMessageBox.information(self, "Saved", "Changes were saved to the file", QMessageBox.Ok) #Title "Saved", Message "Changes were saved to the file"
        # toggle the unsaved_changes variable back to False because we no longer have any unsaved changes
        self.unsaved_changes = False

    def exit_program(self):
        QApplication.closeAllWindows() #When user click close windows
#Example Slot Function
#   def SaveButton_Clicked(self):
#       Make a call to the Save() helper function here

    #ADD HELPER FUNCTIONS HERE
    # These are the functions the slot functions will call, to 
    # contain the custom code that you'll write to make your progam work.
    # Indent to this level (ie. inside the class, at same level as def __init__)
    def LoadCountriesListBox(self):
        with open("Files/countries.txt", "r") as myFile:#Open the file as myFile
            fileData = csv.reader(myFile) 

            for line in fileData:
                self.countries.append(line) #Making a list named countries

            for country in self.countries:
                self.listCountries.addItem(country[0]) #display country names in listwidget

            for row in range(len(self.countries)):
                self.listPopulation.append(int(self.countries[row][1])) #Making a population list 

            for row in range(len(self.countries)):
                self.listTotalArea.append(float(self.countries[row][2])) #Making a total area list
            
    def Display_theData(self, selectedCountryIndex):

        self.selectedCountryIndex = selectedCountryIndex

        countryName = self.countries[selectedCountryIndex][0] #To display country name
        population = self.countries[selectedCountryIndex][1] #To display population
        totalArea = self.countries[selectedCountryIndex][2] #To display total Area

        density = float(population) / float(totalArea) #Calculate density in Square per mile
       
        if not self.area_units: 
            totalArea = float(totalArea) * 2.58999 #Calculate total area in Square per KM

        if not self.density_units:
            totalArea = self.countries[selectedCountryIndex][2]
            density = float(population) / float(totalArea) * 2.58999 #Calculate density in Square per KM
            
        imageName = countryName.replace(" ", "_") #Replacing "_" with " " to display the images
        image = QPixmap("Files/Flags/" + imageName +  ".png") #To display flag images file
        sumOfPopulation = sum(self.listPopulation) #To display sum of population
       
        self.labelCountryName.setText(countryName) #Display the country Name
        self.lineEditInputUserUpdate.setText(population) #Display population
        self.labelAreaNumber.setText("{0:.1f}".format(float(totalArea))) #Display totla area
        self.labelPopulationDensity.setText("{0:.2f}".format(density)) #Display density
        self.labelPicture.setPixmap(image) #Display the image
        self.labelPercentageNumber.setText("{0:.4f}%".format(float(population) / sumOfPopulation * 100)) #Display percentage of world population

    def setAreaUnits(self, selectedAreaIndex):

        if selectedAreaIndex == 0: #ComboBox index which is Sq.Miles
            self.area_units = True
        if selectedAreaIndex == 1: #ComboBox index which is Sq.KM
            self.area_units = False

        self.Display_theData(self.selectedCountryIndex) #Callback 

    def setDensityMiles(self):
        self.density_units = True
        self.Display_theData(self.selectedCountryIndex) #Callback 

    def setDensityKilometers(self):
        self.density_units = False

        self.Display_theData(self.selectedCountryIndex) #Callback 

    def showMessageBox(self):          #Title     #Message                                                                   #Ok button of message windows
        QMessageBox.information(self, "Updated", "Data has been updated in memory, but hasn't been updated in the file yet", QMessageBox.Ok)

    def closeEvent(self, event):

        if self.unsaved_changes == True:

            msg = "Save changes to file before closing?"
            reply = QMessageBox.question(self, "Save?", #Title "Save?"
                     msg, QMessageBox.Yes, QMessageBox.No) #Yes button and No button of the message box

            if reply == QMessageBox.Yes: #If the user click Yes button, save change to the file
                self.save_changes_to_file()
                event.accept()

    def save_changes_to_file(self):
        # open the file for writing (w). Make sure it is the same location as the file you opened.
        with open("Files/countries.txt", "w") as myFile:
            #loop through each list within the in-memory people list
            for country in self.countries: #<- refer to each list as person
                # join each value in the person list and write them with a line break
                myFile.write(",".join(country) + "\n")
  
#Example Helper Function
#    def Save(self):
#       Implement the save functionality here

# DO NOT MODIFY THIS CODE
if __name__ == "__main__":
    app = QApplication(sys.argv)
    the_form = MyForm()
    the_form.show()
    sys.exit(app.exec_())
# END DO NOT MODIFY
