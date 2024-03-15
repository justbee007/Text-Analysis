from app import app
import os

PORT = int(os.getenv('PORT', '5008'))
# Start the server with the 'run()' method
if __name__ == "__main__":
    app.run(debug=True, port=PORT,host='0.0.0.0')