import urllib
from time import sleep

import requests
from bs4 import BeautifulSoup


def get_attribute(html):
    attribute_picture_url = html.get('data-original')
    attribute = urllib.parse.unquote(attribute_picture_url)

    # url形式で入ってるので文字列に
    if '花' in attribute:
        attribute = '花'
    elif '蝶' in attribute:
        attribute = '蝶'
    elif '風' in attribute:
        attribute = '風'
    elif '月' in attribute:
        attribute = '月'
    return {"attribute": attribute}


def get_rarity(html):
    rarity_picture_url = html.get('data-original')
    if 'SSR' in rarity_picture_url:
        rarity = 'SSR'
    elif 'SR' in rarity_picture_url:
        rarity = 'SR'
    elif 'R' in rarity_picture_url:
        rarity = 'R'
    else:
        rarity = 'N'
    return {"rarity": rarity}


def get_position(html):
    position_list = ['先', '継', '抑', '補', '一', '二', '三', '遊', '左', '中', '右']
    position = {}
    for i, level in enumerate(html):
        if level.text != '-':
            position.update({position_list[i]: level.text})

    return position


def get_status(status_list, value_list):
    status_dic = {}
    if len(status_list) != len(value_list):
        status_list.pop(0)
    for status, value in zip(status_list, value_list):
        if status.text != '*' and status.text != '備考':
            status_dic.update({status.text.replace('　', ''): int(value.text.replace('km/h', ''))})
    return status_dic


def get_cinderella_card(html):
    cinderella_card = []
    for i in html.select('tr')[1:]:  # 1行目は項目名のため除外
        card_info = {}
        card_info.update({'rank': i.select('td:nth-of-type(2)')[0].text})
        card_info.update({'card_name': i.select('td:nth-of-type(3)')[0].text})
        card_info.update({'attribute': i.select('td:nth-of-type(4)')[0].text})
        card_info.update({'power': i.select('td:nth-of-type(5)')[0].text})
        card_info.update({'speed': i.select('td:nth-of-type(6)')[0].text})
        card_info.update({'technique': i.select('td:nth-of-type(7)')[0].text})
        card_info.update({'effect': i.select('td:nth-of-type(8)')[0].text})
        cinderella_card.append(card_info)
    return cinderella_card


def get_skill(html):
    skill = []
    for i in html.select('tr')[1:]:  # 1行目は項目名のため除外
        skill_info = {}
        skill_info.update({'rank': i.select('td:nth-of-type(1)')[0].text})
        skill_info.update({'skill_name': i.select('td:nth-of-type(2)')[0].text})
        skill_info.update({'condition': i.select('td:nth-of-type(3)')[0].text})
        skill_info.update({'effect': i.select('td:nth-of-type(4)')[0].text})
        skill.append(skill_info)
    return skill


def get_ability(html):
    ability = []
    for i in html.select('tr')[1:]:  # 1行目は項目名のため除外
        ability_info = {}
        ability_info.update({'ability_name': i.select('td:nth-of-type(1)')[0].text})
        ability_info.update({'max_level': i.select('td:nth-of-type(2)')[0].text})
        ability_info.update({'effect': i.select('td:nth-of-type(3)')[0].text})
        ability.append(ability_info)
    return ability


def get_pages(url):
    card_list_html = requests.get(url)
    card_list_soup = BeautifulSoup(card_list_html.text, 'lxml')

    for card_list in card_list_soup.select('#wikibody table td a[href*="w.atwiki.jp/hachinai_nanj/pages/"]'):
        chara_data = {}
        card_url = 'https:{}'.format(card_list.get('href'))
        card_html = requests.get(card_url)
        card_soup = BeautifulSoup(card_html.text, 'lxml')

        chara_data.update({'card_name': card_soup.select('#wikibody h2:first-of-type')[0].text})

        # table_list = card_soup.select('#wikibody table')
        info_table = card_soup.select('#wikibody table:first-of-type')[0]

        # 最初のテーブル（属性とレア度とポジション）
        chara_data.update(get_attribute(
            info_table.select('tr.atwiki_tr_even.atwiki_tr_2 td:first-child picture img.atwiki_plugin_ref')[0]))
        chara_data.update(get_rarity(
            info_table.select('tr.atwiki_tr_even.atwiki_tr_2 td:nth-child(2) picture img.atwiki_plugin_ref')[0]))
        chara_data.update({'position': get_position(
            info_table.select('tr.atwiki_tr_odd.atwiki_tr_3 td'))})

        # ステータスのテーブル
        status_table = card_soup.select('#wikibody h4:nth-of-type(2) ~ table')[0]
        chara_data.update({'status': get_status(
            status_table.select('tr.atwiki_tr_odd.atwiki_tr_1 th'),
            status_table.select('tr.atwiki_tr_even.atwiki_tr_2 td'))})

        # デレスト
        chara_data.update({'cinderella_cards': get_cinderella_card(
            card_soup.select('#wikibody h4:nth-of-type(3) ~ table')[0])})

        # スキル
        chara_data.update({'cinderella_cards': get_skill(
            card_soup.select('#wikibody h4:nth-of-type(4) ~ table')[0])})

        # 才能
        chara_data.update({'ability': get_ability(
            card_soup.select('#wikibody h4:nth-of-type(5) ~ table')[0])})

        sleep(5)
