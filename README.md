# "Music Streaming App made in Django"
by Andrei-Flavius Văcaru

--------------


## User Features

- User can register and login (as a user or artist)
- User can listen to music
- User can create playlists
- User can see the music of an artist

## Artist Features

- Artist can register and login
- Artist can upload music
- Artist can delete music
- Artist can see the music uploaded by him

## Playlists Features

- Add playlist
- Edit playlist
- Delete playlist
- See playlist
- Add music to playlist
- Delete music from playlist
- See music from playlist
- See playlists

## Music Features

- Add music
- Edit music
- Delete music
- See music


### How to run the app (in the terminal) DEBUG IS SET TO FALSE
1. First create a virtual environment
```bash
python -m venv .venv 
```
2. Then activate the Virtual Environment
```bash
.\.venv\Scripts\activate 
```
3. After that install the requirements and run the server
```bash
pip install -r requirements.txt
```
4. Run the server
```bash
python manage.py runserver
```
5. Stop the server (in the terminal)
```bash
Ctrl + C 
```
6. To deactivate the Virtual Environment
```bash
Deactivate
```

If you want to delete the whole database and start from scratch use this command in the terminal
```bash
python manage.py migrate music_streaming_app zero
```
But after you have done this please be sure to create a superuser with this commands !!!!!
```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```
```bash
python manage.py createsuperuser
```


## Access to the app with the following credentials

account: admin
password: admin

account: user
password: userpassword

account: user2
password: userpassword

account: artist
password: artistpassword

account: artist2
password: artistpassword

I put some music in the songs_to_choose directory, so you can listen and play to it. Enjoy! :D