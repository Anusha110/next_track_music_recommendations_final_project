

# NextTrack Music Recommender

This project is a web application that recommends personalized playlists based on the user's preferences. The application uses Spotify's Web API to search for songs and recommends songs based on the user's preferences.

The project is currently deployed on Render at https://next-track-music-recommendation.onrender.com.
This project should ideally be ideally available until January 2027, but please note that this is not guaranteed.


## Getting Started

Follow these instructions to set up and run the NextTrack Music Recommender project locally.
(Please note that the local setup requires running several scripts for the entire offline data preprocessing and ingestion pipeline. This may take up to 4 hours to complete, as there are over a million songs in the Spotify database and hundreds of thousands of artists & tags from the MusicBrainz dataset.)

Also note that in order to use the Spotify Developer API, you will need to have a Spotify Premium account as of September 2026.

## Prerequisites

### System Environment
- **Developed & Tested On:**  Ubuntu 24.04.2 LTS
- **Python Version:** 3.12.3
- **Django Version:** 6.1.1

### Installing Requirements

Make sure you run the following commands to install the required dependencies for the backend:

```bash
pip install -r music_recommender/requirements-dev.txt
```

requirements-dev.txt - is for local development only. It contains the dependencies required for running the backend locally.

requirements.txt - is for production deployment. It contains the dependencies required for running the backend in production.


## Local DB Setup


### Downloading the Data

This project uses two data sources: Spotify and MusicBrainz.
Since these data sources are large (over 1GB total), and the MusicBrainz files may have licensing restrictions, they are not included in the repository. Download them separately from the following links:

**Spotify**
- Joshi, A. (2023, June 29). Spotify_1Million_Tracks. Kaggle. https://www.kaggle.com/datasets/amitanshjoshi/spotify-1million-tracks/data

**MusicBrainz**
- MetaBrainz Foundation. (2026). MusicBrainz database (Version 20260901-000002 sample export) [Data set]. https://ftp.musicbrainz.org/pub/musicbrainz/data/sample/20260901-000002/
   - I used version 20260901-000002 of the MusicBrainz Sample Dataset as seen in the link. In case it's unavailable, you can download the version that is currently available from the link (https://ftp.musicbrainz.org/pub/musicbrainz/data/sample/).


### Setup Commands

To set up the local database, run the following commands:

- Run the following commands from the `music_recommender/` directory, where `manage.py` is located:
  ```bash
  cd music_recommender
  ```

- Load the local environment variables before running Django commands:
  ```bash
  set -a
  source env_local
  set +a
  ```

- Run ```python manage.py migrate``` to create the local database.

- **Cleaning and ingesting the Spotify data into the local database**
     - Run the following Python script, replacing the input path with the location of the downloaded Spotify CSV file:
       ```bash
       python recommendations/scripts/ingest_spotify_data.py --input /path/to/spotify_data.csv
       ```

- **Creating the Spotify track embeddings**
    - Run ```python recommendations/scripts/build_spotify_embeddings.py --database db.sqlite3``` to create the Spotify track embeddings.

- When you download the MusicBrainz Sample Dataset, there will be many files in the directory. We specifically need the following MusicBrainz dumps:
    - artist
    - artist_tag
    - tag

- Copy the artist, artist_tag, and tag files into a local directory.

- Set `MUSIC_BRAINZ_DATA_PATH` to the local directory containing the `artist`, `artist_tag`, and `tag` files:
  ```bash
  export MUSIC_BRAINZ_DATA_PATH="/path/to/music_brainz_dumps"
  ```

- Run ```python recommendations/scripts/convert_musicbrainz_dumps_to_sqlite.py``` to **convert the MusicBrainz dump files to SQLite**. This creates a separate `music_brainz_db` file in the project directory.

- The following scripts will fetch the relevant artists and artist tags from the MusicBrainz database (`music_brainz_db`) and populate the local database (`db.sqlite3`).
    - Run ```python recommendations/scripts/populate_artists.py``` to populate the artists and update the SpotifyTrack artist foreign key.
    - Run ```python recommendations/scripts/populate_artist_tags.py``` to populate the Spotify artist tags in the local database.

## Environment Variables

**The following environment variables are required to run the backend**,

**The Spotify API requires a client ID and secret. You can get these from the Spotify developer dashboard. The developer dashboard is only available to premium Spotify users as of September 2026.**

Create an `env_local`:
```
DJANGO_DEBUG=true
DJANGO_SECRET_KEY="" # Generate a random key
DJANGO_ALLOWED_HOSTS="127.0.0.1,localhost"
CORS_ALLOWED_ORIGINS="http://127.0.0.1:5500,http://localhost:5500"
DATABASE_PATH="db.sqlite3"
SPOTIFY_CLIENT_ID=""  
SPOTIFY_CLIENT_SECRET=""
```

The `env_local` file is not loaded automatically. Before running the backend, export these variables in the current shell, or load the file manually from the `music_recommender/` directory:

```bash
set -a
source env_local
set +a
```

For a Render deployment using a persistent disk, set `DATABASE_PATH` to the SQLite file location on the mounted disk. Use the following Render settings for the backend service:

```text
Root Directory: music_recommender
Build Command: pip install -r requirements.txt && python manage.py collectstatic --no-input
Start Command: python manage.py migrate && gunicorn music_recommender.wsgi:application --bind 0.0.0.0:$PORT
```

## Running and Testing the App

### Backend

To run the backend locally, run the following command:

```bash
python manage.py runserver 8000
```

To run the tests, run the following command:

```bash 
python manage.py test
```
### Frontend

To run the frontend locally, run the following command:

```bash
cd frontend
python3 -m http.server 5500
```
**NOTE: Ensure the `API_URL` variable in frontend/music_form.js is set to the correct backend URL.**

### MusicBrainz User-Tagging Data License
This project utilizes supplementary user-tagging data from the MusicBrainz database, made available by the MetaBrainz Foundation under the Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported (CC BY-NC-SA 3.0) license. This is cited in the Local DB setup section.

## Attribution

The recommendation system, data-processing scripts, database models, API, frontend, and tests were developed for this project.

Some setup files, including `manage.py`, Django settings, and migration files, were auto-created by Django and adapted for this application.


