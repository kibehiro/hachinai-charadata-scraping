from time import sleep

import psycopg2

from hachinai_scraping import settings
from hachinai_scraping.get_pages import get_card_list, get_pages


def insert_data(data):
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            card_name = data['card_name']
            attribute = data['attribute']
            rarity = data['rarity']

            cur.execute('insert into card_informations('
                        'rarity, card_name, attribute) '
                        'values (%s, %s, %s)', (rarity, card_name, attribute,))

            cur.execute('select card_id from card_informations where card_name = %s;', (card_name,))
            card_id = cur.fetchone()[0]

            positions = data['position']
            for i in positions:
                position = i
                level = positions[i]
                cur.execute('insert into card_positions('
                            'card_id, position, level)'
                            'values (%s, %s, %s)', (card_id, position, level))

            status = data['status']
            for i in status:
                parameter = i
                value = status[i]
                cur.execute('insert into card_status('
                            'card_id, parameter, value)'
                            'values (%s, %s, %s)', (card_id, parameter, value))

            cinderella_cards = data['cinderella_cards']
            for i in cinderella_cards:
                cinderella_card_rank = i['rank']
                cinderella_card_name = i['card_name']
                attribute = i['attribute']
                power = i['power']
                speed = i['speed']
                technique = i['technique']
                cinderella_card_effect = i['effect']

                cur.execute('select cinderella_card_information_id from cinderella_card_informations '
                            'where cinderella_card_name = %s',
                            (cinderella_card_name,))
                fetch_result = cur.fetchone()
                if fetch_result is None:
                    cur.execute('insert into cinderella_card_informations('
                                'rank, cinderella_card_name, card_attribute, effect)'
                                'values (%s, %s, %s, %s)',
                                (cinderella_card_rank, cinderella_card_name, attribute, cinderella_card_effect,))
                    cur.execute('select cinderella_card_information_id from cinderella_card_informations '
                                'where cinderella_card_name = %s',
                                (cinderella_card_name,))
                    fetch_result = cur.fetchone()

                cinderella_card_id = fetch_result[0]
                cur.execute('insert into card_cinderellas('
                            'card_id, cinderella_card_id)'
                            'values (%s, %s)', (card_id, cinderella_card_id,))

            skills = data['skills']
            for i in skills:
                skill_rank = i['rank']
                skill_name = i['skill_name']
                condition = i['condition']
                skill_effect = i['effect']

                cur.execute('select skill_information_id from skill_informations where skill_name = %s',
                            (skill_name,))
                fetch_result = cur.fetchone()

                if fetch_result is None:
                    cur.execute('insert into skill_informations('
                                'rank, skill_name, condition, effect)'
                                'values (%s, %s, %s, %s)',
                                (skill_rank, skill_name, condition, skill_effect,))
                    cur.execute('select skill_information_id from skill_informations where skill_name = %s',
                                (skill_name,))
                    fetch_result = cur.fetchone()

                skill_id = fetch_result[0]
                cur.execute('insert into card_skills('
                            'card_id, skill_id)'
                            'values (%s, %s)', (card_id, skill_id,))

            abilities = data['ability']
            for i in abilities:
                ability_name = i['ability_name']
                max_level = i['max_level']
                ability_effect = i['effect']

                cur.execute('select ability_information_id from ability_informations where ability_name = %s',
                            (ability_name,))
                fetch_result = cur.fetchone()
                if fetch_result is None:
                    cur.execute('insert into ability_informations('
                                'ability_name, max_level, effect)'
                                'values (%s, %s, %s)',
                                (ability_name, max_level, ability_effect,))
                    cur.execute('select ability_information_id from ability_informations where ability_name = %s',
                                (ability_name,))
                    fetch_result = cur.fetchone()

                ability_id = fetch_result[0]
                cur.execute('insert into card_abilities('
                            'card_id, ability_id)'
                            'values (%s, %s)', (card_id, ability_id,))
                
        # スクレイピングなので逐一commit()いれても大丈夫やろの精神
        conn.commit()


def make_db():
    url_list = ['https://www65.atwiki.jp/hachinai_nanj/pages/455.html',
                'https://www65.atwiki.jp/hachinai_nanj/pages/456.html',
                'https://www65.atwiki.jp/hachinai_nanj/pages/457.html',
                'https://www65.atwiki.jp/hachinai_nanj/pages/458.html']
    card_list = []

    # ログの初期化
    with open('../Logs/success.log', mode='w', encoding='UTF-8') as f:
        f.write('')
    with open('../Logs/error.log', mode='w', encoding='UTF-8') as f:
        f.write('')

    for url in url_list:
        card_list += get_card_list(url)
        sleep(10)

    for card_url in card_list:
        data = get_pages(card_url)
        if data is None:
            continue
        insert_data(data)
        sleep(10)


if __name__ == '__main__':
    DATABASE_URL = settings.DATABASE_URL
    make_db()
