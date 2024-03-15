from app import app
import os

PORT = int(os.getenv('PORT', '5010'))
# Run the app
if __name__ == "__main__":
    app.run(debug=True, port=PORT)