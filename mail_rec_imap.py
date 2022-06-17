'''Logic of demo app used for checking and for request\
    downloading attachement from e-mail box '''
import email
import imaplib
from email.header import decode_header

class MailRec:
    '''class Mail_rec'''
    def __init__(self, mail_host, login, password) -> None:
        self.mail_host = mail_host
        self.login = login
        self.password = password
        self.mail_message = None
        self.imap_server = None
        self.mail_message_list = []

    def mail_loging(self, select = 'INBOX'):
        '''class method used for connecting to mailbox, default checking is INBOX,\\
        displays sender, subject and attachment. If no attachment None is displayed'''
        self.imap_server = imaplib.IMAP4_SSL(self.mail_host)
        self.imap_server.login(self.login, self.password)
        self.imap_server.select(select)
        mails = self.imap_server.search(None, 'ALL')

        for mail in mails[1][0].split():

            _, msg = self.imap_server.fetch(mail, 'RFC822')
            self.mail_message = email.message_from_bytes(msg[0][1])
            mail_form, mail_from_encoding = decode_header(self.mail_message['from'])[0]

            if mail_from_encoding is not None:
                mail_form = mail_form.decode('UTF-8')

            mail_subject, _= decode_header(self.mail_message['Subject'])[0]
            if mail_from_encoding is not None:
                mail_subject = mail_subject.decode('utf-8')

            for chunk in self.mail_message.walk():
                attachement = chunk.get_filename()

            print(f'mail from: {mail_form};', f'subject:{mail_subject};',\
                f'attachement: {attachement}\n')
            self.mail_message_list.append(self.mail_message)

        return self.mail_message_list

    def attachement_download(self):
        '''For request if attachemnts exists are downloaded'''
        for mail_in_mail_message_list in self.mail_message_list:
            for chunk in mail_in_mail_message_list.walk():
                if chunk.get_filename() is not None:
                    print(chunk.get_filename())
                    with open(chunk.get_filename(), 'wb') as file:
                        file.write(chunk.get_payload(decode=True))
