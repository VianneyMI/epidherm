# Epidherm Test

This repo host my answers to the take-home test received from the CTO

## Description

This repo contains two sub-folders :

1. web_app_demo contains a demo application to demonstrate my answers to questions one and four
2. Q2and3 as the name implies includes a notebook showcasing my answer to question one

## Web App

### Dependencies

All the dependencies are included in the requirements.txt file

### Init

* Install the dependencies
* Create the database by launching the database builder with the following command

  ``` py build_database.py ```

* Launch the server with

 ``` py server.py ```

* Navigate to the localhost:/5000 for the frontend. You can also visualize the API configuration at localhost:5000/api/ui

### Functionalities

This app leverages a REST API configured with swagger.

The REST API accepts and outputs JSON, it enables role-based authentication
and sets som rate-limits for certain routes.
The pagination has not been implemented but could have been done with Flask_Paginate module.
I checked the documentation. It doesn't seem to complicated. However, it was a bit hard to integrate with my JavaScript MVC setup.

The demo app consists mainly of three pages, a home page that lists all materials grouped by family
a family page that allows an admin user to create, update or delete a family, a materials page that allows a registered user to do the same for materials.

On any page a double click on a cell will lead you to the view corresponding to the element i.e. the details of a family or of a material.

On the family and material page, a single click on one of the element will retrieve the information from that element and display them in the editor.

On the family page, after having selected a family, clicking on the button <button> calculate </button> will call a function that implements my answer to **question one** about the count and the sort of materials by family and display the results in the table.

### Settings

In order to test the functionality above, you will need to log in as an admin, for this you can use the testing below credentials :

* username: admin
* password: Password1

## (Jupyter) Notebook

For question two and three, I chosed to used a Notebook.

For the purpose of the question, I created dummy data matching the structure described in the example.

The approach I took was to deserialize the data using the python json and pandas libraries and then to leverage the pandas toolkit for ordering, filtering sorting ...

Here is my process:

1. I read the file and store the content in a variable called data using ``` open ```
2. I convert the json data to a list of python dictionaries using ``` json.loads() ```
3. I convert the list of dictionaries into a pandas dataframe using ```pandas.json_normalize() ```
4. I do my manipulations over the dataframe using the pandas toolkit
5. I convert back the dataframe to a string in the json format with ```to_json() ```

I did not stricly implemented code for Q3 but the process would be the same. Pandas offers functionalities for double grouping/sorting.

## Environment

I use visual studio code with the following settings :

```javascript

{
    "python.pythonPath": "C:\\Program Files\\Python37\\python.exe",
    "python.linting.pylintArgs": [

        "--init-hook=import sys; sys.path.append('./web_app_demo')",
        "--generated-members", "flask_sqlalchemy",
        "--ignored-classes=scoped_session"
    ],
}



```