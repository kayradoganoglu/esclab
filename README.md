# ESClab v0.2.3 README
## Dependencies:
  **PyQt6** >= *6.7.1*<br>
  **PyQt6-WebEngine** >= *6.7.0*<br>
  **numpy** >= *2.0.2*<br>
  **pandas** >= *2.2.2*<br>
  **plotly** >= *5.24.0*<br>
  **matplotlib** >= *3.4.3*<br>
*Please install packages using* **pip**.<br>
Use command:<br>
**pip install numpy pandas matplotlib plotly pyqt6 pyqt6-webengine**<br>
**python -m pip install spicy**<br>
*After package installation* run **main.py**

**Since the JS Library is taken from the internet, some graphics in the code may not work when not connected to the internet.**

## How to use:
### Main Page:
#### Load Data:
On Main Window, Use "Select Folder" Button to navigate to ESC Log directory that you desire to<br>
open. The directory needs to include "AT LEAST 1" of esc{esc number}.csv file.<br>
Otherwise "Load Data" button will not be available.<br>
After selecting directory, press "Load Data" button, On the console loaded esc{number} will be shown.<br>
This  action Will create a "Raw Data" Tab.
#### Raw Data:
This Tab will include original test data. In this tab View options will be visible.<br>
From here users can navigate to view options or "Process Tool"<br>
You can close the tab to erase loaded data. Any other processed data will not be affected with this action<br>
#### Known Issues:
1. Loading different directories: Before loading different test data to the program<br>
please close the "Raw Data" tab to erase previous files. This creates unwanted plots to include<br>
in "Process Tool" when not all 4 .csv files are loaded.
### Individual View Page
This Page will display tabs to user, how many have been loaded, Every tab will include a Plot<br>
In those plots every attribute of the data foreach ESC will be shown.
#### Known Issues:
This Utility has no outstanding issues.
### Comparison View Page
This Page will display selections on the left side and a single plot on the right side.<br>
Every selection represents an attribute of loaded data, on the plot all ESCs are plotted together<br>
alongside the selected attribute.<br>
Whenever user selects an attribute according plot will be shown on the right side.<br>
This page is scalable on the screen and fullscreen is available.
#### Known Issues:
This Utility has no outstanding issues.
### Combined Comparison View Page
This page will display a canvas on left, and checkboxes for each attribute on left.<br>
For every toggled button, on the canvas according plot will appear, alongside the canvas. Column size is limited to 3.<br>
Displayed plots are X-Axis Locked to each other.
#### Known Issues:
Previously, deselecting the last remaining selected checkbox would cause the application to crash due to having no options selected. This issue has now been resolved by implementing a checkbox validation mechanism that prevents the action and displays a warning via QMessageBox. This ensures UI stability and eliminates the crash risk.
### Process Tool:
This tool is accessible after loading data to enable users to execute post process operations.<br>
User needs to select the test type on top right corner dropbox.(default=Step Test)<br>
Loaded data will be plotted (at least 1) and requires user input to select a span alongside the plots at desired<br>
indexes, Crop Button will be enabled after Span selection numbers and enabled ESC numbers are matched.<br>
After crop operation console will log cropped indexes and Test button will be enabled.<br>
After clicking test button console will log according status, when completes, in main window according tab will be<br>
enabled to view
#### Known Issues:
1. SPANNED PLOTS AND SELECTED ESC NEEDS TO MATCH: if not, test button will be enabled anyway and output no data.<br>
cause no crash on this screen but on main page tab, when user tries to open no data view pages app will crash.
2. CHOOSE CORRECT TEST: when selected span data is not suitable for selected test<br>
i.e. selected span contains flight test, selected test is step test, application will crash.
### Save Test Button:
When clicked it will create a directory inside selected directory and include post processed data as .csv files.<br>
For step test only, inside created folder there will be another subfolder including "Summary" files for each esc.<br>

