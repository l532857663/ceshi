#!/usr/bin/env python
# -*- coding:UTF-8 -*-

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

reload(sys)
sys.setdefaultencoding('UTF-8')


def print_ts(message):
    print "[%s] %s" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                       message)


# get task
class Task:
    # init
    def __init__(self, url):
        # url
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
        self.url = url
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
            liid = content.read()
            print 'The Facebook ID for this task is' + liid
            return liid
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
            print data
            request = urllib2.Request(url=self.url, headers=headers, data=data)
            content = self.opener.open(request)
            html = content.read()
            #print html
        except Exception, e:
            traceback.print_exc()


class RedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        print('############ GOT 302 ###############')
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
        # print cookiemap
        str_cookie = ''
        for key in cookiemap:
            str_cookie = str_cookie + key + '=' + cookiemap[key] + '; '
        str_cookie = str_cookie[:-2]
        # print str_cookie
        req.add_header("Cookie", str_cookie)
        return urllib2.HTTPRedirectHandler.http_error_302(
            self, req, fp, code, msg, headers)


# linkedin spider
class Linkedin:
    # init
    def __init__(self, url):
        # login url
        self.baseURL = 'https://www.linkedin.com'
        self.headers = {
            'Host':
            'www.linkedin.com',
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0',
            'Referer':
            'https://www.linkedin.com/',
            'Content-Type':
            'application/x-www-form-urlencoded',
            'Origin':
            'https://www.linkedin.com',
            'Upgrade-Insecure-Requests':
            '1',
            'Accept-Language':
            'zh-CN,zh;q=0.8',
            'Connection':
            'Keep-Alive'
        }

        self.task = Task(url)
        self.id = ''

        # username
        self.email = ''
        self.password = ''
        self.postData = ''
        self.account_id = ''
        self.async_get_token = ''
        self.loginCsrfParam = ''
        self.cookies = cookielib.CookieJar()
        self.httpHandler = urllib2.HTTPHandler(debuglevel=0)
        self.httpsHandler = urllib2.HTTPSHandler(debuglevel=0)
        self.opener = urllib2.build_opener(
            self.httpHandler, self.httpsHandler, RedirectHandler,
            urllib2.HTTPCookieProcessor(self.cookies))

    # get first page
    def login_first_step(self):
        print('---------------first step start---------------')
        sent_url = 'https://www.linkedin.com'
        request = urllib2.Request(url=sent_url, headers=self.headers)
        content = self.opener.open(request)
        html = content.read()
        pattern = re.compile(
            '<input name="loginCsrfParam" id="loginCsrfParam-login" type="hidden" value="(.*?)"/>',
            re.S)
        result = re.search(pattern, html)
        if result:
            self.loginCsrfParam = result.group(1)
        else:
            self.loginCsrfParam = '-1'

        print self.loginCsrfParam

        for key in self.cookies:
            print key.name, ':', key.value

        self.postData = 'session_key=' + self.email + '&session_password=' + self.password + '&isJsEnabled=false&loginCsrfParam=' + self.loginCsrfParam

        print('---------------first step end-------------------')

    # get second page
    def login_second_step(self):
        print '---------------second step start----------------'
        sent_url = 'https://www.linkedin.com/uas/login-submit?loginSubmitSource=GUEST_HOME'
        request = urllib2.Request(
            url=sent_url, headers=self.headers, data=self.postData)
        content = self.opener.open(request)
        html = content.read()
        print '---------------second step end------------------'

    # get third page
    def login_third_step(self):
        print '---------------thirt step start-----------------'
        sent_url = 'https://www.linkedin.com/feed/'
        request = urllib2.Request(url=sent_url, headers=self.headers)
        content = self.opener.open(request)
        html = content.read()
        print '---------------thirt step end------------------'

    # login api
    def login_linkedin(self):
        self.login_first_step()
        self.login_second_step()
        self.login_third_step()

    # get pictrue image
    def get_pictrue_imag(self, sent_url):
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
        request = urllib2.Request(url=sent_url, headers=headers)
        content = self.opener.open(request)
        ContentType = content.headers['Content-Type']
        imgData = urllib.quote(base64.b64encode(content.read()))
        data_dict = {'Content-Type': ContentType, 'avatar': imgData}
        return data_dict

    # analysis user information
    def analysis_user_information(self, html, url):
        print '---------------get user information start----------------'

        content = unquote(html).replace('&quot;', '"')
        data_dict = {}

        data_dict['index'] = 'social_platform'
        data_dict['type'] = 'linkedin'
        data_dict['id'] = url

        # 个人信息
        profile_txt = ' '.join(
            re.findall(
                '(\{[^\{]*?\{[^\{]*?profile\.Profile"[^\}]*?\}[^\}]*?\}[^\}]*?\}[^\}]*?\})',
                content))
        if profile_txt:

            firstname = re.findall('"firstName":"(.*?)"', profile_txt)
            lastname = re.findall('"lastName":"(.*?)"', profile_txt)
            # 姓名
            if firstname and lastname:
                Name = lastname[0] + firstname[0]
                print 'Name: %s' % Name
                data_dict['lastname'] = lastname[0]
                data_dict['firstname'] = firstname[0]
                data_dict['Name'] = Name

            # 简介
            summary = re.findall('"summary":"(.*?)"', profile_txt)
            if summary:
                print 'summary: %s' % summary[0]
                data_dict['summary'] = summary[0]

            # 职业
            occupation = re.findall('"headline":"(.*?)"', profile_txt)
            if occupation:
                print 'occupation: %s' % occupation[0]
                data_dict['occupation'] = occupation[0]

            # 地址
            locationName = re.findall('"locationName":"(.*?)"', profile_txt)
            if locationName:
                print 'locationName: %s' % locationName[0]
                data_dict['location'] = locationName[0]

        # 好友人数
        networkInfo_txt = ' '.join(
            re.findall('(\{[^\{]*?profile\.ProfileNetworkInfo"[^\}]*?\})',
                       content))
        if networkInfo_txt:
            connectionsCount = re.findall('"connectionsCount":(\d+)',
                                          networkInfo_txt)
            if connectionsCount:
                print 'connectionsCount: %s' % connectionsCount[0]
                data_dict['friends_count'] = connectionsCount[0]

        # 芝麻信用
        sesameCredit_txt = ' '.join(
            re.findall('(\{[^\{]*?profile\.SesameCreditGradeInfo"[^\}]*?\})',
                       content))
        if sesameCredit_txt:
            credit_lastModifiedAt = re.findall('"lastModifiedAt":(\d+)',
                                               sesameCredit_txt)
            credit_grade = re.findall('"grade":"(.*?)"', sesameCredit_txt)

            if credit_grade and credit_grade[0] in CREDIT_GRADE.keys():

                credit_lastModifiedAt_date = time.strftime(
                    '%Y-%m-%d %H:%M:%S',
                    time.localtime(int(credit_lastModifiedAt[0][:10]))
                ) if credit_lastModifiedAt else ''

                sesameCredit = CREDIT_GRADE[credit_grade[
                    0]] + ' 最后更新时间: %s' % credit_lastModifiedAt_date if credit_lastModifiedAt_date else ''
                print '芝麻信用: %s' % sesameCredit
                data_dict['sesame_credit'] = sesameCredit

        # 微信
        wechat_txt = ' '.join(
            re.findall('(\{[^\{]*?profile\.WeChatContactInfo"[^\}]*?\})',
                       content))
        if wechat_txt:
            wechat_image = re.findall('"qrCodeImageUrl":"(http.*?)"',
                                      wechat_txt)
            wechat_name = re.findall('"name":"(.*?)"', wechat_txt)

            # 微信昵称
            if wechat_name:
                print 'wechat_name: %s' % wechat_name[0]
                print 'wechat_image(链接): %s' % (wechat_image[0].replace(
                    '&#61;', '=').replace('&amp;', '&')
                                                if wechat_image else '')
                data_dict['wechat_name'] = wechat_name[0]
                data_dict['wechat_image'] = (wechat_image[0].replace(
                    '&#61;', '=').replace('&amp;', '&')
                                             if wechat_image else '')

            # 微信二维码
            elif wechat_image:
                print 'wechat_image(链接): %s' % wechat_image[0].replace(
                    '&#61;', '')
                data_dict['wechat_image'] = wechat_image[0].replace(
                    '&#61;', '')

        # 个人网站
        website_txt = ' '.join(
            re.findall('("included":.*?profile\.StandardWebsite",.*?\})',
                       content))
        if website_txt:
            website = re.findall('"url":"(.*?)"', website_txt)
            if website:
                print 'website: %s' % website[0]
                data_dict['website'] = website[0]

        # 教育经历
        educations = re.findall('(\{[^\{]*?profile\.Education"[^\}]*?\})',
                                content)
        if educations:
            Education = ''
            for one in educations:
                schoolName = re.findall('"schoolName":"(.*?)"', one)
                fieldOfStudy = re.findall('"fieldOfStudy":"(.*?)"', one)
                degreeName = re.findall('"degreeName":"(.*?)"', one)
                timePeriod = re.findall('"timePeriod":"(.*?)"', one)
                schoolTime = ''
                if timePeriod:
                    startdate_txt = ' '.join(
                        re.findall(
                            '(\{[^\{]*?"\$id":"%s,startDate"[^\}]*?\})' %
                            timePeriod[0].replace('(', '\(').replace(
                                ')', '\)'), content))
                    enddate_txt = ' '.join(
                        re.findall(
                            '(\{[^\{]*?"\$id":"%s,endDate"[^\}]*?\})' %
                            timePeriod[0].replace('(', '\(').replace(
                                ')', '\)'), content))
                    start_year = re.findall('"year":(\d+)', startdate_txt)
                    start_month = re.findall('"month":(\d+)', startdate_txt)
                    end_year = re.findall('"year":(\d+)', enddate_txt)
                    end_month = re.findall('"month":(\d+)', enddate_txt)
                    startdate = ''
                    if start_year:
                        startdate += '%s' % start_year[0]
                    if start_month:
                        startdate += '.%s' % start_month[0]
                    enddate = ''
                    if end_year:
                        enddate += '%s' % end_year[0]
                    if end_month:
                        enddate += '.%s' % end_month[0]
                    if len(startdate) > 0 and len(enddate) == 0:
                        enddate = '现在'
                    schoolTime += '   %s ~ %s' % (startdate, enddate)
                if schoolName:
                    fieldOfStudy = ' %s' % fieldOfStudy[
                        0] if fieldOfStudy else ''
                    degreeName = ' %s' % degreeName[0] if degreeName else ''
                    Education = Education + schoolName[
                        0] + schoolTime + fieldOfStudy + degreeName + '\n'
            if Education:
                data_dict['education'] = Education

        # 工作经历
        position = re.findall('(\{[^\{]*?profile\.Position"[^\}]*?\})',
                              content)
        if position:
            Position = ''
            for one in position:
                companyName = re.findall('"companyName":"(.*?)"', one)
                title = re.findall('"title":"(.*?)"', one)
                locationName = re.findall('"locationName":"(.*?)"', one)
                timePeriod = re.findall('"timePeriod":"(.*?)"', one)
                positionTime = ''
                if timePeriod:
                    startdate_txt = ' '.join(
                        re.findall(
                            '(\{[^\{]*?"\$id":"%s,startDate"[^\}]*?\})' %
                            timePeriod[0].replace('(', '\(').replace(
                                ')', '\)'), content))
                    enddate_txt = ' '.join(
                        re.findall(
                            '(\{[^\{]*?"\$id":"%s,endDate"[^\}]*?\})' %
                            timePeriod[0].replace('(', '\(').replace(
                                ')', '\)'), content))
                    start_year = re.findall('"year":(\d+)', startdate_txt)
                    start_month = re.findall('"month":(\d+)', startdate_txt)
                    end_year = re.findall('"year":(\d+)', enddate_txt)
                    end_month = re.findall('"month":(\d+)', enddate_txt)
                    startdate = ''
                    if start_year:
                        startdate += '%s' % start_year[0]
                    if start_month:
                        startdate += '.%s' % start_month[0]
                    enddate = ''
                    if end_year:
                        enddate += '%s' % end_year[0]
                    if end_month:
                        enddate += '.%s' % end_month[0]
                    if len(startdate) > 0 and len(enddate) == 0:
                        enddate = '现在'
                    positionTime += '   %s ~ %s' % (startdate, enddate)
                if companyName:
                    title = ' %s' % title[0] if title else ''
                    locationName = ' %s' % locationName[
                        0] if locationName else ''
                    Position = Position + companyName[
                        0] + positionTime + title + locationName + '\n'
            if Position:
                data_dict['position'] = Position

        # 出版作品
        publication = re.findall('(\{[^\{]*?profile\.Publication"[^\}]*?\})',
                                 content)
        if publication:
            Publication = ''
            for one in publication:
                name = re.findall('"name":"(.*?)"', one)
                publisher = re.findall('"publisher":"(.*?)"', one)
                if name:
                    Publication = name[0]
                    if publisher:
                        Publication = Publication + '(出版社:' + publisher + ')' + '\n'
                    else:
                        Publication = Publication + '\n'
            if Publication:
                data_dict['publication'] = Publication

        # 荣誉奖项
        honor = re.findall('(\{[^\{]*?profile\.Honor"[^\}]*?\})', content)
        if honor:
            Honor = ''
            for one in honor:
                title = re.findall('"title":"(.*?)"', one)
                issuer = re.findall('"issuer":"(.*?)"', one)
                issueDate = re.findall('"issueDate":"(.*?)"', one)
                issueTime = ''
                if issueDate:
                    issueDate_txt = ' '.join(
                        re.findall(
                            '(\{[^\{]*?"\$id":"%s"[^\}]*?\})' %
                            issueDate[0].replace('(', '\(').replace(')', '\)'),
                            content))
                    year = re.findall('"year":(\d+)', issueDate_txt)
                    month = re.findall('"month":(\d+)', issueDate_txt)
                    if year:
                        issueTime += '   发行时间: %s' % year[0]
                    if month:
                        issueTime += '.%s' % month[0]
                if title:
                    Honor = Honor + title[0] + ' 发行人:' + issuer[
                        0] + ' 发行时间:' + issueTime
            if Honor:
                data_dict['honor'] = Honor

        # 参与组织
        organization = re.findall('(\{[^\{]*?profile\.Organization"[^\}]*?\})',
                                  content)
        if organization:
            Organization = ''
            for one in organization:
                name = re.findall('"name":"(.*?)"', one)
                timePeriod = re.findall('"timePeriod":"(.*?)"', one)
                organizationTime = ''
                if timePeriod:
                    startdate_txt = ' '.join(
                        re.findall(
                            '(\{[^\{]*?"\$id":"%s,startDate"[^\}]*?\})' %
                            timePeriod[0].replace('(', '\(').replace(
                                ')', '\)'), content))
                    enddate_txt = ' '.join(
                        re.findall(
                            '(\{[^\{]*?"\$id":"%s,endDate"[^\}]*?\})' %
                            timePeriod[0].replace('(', '\(').replace(
                                ')', '\)'), content))
                    start_year = re.findall('"year":(\d+)', startdate_txt)
                    start_month = re.findall('"month":(\d+)', startdate_txt)
                    end_year = re.findall('"year":(\d+)', enddate_txt)
                    end_month = re.findall('"month":(\d+)', enddate_txt)
                    startdate = ''
                    if start_year:
                        startdate += '%s' % start_year[0]
                    if start_month:
                        startdate += '.%s' % start_month[0]
                    enddate = ''
                    if end_year:
                        enddate += '%s' % end_year[0]
                    if end_month:
                        enddate += '.%s' % end_month[0]
                    if len(startdate) > 0 and len(enddate) == 0:
                        enddate = '现在'
                    organizationTime += ' %s ~ %s' % (startdate, enddate)
                if name:
                    Organization = Organization + name[
                        0] + organizationTime + '\n'
            if Organization:
                data_dict['organization'] = Organization

        # 专利发明
        patent = re.findall('(\{[^\{]*?profile\.Patent"[^\}]*?\})', content)
        if patent:
            Patent = ''
            for one in patent:
                title = re.findall('"title":"(.*?)"', one)
                issuer = re.findall('"issuer":"(.*?)"', one)
                url = re.findall('"url":"(http.*?)"', one)
                number = re.findall('"number":"(.*?)"', one)
                localizedIssuerCountryName = re.findall(
                    '"localizedIssuerCountryName":"(.*?)"', one)
                issueDate = re.findall('"issueDate":"(.*?)"', one)
                patentTime = ''
                if issueDate:
                    issueDate_txt = ' '.join(
                        re.findall(
                            '(\{[^\{]*?"\$id":"%s"[^\}]*?\})' %
                            issueDate[0].replace('(', '\(').replace(')', '\)'),
                            content))
                    year = re.findall('"year":(\d+)', issueDate_txt)
                    month = re.findall('"month":(\d+)', issueDate_txt)
                    day = re.findall('"day":(\d+)', issueDate_txt)
                    if year:
                        patentTime += ' 发行时间: %s' % year[0]
                    if month:
                        patentTime += '.%s' % month[0]
                    if day:
                        patentTime += '.%s' % day[0]
                if title:
                    print '    %s %s %s %s %s %s' % (
                        title[0], '   发行者: %s' % issuer[0] if issuer else '',
                        '   专利号: %s' % number[0] if number else '',
                        '   所在国家: %s' % localizedIssuerCountryName[0]
                        if localizedIssuerCountryName else '', patentTime,
                        '   专利详情页: %s' % url[0] if url else '')
                    Patent = Patent + title[0] + '发行者: ' + issuer[
                        0] + '专利号: ' + number[
                            0] + '所在国家: ' + localizedIssuerCountryName[
                                0] + patentTime + '专利详情页:' + url[0] + '\n'
            if Patent:
                data_dict['patent'] = Patent

        # 所做项目
        project = re.findall('(\{[^\{]*?profile\.Project"[^\}]*?\})', content)
        if project:
            Project = ''
            for one in project:
                title = re.findall('"title":"(.*?)"', one)
                description = re.findall('"description":"(.*?)"', one)
                timePeriod = re.findall('"timePeriod":"(.*?)"', one)
                projectTime = ''
                if timePeriod:
                    startdate_txt = ' '.join(
                        re.findall(
                            '(\{[^\{]*?"\$id":"%s,startDate"[^\}]*?\})' %
                            timePeriod[0].replace('(', '\(').replace(
                                ')', '\)'), content))
                    enddate_txt = ' '.join(
                        re.findall(
                            '(\{[^\{]*?"\$id":"%s,endDate"[^\}]*?\})' %
                            timePeriod[0].replace('(', '\(').replace(
                                ')', '\)'), content))
                    start_year = re.findall('"year":(\d+)', startdate_txt)
                    start_month = re.findall('"month":(\d+)', startdate_txt)
                    end_year = re.findall('"year":(\d+)', enddate_txt)
                    end_month = re.findall('"month":(\d+)', enddate_txt)
                    startdate = ''
                    if start_year:
                        startdate += '%s' % start_year[0]
                    if start_month:
                        startdate += '.%s' % start_month[0]
                    enddate = ''
                    if end_year:
                        enddate += '%s' % end_year[0]
                    if end_month:
                        enddate += '.%s' % end_month[0]
                    if len(startdate) > 0 and len(enddate) == 0:
                        enddate = '现在'
                        projectTime += '   时间: %s ~ %s' % (startdate, enddate)
                if title:
                    Project = Project + title[0] + '发行者: ' + projectTime[
                        0] + '项目描述: ' + description[0] + '\n'
            if Project:
                data_dict['project'] = Project

        # 志愿者经历
        volunteer = re.findall(
            '(\{[^\{]*?profile\.VolunteerExperience"[^\}]*?\})', content)
        if volunteer:
            Volunteer = ''
            for one in volunteer:
                companyName = re.findall('"companyName":"(.*?)"', one)
                role = re.findall('"role":"(.*?)"', one)
                timePeriod = re.findall('"timePeriod":"(.*?)"', one)
                volunteerTime = ''
                if timePeriod:
                    startdate_txt = ' '.join(
                        re.findall(
                            '(\{[^\{]*?"\$id":"%s,startDate"[^\}]*?\})' %
                            timePeriod[0].replace('(', '\(').replace(
                                ')', '\)'), content))
                    enddate_txt = ' '.join(
                        re.findall(
                            '(\{[^\{]*?"\$id":"%s,endDate"[^\}]*?\})' %
                            timePeriod[0].replace('(', '\(').replace(
                                ')', '\)'), content))
                    start_year = re.findall('"year":(\d+)', startdate_txt)
                    start_month = re.findall('"month":(\d+)', startdate_txt)
                    end_year = re.findall('"year":(\d+)', enddate_txt)
                    end_month = re.findall('"month":(\d+)', enddate_txt)
                    startdate = ''
                    if start_year:
                        startdate += '%s' % start_year[0]
                    if start_month:
                        startdate += '.%s' % start_month[0]
                    enddate = ''
                    if end_year:
                        enddate += '%s' % end_year[0]
                    if end_month:
                        enddate += '.%s' % end_month[0]
                    if len(startdate) > 0 and len(enddate) == 0:
                        enddate = '现在'
                volunteerTime += ' 时间: %s ~ %s' % (startdate, enddate)
                if companyName:
                    Volunteer = Volunteer + companyName[0] + volunteerTime[
                        0] + ' 角色: ' + role[0] + '\n'
            if Volunteer:
                data_dict['volunteer'] = Volunteer

        self.task.send_data(data_dict)
        print data_dict
        print '---------------get user information end----------------'

    # get user information
    def get_user_information(self):
        try:
            print '--------------get user information start---------------'
            sent_url = 'https://www.linkedin.com/in/' + self.id
            print sent_url
            request = urllib2.Request(url=sent_url, headers=self.headers)
            content = self.opener.open(request)
            html = content.read()
            self.analysis_user_information(html,
                                           'www.linkedin.com/in/' + self.id)
        except Exception, e:
            traceback.print_exc()
            print e

    def run(self, interval, id, email, password):
        try:
            self.id = id
            self.email = email
            self.password = password
            self.login_linkedin()

            # sleep for the remaining seconds of interval
            #time_remaining = interval - time.time() % interval
            #print_ts("Sleeping until %s (%s seconds)..." % (
            #(time.ctime(time.time() + time_remaining)), time_remaining))
            #time.sleep(time_remaining)

            # get linkedin data
            if self.id != '-1':
                # get data
                self.get_user_information()

        except Exception, e:
            traceback.print_exc()
            print e


# linkedin data entry

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

    linkedin = Linkedin(receive_url)
    linkedin.run(interval, userid, email, password)
