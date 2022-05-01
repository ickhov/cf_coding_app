# Channel Factory Coding App

Channel Factory Coding App written using Django and Python.

## Set up the project

1. Set up a virtual environment for this project. I recommend using virtualenv, but you can use other library of choice.

2. Activate the virtual environment

3. Clone this repository
    ```
    git clone git@github.com:ickhov/cf_coding_app.git
    ```

4. Generate an API key for the Google Map API on the GCP

5. Create a .env file at the root directory and copy and paste the following data to the file
    ```
    SECRET_KEY=random-string
    API_KEY=your-google-map-api-key
    ```

6. Install the dependencies
    ```
    pip install -r requirements.txt
    ```

7. Run the migration
    ```
    python manage.py migrate
    ```

## Run the project

Run the following command
```
python manage.py runserver
```

## Access the API through the browser

You can access the API through http://127.0.0.1:8000/ and the available endpoint is:
- (POST) /address/distance/