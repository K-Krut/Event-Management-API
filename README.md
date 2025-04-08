# Task:
Develop a Django REST-Api for Event Management 
The primary goal of this task is to create a Django-based REST-Api that manages events (like conferences, meetups, etc.). The application will allow users to create, view, update, and delete events. It should also handle user registrations for these events.

##### Key Requirements:
- Design an Event model with fields such as title, description, date, location, and organizer.
- Implement CRUD (Create, Read, Update, Delete) operations for the Event model.
- Basic User Registration and Authentication.
- Event Registration
- API documentation
- Docker
- Readme file

##### Bonus Points:
- Implement an advanced feature like event search or filtering.
- Add a feature for sending email notifications to users upon event registration.


# Realization

## Features

- User auth with JWT tokens
- CRUD operations for notes with  version tracking
- AI summarization of notes (via OpenAI API)
- Note analytics
- Unit and integration tests

## Project Structure

```
.
├── Dockerfile
├── README.md
├── manage.py
├── requirements.txt
│
├── EventManagementAPI
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── events
│   ├── admin.py
│   ├── apps.py
│   ├── constants.py
│   ├── decorators.py
│   ├── management
│   │   └── commands/
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views/
│       ├── mixins.py
│       └── views.py
└── users
    ├── admin.py
    ├── apps.py
    ├── management
    │   └── commands/
    ├── migrations/ 
    ├── models.py
    ├── serializers.py
    ├── tests.py
    ├── urls.py
    ├── utils.py
    └── views.py
```


## Implementation 

### Authentication

- Created registration / login / logout / refresh tokens functional 
- for secure used jwt tokens (it is required for all protected endpoints)
- passwords are saving in db in hashed form

### Events

- Only authenticated users have access for events functional, except only all users can see events list and partly event details
- Users can create / delete / list / get / update (fully / partially) events
- Created also endpoint for listing event participants
- Users can also list events where they are already registered and events that they organized
- Also there was created endpoints for listing event types / formats / statuses
 

---

## Local Dev

1. ! Before launch please create .env file with this structure:
```
SECRET_KEY=
DEBUG=  
ALLOWED_HOSTS=
  
AWS_ACCESS_KEY_ID=  
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME= 
AWS_S3_SIGNATURE_NAME= 
AWS_S3_REGION_NAME= 
AWS_S3_FILE_OVERWRITE=  
AWS_DEFAULT_ACL=  
AWS_S3_VERITY=  
  
AWS_BUCKET_URL=

  
POSTGRES_DB=  
POSTGRES_USER=  
POSTGRES_HOST=
POSTGRES_PORT=  
POSTGRES_PASSWORD= 
  
  
ACCESS_TOKEN_LIFETIME=
REFRESH_TOKEN_LIFETIME=
```
1. Install dependencies

```bash
pip install -r requirements.txt
```

2. Run the app
```bash
python manage.py migrate
python manage.py runserver
```


## API Endpoints

- `/` => `/api/docs/`
- `/api/schema/`
- `/api/docs/`
- `/admin/

- POST `/api/v1/auth/register`
- POST `/api/v1/auth/login`
- POST`/api/v1/auth/logout`
- POST`/api/v1/auth/token/refresh`

- GET `/api/v1/events/` 
- GET `/api/v1/events/my/` 
- GET `/api/v1/events/my/organized/` 
- POST `/api/v1/events/create/` 
- GET `/api/v1/events/{id}/` 
- PUT `/api/v1/events/{id}/` 
- PATCH `/api/v1/events/{id}/` 
- DELETE `/api/v1/events/{id}/` 
- GET `/api/v1/events/{id}/participants/` 

- GET `/api/v1/events/statuses/` 
- GET `/api/v1/events/formats/`
- GET `/api/v1/events/types/`


---

## API Endpoints Detailed Description

Fields Labels:

-[u] - field value must be unique
-[?] - field is optional


#### `/admin/
Access to admin panel 
Superuser credentials will be send separately 

#### `/api/docs/`

Swagger documentation 

#### POST `/api/v1/auth/register`

Endpoint for new Users registration

Request Body Fields:
1. -[u] email - user's email
2. first_name - user's first name
3. last_name - user's last name
4. password - user's password
5. -[?] avatar - user's avatar

Response Status:
- 201 - success
- 400 - validation error
- 400 - user's email isnt unique
- 500 - server error

Request Example: 
```json
{
	"email": "user12@gmail.com",
	"first_name": "user1",
	"last_name": "test",
	"password": "passworduser1",
	"avatar": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAp8AAAKdCA..."
}
```

Response Example:
```json
{
	"id": 14,
	"email": "user12@gmail.com",
	"first_name": "user1",
	"last_name": "test",
	"email_notifications": true,
	"avatar_url": "https://event-management-api.s3.amazonaws.com/users/profile-pictures/avatar_tl78Ndh.png"
}
```


#### POST `/api/v1/auth/login`

Endpoint for User's Authorization

Request Body Fields:
- email - user's email
- password - user's password

Response Status:
- 200 - success
- 400 - invalid credentials
- 500 - server error

returning access_token, refresh_token and user's info
access_token - available for 1 day
refresh_token - available for 7 days


Request Example: 
```json
{
	"email": "user8@gmail.com",
	"password": "passworduser89"
}
```

Response Example:
```json
{
	"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ0MjAzNzcwLCJpYXQiOjE3NDQxMTczNzAsImp0aSI6IjMxNThlMTY3M2E5YjRmYTZiMWY5NmMxNzcxNjg2ZDIzIiwidXNlcl9pZCI6MX0.jEqILJJO6Zw9kZRxpbq7THC2IbrtR5LWRNbBc5usTcg",
	"refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NDcyMjE3MCwiaWF0IjoxNzQ0MTE3MzcwLCJqdGkiOiIxMGE4MjNkNDUwNGE0MDNmODAwYjk4ZGQ3MzczZWM4ZSIsInVzZXJfaWQiOjF9.5_O6mPOlSVuQf5bhpvQrIsugwbew-DvE05aU-ySpwcY",
	"user": {
		"id": 1,
		"email": "katiakrut448@gmail.com",
		"first_name": "kate",
		"last_name": "krut",
		"email_notifications": true,
		"avatar_url": "https://event-management-api.s3.amazonaws.com/users/profile-pictures/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA_%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0_2025-03-27_%D0%B2_20_MPCGNPi.27.52.png"
	}
}
```

#### POST `/api/v1/auth/logout`

Endpoint for user's logout. Needed for blacklisting refresh_token

Request Body Fields:
- refresh_token - user's refresh_token

Response Status:
- 200 - success
- 400 - invalid token / refresh_token field is missing in the request body
- 500 - server error

Request Example: 
```json
{
	"refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDY5Mjk3MywiaWF0IjoxNzQwMDg4MTczLCJqdGkiOiIzMmQ2ZTE3MWQyZDE0MTUzOWYwYTg2YTM5NGUzZTc2NyIsInVzZXJfaWQiOjh9.CsDqDUHhuOLCyARV0zDDznrGTbA5ign24jZysnQaeeY"
}
```

Response Example:
```json
{
    "errors": "Token is invalid or expired"
}
```

#### POST `/api/v1/auth/token/refresh`

Edpoint for refreshing acccess_token

Request Body Fields:
- refresh - user's refresh_token

Response Status:
- 200 - success
- 401 - invalid token
- 500 - server error


returning access_token, refresh_token
access_token - available for 1 day
refresh_token - available for 7 days


Request Example: 
```json
{
	"refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDY5Mjk3MywiaWF0IjoxNzQwMDg4MTczLCJqdGkiOiIzMmQ2ZTE3MWQyZDE0MTUzOWYwYTg2YTM5NGUzZTc2NyIsInVzZXJfaWQiOjh9.CsDqDUHhuOLCyARV0zDDznrGTbA5ign24jZysnQaeeY"
}
```

Response Example:
```json
{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQwMTc0NTczLCJpYXQiOjE3NDAwNzEyOTMsImp0aSI6IjhlYWMwY2ExNTI2MDQ2YWQ4NjcxMmVkYWUxNWY5MmRiIiwidXNlcl9pZCI6OH0.-U0pL11xqewU2fmuZ7pwNsBigYgL-yZoayeZhIaF07E",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MDY5Mjk3MywiaWF0IjoxNzQwMDg4MTczLCJqdGkiOiIzMmQ2ZTE3MWQyZDE0MTUzOWYwYTg2YTM5NGUzZTc2NyIsInVzZXJfaWQiOjh9.CsDqDUHhuOLCyARV0zDDznrGTbA5ign24jZysnQaeeY"
}
```


## Events Listing Endpoints
### Event Response Fields:

- id - event's id
- title - event's name
- date_start - date and time of event's start
- date_end - date and time of event's end
- status - event's status
- is_registered - is displaying id current user is already registered for the event

### Pagination:
- default page_size - 30
- max page_size - 100

### Ordering:

##### Default ordering:
- date_start - in reverse order
- status

##### Fields available for ordering:
- title
- date_start
- date_end
- status
- type

### Search Fields:
- title

#### GET `/api/v1/events/`

Endpoint for getting events list

Bearer Token is not required

But if token is passed backend will check if current user is already registered (is_registered field) for events in the list otherwise is_registered will be always false

Endpoint is listing only events with status Active or Done (ones with Draft and Canceled statuses are not displaying)



Response Example:
```json
{
    "count": 98,
    "next": "http://127.0.0.1:8000/api/v1/events/?page=2",
    "previous": null,
    "results": [
        {
            "id": 98,
            "title": "Agree activity build meet response likely.",
            "date_start": "2025-04-01T00:00:00Z",
            "date_end": "2025-04-06T00:00:00Z",
            "status": {
                "id": 2,
                "name": "Active"
            },
            "is_registered": false
        },
        {
            "id": 85,
            "title": "While key international.",
            "date_start": "2025-04-01T00:00:00Z",
            "date_end": "2025-04-05T00:00:00Z",
            "status": {
                "id": 2,
                "name": "Active"
            },
            "is_registered": false
        },
        {
            "id": 143,
            "title": "Site might focus party.",
            "date_start": "2025-04-01T00:00:00Z",
            "date_end": "2025-04-08T00:00:00Z",
            "status": {
                "id": 2,
                "name": "Active"
            },
            "is_registered": false
        },
        ...
    ]
}
```



#### GET `/api/v1/events/my/`

Endpoint for getting all user's events list

Returns events were user is registered

**Bearer Token is required**


Response Example:
```json
{
    "count": 30,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 98,
            "title": "Agree activity build meet response likely.",
            "date_start": "2025-04-01T00:00:00Z",
            "date_end": "2025-04-06T00:00:00Z",
            "status": {
                "id": 2,
                "name": "Active"
            },
            "is_registered": true
        },
        {
            "id": 116,
            "title": "Military alone company manager population state set business.",
            "date_start": "2025-04-03T00:00:00Z",
            "date_end": "2025-04-07T00:00:00Z",
            "status": {
                "id": 6,
                "name": "Finished"
            },
            "is_registered": true
        },
        {
            "id": 68,
            "title": "Quite car store right yourself national.",
            "date_start": "2025-04-04T00:00:00Z",
            "date_end": "2025-04-07T00:00:00Z",
            "status": {
                "id": 4,
                "name": "Ongoing"
            },
            "is_registered": true
        },
        ...
    ]
}
```


#### GET `/api/v1/events/my/organized/`


Endpoint for getting all user's events list

Returns events were user is organizer

**Bearer Token is required**


Response Example:
```json
{
    "count": 11,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 36,
            "title": "Air oil join girl each.",
            "date_start": "2025-04-06T00:00:00Z",
            "date_end": "2025-04-11T00:00:00Z",
            "status": {
                "id": 2,
                "name": "Active"
            },
            "is_registered": true
        },
        {
            "id": 51,
            "title": "Pull drive study seven popular offer again home.",
            "date_start": "2025-04-07T00:00:00Z",
            "date_end": "2025-04-14T00:00:00Z",
            "status": {
                "id": 2,
                "name": "Active"
            },
            "is_registered": true
        },
        {
            "id": 88,
            "title": "Officer significant mention into.",
            "date_start": "2025-04-13T00:00:00Z",
            "date_end": "2025-04-20T00:00:00Z",
            "status": {
                "id": 2,
                "name": "Active"
            },
            "is_registered": true
        },
        ...
    ]
}
```


#### POST ``/api/v1/events/create/``

Endpoint for creating event

Only registered users can create events => Bearer Token is required

### Body Fields:

- title - event's name
- description - event's details
- date_start - date and time of event's start. date_start must be earlier than date_end
- date_end - date and time of event's end
- status - event's status
- type - event's type
- format - vent's format
- -[?] location - if is_online value is true location field should not be passed, otherwise location is required
    

Other Fields Description
- organizer - event's organizer. is set automatically as user who is creatting the event

### Response Status:
- 201 - success  
    in response will be event details
- 500 - server error
- 401 - if passed invalid token    
- 400 - invalid fields values

Request Example: 
```json
{
	"title": "AI & Future Tech Conference",
	"description": "A conference exploring the future of artificial intelligence and emerging technologies.",
	"date_start": "2025-05-15T10:00:00Z",
	"date_end": "2025-05-17T17:00:00Z",
	"location": "Berlin, Germany",
	"status": 2,
	"type": 1,
	"format": 2
}
```

Response Example:
```json
{
    "id": 154,
    "title": "AI & Future Tech Conference",
    "date_start": "2025-05-15T10:00:00Z",
    "date_end": "2025-05-17T17:00:00Z",
    "description": "A conference exploring the future of artificial intelligence and emerging technologies.",
    "location": "Berlin, Germany",
    "status": {
        "id": 2,
        "name": "Active"
    },
    "format": {
        "id": 2,
        "name": "Offline"
    },
    "type": {
        "id": 1,
        "name": "Conference"
    },
    "is_registered": true,
    "participants_number": 1,
    "organizer": {
        "id": 1,
        "email": "katiakrut448@gmail.com",
        "first_name": "kate",
        "last_name": "krut",
        "avatar_url": "https://event-management-api.s3.amazonaws.com/users/profile-pictures/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA_%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0_2025-03-27_%D0%B2_20_MPCGNPi.27.52.png"
    }
}
```


#### GET `/api/v1/events/{id}/`

Endpoint for retreiveing Event's detailed information

Only authenitificated users can get event's details => Bearer Token is reqired

### Query params:
- id - event'd id

### Response Fields Description:
- id - event's id
- title- event’s title
- date_start- date and time of the event's start
- date_end - date and time of the event's end
- description - event's description
- location - event's location (for offline events)
- status - status of the event. Possible values: Active, Draft, Done, Canceled
- type - event's type. Possible values: Public, Private
- is_registered - indicates if the current user is registered for the event
- participants_number - number of users already registered for the event
- organizer - organizer’s details
    - id - user id of the organizer
    - email - organizer's email
    - first_name - organizer's first name
    - last_name - organizer's last name
    - avatar_url - organizer's aws avatar url


### **Response Status Codes and Descriptions:**
- 200 - success
- 404 - event with the given id was not found
- 401 - invalid token
- 500 - server error
- 503 - request timeout

Response Example:
```json
{
    "id": 38,
    "title": "Finally skill heavy stuff whole finally.",
    "date_start": "2025-04-27T00:00:00Z",
    "date_end": "2025-04-30T00:00:00Z",
    "description": "Long she purpose term. Maintain capital generation campaign high improve real. Feeling cell fall interest policy analysis. Hold hand red. How voice trade something. Difficult officer somebody mouth. Education analysis yet former American travel development. Alone team travel issue player. Choice stand week. Tend read certainly military we PM. Whose wait arrive by high owner. Play agent campaign whether large religious item. Range oil should now. Buy all ability list south room most. Last modern mention force seek organization. Try prove behind fill various then finally walk. Degree seven nor statement house paper amount. Now gas ground sister skin those. Already painting nothing month pick.",
    "location": "72531 Garcia Mountains\nSuarezland, FL 28018",
    "status": {
        "id": 4,
        "name": "Ongoing"
    },
    "format": {
        "id": 3,
        "name": "Hybrid"
    },
    "type": {
        "id": 3,
        "name": "Webinar"
    },
    "is_registered": true,
    "participants_number": 70,
    "organizer": {
        "id": 1,
        "email": "katiakrut448@gmail.com",
        "first_name": "kate",
        "last_name": "krut",
        "avatar_url": "https://event-management-api.s3.amazonaws.com/users/profile-pictures/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA_%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0_2025-03-27_%D0%B2_20_MPCGNPi.27.52.png"
    }
}
```

#### PUT `/api/v1/events/{id}/```

Endpoint for full updating event information (all required fields must be passed)

Only autheniticated users and ONLY event organier can delete event => Bearer Token is reqired

### Conditions
- user must be event's organizer
- finished events cant be updated


Request Example: 
```json
{
	"title": "Updated Event Title",
	"description": "This is an updated description of the event.",
	"date_start": "2025-04-20T10:00:00Z",
	"date_end": "2025-04-20T12:00:00Z",
	"location": "Main Hall A",
	"status": 1,
	"format": 2,
	"type": 3
}
```

Response Example:
```json
{
    "id": 34,
    "title": "Updated Event Title",
    "date_start": "2025-04-20T10:00:00Z",
    "date_end": "2025-04-20T12:00:00Z",
    "description": "This is an updated description of the event.",
    "location": "Main Hall A",
    "status": {
        "id": 1,
        "name": "Draft"
    },
    "format": {
        "id": 2,
        "name": "Offline"
    },
    "type": {
        "id": 3,
        "name": "Webinar"
    },
    "is_registered": true,
    "participants_number": 2,
    "organizer": {
        "id": 1,
        "email": "katiakrut448@gmail.com",
        "first_name": "kate",
        "last_name": "krut",
        "avatar_url": "https://event-management-api.s3.amazonaws.com/users/profile-pictures/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA_%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0_2025-03-27_%D0%B2_20_MPCGNPi.27.52.png"
    }
}
```


#### PATCH `/api/v1/events/{id}/`

Endpoint for partial updating event information

Only autheniticated users and ONLY event organier can delete event => Bearer Token is reqired

### Conditions
- user must be event's organizer
- finished events cant be updated


Request Example: 
```json
{
	"title": "UPDATED PATCH API TEST CREATION",
	"description": "UPDATED PATCH test tatatat lalala"
}
```

Response Example:
```json
{
    "id": 34,
    "title": "UPDATED PATCH API TEST CREATION",
    "date_start": "2025-04-20T10:00:00Z",
    "date_end": "2025-04-20T12:00:00Z",
    "description": "UPDATED PATCH test tatatat lalala",
    "location": "Main Hall A",
    "status": {
        "id": 1,
        "name": "Draft"
    },
    "format": {
        "id": 2,
        "name": "Offline"
    },
    "type": {
        "id": 3,
        "name": "Webinar"
    },
    "is_registered": true,
    "participants_number": 2,
    "organizer": {
        "id": 1,
        "email": "katiakrut448@gmail.com",
        "first_name": "kate",
        "last_name": "krut",
        "avatar_url": "https://event-management-api.s3.amazonaws.com/users/profile-pictures/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA_%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0_2025-03-27_%D0%B2_20_MPCGNPi.27.52.png"
    }
}
```


#### DELETE `/api/v1/events/{id}/`

Endpoint for deleting event
Only authenitificated users and ONLY event organier can delete event => Bearer Token is reqired

### Conditions:
- user must be event's organizer
- finished events cant be deleted
- events with status Active and registered participants (except organizer) cant be deleted

### Query params:
- id - event'd id

### **Response Status Codes and Descriptions:**
- 204 - success
- 400 - conditions for deleting event are not met
- 404 - event with the given id was not found
- 401 - invalid token
- 403 - access forbidden
- 500 - server error
- 503 - request timeout

#### GET `/api/v1/events/{id}/participants/`

Endpoint for retreiveing Event's participants information

Only authenitificated users and ONLY event organier can get event's information about participants => Bearer Token is reqired

### Query params:
- id - event'd id

### Response Fields Description:
- participants_number - number of all participants without organizer
- organizer - organizer’s details
    - id - user id of the organizer
    - email - organizer's email
    - first_name - organizer's first name
    - last_name - organizer's last name
    
- participants - all participants data
    - user - participant's details
        - id - user id of the organizer
        - email - organizer's email
        - first_name - organizer's first name
        - last_name - organizer's last name
    - registered_at - datetime of user's registration for the event

### **Response Status Codes and Descriptions:**
- 200 - success
- 404 - event with the given id was not found
- 401 - invalid token
- 403 - access forbidden
- 500 - server error
- 503 - request timeout


Response Example:
```json
{
    "participants_number": 69,
    "organizer": {
        "id": 1,
        "email": "katiakrut448@gmail.com",
        "first_name": "kate",
        "last_name": "krut",
        "avatar_url": "https://event-management-api.s3.amazonaws.com/users/profile-pictures/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA_%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0_2025-03-27_%D0%B2_20_MPCGNPi.27.52.png"
    },
    "participants": [
        {
            "user": {
                "id": 19,
                "email": "ewelch@example.net",
                "first_name": "Sabrina",
                "last_name": "Marks",
                "avatar_url": "https://event-management-api.s3.amazonaws.com/users/profile-pictures/avatar_i3yqRli.jpeg"
            },
            "registered_at": "2025-04-07T16:51:52.898728Z"
        },
        {
            "user": {
                "id": 65,
                "email": "shannon73@example.org",
                "first_name": "Sara",
                "last_name": "Allen",
                "avatar_url": "https://event-management-api.s3.amazonaws.com/users/profile-pictures/avatar_JyP2Mzf.jpeg"
            },
            "registered_at": "2025-04-07T16:51:52.844617Z"
        },
        {
            "user": {
                "id": 105,
                "email": "annette86@example.com",
                "first_name": "Taylor",
                "last_name": "Rodriguez",
                "avatar_url": "https://event-management-api.s3.amazonaws.com/users/profile-pictures/avatar_ZLt8mbr.jpeg"
            },
            "registered_at": "2025-04-07T16:51:52.792264Z"
        },
        ...
    ]
}
```




#### GET `/api/v1/events/statuses/`


Endpoint for getting all event's statuses

**Bearer Token is required**


Response Example:
```json
{
    "count": 6,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Draft"
        },
        {
            "id": 2,
            "name": "Active"
        },
        {
            "id": 3,
            "name": "Upcoming"
        },
        {
            "id": 4,
            "name": "Ongoing"
        },
        {
            "id": 5,
            "name": "Canceled"
        },
        {
            "id": 6,
            "name": "Finished"
        }
    ]
}
```




#### GET `/api/v1/events/formats/`


Endpoint for getting all event's formats

**Bearer Token is required***


Response Example:
```json
{
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Online"
        },
        {
            "id": 2,
            "name": "Offline"
        },
        {
            "id": 3,
            "name": "Hybrid"
        }
    ]
}
```




#### GET `/api/v1/events/types/`

Endpoint for getting all event's types

**Bearer Token is required**


Response Example:
```json
{
    "count": 7,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Conference"
        },
        {
            "id": 2,
            "name": "Meetup"
        },
        {
            "id": 3,
            "name": "Webinar"
        },
        {
            "id": 4,
            "name": "Hackathon"
        },
        {
            "id": 5,
            "name": "Lecture"
        },
        {
            "id": 6,
            "name": "Networking"
        },
        {
            "id": 7,
            "name": "Exhibition"
        }
    ]
}
```
