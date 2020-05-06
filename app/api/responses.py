from flask import jsonify
from .messages import (
    DOES_NOT_EXIST, EXCEPTION,
    INVALID_DATA, PERMISSION_DENIED, TYPE_REQUIRED,
    SUCCESSFULLY_CREATED)


def invalid_data_response(
    resource: str, errors: dict, msg: str = INVALID_DATA
):
    '''

    Responses 422 Unprocessable Entity
    '''

    if not isinstance(resource, str):
        raise ValueError(TYPE_REQUIRED.format('string'))

    resp = jsonify({
        'resource': resource,
        'message': msg,
        'errors': errors,
    })

    resp.status_code = 422

    return resp


def exception_raised_response(
    resource: str, description: str = '', msg: str = EXCEPTION
):
    '''
    Responses 500 - Internal Error
    '''

    if not isinstance(resource, str):
        raise ValueError(TYPE_REQUIRED.format('string'))

    resp = jsonify({
        'resource': resource,
        'message': msg,
        'description': description
    })

    resp.status_code = 500

    return resp


def not_found_response(resource: str, description: str):
    '''
    Responses 404 Not Found
    '''

    if not isinstance(resource, str):
        raise ValueError(TYPE_REQUIRED.format('string'))

    resp = jsonify({
        'resource': resource,
        'message': DOES_NOT_EXIST.format(description),
    })

    resp.status_code = 404

    return resp


def bad_request_response(resource: str, description: str):
    '''
    Responses 400 - Bad Request
    '''

    if not isinstance(resource, str):
        raise ValueError(TYPE_REQUIRED.format('string'))

    resp = jsonify({
        'resource': resource,
        'message': INVALID_DATA.format(description),
    })

    resp.status_code = 400

    return resp


def resource_found_response(resource: str, message: str, data=None, **extras):
    '''
    Responses 200 - Found
    '''
    if not isinstance(resource, str):
        raise ValueError(TYPE_REQUIRED.format('string'))

    response = {'status': 200, 'message': message, 'resource': resource}

    if data:
        response['data'] = data

    response.update(extras)

    resp = jsonify(response)

    resp.status_code = 200

    return resp


def response_ok(message: str):
    '''
    Responses 200 - OK
    '''
    response = {'status': 200, 'message': message}

    resp = jsonify(response)

    resp.status_code = 200

    return resp


def created_response(resource: str, data=None, **kwargs):
    '''
    Responses 201 - Created
    '''

    if not isinstance(resource, str):
        raise ValueError(TYPE_REQUIRED.format('string'))

    response = {'status': 201, 'resource': resource}
    response['message'] = SUCCESSFULLY_CREATED.format(resource)
    if data:
        response['data'] = data

    response.update(kwargs)

    resp = jsonify(response)

    resp.status_code = 201

    return resp


def no_content_response(resource: str, message: str):
    '''
    Responses 204 - no content
    '''

    if not isinstance(resource, str):
        raise ValueError(TYPE_REQUIRED.format('string'))

    response = {'status': 204, 'message': message, 'resource': resource}

    resp = jsonify(response)

    resp.status_code = 204

    return resp


def user_not_allowed_response(resource: str, msg: str = PERMISSION_DENIED):
    '''
        Responses 401
    '''
    if not isinstance(resource, str):
        raise ValueError(TYPE_REQUIRED.format('string'))

    resp = jsonify({
        'status': 401,
        'resource': resource,
        'message': msg
    })

    resp.status_code = 401

    return resp
