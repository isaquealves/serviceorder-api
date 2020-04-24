from flask import jsonify
def root():
    return jsonify({'message': 'Welcome to Service order api'})