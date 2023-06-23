# Django REST API Social Network

This project is a simple REST API based social network built using Django and Django REST Framework. It allows users to sign up, create text posts, view, like, and unlike other users' posts. The API also enriches the user with geolocation data based on the IP address used during signup and checks if the signup date coincides with a holiday in the user's country.

## Installation

Clone the repository:
```
git clone https://github.com/siddythings/abstractapi.git
```

Change into the project directory:
```
cd abstractapi
```

Install the dependencies:
```
pip install -r requirements.txt
```

Set up the database:
```
python manage.py migrate
```

Create a superuser (admin) account:
```
python manage.py createsuperuser
```
## Configuration

Obtain API keys:

 - Abstract API: Register for an account and obtain an API key from [Abstract API](https://www.abstractapi.com/).

Update the settings:

- Open `social_network/settings.py` and replace `GEOLOCATION_ABSTRACT_API_KEY and
HOLIDAY_ABSTRACT_API_KEY` with your Abstract API key.

## Usage

Start the development server:
```
python manage.py runserver
```

2. Access the API endpoints:

- Open your browser or API testing tool and navigate to `http://localhost:8000/api/`.

3. API Endpoints:
```
- User Signup:
- 
  - Route: POST `/api/register/`
  - Request body: {
    "username":"admin2",
    "password": "12345678@#",
    "password2": "12345678@#",
    "email":"admin11@gmail.com"
}
```
```
- User Login:
  - Route: POST `/api/login/`
  - Request body: {
    "password": "12345678@#",
    "email":"admin11@gmail.com"
}
  - Response: JWT token
```
```
- Get User Data:
  - Route: GET `/api/users/{user_id}/`
  - Authorization header: Bearer {JWT-token}
```
```
- Create Post:
  - Route: POST `/api/posts/`
  - Request body: { "content": "This is my post." }
  - Authorization header: Bearer {JWT-token}
```
```
- Read Post:
  - Route: GET `/api/posts/{post_id}/`
  - Request body: {"content":"Hello"}
```
```
- Update Post:
  - Route: PUT `/api/posts/{post_id}/`
  - Request body: { "content": "Updated post content." }
  - Authorization header: Bearer {JWT-token}
```
```
- Delete Post:
  - Route: DELETE `/api/posts/{post_id}/`
  - Authorization header: Bearer {JWT-token}
```
```
- Like Post:
  - Route: POST `/api/posts/{post_id}/like/`
  - Authorization header: Bearer {JWT-token}
```
```
- Unlike Post:
  - Route: POST `/api/posts/{post_id}/unlike/`
  - Authorization header: Bearer {JWT-token}
```


** API Test

```
python manage.py test
```