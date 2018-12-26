#!/usr/bin/env python
# -- coding: utf-8 --

import os
import time
import urllib
import urllib2
import cookielib
import json
import base64
import re
import sys
import chardet
import HTMLParser
import traceback
from urllib import unquote


def print_ts(message):
    print "[%s] %s" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                       message)


# get task
class Task:
    # init
    def __init__(self, url):
        # url
        self.url = url
        self.headers = {
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0',
            'Upgrade-Insecure-Requests':
            '1',
            'Accept-Language':
            'zh-CN,zh;q=0.8',
            'Connection':
            'Keep-Alive'
        }
        self.postData = ''
        self.httpHandler = urllib2.HTTPHandler(debuglevel=0)
        self.httpsHandler = urllib2.HTTPSHandler(debuglevel=0)
        self.cookies = cookielib.CookieJar()
        self.opener = urllib2.build_opener(
            self.httpHandler, self.httpsHandler,
            urllib2.HTTPCookieProcessor(self.cookies))

    # get id
    def get_id(self):
        try:
            sent_url = 'http://192.168.11.12:8080/get_task.php'
            request = urllib2.Request(url=sent_url, headers=self.headers)
            content = self.opener.open(request)
            twid = content.read()
            print 'The Twitter ID for this task is' + twid
            return twid
        except Exception, e:
            traceback.print_exc()
            print e
            return '-1'

    # sent data
    def send_data(self, formdata):
        try:
            headers = {
                'Accept':
                'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'User-Agent':
                'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0',
                'Content-Type':
                'application/x-www-form-urlencoded',
                'Upgrade-Insecure-Requests':
                '1',
                'Accept-Language':
                'zh-CN,zh;q=0.8',
                'Connection':
                'Keep-Alive'
            }
            data = urllib.urlencode(formdata)
            #====================================================
            _file = open('data_Twitter', 'ab')
            _file.write(data)
            _file.close()
            #====================================================
            request = urllib2.Request(url=self.url, headers=headers, data=data)
            content = self.opener.open(request)
            html = content.read()
            print html
        except Exception, e:
            traceback.print_exc()
            print "receive server err"
            print e


class RedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        print '############ GOT 302 ###############'
        cookiemap = {}
        setcookie = str(headers["Set-Cookie"])
        cookieTokens = [
            "Domain", "Expires", "Path", "Max-Age", 'path', 'domain'
        ]
        tokens = setcookie.split(";")
        for cookie in tokens:
            cookie = cookie.strip()
            if cookie.startswith("Expires="):
                cookies = cookie.split(",", 2)
                if len(cookies) > 2:
                    cookie = cookies[2]
                    cookie = cookie.strip()
            else:
                cookies = cookie.split(",", 1)
                if len(cookies) > 1:
                    cookie = cookies[1]
                    cookie = cookie.strip()
            namevalue = cookie.split("=", 1)
            if len(namevalue) > 1:
                name = namevalue[0]
                value = namevalue[1]
                if name not in cookieTokens:
                    cookiemap[name] = value
        str_cookie = ''
        for key in cookiemap:
            str_cookie = str_cookie + key + '=' + cookiemap[key] + '; '
        str_cookie = str_cookie[:-2]
        req.add_header("Cookie", str_cookie)
        return urllib2.HTTPRedirectHandler.http_error_302(
            self, req, fp, code, msg, headers)


# twitter spider
class Twitter:
    # init
    def __init__(self, url):
        # login url
        self.baseURL = 'https://twitter.com'
        self.headers = {
            'Host':
            'twitter.com',
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'User-Agent':
            'Mozilla/5.0 (Windows NT 5.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
            'Referer':
            'https://twitter.com/',
            'Content-Type':
            'application/x-www-form-urlencoded',
            'Origin':
            'https://twitter.com',
            'Upgrade-Insecure-Requests':
            '1',
            'Accept-Language':
            'zh-CN,zh;q=0.8',
            'Connection':
            'Keep-Alive'
        }

        self.id = ''
        self.task = Task(url)

        # username
        self.email = ''
        self.password = ''
        self.postData = ''
        self.authenticity_token = ''
        self.a = ''
        self.b = ''
        self.c = ''
        self.d = ''
        self.s = ''
        self.cookies = cookielib.CookieJar()
        self.httpHandler = urllib2.HTTPHandler(debuglevel=0)
        self.httpsHandler = urllib2.HTTPSHandler(debuglevel=0)
        self.opener = urllib2.build_opener(
            self.httpHandler, self.httpsHandler, RedirectHandler,
            urllib2.HTTPCookieProcessor(self.cookies))

    # get first page
    def login_first_step(self):
        print '---------------first step start---------------'
        sent_url = 'https://twitter.com'
        request = urllib2.Request(url=sent_url, headers=self.headers)
        html = self.opener.open(request)
        content = html.read()
        pattern = re.compile(
            '<input type="hidden" value="(.*?)" name="authenticity_token">',
            re.S)
        result = re.search(pattern, content)
        if result:
            self.authenticity_token = result.group(1)
        else:
            self.authenticity_token = '-1'
        print self.authenticity_token
        for key in self.cookies:
            print key.name, ':', key.value

        print '---------------first step end-------------------'

    # get second page
    def login_second_step(self):
        print '---------------second step start----------------'
        sent_url = 'https://twitter.com/i/js_inst?c_name=ui_metrics'
        request = urllib2.Request(url=sent_url, headers=self.headers)
        html = self.opener.open(request)
        content = html.read()

        pattern = re.compile("'rf':(.*?);", re.S)
        result = re.search(pattern, content)
        rf = ''
        if result:
            rf = result.group(1)
        pattern = re.compile(
            "{'(.*?)':.*?,'(.*?)':.*?,'(.*?)':.*?,'(.*?)':.*?,'s':'(.*?)'}")
        result = re.search(pattern, rf)
        if result:
            self.a = result.group(1)
            self.b = result.group(2)
            self.c = result.group(3)
            self.d = result.group(4)
            self.s = result.group(5)
            print self.a
            print self.b
            print self.c
            print self.d
            print self.s
        print '---------------second step end------------------'

    # get third page
    def login_third_step(self):
        print '---------------thirt step start-----------------'
        self.postData = 'session[username_or_email]=%s&session[password]=%s&return_to_ssl=true&scribe_log=&redirect_after_login=/&authenticity_token=%s&ui_metrics={"rf":{"%s":-129,"%s":-143,"%s":-33,"%s":-44},"s":"%s"}' % (
            self.email, self.password, self.authenticity_token, self.a, self.b,
            self.c, self.d, self.s)
        sent_url = 'https://twitter.com/sessions'
        request = urllib2.Request(
            url=sent_url, headers=self.headers, data=self.postData)
        html = self.opener.open(request)
        # content = html.read()
        # print content
        print '---------------thirt step end------------------'

    # login api
    def login_twitter(self):
        self.login_first_step()
        self.login_second_step()
        self.login_third_step()

    # get min position
    def get_min_position(self, html):
        result = ''
        html = html.replace('\\"', '"')
        pattern = re.compile('data-min-position="(.*?)"', re.S)
        result = re.search(pattern, html)
        if result:
            return result.group(1)
        else:
            pattern = re.compile('data-min-position=\\\\"(.*?)\\\\"', re.S)
            result = re.search(pattern, html)
            if result:
                return result.group(1)
            else:
                if result:
                    return result.group(1)
                else:
                    pattern = re.compile('"min_position":"(.*?)",', re.S)
                    result = re.search(pattern, html)
                    if result:
                        return result.group(1)
                    else:
                        pattern = re.compile('"max_position":"(.*?)",', re.S)
                        result = re.search(pattern, html)
                        if result:
                            return result.group(1)
                        else:
                            return '0'

    # get pictrue image
    def get_pictrue_imag(self, html):
        sent_url = HTMLParser.HTMLParser().unescape(html)
        headers = {
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0',
            'Content-Type':
            'application/x-www-form-urlencoded',
            'Accept-Language':
            'zh-CN,zh;q=0.8',
            'Connection':
            'Keep-Alive'
        }
        print 'sent_url: ' + sent_url
        request = urllib2.Request(url=sent_url, headers=headers)
        content = self.opener.open(request)
        ContentType = content.headers['Content-Type']
        imgData = base64.b64encode(content.read())
        data_dict = {}
        data_dict['icon_type'] = ContentType
        data_dict['icon'] = imgData
        return data_dict

    # analysis user following
    def analysis_user_following(self, html):
        print '---------------analysis user following start----------------'
        content = unquote(html).replace('&quot;', '"').replace('\n', '')
        strtype = chardet.detect(html)
        if strtype['encoding'] == 'ascii':
            content = content.replace('\\u003c', '<').replace(
                '\\u003e', '>').replace('\\n', '').replace('\\"', '"').replace(
                    '\\/', '/')
            content = content.encode().decode('unicode_escape')
        pattern = re.compile(
            '<div class="js-stream-item".*?</div>  </div></div></div>  </div>',
            re.S)
        items = re.findall(pattern, content)
        for item in items:
            pattern = re.compile(
                'data-screen-name="(.*?)".*?data-user-id="(.*?)".*?class="ProfileCard-avatarImage js-action-profile-avatar" src="(.*?)".*?data-name="(.*?)".*? <p class="ProfileCard-bio u-dir js-ellipsis" dir="ltr" data-aria-label-part>(.*?)<',
                re.S)
            result = re.search(pattern, item)
            if result:
                screen_name = result.group(1)
                user_id = result.group(2)
                name = result.group(4)
                avatar_url = result.group(3)
                remark = result.group(5)
                if remark == '':
                    remark = 'none'
                formdata = {
                    'index': 'social_platform',
                    'type': 'twitter',
                    'id': screen_name,
                    'user_id': user_id,
                    'username': screen_name,
                    'nickname': name,
                    'summary': remark,
                }
                avatar = self.get_pictrue_imag(avatar_url)
                formdata = dict(formdata, **avatar)
                self.task.send_data(formdata)
                formdata = {
                    'index': 'social_platform_relation',
                    'type': 'twitter',
                    'id': self.id + '_' + screen_name,
                    'source': self.id,
                    'target': screen_name,
                    'relation': 'following',
                }
                self.task.send_data(formdata)
        print '---------------analysis user following end----------------'

    # get user followers
    def get_user_following(self):
        try:
            print '--------------get user following start---------------'
            sent_url = 'https://twitter.com/%s/following' % (self.id)
            request = urllib2.Request(url=sent_url, headers=self.headers)
            content = self.opener.open(request)
            html = content.read()
            while True:
                data_min_position = self.get_min_position(html)
                self.analysis_user_following(html)
                if data_min_position == '' or data_min_position == '0':
                    break
                sent_url = 'https://twitter.com/%s/following/users?include_available_features=1&include_entities=1&max_position=%s&reset_error_state=false' % (
                    self.id, data_min_position)
                request = urllib2.Request(url=sent_url, headers=self.headers)
                content = self.opener.open(request)
                html = content.read()
            print '---------------get user following end----------------'
        except Exception, e:
            traceback.print_exc()
            print e

    # analysis user followers
    def analysis_user_followers(self, html):
        print '---------------analysis user followers start----------------'
        content = unquote(html).replace('&quot;', '"').replace('\n', '')
        strtype = chardet.detect(html)
        if strtype['encoding'] == 'ascii':
            content = content.replace('\\u003c', '<').replace(
                '\\u003e', '>').replace('\\n', '').replace('\\"', '"').replace(
                    '\\/', '/')
            content = content.encode().decode('unicode_escape')
        pattern = re.compile(
            '<div class="js-stream-item".*?</div>  </div></div></div>  </div>',
            re.S)
        items = re.findall(pattern, content)
        for item in items:
            pattern = re.compile(
                'data-screen-name="(.*?)".*?data-user-id="(.*?)".*?class="ProfileCard-avatarImage js-action-profile-avatar" src="(.*?)".*?data-name="(.*?)".*? <p class="ProfileCard-bio u-dir js-ellipsis" dir="ltr" data-aria-label-part>(.*?)<',
                re.S)
            result = re.search(pattern, item)
            if result:
                screen_name = result.group(1)
                user_id = result.group(2)
                name = result.group(4)
                avatar_url = result.group(3)
                remark = result.group(5)
                if remark == '':
                    remark = 'none'
                formdata = {
                    'index': 'social_platform',
                    'type': 'twitter',
                    'id': screen_name,
                    'user_id': user_id,
                    'username': screen_name,
                    'nickname': name,
                    'summary': remark,
                }
                avatar = self.get_pictrue_imag(avatar_url)
                formdata = dict(formdata, **avatar)
                self.task.send_data(formdata)
                formdata = {
                    'index': 'social_platform_relation',
                    'type': 'twitter',
                    'id': self.id + '_' + screen_name,
                    'source': self.id,
                    'target': screen_name,
                    'relation': 'followers',
                }
                self.task.send_data(formdata)
        print '---------------analysis user followers end----------------'

    # get user followers
    def get_user_followers(self):
        try:
            print '--------------get user followers start---------------'
            sent_url = 'https://twitter.com/%s/followers' % (self.id)
            print sent_url
            request = urllib2.Request(url=sent_url, headers=self.headers)
            content = self.opener.open(request)
            html = content.read()
            while True:
                data_min_position = self.get_min_position(html)
                print 'data_min_position is ' + data_min_position
                self.analysis_user_followers(html)
                if data_min_position == '' or data_min_position == '0':
                    break
                sent_url = 'https://twitter.com/%s/followers/users?include_available_features=1&include_entities=1&max_position=%s&reset_error_state=false' % (
                    self.id, data_min_position)
                request = urllib2.Request(url=sent_url, headers=self.headers)
                content = self.opener.open(request)
                html = content.read()
            print '---------------get user followers end----------------'
        except Exception, e:
            traceback.print_exc()
            print e

    # analysis user like
    def analysis_user_likes(self, html):
        print '---------------analysis user like start----------------'
        content = unquote(html).replace('&quot;', '"').replace('\n', '')
        strtype = chardet.detect(html)
        if strtype['encoding'] == 'ascii':
            content = content.replace('\\u003c', '<').replace(
                '\\u003e', '>').replace('\\n', '').replace('\\"', '"').replace(
                    '\\/', '/')
            content = content.encode().decode('unicode_escape')
        pattern = re.compile(
            '<li class="js-stream-item stream-item stream-item".*?<span class="u-hiddenVisually">.*?stream-item-footer">',
            re.S)
        items = re.findall(pattern, content)
        for item in items:
            pattern = re.compile(
                'data-screen-name="(.*?)".*?data-name="(.*?)".*?data-user-id="(.*?)".*?class="avatar js-action-profile-avatar" src="(.*?)".*?data-time="(.*?)".*?<p class="TweetTextSize TweetTextSize--normal.*?>(.*?)<',
                re.S)
            result = re.search(pattern, item)
            if result:
                screen_name = result.group(1)
                name = result.group(2)
                user_id = result.group(3)
                avatar_url = result.group(4)
                timestamp = result.group(5)
                remark = result.group(6)
                if remark == '':
                    remark = 'none'
                formdata = {
                    'index': 'social_platform_content_data',
                    'type': 'twitter',
                    'id': user_id + '_' + timestamp,
                    'user_id': user_id,
                    'username': screen_name,
                    'nickname': name,
                    'timestamp': timestamp,
                    'content': remark,
                }
                avatar = self.get_pictrue_imag(avatar_url)
                formdata = dict(formdata, **avatar)
                self.task.send_data(formdata)
                formdata = {
                    'index': 'social_platform_content_relation',
                    'type': 'twitter',
                    'id': self.id + '_' + timestamp,
                    'source': self.id,
                    'target': user_id + '_' + timestamp,
                    'relation': 'like',
                }
                self.task.send_data(formdata)
        print '---------------analysis user like end----------------'

    # get user likes
    def get_user_likes(self):
        try:
            print '--------------get user likes start---------------'
            sent_url = 'https://twitter.com/%s/likes' % (self.id)
            print sent_url
            request = urllib2.Request(url=sent_url, headers=self.headers)
            content = self.opener.open(request)
            html = content.read()
            data_min_position = ''
            while True:
                data_min_position_bak = data_min_position
                data_min_position = self.get_min_position(html)
                self.analysis_user_likes(html)
                print 'data_min_position : '
                print data_min_position
                if data_min_position == '' or data_min_position == '0' or data_min_position == data_min_position_bak:
                    break
                sent_url = 'https://twitter.com/%s/likes/timeline?include_available_features=1&include_entities=1&max_position=%s&reset_error_state=false' % (
                    self.id, data_min_position)
                request = urllib2.Request(url=sent_url, headers=self.headers)
                content = self.opener.open(request)
                html = content.read()
            print '---------------get user likes end----------------'
        except Exception, e:
            traceback.print_exc()
            print e

    # analysis user media
    def analysis_user_media(self, html):
        print '---------------analysis user media start----------------'
        content = unquote(html).replace('&quot;', '"').replace('\n', '')
        strtype = chardet.detect(html)
        if strtype['encoding'] == 'ascii':
            content = content.replace('\\u003c', '<').replace(
                '\\u003e', '>').replace('\\n', '').replace('\\"', '"').replace(
                    '\\/', '/')
            content = content.encode().decode('unicode_escape')
        pattern = re.compile(
            '<li class="js-stream-item stream-item stream-item".*?<span class="u-hiddenVisually">Direct message</span>',
            re.S)
        items = re.findall(pattern, content)
        for item in items:
            pattern = re.compile(
                'data-screen-name="(.*?)".*?data-name="(.*?)".*?data-user-id="(.*?)".*?<img class="avatar js-action-profile-avatar" src="(.*?)".*?data-time="(.*?)".*?<p class="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text".*?>(.*?)<',
                re.S)
            result = re.search(pattern, item)
            if result:
                screen_name = result.group(1)
                name = result.group(2)
                user_id = result.group(3)
                avatar_url = result.group(4)
                timestamp = result.group(5)
                remark = result.group(6)
                if remark == '':
                    remark = 'none'
                formdata = {
                    'index': 'social_platform_content_data',
                    'type': 'twitter',
                    'id': user_id + '_' + timestamp,
                    'user_id': user_id,
                    'username': screen_name,
                    'nickname': name,
                    'timestamp': timestamp,
                    'content': remark,
                }
                avatar = self.get_pictrue_imag(avatar_url)
                formdata = dict(formdata, **avatar)
                self.task.send_data(formdata)
                formdata = {
                    'index': 'social_platform_content_relation',
                    'type': 'twitter',
                    'id': self.id + '_' + timestamp,
                    'source': self.id,
                    'target': user_id + '_' + timestamp,
                    'relation': 'forward',
                }
                self.task.send_data(formdata)
        print '---------------analysis user media end----------------'

    # get user media
    def get_user_media(self):
        try:
            print '--------------get user likes start---------------'
            sent_url = 'https://twitter.com/%s/media' % (self.id)
            print sent_url
            request = urllib2.Request(url=sent_url, headers=self.headers)
            content = self.opener.open(request)
            html = content.read()
            while True:
                data_min_position = self.get_min_position(html)
                self.analysis_user_media(html)
                print 'data_min_position : '
                print data_min_position
                if data_min_position == '' or data_min_position == '0':
                    break
                sent_url = 'https://twitter.com/i/profiles/show/%s/media_timeline?include_available_features=1&include_entities=1&max_position=%s&reset_error_state=false' % (
                    self.id, data_min_position)
                request = urllib2.Request(url=sent_url, headers=self.headers)
                content = self.opener.open(request)
                html = content.read()
            print '---------------get user likes end----------------'
        except Exception, e:
            traceback.print_exc()
            print e

    # analysis user tweets
    def analysis_user_tweets(self, html):
        print '---------------analysis user tweets start----------------'
        content = unquote(html).replace('&quot;', '"').replace('\n', '')
        strtype = chardet.detect(html)
        if strtype['encoding'] == 'ascii':
            content = content.replace('\\u003c', '<').replace(
                '\\u003e', '>').replace('\\n', '').replace('\\"', '"').replace(
                    '\\/', '/')
        pattern = re.compile(
            '<li class="js-stream-item stream-item stream-item".*?<span class="Icon Icon--medium Icon--reply"></span>',
            re.S)
        items = re.findall(pattern, content)
        for item in items:
            pattern = re.compile(
                '.-screen-name="(.*?)".*?data-name="(.*?)".*?data-user-id="(.*?)".*?<img class="avatar js-action-profile-avatar" src="(.*?)".*?data-time="(.*?)".*?<p class="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text".*?>(.*?)</p>',
                re.S)
            result = re.search(pattern, item)
            if result:
                screen_name = result.group(1)
                name = result.group(2)
                user_id = result.group(3)
                avatar_url = result.group(4)
                timestamp = result.group(5)
                remark = result.group(6)
                if remark == '':
                    remark = 'none'
                formdata = {
                    'index': 'social_platform_content_data',
                    'type': 'twitter',
                    'id': user_id + '_' + timestamp,
                    'user_id': user_id,
                    'username': screen_name,
                    'nickname': name,
                    'timestamp': timestamp,
                    'content': remark,
                }
                avatar = self.get_pictrue_imag(avatar_url)
                formdata = dict(formdata, **avatar)
                self.task.send_data(formdata)
                formdata = {
                    'index': 'social_platform_content_relation',
                    'type': 'twitter',
                    'id': self.id + '_' + timestamp,
                    'source': self.id,
                    'target': user_id + '_' + timestamp,
                    'relation': 'forward',
                }
                self.task.send_data(formdata)
        print '---------------analysis user tweets end----------------'

    # get user tweets
    def get_user_tweets(self):
        try:
            print '--------------get user tweets start---------------'
            sent_url = 'https://twitter.com/i/profiles/show/%s/timeline/tweets' % (
                self.id)
            print sent_url
            request = urllib2.Request(url=sent_url, headers=self.headers)
            content = self.opener.open(request)
            html = content.read()
            while True:
                data_min_position = self.get_min_position(html)
                self.analysis_user_tweets(html)
                if data_min_position == '' or data_min_position == '0':
                    break
                sent_url = 'https://twitter.com/i/profiles/show/%s/timeline/tweets?include_available_features=1&include_entities=1&max_position=%s&reset_error_state=false' % (
                    self.id, data_min_position)
                request = urllib2.Request(url=sent_url, headers=self.headers)
                content = self.opener.open(request)
                html = content.read()
            print '---------------get user tweets end----------------'
        except Exception, e:
            traceback.print_exc()
            print e

    # analysis user tweets_replies
    def analysis_user_tweets_replies(self, html):
        print '---------------analysis user tweets_replies start----------------'
        content = unquote(html).replace('&quot;', '"').replace('\n', '')
        strtype = chardet.detect(html)
        if strtype['encoding'] == 'ascii':
            content = content.replace('\\u003c', '<').replace(
                '\\u003e', '>').replace('\\n', '').replace('\\"', '"').replace(
                    '\\/', '/')
        pattern = re.compile(
            '<li class="js-stream-item stream-item stream-item".*?<span class="Icon Icon--medium Icon--reply"></span>',
            re.S)
        items = re.findall(pattern, content)
        for item in items:
            pattern = re.compile(
                'data-screen-name="(.*?)".*?data-name="(.*?)".*?data-user-id="(.*?)".*?<img class="avatar js-action-profile-avatar" src="(.*?)".*?data-time="(.*?)".*?<p class="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text".*?>(.*?)</p>',
                re.S)
            result = re.search(pattern, item)
            if result:
                screen_name = result.group(1)
                name = result.group(2)
                user_id = result.group(3)
                avatar_url = result.group(4)
                timestamp = result.group(5)
                remark = result.group(6)
                if remark == '':
                    remark = 'none'
                formdata = {
                    'index': 'social_platform_content_data',
                    'type': 'twitter',
                    'id': user_id + '_' + timestamp,
                    'user_id': user_id,
                    'username': screen_name,
                    'nickname': name,
                    'timestamp': timestamp,
                    'content': remark,
                }
                avatar = self.get_pictrue_imag(avatar_url)
                formdata = dict(formdata, **avatar)
                self.task.send_data(formdata)
                formdata = {
                    'index': 'social_platform_content_relation',
                    'type': 'twitter',
                    'id': self.id + '_' + timestamp,
                    'source': self.id,
                    'target': user_id + '_' + timestamp,
                    'relation': 'forward',
                }
                self.task.send_data(formdata)
        print '---------------analysis user tweets_replies end----------------'

    # get user tweets
    def get_user_tweets_replies(self):
        try:
            print '--------------get user replies start---------------'
            sent_url = 'https://twitter.com/%s/with_replies' % (self.id)
            print sent_url
            request = urllib2.Request(url=sent_url, headers=self.headers)
            content = self.opener.open(request)
            html = content.read()
            while True:
                data_min_position = self.get_min_position(html)
                self.analysis_user_tweets_replies(html)
                if data_min_position == '' or data_min_position == '0':
                    break
                sent_url = 'https://twitter.com/i/profiles/show/%s/timeline/with_replies?include_available_features=1&include_entities=1&max_position=%s&reset_error_state=false' % (
                    self.id, data_min_position)
                request = urllib2.Request(url=sent_url, headers=self.headers)
                content = self.opener.open(request)
                html = content.read()
            print '---------------get user replies end----------------'
        except Exception, e:
            traceback.print_exc()
            print e

    # analysis user information
    def analysis_user_information(self, html):
        print '---------------analysis user information start----------------'
        content = unquote(html).replace('&quot;', '"').replace('\n', '')
        pattern = re.compile(
            '<img class="ProfileAvatar-image " src="(.*?)" alt="(.*?)">', re.S)
        result = re.search(pattern, content)
        if result:
            avatar_url = result.group(1)
            name = result.group(2)
            print 'avatar_url is ' + avatar_url
            print 'name is ' + name
        else:
            avatar_url = ''
            name = ''
            print 'avatar_url is empty'
            print 'name is empty'

        pattern = re.compile(
            '    <div class="user-actions btn-group not-following not-muting " data-user-id="(.*?)".*?data-screen-name="(.*?)" data-name=".*?" data-protected="false">',
            re.S)
        result = re.search(pattern, content)
        if result:
            user_id = result.group(1)
            screen_name = result.group(2)
            print 'user_id is ' + user_id
            print 'screen_name is ' + screen_name
        else:
            user_id = ''
            screen_name = ''
            print 'user_id is empty'
            print 'screen_name is empty'

        pattern = re.compile(
            '<span class="ProfileNav-label" aria-hidden="true">Tweets</span>.*?data-count=(.*?) data-is-compact="true">',
            re.S)
        result = re.search(pattern, content)
        if result:
            tweets_count = result.group(1)
            print 'tweets_count is ' + tweets_count
        else:
            tweets_count = ''
            print 'tweets_count is empty'

        pattern = re.compile(
            '<span class="ProfileNav-label" aria-hidden="true">Following</span>.*?data-count=(.*?) data-is-compact="false">',
            re.S)
        result = re.search(pattern, content)
        if result:
            following_count = result.group(1)
            print 'following_count is ' + following_count
        else:
            following_count = ''
            print 'following_count is empty'

        pattern = re.compile(
            '<span class="ProfileNav-label" aria-hidden="true">Followers</span>.*?data-count=(.*?) data-is-compact="true">',
            re.S)
        result = re.search(pattern, content)
        if result:
            followers_count = result.group(1)
            print 'followers_count is ' + followers_count
        else:
            followers_count = ''
            print 'followers_count is empty'

        pattern = re.compile(
            '<span class="ProfileNav-label" aria-hidden="true">Likes</span>.*?data-count=(.*?) data-is-compact="false">',
            re.S)
        result = re.search(pattern, content)
        if result:
            likes_count = result.group(1)
            print 'likes_count is ' + likes_count
        else:
            likes_count = ''
            print 'likes_count is empty'
        formdata = {
            'index': 'social_platform',
            'type': 'twitter',
            'id': screen_name,
            'nickname': name,
            'username': screen_name,
            'user_id': user_id,
            'article_count': tweets_count,
            'following_count': following_count,
            'followers_count': followers_count,
            'likes_count': likes_count,
        }
        avatar = self.get_pictrue_imag(avatar_url)
        formdata = dict(formdata, **avatar)
        self.task.send_data(formdata)
        print '---------------analysis user information end----------------'

    # get user information
    def get_user_information(self):
        try:
            print '--------------get user information start---------------'
            sent_url = 'https://twitter.com/%s' % (self.id)
            print sent_url
            request = urllib2.Request(url=sent_url, headers=self.headers)
            content = self.opener.open(request)
            html = content.read()
            self.analysis_user_information(html)
            print '---------------get user information end----------------'
        except Exception, e:
            traceback.print_exc()
            print e

    def run(self, interval, userid, email, password):
        try:
            self.id = userid
            self.email = email
            self.password = password
            self.login_twitter()

            # sleep for the remaining seconds of interval
            time_remaining = interval - time.time() % interval
            print("Sleeping until %s (%s seconds)..." % (
                (time.ctime(time.time() + time_remaining)), time_remaining))
            time.sleep(time_remaining)
            # get twitter data
            if self.id != '-1':
                # get data
                self.get_user_information()
                self.get_user_followers()
                self.get_user_following()
                self.get_user_likes()
                self.get_user_media()
                self.get_user_tweets()
                self.get_user_tweets_replies()

        except Exception, e:
            traceback.print_exc()
            print e


if __name__ == "__main__":

    if len(sys.argv) != 5:
        print 'The parameters are incorrect, please check the parameters.'
        exit()

    # userid = 目标ID
    # email = 爬虫配置账号
    # password = 爬虫配置密码
    # receive_url = 服务器回连地址

    interval = 60
    userid = sys.argv[1]
    email = sys.argv[2]
    password = sys.argv[3]
    receive_url = sys.argv[4]

    twitter = Twitter(receive_url)
    twitter.run(interval, userid, email, password)
