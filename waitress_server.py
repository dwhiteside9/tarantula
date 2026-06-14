#https://stackoverflow.com/questions/51045911/serving-flask-app-with-waitress-on-windows
import waitress
import app #app.py

if __name__ == '__main__':
    myapp = app.create_app()
    waitress.serve(myapp, host='0.0.0.0', port=myapp.config['PORT'])