#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import hashlib
import string
import random
from math import ceil

from bs4 import BeautifulSoup

from .escape import to_unicode


def safe_float(value, default=0):
    try:
        value = float(value)
    except:
        value = default
    return value


def safe_int(value, default=0):
    try:
        value = int(value)
    except:
        value = default
    return value


def compatmd5(key):
    if isinstance(key, unicode):
        key = key.encode('utf8')
    m = hashlib.md5(str(key))
    return m.hexdigest()


code_list = list(string.ascii_lowercase + string.digits + string.ascii_uppercase)


def get_random_string(num=5):
    return ''.join(random.sample(code_list, num))


def get_ch_text(text):
    """
        返回内容中的中文字符
    """
    if not text:
        return ""
    res = re.findall(u"[\u4e00-\u9fa5]+", to_unicode(text))
    return " ".join(" ".join(res).split()) if res else ""


def remove_emoj(text):
    text = to_unicode(text)
    re_pattern = re.compile(u'[^\u0000-\uD7FF\uE000-\uFFFF]', re.UNICODE)
    filtered_string = re_pattern.sub(u'', text)
    return filtered_string


def remove_html_code(text):
    return re.sub('&#\d+;', '', text)


class FancyDict(dict):

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            return None

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError, k:
            raise AttributeError, k


class Singleton(type):

    '''
    指定 __metaclass__ = Singleton 实现单例
    '''
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Pagination(object):

    def __init__(self, page, per_page, total_count, endpoint=None, params=None):
        self.params = params
        self.endpoint = endpoint
        self.page = page
        self.per_page = per_page
        self.total_count = total_count

    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0
        for num in xrange(1, self.pages + 1):
            if num <= left_edge or \
                (num > self.page - left_current - 1 and
                 num < self.page + right_current) or \
                    num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num


class ClearElement(object):
    allow_tag = ['p', 'img', 'span']

    def __init__(self, content):
        self.content = content
        self.b = BeautifulSoup("")

    def clearup_element(self, element):
        for e in element.find_all(self.allow_tag):
            if e.name == 'p':
                _attrs = ['class']
                e_class = e.get('class', [])
                if e_class and ''.join(e_class) == 'titledesc':
                    _attrs.remove('class')
                for _ in _attrs:
                    del e[_]

            def is_empty():
                return e.string is None or e.string.strip() == "" or not re.sub(r'\\UFEFF', '', e.string.strip(), flags=re.IGNORECASE)

            if e.find_all(True, recursive=False) == [] and is_empty():
                text = re.sub(r'\\UFEFF', '', ''.join(e.get_text().strip().split()), flags=re.IGNORECASE)
                if e.name != 'img' and not text:
                    e.extract()
            else:
                self.clearup_element(e)

    def unwrap_img(self, element, soup):
        top_tag = '[document]'
        parent = element.parent
        if parent.name == 'p':
            parent_parent = parent.parent

            parent_index = parent_parent.index(parent)
            my_index = parent.index(element)

            contents_list = parent.contents[:]

            # 分割后的第一部分
            first_tag = self.b.new_tag("p")
            second_tag = self.b.new_tag("p")
            third_tag = self.b.new_tag("p")
            parent.extract()

            parent_parent.insert(parent_index, third_tag)
            parent_parent.insert(parent_index, second_tag)
            parent_parent.insert(parent_index, first_tag)

            for child in contents_list[:my_index]:
                first_tag.append(child)

            # 分割后的第二部分，也就是img部分

            second_tag.append(element)

            # 分割后的第三部分

            for child in contents_list[my_index + 1:]:
                third_tag.append(child)

        elif parent.name == top_tag:
            element.wrap(self.b.new_tag("p"))
        else:
            self.unwrap_img(parent, soup)

    def process_img(self, soup):
        imgs = soup.find_all('img')
        for c in imgs:
            src = c.get('src', '')
            if src and (src.startswith("http") or src.startswith("https")):
                _attrs = [_ for _ in c.attrs]
                _attrs.remove('src')
                for _ in _attrs:
                    del c[_]
                self.unwrap_img(c, soup)
            else:
                c.extract()

    def clear_spacing(self, soup):
        for e in soup.find_all('p'):
            _s = to_unicode(''.join(e.get_text().strip().split()))
            if _s and not e.find_all():  # 没有字节点才替换内容
                e.string = _s

    def merget_element(self, soup):
        _s = BeautifulSoup("")
        l = ['span']
        #span 嵌套
        for e in soup.find_all(l):
            es = e.find_all(True, recursive=False)
            if es :
                continue
            _ = to_unicode(' '.join(e.get_text().strip().split())).strip()
            if _:
                e.string = _
        for e in soup.find_all(l):
            e.unwrap()
        for e in soup.find_all('p'):
            _s.append(e)
        return _s


    def clearup_content(self):
        soup = BeautifulSoup(self.content)
        self.process_img(soup)
        self.clearup_element(soup)
        soup = self.merget_element(soup)
        self.clear_spacing(soup)
        c = soup.prettify() \
            .replace("<html>", '').replace('<body>', '') \
            .replace("</html>", '').replace('</body>', '')
        return c
