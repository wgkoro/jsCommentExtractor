#!/usr/bin/env python
# -*- coding:utf-8 -*-
import urllib.request
import pyparsing
import sys
import os
import datetime
import time
from xml.sax.saxutils import *

class JsCommentExtractor:
    def __init__(self):
        self._comments = []
        self._charset = 'utf-8'

    def _extractComment(self, js):
        for match in pyparsing.javaStyleComment.scanString(js):
            self._comments.append(match[0][0])

        return self._comments

    def extract(self, url, charset='utf-8'):
        self._charset = charset
        js = self._fetchPage(url)
        self._extractComment(js)

    def getCommentList(self):
        return self._comments

    def _fetchPage(self, url):
        js = ''
        with urllib.request.urlopen(url) as page:
            for line in page.readlines():
                js += line.decode(self._charset)

        return js



class RenderResult:
    def __init__(self):
        self._current_dir = os.path.abspath(os.path.dirname(__file__))

    def render(self, url, comment_list, charset='utf-8'):
        template = self._readTemplate(charset)
        html = self._assembleList(comment_list)

        now = datetime.datetime.now()
        file_name = '%s.html' % time.mktime(now.timetuple())
        output = os.path.join(self._current_dir, file_name)

        output_html = template.replace('%url', url)
        output_html = output_html.replace('%list', html)
    
        fh = open(output, 'w')
        fh.write(output_html)
        fh.close()


    def _readTemplate(self, charset):
        template_path = os.path.join(self._current_dir, 'template.html')
        html = ''
        for line in open(template_path, 'r'):
            html += line

        if charset != 'utf-8':
            html = html.decode(charset)

        return html

    def _assembleList(self, comment_list):
        html = ''
        template = '<li>%s</li>\n'
        for comment in comment_list:
            li = template % escape(comment)
            html += li.replace('\n', '<br>')

        return html



if __name__ == '__main__':
    argvs = sys.argv
    count = len(argvs)
    charset = 'utf-8'

    if count < 2:
        sys.exit('URL not defined.')

    if count > 3:
        charset = argvs[2]

    url = argvs[1]

    ex = JsCommentExtractor()
    ex.extract(url, charset)
    comments = ex.getCommentList()

    result = RenderResult()
    result.render(url, comments)
