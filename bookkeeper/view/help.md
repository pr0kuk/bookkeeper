# GUI Help
## Description
Educational project for a course on the practice of programming in Python  
Simple application for monitoring personal finances (home accounting)  

### Technical features
The backend is based on sqlite3  
The frontend is based on PySide6  

## Main Window
### Expenses
Here is a table of your expenses. To delete an entry, right-click on the desired entry and select delete.  
To add a new entry, right-click on the empty space and click add.  
A category window will open, you need to select the one you need and click the Select button.  
All fields of this table can be edited by double-clicking on the required field with the left mouse button.  

### Budget
This table has two columns.  
The amount column shows the total of all your expenses for the specified time period.  
In the budget column you can put the value you want to spend over a specified period of time.  

## Category Window
This window contains a tree of categories.  
To add a new category, you need to right-click on an existing category that you want to make a parent,  
or click the add category button if you want to make a category without a parent, and click add.  
To delete an existing category, you need to right-click on it and click delete.  
Deleting a category will lead to a change in the category of expenses recorded for it to the category of the parent,  
or to the category before this one, if it does not have a parent.  
Clicking the select button will create a new expense for the specified category and close the category window.

## Author
Aleksei A. Shcherbakov, M01-305в  
MIPT, Dolgoprudny  
Apr, 2024  