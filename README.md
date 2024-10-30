# Django Blogs-API
A RESTful API for managing blog posts, user profiles, comments, and follower relationships. Built using Django and Django REST Framework.

## Features
* `User Authentication`: User signup, login, and logout functionality.
* `Profile Management`: Users can create, update, and delete their profiles.
* `Blog Management`: Create, retrieve, update, and delete blog posts.
* `Commenting System`: Comment on blog posts.
* `Follower System`: Follow/unfollow users, view followers/following lists.
  
## Project Structure
*`user`: Manages user accounts and profiles.
*`post`: Manages blog posts and comments.
*`api_root`: Provides a central API root endpoint to navigate the API.

## Prerequisites
Python 3.8+
Django 4.0+
Django REST Framework

## Endpoints
### API Root
`GET /api/`: The root of the API, listing available endpoints.
### User Management
`POST /api/users/`: Register a new user.
`GET/PUT/DELETE /api/profiles/{id}/`: Manage profiles.
### Blog Management
`POST /api/posts/`: Create a new blog post.
`GET/PUT/DELETE /api/posts/{id}/`: Retrieve, update, or delete a specific blog post.
### Comments
`POST /api/posts/{post_id}/comments/`: Add a comment to a post.
### Follow System
`POST /api/profiles/{id}/follow/`: Follow a user.
`POST /api/profiles/{id}/unfollow/`: Unfollow a user.
`GET /api/profiles/{id}/followers/`: List followers of a user.
`GET /api/profiles/{id}/following/`: List users a profile is following.

## License
This project is licensed under the MIT License.
