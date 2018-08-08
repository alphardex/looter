from eve import Eve

app = Eve(settings='jav_settings.py')

if __name__ == '__main__':
    app.run(debug=True)