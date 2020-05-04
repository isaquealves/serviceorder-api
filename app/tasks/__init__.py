import logging
from decouple import config
from python_http_client.exceptions import BadRequestsError, ForbiddenError
from app.providers.celery import celery
from app.providers.mail import sg
from app.helpers import encrypt_data, encode_user_identification

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@celery.task(serializer='pickle')
def send_activation_email(user):

    code = encrypt_data(user)
    user_id = encode_user_identification(user.pub_key)
    link = f'{config("BASE_URL")}/{config("API_VERSION", "v1")}/' + \
           f'users/activate/?code={user_id.decode()}+{code}'

    html = f"""<h1>Welcome {user.first_name}</h1>
            <p>You just need to click link below to activate your account</p>
            <p><a href='{link}' style="box-sizing: border-box;
                padding: 1em;
                border-radius: .5em;
                background-color: #d3334b; color: #FBEFFB">Activate</a></p>
            <p>If your client doesn't allow html emails,
            just copy and past the link below:</p>
            <p>{link}</p>"""
    try:
        result = sg.send_email(
            to_email=user.email,
            subject="Service Orders Management Account Activation",
            from_email=config(
                'APP_ACTIVATION_MAIL_FROM',
                'isaquealves@gmail.com'
            ),
            html=html
        )

        LOGGER.info(link)
        return result.to_dict
    except BadRequestsError as badErr:
        LOGGER.error(badErr)
        return {}
    except ForbiddenError as err:
        LOGGER.error(err)
