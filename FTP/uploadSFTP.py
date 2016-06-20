import editor
import console
import keychain
import pickle
import paramiko

#keychain.delete_password('macdrifter', 'editorial')
login = keychain.get_password('vaughanj_ssh', 'editorial')
if login is not None:
	user, pw = pickle.loads(login)
else:
	user, pw = console.login_alert('FTPS Login Needed', 'No login credentials found.')
	pickle_token = pickle.dumps((user, pw))
	keychain.set_password('vaughanj_ssh', 'editorial', pickle_token)



remote_path = 'public_html/blog/source/'
host = 'crawlab.org'
port = 2222

#file_name = workflow.get_variable('postTitleVar')

file_name = console.input_alert("Filename", "Enter File Name")
confirmation = console.alert('Confirm', 'Go ahead and post?','Yes','No')

file_path = editor.get_path()


try:

	transport = paramiko.Transport((host, port))
	transport.connect(username=user, password=pw)
	sftp = paramiko.SFTPClient.from_transport(transport)
	#sftp.chdir(remote_path)
	sftp.put(remotepath=remote_path+file_name+'.md', localpath=file_path)

	sftp.close()
	transport.close()
	console.hud_alert(file_name + '.md uploaded', 'success')

except Exception, e:
	print e
	console.alert('Error', e)

