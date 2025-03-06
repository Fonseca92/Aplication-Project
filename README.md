# My Flask App

This is a web application built with Flask, SQLAlchemy, and Azure Blob Storage.

## Features
- User and Article models with relationships.
- Image upload feature.
- Microsoft authentication using MSAL.
- Deployed on Azure.

## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/my-flask-app.git
    cd my-flask-app
    ```

2. Create a virtual environment and activate it:
    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up the database and run the SQL scripts in the `SQL Scripts` folder.

5. Create an `.env` file with the following environment variables:
    ```
    SECRET_KEY=your_secret_key
    DATABASE_URL=your_database_url
    BLOB_ACCOUNT_NAME=your_blob_account_name
    BLOB_ACCOUNT_KEY=your_blob_account_key
    BLOB_CONTAINER_NAME=images
    CLIENT_ID=your_client_id
    CLIENT_SECRET=your_client_secret
    AUTHORITY=https://login.microsoftonline.com/your_tenant_id
    ```

6. Run the application:
    ```sh
    flask run
    ```

7. Open your web browser and go to `http://127.0.0.1:5000`.

## Deployment
Choose between a VM or App Service for deployment. See `WRITEUP.md` for an analysis of both options.

## License
This project is licensed under the MIT License.