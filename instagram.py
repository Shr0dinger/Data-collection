import scrapy
import re
import json
from scrapy.http import HtmlResponse
from urllib.parse import urlencode
from instaparser.items import InstaparserItem
from copy import deepcopy

class InstaSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://instagram.com/']
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    inst_login = 'dinger128'
    inst_pwd = '#PWD_INSTAGRAM_BROWSER:10:1638876494:AUlQALPZXuyqeBL+KmUHy2vhlW5F73jKt95BTzUwyaJOqOxoOPybKwRTJ2SbYIn4lBpWWlPYiNVUlod5E2EP5cURy3n6XtxtJhMFp3Oa5mT84wH+2gul2F7k4M470VZFnIibIAJdKlb5b6AY/kTt'
    inst_follow_link = 'https://i.instagram.com/api/v1/friendships/'

    def __init__(self, users):
        super().__init__()
        self.users = users

    def parse(self, response: HtmlResponse):
        csrf = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(self.inst_login_link,
                                 method='POST',
                                 callback=self.login,
                                 formdata={'username': self.inst_login,
                                           'enc_password': self.inst_pwd},
                                 headers={'x-csrftoken': csrf})

    def login(self, response: HtmlResponse):
        j_data = response.json()
        if j_data.get('authenticated'):
            for i in self.users:
                yield response.follow(f'/{i}', callback=self.follow_parse, cb_kwargs={'username': i})


    def follow_parse(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        variables = {'id': user_id, 'first': 12}
        url_posts = f'{self.inst_follow_link}{user_id}/followers/?count=12&search_surface=follow_list_page'
        print()

        yield response.follow(
            url_posts,
            callback=self.follow_user_parse,
            cb_kwargs={'username': username,
                       'user_id': user_id,
                       'variables': deepcopy(variables)}
        )

    def follow_user_parse(self, response: HtmlResponse, username, user_id, variables):
        try:
            j_data = response.json()
            follow_info = j_data.get('users')
            for i in follow_info:
                item = InstaparserItem(
                    user=username,
                    follower_name=i['username'],
                    follower_full_name=i['full_name'],
                    follower_profile_pic_url=i['profile_pic_url']
                )
                yield item
        except Exception as e:
            print(e)

    def fetch_csrf_token(self, text):
        ''' Get csrf-token for auth '''
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')
