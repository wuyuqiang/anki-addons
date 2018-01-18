#-*- coding:utf-8 -*-
import base64
import re
import urllib
import urllib2

from aqt.utils import showInfo
from BeautifulSoup import BeautifulSoup
from .base import WebService, export, register, with_styles

# Anki buit-in BeautifulSoup is bs3 not bs4


css = ''


@register(u'西语助手')
class Esdict(WebService):

    def __init__(self):
        super(Esdict, self).__init__()

    def _get_content(self):
        url = 'https://www.esdict.cn/mdicts/es/{word}'.format(
            word=urllib.quote(self.word.encode('utf-8')))
        try:
            result = {}
            html = urllib2.urlopen(url, timeout=5).read()
            soup = BeautifulSoup(html)

            def _get_from_element(dict, key, soup, tag, id=None, class_=None):
                baseURL = 'https://www.esdict.cn/'
                # element = soup.find(tag, id=id, class_=class_)  # bs4
                if id:
                    element = soup.find(tag, {"id": id})
                if class_:
                    element = soup.find(tag, {"class": class_})
                if element:
                    dict[key] = str(element)
                    dict[key] = re.sub(
                        r'href="/', 'href="' + baseURL, dict[key])
                    dict[key] = re.sub(r'声明：.*。', '', dict[key])
                    dict[key] = dict[key].decode('utf-8')
                return dict

            # '<span class="Phonitic">[bɔ̃ʒur]</span>'
            result = _get_from_element(
                result, 'phonitic', soup, 'span', class_='Phonitic')
            # '<div id='FCChild'  class='expDiv'>'
            result = _get_from_element(
                result, 'fccf', soup, 'div', id='FCChild')  # 西汉-汉西词典
            result = _get_from_element(
                result, 'example', soup, 'div', id='LJChild')  # 西语例句库
            result = _get_from_element(
                result, 'syn', soup, 'div', id='SYNChild')  # 近义、反义、派生词典
            result = _get_from_element(
                result, 'ff', soup, 'div', id='FFChild')  # 西西词典
            result = _get_from_element(
                result, 'fe', soup, 'div', id='FEChild')  # 西英词典

            return self.cache_this(result)
        except Exception as e:
            return {}

    def _get_field(self, key, default=u''):
        return self.cache_result(key) if self.cached(key) else self._get_content().get(key, default)

    @export(u'真人发音', 0)
    def fld_sound(self):
        # base64.b64encode('bonjour') == 'Ym9uam91cg=='
        # https://api.frdic.com/api/v2/speech/speakweb?langid=fr&txt=QYNYm9uam91cg%3d%3d
        url = 'https://api.frdic.com/api/v2/speech/speakweb?langid=es&txt=QYN{word}'.format(
            word=urllib.quote(base64.b64encode(self.word.encode('utf-8'))))
        audio_name = u'esdict_{word}.mp3'.format(word=self.word)
        try:
            urllib.urlretrieve(url, audio_name)
            return self.get_anki_label(audio_name, 'audio')
        except Exception as e:
            return ''

    @export(u'音标', 1)
    def fld_phonetic(self):
        return self._get_field('phonitic')

    @export(u'西汉-汉西词典', 2)
    @with_styles(css=css)
    def fld_fccf(self):
        return self._get_field('fccf')

    @export(u'西语例句库', 3)
    @with_styles(css=css)
    def fld_example(self):
        return self._get_field('example')

    @export(u'近义、反义、派生词典', 4)
    def fld_syn(self):
        return self._get_field('syn')

    @export(u'西西词典', 5)
    @with_styles(css=css)
    def fld_ff(self):
        return self._get_field('ff')

    @export(u'西英词典', 6)
    @with_styles(css=css)
    def fld_fe(self):
        return self._get_field('fe')
