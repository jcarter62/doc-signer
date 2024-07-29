import logging
from waitress import serve
from app import app
from dotenv import load_dotenv
import os


# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


if __name__ == '__main__':
    _host = os.getenv('HOST', '0.0.0.0')
    _port = int(os.getenv('PORT', 5000))
    logging.info(f'Starting server on {_host}:{_port}')
    serve(app, host=_host, port=_port)

