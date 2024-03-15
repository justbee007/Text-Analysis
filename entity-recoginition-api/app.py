from app import app
import os
PORT = int(os.getenv('PORT', '5009'))
#  start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True,port=PORT)