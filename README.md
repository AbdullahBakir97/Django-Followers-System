# Django Followers System

Django Followers System is a web application that provides functionality for users to follow each other, send follow requests, accept or reject follow requests, and manage followers and following lists.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)

## Introduction

The Django Followers System project aims to provide a robust system for managing user relationships within a Django web application. With this system, users can easily follow and unfollow each other, send and receive follow requests, and manage their follower and following lists. This project can be integrated into various types of social networking platforms, community forums, or any application that requires user interactions and connections.

## Features

- User registration and authentication
- User profile management with bio, profile picture, and privacy settings
- Following and unfollowing other users
- Sending and accepting/rejecting follow requests
- View and manage follower and following lists
- API endpoints for integrating with external applications

## Installation

To install and set up the Django Followers System project, follow these steps:


# Clone the repository
```bash
git clone https://github.com/AbdullahBakir97/Django-Followers-System.git
```

# Navigate to the project directory
```bash
cd Django-Followers-System
```

# Create a virtual environment (optional but recommended)
```bash
python -m venv env
```

# Activate the virtual environment
```bash
source env/bin/activate  # for Unix/Linux
env\Scripts\activate  # for Windows
```

# Install dependencies
```bash
pip install -r requirements.txt
```

# Apply database migrations
```bash
python manage.py migrate
```

# Create a superuser (optional)
```bash
python manage.py createsuperuser
```

# Run the development server
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

## API Documentation
The Django Followers System provides RESTful API endpoints for integrating with external applications. Refer to the API documentation for detailed information on how to use these endpoints.

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
