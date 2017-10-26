import uuid, random, requests

class Viva:
	def __init__(self):
		self.session = requests.session()
		self.headers = {
			'Host':             'union.barstoolsports.com', 
			'Content-Type':     'application/x-www-form-urlencoded; charset=utf-8',
			'User-Agent':       'Barstool/730 CFNetwork/808.2.16 Darwin/16.3.0', 
			'X-App-Id':         'ios' 
		}

	def login(self, email:str, password:str):
		self.my_email = email
		self.my_password = password
		self.login_url = 'https://union.barstoolsports.com/v2/auth/login'
		self.login_form_data = {'email':self.my_email, 'password': self.my_password}
		self.response = self.session.post(self.login_url, headers=self.headers, data=self.login_form_data)
		self.login_response = self.response.json()
		return self.login_response

	def get_profile(self):
		self.profile_url = 'https://union.barstoolsports.com/v2/user/profile'
		self.headers['Authorization'] = f'{self.login_response["token_type"]} {self.login_response["token"]}'
		self.response = self.session.get(self.profile_url, headers=self.headers)
		self.profile_response - self.response.json()
		return self.profile_response
	
	def update_profile(self, full_name:str, subscribe_to_newsletter:bool)
		self.full_name = full_name
		self.subscribe_to_newsletter = subscribe_to_newsletter
		self.headers['Authorization'] = f'{self.login_response["token_type"]} {self.login_response["token"]}'
		self.profile_form = {'email':self.my_email, 'name':self.full_name, 'newsletter':int(self.subscribe_to_newsletter),'username':self.login_response['username']}
		self.response = self.session.put(self.profile_url, headers=self.headers, data=self.profile_form)
		self.complete_profile_response = self.response.json()
		return self.complete_profile_response

	def logout(self):
		self.logout_url = f'https://union.barstoolsports.com/v2/user/{self.login_response["userid"]}/notifications/device/unregister/ios'
		self.headers['Authorization'] = f'{self.login_response["token_type"]} {self.login_response["token"]}'
		self.logout_data = {'device_id':str(uuid.uuid4()).upper()} # my device: D75D08DA-3F7E-44FD-982F-76940668659C
		self.response = self.session.post(self.logout_url, headers=self.headers, data=self.logout_data)
		self.logout_response = self.response.json()
		return self.logout_response

	def get_stories(self, number_of_stories:int):
		self.number_of_stories = number_of_stories
		self.story_params = {'limit':str(self.number_of_stories), 'page':'1'}
		self.headers['Authorization'] = f'{self.login_response["token_type"]} {self.login_response["token"]}'
		self.stories_url = f'https://union.barstoolsports.com/v2/stories'
		self.response = self.session.get(self.stories_url, headers=self.headers, params=self.story_params)
		self.stories_response = self.response.json()
		return self.stories_response # submethods here for parsing stories rather than return	

	# nest this method
	def get_story(self):
		self.story_url = f'{self.stories_url}/id/{self.story_id}' # self.story_id from method above - need to parse/integrate methods 
		self.headers['Authorization'] = f'{self.login_response["token_type"]} {self.login_response["token"]}'
		self.response = self.session.get(self.story_url, headers=self.headers)
		self.story_response = self.response.json()
		return self.story_response

	# nest-nest this methods so that we can return for individual story all various attributes
	def get_story_comments(self):
		self.story_comments_url = f'{self.story_url}/comments'
		self.headers['Authorization'] = f'{self.login_response["token_type"]} {self.login_response["token"]}'
		self.response = self.session.get(self.story_comments_url, headers=self.headers)
		self.story_comments_response = self.response.json()
		return self.story_comments_response

	# nest-nest this method
	def post_comment(self, comment:str):
		self.comment = comment
		self.post_comment_url = f'{self.story_comments_url}/add'
		self.headers['Authorization'] = f'{self.login_response["token_type"]} {self.login_response["token"]}'		
		self.comment_form_data = {'message':self.comment, 'username':self.login_response["username"]}
		self.response = self.session.post(self.post_comment_url, headers=self.headers, data=self.comment_form_data)
		self.comment_post_response = self.response.json()
		return self.comment_post_response

	# nest-nest this methods so that we can return for individual story all various attributes
	def get_story_recommendations(self):
		self.story_recommendations_url = f'{self.story_url}/recommendations'
		self.headers['Authorization'] = f'{self.login_response["token_type"]} {self.login_response["token"]}'
		self.response = self.session.get(self.story_recommendations_url, headers=self.headers)
		self.story_recommendations_response = self.response.json()
		return self.story_recommendations_response

	def update_password(self, new_password:str):
		self.new_password = new_password
		self.headers['Authorization'] = f'{self.login_response["token_type"]} {self.login_response["token"]}'
		self.update_password_data = {'new_password':self.new_password, 'password':self.my_password}
		self.response = self.session.put(self.profile_url, headers=self.headers, data=self.update_password_data)
		self.update_password_data_response = self.response.json()
		return self.update_password_data_response

	def get_notification_settings(self):
		self.notifications_url = f'https://union.barstoolsports.com/v2/user/{self.login_response["userid"]}/notifications'
		self.headers['Authorization'] = f'{self.login_response["token_type"]} {self.login_response["token"]}'
		self.response = self.session.get(self.notifications_url, headers=self.headers)
		self.notifications_settings_response = self.response.json()
		return self.notifications_settings_response # get ids of bloggers and authors here to use in change notification method

	# nest this method
	def toggle_notification(self, notifications_on:bool):
		self.notifications_on = notifications_on
		self.toggle_notification_url = f'https://union.barstoolsports.com/v2/user/{self.login_response["userid"]}/notifications/id/{self.blogger_id}' # self.blogger_id from method above - need to parse/integrate methods
		self.headers['Authorization'] = f'{self.login_response["token_type"]} {self.login_response["token"]}'
		self.response = self.session.put(self.toggle_notification_url, headers=self.headers, data={'is_on':str(self.notifications_on).lower()})
		self.toggle_notification_response = self.response.json()
		return self.toggle_notification_response

	def register_device(self):
		self.register_device_url = f'https://union.barstoolsports.com/v2/user/{self.login_response["userid"]}/notifications/device/register/ios'
		self.headers['Authorization'] = f'{self.login_response["token_type"]} {self.login_response["token"]}'
		self.register_data = {'device_id':str(uuid.uuid4()).upper(), 'token':''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(64))} # my device: D75D08DA-3F7E-44FD-982F-76940668659C, see if there is correlation between token and device id
		self.response = self.session.post(self.register_device_url, headers=self.headers, data=self.register_data)
		self.register_device_response = self.response.json()
		return self.register_device_response

	def get_popular_stories(self, number_of_stories:int):
		self.number_of_popular_stories = number_of_stories
		self.headers['Authorization'] = f'{self.login_response["token_type"]} {self.login_response["token"]}'		
		self.popular_story_params = {'limit':str(self.number_of_popular_stories), 'page':'1'}
		self.popular_stories_url = f'{stories_url}/popular'
		self.response = self.session.get(self.popular_stories_url, headers=self.headers, params=self.popular_story_params)
		self.popular_stories_response = self.response.json()
		return self.popular_stories_response

	# integrate the 'brand' and originals methods to be able to pull from a specific author (term_id) 
	def get_brands(self):
		self.brands_url = 'https://union.barstoolsports.com/v2/brands'
		self.headers['Authorization'] = f'{self.login_response["token_type"]} {self.login_response["token"]}'
		self.response = self.session.get(self.brands_url, headers=self.headers)
		self.brands_response = self.response.json()
		return self.brands_response

	def get_all_barstool_originals(self, number_of_barstool_originals:int):
		self.number_of_barstool_originals = number_of_barstool_originals
		self.barsool_originals_url = f'{self.stories_url}/type/barstool_original'
		self.headers['Authorization'] = f'{self.login_response["token_type"]} {self.login_response["token"]}'
		self.barstool_originals_params = {'limit':str(self.number_of_barstool_originals), 'page':'1'}
		self.response = self.session.get(self.barsool_originals_url, headers=self.headers, params=self.barstool_originals_params)
		self.barstool_originals_response = self.response.json()
		return self.barstool_originals_response

	def get_authored_barstool_originals(self, number_of_authored_barstool_originals:int):
		self.number_of_authored_barstool_originals = number_of_authored_barstool_originals
		self.author_barstool_originals_url = f'{self.barsool_originals_url}/{self.author_term_id}' # self.author_term_id pulled from get_brands method for specific author (parse)
		self.headers['Authorization'] = f'{self.login_response["token_type"]} {self.login_response["token"]}'
		self.authored_barstool_originals_params = {'limit':str(self.number_of_authored_barstool_originals), 'page':'1'}
		self.response = self.session.get(self.author_barstool_originals_url, headers=self.headers, params=self.authored_barstool_originals_params)
		self.authored_barstool_originals_response = self.response.json()
		return self.authored_barstool_originals_response

	def get_podcasts(self, number_of_podcasts:int):
		self.number_of_podcasts = number_of_podcasts
		self.podcasts_url = f'{self.stories_url}/type/podcast'
		self.headers['Authorization'] = f'{self.login_response["token_type"]} {self.login_response["token"]}'
		self.podcast_params = {'limit':str(self.number_of_podcasts), 'page':'1'}
		self.response = self.session.get(self.number_of_podcasts, headers=self.headers, params=self.podcast_params)
		self.podcast_response = self.response.json()
		return self.podcast_response

	def get_categories(self):
		self.categories_url = f'{self.stories_url}/categories'
		self.headers['Authorization'] = f'{self.login_response["token_type"]} {self.login_response["token"]}'
		self.response = self.session.get(self.categories_url, headers=self.headers)
		self.categories_response = self.response.json()
		return self.categories_response #ids from here for finer scope feed - used in method below

	def get_category_stories(self, number_of_filtered_stories:int):
		self.number_of_filtered_stories = number_of_filtered_stories
		self.categories_stories_url = f'{self.stories_url}/category/{self.category_id}' # self.category_id from above
		self.headers['Authorization'] = f'{self.login_response["token_type"]} {self.login_response["token"]}'
		self.category_params = {'limit':str(self.number_of_filtered_stories), 'page':'1'}
		self.response = self.session.get(self.categories_stories_url, headers=self.headers, params=self.category_params)
		self.category_stories_response = self.response.json()
		return self.category_stories_response

	def get_top_stories(self, number_of_top_stories:int):
		self.number_of_top_stories = number_of_top_stories
		self.top_stories_url = f'{self.stories_url}/top'
		self.headers['Authorization'] = f'{self.login_response["token_type"]} {self.login_response["token"]}'
		self.top_story_params = {'limit':str(self.number_of_top_stories), 'page':'1'}
		self.response = self.session.get(self.top_stories_url, headers=self.headers, params=self.top_story_params)
		self.top_stories_response = self.response.json()
		return self.top_stories_response

	def search_stories(self, query_text:str):
		self.query_text = query_text
		self.search_url = 'https://f9hcdr2smh-dsn.algolia.net/1/indexes/BarstoolSports/query'
		self.search_headers = {
			'Host':                      'f9hcdr2smh-dsn.algolia.net',
			'Content-Type':              'application/json',
			'X-Algolia-API-Key':         '6796a647ff7046ff14ebe5a07a5c8ec0',
			'User-Agent':                'Algolia for Swift (5.1.0); iOS (10.2)',
			'X-Algolia-Application-Id':  'F9HCDR2SMH'
		}
		self.search_payload = {"params": f'hitsPerPage=10&page=0&query={self.query_text}'}
		self.response = self.session.post(self.search_url, headers=self.search_headers, json=self.search_payload)
		self.search_response = self.response.json()
		return self.search_response # yikes - this parse is going to be scary

	### Store uses shopify ecommerce platform - just search permalinks - I've done enough automating for shopfiy
	### Basically get product id and then can cart with a permalink specifying quantity - product details can be
	### loaded by simply appending json. There's also oembed. Check/poll sitemap for updates - I may flesh this out 
	### when i get around to it

my_account = Viva()
print(my_account.login('myEmail@domain.com', 'thisIsABadPassword1234'))