from coodesh_app.src import notification
import configparser


def notify_caller(message_body):
        parser = configparser.ConfigParser()
        try:
            parser.read("configEmailAlarm.cfg")
        except:
            print(f" {__file__} parser.read() exception")
        else:
            str_message_body = str(message_body)

            receiver_email = parser['DEFAULT'].get('RECEIVER_EMAIL')
            notification.main(receiver_email=receiver_email,
                        subject_line='[Notificação] Falha banco de dados sfn-project', message_body=str_message_body)



class UnknownExceptionNotify(Exception):
    '''Exception handler error with a notify method.'''
    def __init__(self, *args, notify=False):
        if args:
            print(args)
            if notify is True:
                notify_caller(args)
            


class SFNArticlesDoesNotExistNotify(Exception):
    '''SFNArticles.DoesNotExist error handler'''
    def __init__(self, *args, notify=False):
        if args:
            print(args)
            if notify is True:
                notify_caller(args)