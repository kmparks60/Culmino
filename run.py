import os
from dotenv import load_dotenv
from application import app

load_dotenv()


port = int(os.environ.get("PORT", 5000))
if __name__ == "__main__":
	app.run(host="0.0.0.0", port=port)