creating virtual environment:
step 1:

pip install virtualenv

step 2:

virtualenv venv --python=python3.6

step 3:

source venv/bin/activate

or 

./venv/Scripts/activate.bat


**************************

pip install flask-RESTful

pip install flask-JWT   (JSon Web token)

pip install Flask-SQLAlchemy

pip freeze

*******************************************************

step 1:

create a user:

http://localhost:5000/register

{
	"username": "venkatram",
	"password": "venkat"
}

step 3:

Create a store

localhost:5000/store/Big Bazar

step 4:

Fetch stores along with items

localhost:5000/store/Big Bazar

step 5:

generate JWT token
http://localhost:5000/auth

{
	"username": "venkatram",
	"password": "venkat"
}

step 6:

creating item

http://localhost:5000/item/chair

{
	"price": "19.20"
}

step 7: 
get request:
http://localhost:5000/item/chair

step 8: 
get request:
http://localhost:5000/items

step 9: 
delete request:
http://localhost:5000/item/chair

step 10: 
put request:
http://localhost:5000/item/chair

{
	"price": "12.98"
}
