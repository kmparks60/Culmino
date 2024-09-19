import os
from dotenv import load_dotenv
from application import app

load_dotenv()


if __name__ == "__main__":
	port = int(os.environ.get('PORT'))
	app.run(host='0.0.0.0', port=port)