# 1001-songs-backend



Description of the project.

## Installation and Usage

### Building the Docker Container

To run the project in a Docker container, follow these steps:

1. Install Docker if you haven't already. .

2. Open a terminal or command prompt in the project directory.

3. Build the container using the following command:
    ```bash
    docker build -t songs .
    ```

### Running the Container

To launch the project in a Docker container, execute the following command:

```bash
  docker run -p 8080:80 songs
```



## If you prefer to run the project without Docker, follow these steps:

1. Make sure you have Python installed on your machine.

2. Install project dependencies using pip:
    ```bash
    pip install -r requirements.txt
    ```

3. Apply migrations to set up the database (if applicable):
    ```bash
    python manage.py migrate
    ```

4. Start the server:
    ```bash
    python manage.py runserver
    ```

The project should now be running locally. Access it through your web browser at [http://localhost:8000](http://localhost:8000) or the appropriate address if you've configured a different port.