# URL Shortener API with FastAPI and Streamlit

This project is a simple URL Shortener API built using **FastAPI** for the backend and **Streamlit** for the frontend. The application allows users to shorten long URLs, retrieve the metadata for shortened URLs, and delete URLs. The backend is implemented with FastAPI, utilizing SQLAlchemy for database interaction. The frontend is a minimal interface using Streamlit for easy user interaction with the API.

## Features

- **Shorten URL**: Input a long URL, and get a short URL in return.
- **Redirect**: Shortened URLs redirect to the original URL when accessed.
- **URL Management**: View and manage all shortened URLs, with options to delete them.
- **Expiration Time**: URLs can have an optional expiration time, with a default of 1 year if not specified.
- **URL Normalization**: URLs are normalized to ensure consistent handling (e.g., decoding URL-encoded characters).
  
## API Endpoints

- **POST** `/api/v1/shorten`: Shorten a given long URL (with optional expiration time).
- **GET** `/api/v1/urls`: Retrieve all shortened URLs with metadata.
- **GET** `/api/v1/urls/{short_url}`: Retrieve metadata for a specific shortened URL.
- **DELETE** `/api/v1/{short_url}`: Delete a specific shortened URL.
- **GET** `/{short_url}`: Redirect to the original URL from the shortened URL.

## Prerequisites

- **Python 3.8+**
- **Pip** (Python package manager)

## Installation

1. **Clone the repository**:

```
git clone https://github.com/your-username/url-shortener.git
cd url-shortener
```

2. **Create a virtual environment**:

```
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
```

3. **Install the dependencies**:

```
pip install -r requirements.txt
```

4. **Set up environment variables**:
   - Create an `.env` file with the following content:

```
DATABASE_URL=sqlite:///./test.db  # For local development with SQLite
```

5. **Initialize the database**:

Run the FastAPI application and it will automatically create the necessary database tables.

## Running the Application

### 1. **Backend (FastAPI)**

To start the FastAPI backend:

```
uvicorn app.main:app --reload
```

This will run the backend at `http://localhost:8000`. You can access the **Swagger UI** for the API documentation and testing at: `http://localhost:8000/docs`


### 2. **Frontend (Streamlit)**

To start the Streamlit frontend:

```
streamlit run frontend/app.py
```

The Streamlit app will open in your browser at `http://localhost:8501`, where you can interact with the URL shortener API.


## Future Enhancements

- Add more detailed URL analytics (e.g., number of clicks, time of access).
- Implement user authentication for managing URLs (optional).
- Extend the frontend with a more feature-rich UI using React or Next.js.
  
## Contributing

Contributions are welcome! Please fork the repository and create a pull request for any improvements.


