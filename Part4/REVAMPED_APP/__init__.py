@app.route('/ping')
def ping():
    return {'status': 'ok'}

