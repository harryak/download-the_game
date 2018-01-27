#!/usr/bin/env python
from bottle import route, run

# For URL http://localhost:8080/join
@post('<group_name>/join')
def action_join(group_name):
    # Get username from request.
    username = request.json.username
    return { status: "OK" }

# Main function
if __name__ == '__main__':
    run(host='localhost', port=8080)
