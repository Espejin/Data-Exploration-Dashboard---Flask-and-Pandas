# Data-Exploration-Dashboard - Flask-and-Pandas
Data Exploration Dashboard - Flask and Pandas

# Datasource:


The database was extracted from the annual survey carried out among participating developers of the Stack Overflow website.

This survey aims to analyze users, in order to get an idea of ​​the current technology field. The database is loaded by the SO team, making all information anonymous with respect to the user who generated the information. This survey is available in the following link.

https://survey.stackoverflow.co


# Dataset features:


The dataset provided by Stack Overflow Team has the following characteristics:

CSV Format.
89,183 rows.
82 columns.
Irregular Datatypes - Some categorical fields.
The mayority of fields wasn't mandatory.
A lot of null information.
Survey Data!


With all this in mind, what type of information does the data set contain?

Salary.
Developer Type.
Industry.
Age.
Work Experience.
Professional Coding Experience.
Time Coding
Principal Web Frameworks used.
Principal Databases used.


# Objectives:


- Explore the usage of Pandas for filtering and data processing.
- Explore the usage of a full Python backend using Flask.


# Pipeline:

![Alt text](relative%20path/to/img.jpg](https://github.dev/Espejin/Data-Exploration-Dashboard---Flask-and-Pandas/blob/main/app/static/images/pipeline.png?raw=true "Title")

# Data Processing Considerations:


Cause of the nature of the data. It needed a lot of work to give a good database to work:

- Delete of NULL values, if the data is useless.
- Field Data Regularization. (Dev Type, Org Size, YearsCodePro, WorkExp, ConvertedCompYearly)
- Second Delete of data.


# Data Storage Considerations:

- General DB Normalization.
- Only not NULL info it was inserted to the database.

Data Analyitics Considerations:


About the analyisis of data. We are going to usea a Flask app as a dashboard. This as such has its considerations:

- Flask is a full Python web framework.
- It is different from traditional developments.
- Some libraries need special requirements to work. (matplotlib.use('Agg'))


# Libraries:

- Pandas.
- Numpy.
- Seaborn.
- Flask.
- base64.
- IO.

# Repository Data:
- Flask App
- DBB SQLite
- Python Jupyter Notebook of Data Transformation
