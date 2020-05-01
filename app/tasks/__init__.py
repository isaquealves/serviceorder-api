from decouple import config
import logging
from python_http_client.exceptions import BadRequestsError, ForbiddenError
from app.providers.celery import celery
from app.providers.mail import sg
from app.helpers import encrypt_data

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@celery.task(serializer='pickle')
def send_activation_email(user):

    code = encrypt_data(user)
    link = f'{config("BASE_URL")}/{code}'

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
        print(result.body)
        print(result.status_code)
        print(result.headers)
        return result.to_dict
    except BadRequestsError as badErr:
        LOGGER.error(badErr)
        return {}
    except ForbiddenError as err:
        LOGGER.error(err)
