# Varanasi AI Guide

Welcome to the Varanasi AI Guide, a comprehensive platform to explore the city of Varanasi through an intelligent chat interface. This project provides information about places to visit, historical stories, development projects, and more.

## Project Overview

This project consists of three main components:

1.  **Web Scraper:** A Python script that scrapes data from various official and informational websites about Varanasi.
2.  **AI Agent (RAG Pipeline):** A Retrieval-Augmented Generation (RAG) pipeline that uses the scraped data to provide answers to user queries. It leverages LangChain, ChromaDB, and a Large Language Model (LLM) like OpenAI's GPT.
3.  **Web Application:** A user-friendly chat interface built with Svelte for the frontend and FastAPI for the backend.

The entire application is containerized using Docker for easy setup and deployment.

## Project Structure

```
.
├── backend/
│   ├── data/             # (Generated) Scraped data will be stored here
│   ├── vectorstore/      # (Generated) Vector embeddings will be stored here
│   ├── .env              # (You need to create this) For storing API keys
│   ├── .gitignore
│   ├── Dockerfile
│   ├── main.py           # FastAPI application
│   ├── rag_pipeline.py   # RAG pipeline logic
│   ├── scraper.py        # Web scraping logic
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.svelte    # Main Svelte component
│   │   └── main.js       # Entry point
│   ├── .gitignore
│   ├── Dockerfile
│   ├── index.html
│   ├── nginx.conf        # Nginx configuration for serving the SPA
│   └── package.json
├── docker-compose.yml
└── README.md
```

## Prerequisites

Before you begin, ensure you have the following installed:

-   [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/install/)
-   An **OpenAI API Key**. This project is configured to use OpenAI's models.

## Setup and Execution

Follow these steps to get the application running:

### 1. Set up the Environment

-   **Create the `.env` file:** In the `backend` directory, create a file named `.env` and add your OpenAI API key to it:

    ```
    OPENAI_API_KEY="your_openai_api_key_here"
    ```

### 2. Build and Run the Application

-   Open your terminal in the root directory of the project and run the following command:

    ```bash
    docker-compose up --build
    ```

    This command will:
    -   Build the Docker images for both the backend and frontend.
    -   Start the containers.
    -   Set up the network and volumes.

    The initial build may take some time as it needs to download the base images and install all the dependencies.

### 3. Scrape the Data

-   The first time you run the application, the database will be empty. You need to trigger the web scraper to collect the data.
-   Open a new terminal and run the following `curl` command:

    ```bash
    curl -X POST http://localhost:8000/api/scrape
    ```

    -   This will trigger the scraping process. You will see the progress in the `docker-compose` logs for the `backend` service.
    -   After scraping, the data will be saved in `backend/data`, and the RAG pipeline will automatically create the vector store in `backend/vectorstore` the first time you ask a question.

### 4. Access the Application

-   **Frontend Chat Interface:** Open your web browser and navigate to `http://localhost:5173`. You should see the chat interface.
-   **Backend API Docs:** You can access the interactive API documentation (provided by Swagger UI) at `http://localhost:8000/docs`.

## Automated Data Updates

The data can be updated on a weekly basis by re-running the scraping process.

-   To manually trigger an update, simply run the `curl` command from Step 3 again.
-   For automated weekly updates, you can set up a cron job on your server to execute the `curl` command every week.

    Example cron job (runs every Sunday at 3 AM):
    ```cron
    0 3 * * 0 curl -X POST http://localhost:8000/api/scrape
    ```

## Important Notes

-   **Untested Code:** Please be aware that the code in this repository was written without the ability to run or test it due to environment constraints. You may encounter bugs or issues that need to be resolved.
-   **Scraper Robustness:** The current web scraper is basic and might break if the layout of the target websites changes. For a production system, a more robust scraping solution would be needed.
-   **LLM Choice:** The RAG pipeline is configured to use OpenAI. You can modify `backend/rag_pipeline.py` to use a different LLM provider supported by LangChain if you prefer.
