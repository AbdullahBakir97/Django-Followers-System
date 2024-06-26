# Django Followers System

Django Followers System is a web application that provides functionality for users to follow each other, send follow requests, accept or reject follow requests, manage followers and following lists, and chat with each other.

## Introduction

The Django Followers System project aims to provide a robust system for managing user relationships within a Django web application. With this system, users can easily follow and unfollow each other, send and receive follow requests, manage their follower and following lists, and engage in real-time chat. This project can be integrated into various types of social networking platforms, community forums, or any application that requires user interactions and connections.

## Features

- User registration and authentication
- User profile management with bio, profile picture, and privacy settings
- Following and unfollowing other users
- Sending and accepting/rejecting follow requests
- View and manage follower and following lists
- Real-time chat between users
- API endpoints for integrating with external applications

## Installation

To install and set up the Django Followers System project, follow these steps:


### Clone the repository
```bash
git clone https://github.com/AbdullahBakir97/Django-Followers-System.git
```

### Navigate to the project directory
```bash
cd Django-Followers-System
```

### Create a virtual environment (optional but recommended)
```bash
python -m venv env
```

### Activate the virtual environment
```bash
source env/bin/activate  # for Unix/Linux
env\Scripts\activate  # for Windows
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Apply database migrations
```bash
python manage.py migrate
```

### Create a superuser (optional)
```bash
python manage.py createsuperuser
```

### Run the development server
```bash
python manage.py runserver
```


## Usage
To use the Django Followers System, follow these steps:

1. Register a new account or log in with an existing account.
2. Set up your profile with a bio, profile picture, and privacy settings.
3. Explore other users and follow/unfollow them.
4. Send follow requests to private users or accept/reject follow requests from others.
5. View and manage your follower and following lists from your profile dashboard.
6. Engage in real-time chat with other users.

## API Documentation

### Accounts Endpoints
- **List Accounts API**: `GET /accounts/api/`
- **Update Follow Request**: `PUT /accounts/api/follow-request/{request_id}/`
- **Partial Update Follow Request**: `PATCH /accounts/api/follow-request/{request_id}/`
- **Create Follow**: `POST /accounts/api/follow/` 
- **Read Profile**: `GET /accounts/api/profile/`
- **Update Profile**: `PUT /accounts/api/profile/`
- **Partial Update Profile**: `PATCH /accounts/api/profile/`
- **Read User Profile**: `GET /accounts/api/profile/{user_id}/`
- **Delete Unfollow**: `DELETE /accounts/api/unfollow/{user_id}/`

### Chat Endpoints
- **List Chat Rooms**: `GET /chat/api/rooms/`
- **Create Chat Room**: `POST /chat/api/rooms/`
- **Read Chat Room**: `GET /chat/api/rooms/{room_id}/`
- **List Messages**: `GET /chat/api/messages/`
- **Create Message**: `POST /chat/api/messages/`
- **Read Message**: `GET /chat/api/messages/{message_id}/`

### Authentication Endpoints
- **User Login**: `POST /api/auth/login/`
- **User Logout (GET)**: `GET /api/auth/logout/`
- **User Logout (POST)**: `POST /api/auth/logout/`
- **Change Password**: `POST /api/auth/password/change/`
- **Reset Password**: `POST /api/auth/password/reset/` 
- **Confirm Password Reset**: `POST /api/auth/password/reset/confirm/`
- **User Registration**: `POST /api/auth/registration/`
- **Resend Email for Registration**: `POST /api/auth/registration/resend-email/`
- **Verify Email for Registration**: `POST /api/auth/registration/verify-email/`
- **Read and Update User**: `GET/PUT/PATCH /api/auth/user/`


## Contributing
Contributions to the Django Followers System project are welcome! To contribute, follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Make your changes and commit them (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature-branch`)
5. Create a new Pull Request

For major changes, please open an issue first to discuss the proposed changes.

## License
This project is licensed under the [MIT License](LICENSE).
