#!/usr/bin/env python3

import connexion


def post_greeting(name: str) -> str:
    return 'Hello {name}'.format(name=name)

if __name__ == '__main__':
    #or server=gevent
    app = connexion.FlaskApp(__name__, port = 8080, specification_dir='openapi/', server='tornado')
    #or     
    #app = connexion.AioHttpApp(__name__, port = 8080, specification_dir='openapi/')
    app.add_api('helloworld-api.yaml', 
        arguments={'title': 'Hello World Example'}
        )
    app.run()
