# 'Homicides in 50 US cities' RESTful API
This project is a Django-based RESTful API that provides comprehensive endpoints to interact with a dataset of homicide records.
The API allows users to create, read, update, and delete records of homicides, as well as perform various filtering and aggregation operations. 
The primary goal of this project is to demonstrate the ability to implement a robust and flexible API using Django and Django REST Framework, complete with serialization, 
pagination, and unit testing.

## The API contains the following endpoints:

- GET http://127.0.0.1:8080/homicides/by-victim-race/?race=[RACE VALUE]
http://127.0.0.1:8080/homicides/by-victim-race/?race=White
-> This endpoint filters homicides by victim race. Change the `race` parameter to filter by other races (eg. White, Black, Asian, Hispanic).

- GET http://127.0.0.1:8080/homicides/by-gender-age-range/?gender=[GENDER VALUE]&min_age=[AGE VALUE]&max_age=[AGE VALUE]
http://127.0.0.1:8080/homicides/by-gender-age-range/?gender=Male&min_age=20&max_age=30
-> This endpoint filters homicides by victim gender and age range. Adjust the `gender`, `min_age`, and `max_age` parameters as needed.

- GET http://127.0.0.1:8080/homicides/homicides-count-by-city/
http://127.0.0.1:8080/homicides/homicides-count-by-city/
-> This endpoint returns the count of homicides by city.

- POST http://127.0.0.1:8080/homicides/
http://127.0.0.1:8080/homicides/
-> Use the form at the end of this endpoint to add a new homicide record.

- PUT http://127.0.0.1:8080/homicides/{id}/
http://127.0.0.1:8080/homicides/1235/
-> Use the form at the end of this endpoint to update an existing homicide record.

- DELETE http://127.0.0.1:8080/homicides/{id}/
http://127.0.0.1:8080/homicides/1236/
-> Use the 'DELETE' button at the top-right of the endpoint to delete a homicide record.

## Additional Default Endpoints
- GET: List of all Victims
/victims/
-> This endpoint returns a paginated list of all victim records.

- GET: List of all Locations
/locations/
-> This endpoint returns a paginated list of all location records.

- GET: List of all Dispositions
/dispositions/
-> This endpoint returns a paginated list of all dispositions records.

- GET: List of all homicides
/homicides/
-> This endpoint returns a paginated list of all homicide records.

## Application Details:
- Python Ver = 3.12
- Django Ver = 4.2
- Django Rest Framework (DRF) Ver = 3.14
