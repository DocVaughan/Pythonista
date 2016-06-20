# coding: utf-8
import twitter

def main():
	accounts = twitter.get_all_accounts()
	if not accounts:
		print('No Twitter accounts were found. You can configure Twitter accounts in the settings app. If you have denied access to your accounts when prompted, you can also change your mind there.')
	account = accounts[0]
	username = account['username']
	print('Loading recent tweets in %s\'s timeline...' % (username,))
	tweets = twitter.get_home_timeline(account)
	for tweet in tweets:
		print('%s:\n\n%s' % (tweet['user']['screen_name'], tweet['text']))
		print('-' * 40)

if __name__ == '__main__':
	main()