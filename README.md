# Streamlit PDF to Image Converter

This application is a webapp that provides a simple interface to convert PDF files to images. It is based on two main components: a backend API built on FastAPI and a frontend built on Streamlit.

This repo contains all the scripts that are part of the application and also provides all the files to conveniently build and run the application using Docker Compose.


# Run the application locally through Docker Compose (recommended)
The following steps describe how to build and run the application using Docker Compose:
- Install Docker and Docker Compose
- Clone the repo
- Build and run the application using Docker Compose:
	- Open a terminal and move into the cloned project root through `cd`
	- Build the application: `docker compose build --no-cache`
	- Run the application: `docker compose up`
	- Open a browser and go to `http://localhost:8011/pdf2img/home` to access the application
	- Check the backend API documentation at `http://localhost:8010/docs`


# Run the application in a local environment
The following steps describe how to run the application in a local environment, for example for debugging purposes:
- Clone the repo
- Create a virtual environment and activate it:
	- Open a terminal and move to the folder that contains the repo folder through `cd`
	- Create the virtual environment: `python -m venv streamlitpdf2img-env`
	- Activate the virtual environment: `"streamlitpdf2img-env/Scripts/activate.bat"`
	- Move to the project root: `cd streamlit-pdf2img`
- Install the dependencies for the backend and frontend projects using Poetry:
	- Project: pdf2imgbe
		- Move to the backend folder: `cd be`
		- Install the Poetry project: `poetry install`
	- Project: pdf2imgfe
		- Move to the frontend folder: `cd ../fe`
		- Install the Poetry project: `poetry install`
- Run the application components:
	- Run a local instance of the SQL database; one of the easiest ways to do this is through Docker Compose:
		- Open a terminal and move to the folder that contains the repo folder through `cd`
		- Run the SQL server: `docker compose -f streamlit-pdf2img\compose.yaml up -d --build db-service`
	- Run the backend API by ensuring that the environment variables from the .env.local file are loaded (e.g. through a debug configuration in VS Code)
	- Run the frontend by ensuring that the environment variables from the .env.local file are loaded (e.g. through a debug configuration in VS Code)
