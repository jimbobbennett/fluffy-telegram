import logging

import azure.functions as func

import shared.storage as storage

# Get all the users
users = storage.get_all_users()


def main(req: func.HttpRequest) -> func.HttpResponse:
    '''
    Returns the details for a user

    :param req: The HTTP request
    :type req: func.HttpRequest
    :return: The HTTP response
    :rtype: func.HttpResponse
    '''
    # Get the user ID from the route parameters
    user_id = req.route_params.get('user_id')

    logging.info(f'Getting details for user {user_id}')

    # Check if the user exists
    if user_id in users:
        # Return the user details
        return func.HttpResponse(users[user_id], mimetype='application/json')

    # Return a 404 if the user doesn't exist
    return func.HttpResponse(f'User {user_id} not found', status_code=404)
