import editor
import ftplib
import console
import StringIO
import keychain
import pickle
import cgi
import sys




# Uncomment this line to reset stored password
# keychain.delete_password('vaughanje', 'editorial')
login = keychain.get_password('vaughanje', 'editorial')
if login is not None:
	user, pw = pickle.loads(login)
else:
	user, pw = console.login_alert('FTPS Login Needed', 'No login credentials found.')
	pickle_token = pickle.dumps((user, pw))
	keychain.set_password('vaughanje', 'editorial', pickle_token)


# 

remotePath = "/public_html/blog/source/"
host = "crawlab.org"
port = 21


docTitle = console.input_alert("Filename", "Enter File Name")
fileName = docTitle+'.md'
confirmation = console.alert('Confirm', 'Go ahead and post?','Yes','No')

postContent = sys.argv[1]#editor.get_text()

# Text encoidng sucks!
#encode_string = cgi.escape(postContent).encode('ascii', 'xmlcharrefreplace')
#postContent.encode('ascii', 'replace')

encode_string = postContent

# console.alert(postContent)

buffer = StringIO.StringIO(encode_string)
#buffer.write(postContent)
buffer.seek(0)

try:
	ftp = ftplib.FTP(host, user, pw)	
	ftp.cwd(remotePath)
	ftp.storbinary('STOR '+ fileName, buffer)
	ftp.quit()
except Exception, e:
	print e
	console.alert('Error', e)


#console.hud_alert('Posted '+fileName, 'success')
