import webview
import os

if __name__ == '__main__':
    #os.system('python app.py')
    webview.create_window('Hello world', 'http://127.0.0.1:5000/')
    webview.start()

#https://pywebview.flowrl.com/guide/
#https://stackoverflow.com/questions/62672182/how-to-run-python-flask-app-and-webview-simultaneosuly