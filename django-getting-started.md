# Getting Started
* Starting a new django project
  * Start Conda Environment
  * Download Django (If not already done)
    * conda install django
  * Start new django project
    * django-admin startproject digitalmarket(Name can vary)


# Getting the database Started
* Start a new database in elephantsql
* Make settings changes for settings.py so that it will point to correct database
* Migrate to database
  * navigate to "src"
  * python manage.py migrate


# CRUD

Create -- add item to database -- POST
Retrieve -- get item (s) from the database -- detail_view -- GET
Update -- Make changes/updates to the item(s) in the database -- PATCH / PUT / POST
Delete -- delete item from database -- DELETE

List -- list all items from database (or a queryset)
Search -- search items from the database


#Common Django errors
**raise TypeError('view must be a callable or a list/tuple in the case of include().')
TypeError: view must be a callable or a list/tuple in the case of include().**
