from application import app
from application.db import init_db, close_db

if __name__ == '__main__':
    try:
        init_db()
        app.secret_key = 'DEV'
        app.run(debug=True, port=7070)  
    except Exception as err:
        print(err)
        
    close_db()
    



    