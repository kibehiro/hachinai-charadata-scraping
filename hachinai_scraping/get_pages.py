import json
import re
import traceback
import urllib

import requests
from bs4 import BeautifulSoup
from jsonschema import validate, ValidationError


def get_card_list(url):
    card_list_html = requests.get(url)
    card_list_soup = BeautifulSoup(card_list_html.text, 'lxml')
    card_url_list = []
    for card_list in card_list_soup.select(
            '#wikibody table td:nth-of-type(2) a[href*="w.atwiki.jp/hachinai_nanj/pages/"]'):
        card_url_list.append('https:{}'.format(card_list.get('href')))
    return card_url_list


def get_attribute(html):
    html = html.select('tr.atwiki_tr_even.atwiki_tr_2 td:first-child picture img.atwiki_plugin_ref')[0]
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
    return attribute


def get_rarity(html):
    html = html.select('tr.atwiki_tr_even.atwiki_tr_2 td:nth-child(2) picture img.atwiki_plugin_ref')[0]
    rarity_picture_url = html.get('data-original')
    if 'SSR' in rarity_picture_url:
        rarity = 'SSR'
    elif 'SR' in rarity_picture_url:
        rarity = 'SR'
    elif 'R' in rarity_picture_url:
        rarity = 'R'
    else:
        rarity = 'N'
    return rarity


def get_position(html):
    html = html.select('tr.atwiki_tr_odd.atwiki_tr_3 td')
    position_list = ['先', '継', '抑', '補', '一', '二', '三', '遊', '左', '中', '右']
    position = {}
    for i, level in enumerate(html):
        if level.text != '-':
            position.update({position_list[i]: level.text})

    return position


def get_status(table):
    status_dic = {}
    status_list = table.select('tr.atwiki_tr_odd.atwiki_tr_1 th')
    value_list = table.select('tr.atwiki_tr_even.atwiki_tr_2 td')
    if len(status_list) != len(value_list):
        status_list.pop(0)
    for status, value in zip(status_list, value_list):
        status_text = status.text.replace('　', '')
        if status_text != '*' and status_text != '備考' and status_text != 'その他':
            value = value.text.replace('km/h', '')
            if value == '-':
                value = None
            else:
                value = int(value)
            status_dic.update({status_text: value})
    return status_dic


def get_cinderella_card(html):
    cinderella_card = []
    for i in html.select('tr')[1:]:
        card_info = {}
        card_info.update({'rank': i.select('td:nth-of-type(1)')[0].text})
        if html.select('th')[2].text == '画像':  # 画像列があるとき
            card_info.update({'card_name': i.select('td:nth-of-type(4)')[0].text})
            card_info.update({'attribute': i.select('td:nth-of-type(5)')[0].text})
            card_info.update({'power': i.select('td:nth-of-type(6)')[0].text})
            card_info.update({'speed': i.select('td:nth-of-type(7)')[0].text})
            card_info.update({'technique': i.select('td:nth-of-type(8)')[0].text})
            card_info.update({'effect': i.select('td:nth-of-type(9)')[0].text})
        else:
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
        if html.select('th')[2].text == '効果':  # 条件列がない時
            skill_info.update({'condition': '-'})
            skill_info.update({'effect': i.select('td:nth-of-type(3)')[0].text})
        else:
            skill_info.update({'condition': i.select('td:nth-of-type(3)')[0].text})
            skill_info.update({'effect': i.select('td:nth-of-type(4)')[0].text})
        skill.append(skill_info)
    return skill


def get_ability(html):
    ability = []
    # TODO: 才能の条件をDBに追加する
    for i in html.select('tr')[1:]:
        ability_info = {}
        ability_info.update({'ability_name': i.select('td:nth-of-type(1)')[0].text})
        ability_info.update({'max_level': int(i.select('td:nth-of-type(2)')[0].text)})
        if html.select('th')[2].text == '条件':  # 条件列があるとき
            ability_info.update({'effect': i.select('td:nth-of-type(4)')[0].text})
        else:
            ability_info.update({'effect': i.select('td:nth-of-type(3)')[0].text})
        ability.append(ability_info)
    return ability


def write_error_log(card_url):
    with open('../Logs/error.log', mode='a', encoding='UTF-8') as f:
        error_page = 'ERROR URL: https:{}'.format(card_url)
        print(error_page)
        f.write('\n' + error_page + '\n' + traceback.format_exc())


def get_pages(card_url):
    chara_data = {}
    card_html = requests.get(card_url)
    card_soup = BeautifulSoup(card_html.text, 'lxml')

    chara_data.update({'card_name': card_soup.select('#wikibody h2:first-of-type')[0].text})

    for table in card_soup.select('#wikibody table'):
        try:
            table_type = table.select('th')[1].text
        except IndexError:
            continue

        # 最初のテーブル（属性とレア度とポジション）
        if table_type == 'レア':
            try:
                chara_data.update({'attribute': get_attribute(table)})
                chara_data.update({'rarity': get_rarity(table)})
                chara_data.update({'position': get_position(table)})
            except (IndexError, TypeError, ValueError) as e:
                write_error_log(card_url)

        # ステータスのテーブル
        if (table_type == 'ミート' or table_type.replace('　', '') == '球速') and \
                re.search(r'^素?パラメーター?', table.select('tr:nth-of-type(2) th,td:not([rowspan])')[0].text):
            try:
                chara_data.update({'status': get_status(table)})
            except (IndexError, TypeError, ValueError) as e:
                write_error_log(card_url)

        # デレスト
        if table_type == 'ランク':
            try:
                chara_data.update({'cinderella_cards': get_cinderella_card(table)})
            except (IndexError, TypeError, ValueError) as e:
                write_error_log(card_url)
        # スキル
        if table_type == 'スキル名':
            try:
                chara_data.update({'skills': get_skill(table)})
            except (IndexError, TypeError, ValueError) as e:
                write_error_log(card_url)

        # 才能
        if table_type == 'Lv':
            try:
                chara_data.update({'ability': get_ability(table)})
            except (IndexError, TypeError, ValueError) as e:
                write_error_log(card_url)

    with open('../json/schema.json', encoding='utf-8', mode='r') as f:
        json_schema = json.load(f)

    try:
        validate(chara_data, json_schema)
    except ValidationError as e:
        write_error_log(card_url)

    print('SUCCESS URL: {}'.format(card_url))
    with open('../Logs/success.log', mode='a', encoding='UTF-8') as f:
        f.write('\nSUCCESS URL: {}'.format(card_url))

    return chara_data
