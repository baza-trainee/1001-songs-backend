<div class="badge_container" style="display: flex; justify-content: center;">

![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/docker-blue.svg)](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-22-04)
[![Docker-compose](https://img.shields.io/badge/docker-compose-orange.svg)](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-22-04)
![Linux (Ubuntu 20.04+)](https://img.shields.io/badge/linux-ubuntu%2020.04%2B-green.svg)
</div>
<h1 align="center" style="color: #B5E5E8;">1000 and 1 songs API</h1>

> *"1000 and 1 Song" is an online platform dedicated to preserving and promoting Ukrainian folk music. Through expeditions across Ukraine, we capture traditional melodies, enriching them with modern interpretations, and share them with the world, fostering a deeper appreciation for Ukraine's rich musical heritage.*

---
Built on the asynchronous **FastAPI** framework, the API utilizes a **PostgreSQL** database with the asynchronous adapter **asyncpg** and **Pydantic v2** for data serialization. For site management and content population, the project utilizes the **SQLalchemy Admin** panel. It features a robust authentication system, employing the JWTStrategy and BearerTransport for secure user authentication and management, powered by the **FastAPI-Users**. For sending emails in the project, the **FastAPI-Mail** library is used.

<h3 align="center">TECHNOLOGY</h3>
<p align="center">
  <a href="https://fastapi.tiangolo.com/" target="_blank">
    <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI">
  </a>
  <a href="https://fastapi-users.github.io/fastapi-users" target="_blank">
    <img src="https://img.shields.io/badge/FastAPI%20Users-ef5552?style=for-the-badge" alt="FastAPI-Users">
  </a>
  <a href="https://www.sqlalchemy.org/" target="_blank">
    <img src="https://img.shields.io/badge/sqlalchemy-fbfbfb?style=for-the-badge" alt="SQLAlchemy">
  </a>
  <a href="https://pydantic-docs.helpmanual.io/" target="_blank">
    <img src="https://img.shields.io/badge/Pydantic-14354C?style=for-the-badge&logo=Pydantic" alt="Pydantic-v2">
  </a>
  <a href="https://pypi.org/project/fastapi-mail/" target="_blank">
    <img src="https://img.shields.io/badge/FastAPI%20Mail-0078D4?style=for-the-badge" alt="FastAPI-Mail">
  </a>
  <a href="https://www.your-link-here.com/" target="_blank">
    <img src="https://img.shields.io/badge/SQLAdmin-14341b?style=for-the-badge" alt="SQLAdmin">
  </a>
</p>


<h2 align="center" style="color: #B5E5E8;">INSTALLATION</h2>

To run the project, you will need [Docker-compose](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-22-04) installed. Follow these steps to install and run the project:

1. Create a new folder for your project.

2. Open the project in an IDE

3. Initialize Git

    ```
    git init
    ```
4. Add the remote repository
    ```
    git remote add origin https://github.com/baza-trainee/1001-songs-backend.git
    ```
5. Sync with the remote repository

    ```
    git pull origin dev
    ```
6. Create a `.env` file and define all environment variables from the .`env_example` file:
    <details class="custom-details">
    <summary><b>DB settings</b></summary>
    <p class="custom-details-description"><i>Variables for database and the project configuration.</i></p>

    <b class="variable-name">POSTGRES_HOST</b>=<span class="variable-value">localhost</span><br>
    <b class="variable-name">POSTGRES_PORT</b>=<span class="variable-value">5432</span><br>
    <b class="variable-name">POSTGRES_DB</b>=<span class="variable-value">cats_db</span><br>
    <b class="variable-name">POSTGRES_USER</b>=<span class="variable-value">admin</span><br>
    <b class="variable-name">POSTGRES_PASSWORD</b>=<span class="variable-value">admin</span><br><br>
    <b class="variable-name">BASE_URL</b>=<span class="variable-value">http://localhost:8000</span><br>
    <b class="variable-name">SITE_URL</b>=<span class="variable-value">http://localhost:3000</span><br>
    <b class="variable-name">BACKEND_PORT</b>=<span class="variable-value">8000</span><br>
    <b class="variable-name">SECRET_AUTH</b>=<span class="variable-value">SECRET</span>
    </details>

    <details class="custom-details">
    <summary><b>Admin settings</b></summary>
    <p class="custom-details-description"><i>Variables for initialization of superuser (administrator).</i></p>

    <b class="variable-name">ADMIN_USERNAME</b>=<span class="variable-value">admin@example.com</span><br>
    <b class="variable-name">ADMIN_PASSWORD</b>=<span class="variable-value">Adm1n123$</span>
    </details>

    <details class="custom-details">
    <summary><b>Mail settings</b></summary>
    <p class="custom-details-description"><i>Variables for configuring FastAPI-Mail service.</i></p>

    <b class="variable-name">EMAIL_HOST</b>=<span class="variable-value">outlook.office365.com or smtp.gmail.com</span><br>
    <b class="variable-name">EMAIL_PORT</b>=<span class="variable-value">587</span><br>
    <b class="variable-name">EMAIL_USER</b>=<span class="variable-value">your email</span><br>
    <b class="variable-name">EMAIL_PASSWORD</b>=<span class="variable-value">Password or Key (if use gmail)</span>
    </details>


    <details class="custom-details">
    <summary><b>Redis settings</b></summary>
    <p class="custom-details-description"><i>Variables for configuring Redis service.</i></p>

    <b class="variable-name">REDIS_HOST</b>=<span class="variable-value">localhost</span><br>
    <b class="variable-name">REDIS_PORT</b>=<span class="variable-value">6379</span><br>
    <b class="variable-name">REDIS_PASS</b>=<span class="variable-value">ReDiSpAsS</span>
    </details>

<h2 align="center" style="color: #B5E5E8;">USAGE</h2>

1. Create a virtual environment:
    ```
    python -m venv venv
    ```
2. Install dependencies:
    ```
    pip install -r requirements.txt
    ```
3. Run the project using the Makefile command:
    ```
    make run
    ```
    This command will create a container with the database, initiate migrations, and start the server on port `8000`.<br>
    Subsequent launches of the application are carried out with the command:
    ```
    make start
    ```
    To run the project in the background in containers, run the following command:
    ```
    make prod
    ```

    The admin panel is accessible at `BASE_URL/admin`, use the login credentials you specified **in the environment variables**.

<h2 align="center" style="color: #B5E5E8;">MAKEFILE COMMANDS</h2>

*These commands streamline various development and deployment tasks, including container management, database operations, backups, and frontend management.*


- `prod`: Stops existing containers, builds Docker images, and starts containers, followed by upgrading the database and launching the application. This command prepares the project for production use.
- `down:` Stop and remove all Docker containers.
- `build`: Builds Docker images for the project.
- `run`: Starts Docker containers for Postgres and Redis, waits until they are healthy, upgrades the database, and then launches the application.
- `start`: Initiates the web application using Uvicorn.
- `open-redis`: Open a Redis CLI session for the Redis container.
- `clean`: Removes Python-related files like pycache, .pyc, and .pyo from the project.
- `auto_backup`: Adds a cron job to execute the backup script every midnight.
- `stop_backup`: Removes the backup script from the cron job.
- `backup`: Executes the backup script to create a backup of the database.
- `restore`: Executes the restore script to restore the database.
- `frontend_build`: Archives the frontend files into a compressed tarball.
- `frontend_export`: Extracts the compressed frontend files to the specified directory.
- `drop_db`: Stops containers and removes volumes associated with the database.
- `prune`: Stops containers, removes unused Docker images, and prunes Docker volumes.

    <h2 align="center" style="color: #B5E5E8;">DOCUMENTATION</h2>

    Interactive documentation is available at `/docs` and `/redoc` for two different interfaces: [Swagger](https://swagger.io/) and [ReDoc](https://redoc.ly/). They allow you to view and test all the API endpoints, as well as get information about the parameters, data types, and response codes. You can learn more about Swagger and ReDoc on their official websites.
<p align="center">
  <a href="https://swagger.io/" target="_blank">
    <img src="https://img.shields.io/badge/Swagger-85EA2D?style=for-the-badge&logo=swagger&logoColor=black" alt="Swagger">
  </a>
  <a href="https://redoc.ly/" target="_blank">
    <img src="https://img.shields.io/badge/Redoc-8A2BE2?style=for-the-badge&logo=redoc&logoColor=white" alt="Swagger">
  </a>
</p>
