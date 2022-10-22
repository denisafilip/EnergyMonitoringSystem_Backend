import json

from rest_framework.renderers import JSONRenderer


class UserJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        error = data.get('error', None)
        token = data.get('token', None)

        if error:
            return super(UserJSONRenderer, self).render(data)

        if token is not None and isinstance(token, bytes):
            data['token'] = token.decode('utf-8')

        # Finally, we can render our data under the "user" namespace.
        print(data)
        return json.dumps(data)
