import urllib
from time import sleep

import bs4
import requests


class GetPages:
    def __init__(self, url):
        self.url = url

    def main(self):
        card_list_url = self.ger_card_list()
        card_info = self.get_card_information(card_list_url)
        print(card_info)
        return card_info

    def ger_card_list(self):
        card_list_html = requests.get(self.url)
        soup = bs4.BeautifulSoup(card_list_html.text, 'html.parser')
        card_list_link = soup.select('#wikibody a[href*="//www65.atwiki"]')
        card_list_url = []
        for i in range(len(card_list_link)):
            card_list_url.append('https:' + card_list_link[i].get('href'))

        # print(card_list_url)
        return card_list_url

    def get_card_information(self, card_list_url):

        card_info = []

        for card_url in card_list_url:
            # print(card_url)
            card_url_html = requests.get(card_url)
            # card_url_html = requests.get('https://www65.atwiki.jp/hachinai_nanj/pages/541.html')
            # card_url_html = requests.get('https://www65.atwiki.jp/hachinai_nanj/pages/23.html')

            soup = bs4.BeautifulSoup(card_url_html.text, 'html.parser')

            player_pages = self.check_player_pages(soup)

            if not player_pages:
                continue

            card_name = self.get_card_name(soup)
            card_element = self.get_card_element(soup)

            table_data = soup.select('#wikibody table')
            for j, th_data in enumerate(table_data):
                th_data_list = th_data.select('th:first-child')
                try:
                    if th_data_list[0].text == 'メニュー':
                        cinderella_story_card = self.get_cinderella_story_card(table_data[j])
                    elif th_data_list[0].text == 'ランク':
                        skill = self.get_skill(table_data[j])
                    elif th_data_list[0].text == '才能名':
                        talent = self.get_talent(table_data[j])
                except IndexError:
                    pass
            card_info.append(self.make_dictionary(card_name, card_element,
                                                  cinderella_story_card, skill, talent))
            # print(card_info)
            print(card_name)
            print('waiting...')
            sleep(10)
        return card_info

    @staticmethod
    def get_card_name(soup):
        card_name = soup.select('#wikibody h2:first-child')
        # selectでとったのはリスト型なので再代入でテキスト型に
        card_name = card_name[0].text
        # print(card_name)
        return card_name

    @staticmethod
    def get_card_element(soup):
        element = soup.select('#wikibody .atwiki_plugin_ref')
        element_picture_url = element[0].get('data-original')
        element = urllib.parse.unquote(element_picture_url)

        # url形式で入ってるので文字列に
        if '花' in element:
            element = '花'
        elif '蝶' in element:
            element = '蝶'
        elif '風' in element:
            element = '風'
        elif '月' in element:
            element = '月'
        else:
            print('属性のスクレイピングエラー')
            element = 'element_error'

        # print(element)
        return element

    @staticmethod
    def get_cinderella_story_card(table_data):
        rank = []
        card_name = []
        card_element = []
        # print(table_data)
        for i, dummy in enumerate(table_data):
            if i > 1:  # .atwiki_tr_0 tdは最初の行、つまり列項目名なので取得しない
                table_data_select = table_data.select('.atwiki_tr_' + str(i) + ' td')
                # print(table_data_select)
                try:
                    rank.append(table_data_select[1].text)
                    card_name.append(table_data_select[2].text)
                    card_element.append(table_data_select[3].text)
                except IndexError:
                    pass
        # print(rank, card_name, card_element)
        return rank, card_name, card_element

    @staticmethod
    def get_skill(table_data):
        rank = []
        skill_name = []
        # print(table_data)
        for i, dummy in enumerate(table_data):
            if i > 1:
                table_data_select = table_data.select('.atwiki_tr_' + str(i) + ' td')
                # print(table_data_select)
                try:
                    rank.append(table_data_select[0].text)
                    skill_name.append(table_data_select[1].text)
                except IndexError:
                    pass
        # print(rank, skill_name)
        return rank, skill_name

    def get_talent(self, table_data):
        talent_name = []
        talent_effect = []
        for i, dummy in enumerate(table_data):
            if i > 1:
                table_data_select = table_data.select('.atwiki_tr_' + str(i) + ' td')
                # print(table_data_select)
                try:
                    talent_name.append(table_data_select[0].text)
                    talent_effect.append(table_data_select[2].text)
                except IndexError:
                    pass
        # print(talent_name, talent_effect)
        return talent_name, talent_effect

    @staticmethod
    def check_player_pages(soup):
        check_player_pages = soup.select('#wikibody h2:first-child[id="id_da638b6d"]')
        # print(card_name)
        if check_player_pages:
            return True
        else:
            return False

    @staticmethod
    def make_dictionary(card_name, card_element, cinderella_story_card, skill, talent):
        cinderella_story_card_dic = {}
        j = 0
        try:
            for i in range(len(cinderella_story_card)):
                cinderella_story_card_dic[i] = []
                j = i
                cinderella_story_card_dic[i].append(cinderella_story_card[0][i])
                cinderella_story_card_dic[i].append(cinderella_story_card[1][i])
                cinderella_story_card_dic[i].append(cinderella_story_card[2][i])
        except IndexError:
            cinderella_story_card_dic.pop(j)  # デレストカードが1枚しかない時IndexErrorをおこし、空の配列ができちゃうのでそれを消す
            pass
        skill_dic = dict(zip(skill[1], skill[0]))
        talent_dic = dict(zip(talent[0], talent[1]))
        card_dic = dict(カード名=card_name, 属性=card_element, デレスト=cinderella_story_card_dic, スキル=skill_dic, 才能=talent_dic)
        # print(card_dic)
        return card_dic
