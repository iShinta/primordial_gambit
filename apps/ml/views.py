from django.shortcuts import render
import imaplib
	
def read():
	imap = imaplib.IMAP4_SSL('imap.gmail.com')
	imap.login('primordialgambit@gmail.com', 'md5hackathon')
	imap.select('INBOX')

	status, response = imap.search(None, '(UNSEEN)', '(FROM "Google Voice")')
	unread_msg_nums = response[0].split()
	da = []
	if status == "OK":
		for e_id in unread_msg_nums:
			_, response = imap.fetch(e_id, '(RFC822)')
			start = "<https://www.google.com/voice/>"
			end = "play message"
			res = response[0][1]
			da.append(res[res.find(start)+len(start):res.find(end)].replace("\r\n",''))

	return da


