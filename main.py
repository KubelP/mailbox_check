'''Main file of demo app used for checking and for request\
    downloading attachement from e-mail box. Credentials are putted in config.yamal file.\
    For change searching box (default is INBOX) put --select [box_name]. For download\
    attachements put --download download.
    '''
import yaml
from imaplib import IMAP4
import click
from mail_rec_imap import MailRec

@click.command()
@click.option('--download', help = 'for download attachments put "download"')
@click.option('--select', help = 'for change default folder "INBOX" put new folder to check')
def main(download, select):
    '''Demo app used for checking and for request\
 downloading attachement from e-mail box. Credentials are putted in config.yamal file.\
 For change searching box (default is INBOX) put --select [box_name]. For download\
 attachements put --download download.'''
    with open('config.yaml', 'r', encoding='utf-8') as config:
        credentials = yaml.safe_load(config)
    try:
        mail = MailRec(**credentials)
        if select:
            mail.mail_loging(select)
        mail.mail_loging()
        if download == 'download':
            mail.attachement_download()
    except IMAP4.error:
        print('*'*5, 'No such directory in mail box. Please check \
spelling or existing folders in your mailbox.', '*'*5)
    except ConnectionRefusedError: 
        print('*'*5, 'No imap server, login and password in config.yamal file', '*'*5)

if __name__ == '__main__':
    main()
