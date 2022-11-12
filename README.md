# CZ4031-Database-Project02

CZ4031-Database-Project02 PostgreSQL

### PostgreSQL

1. Ensure that you have setup PostgreSQL with TPC-H Database created.
2. You may use tbl_trim.py to convert the .tbl files to .csv files to import the data into PostgreSQL.

### Visual Studio Code

Open project and Terminal. Install the following libraries

1. pip install treelib
2. pip install psycopg2
3. pip install sqlparse
4. pip install json

### Instruction Guide to Run the Software

1. Run the 'project.py' file OR execute this command in the terminal <PATH OF PYTHON DIRECTORY>\python.exe -u "<PATH OF PROJECT FOLDER>\project.py"
2. A window will pop up. Enter your query into the query input box (Note: 12 test queries are provided inside the ‘Queries’ folder under the main project folder)
3. Click the ‘Run’ button directly and leave the checkboxes in default selection, the QEP displayed is the best QEP generated by the ProgresSQL system. In this case, 11 types of joins are enabled).
4. You can hover or click on any nodes of the tree to view the annotations which include the costs.
5. Similarly, you can also run the input query by unchecking the checkboxes to select from the 4 types of join algorithms we offered. Then repeat step 3 and step 4 to view the corresponding QEP & AQP.
