import json


def create_table(cur):
    cur.execute('create table if not exists card_informations('
                'card_id serial primary key,'
                'rarity varchar(5),'
                'card_name varchar(50),'
                'attribute varchar(5));')

    cur.execute('create table if not exists card_status('
                'card_status_id serial primary key,'
                'card_id integer ,'
                'parameter varchar(20),'
                'value integer,'
                'foreign key (card_id) references card_informations (card_id));')

    cur.execute('create table if not exists card_positions('
                'card_position_id serial primary key,'
                'card_id integer ,'
                'position varchar(20),'
                'level varchar (5),'
                'foreign key (card_id) references card_informations (card_id));')

    cur.execute('create table if not exists cinderella_card_informations('
                'cinderella_card_information_id serial primary key,'
                'rank varchar (10),'
                'cinderella_card_name varchar(20),'
                'card_attribute varchar (5),'
                'effect text);')

    cur.execute('create table if not exists skill_informations('
                'skill_information_id serial primary key,'
                'rank varchar (10),'
                'skill_name varchar(20),'
                'condition varchar (30),'
                'effect text);')

    cur.execute('create table if not exists ability_informations('
                'ability_information_id serial primary key,'
                'ability_name varchar(20),'
                'max_level smallint ,'
                'effect text);')

    cur.execute('create table if not exists card_cinderellas('
                'card_cinderella_id serial primary key,'
                'card_id integer ,'
                'cinderella_card_id integer ,'
                'foreign key (card_id) references card_informations (card_id),'
                'foreign key (cinderella_card_id) references cinderella_card_informations'
                ' (cinderella_card_information_id));')

    cur.execute('create table if not exists card_skills('
                'card_skill_id serial primary key,'
                'card_id integer ,'
                'skill_id integer ,'
                'foreign key (card_id) references card_informations (card_id),'
                'foreign key (skill_id) references skill_informations (skill_information_id));')

    cur.execute('create table if not exists card_abilities('
                'card_ability_id serial primary key,'
                'card_id integer ,'
                'ability_id integer ,'
                'foreign key (card_id) references card_informations (card_id),'
                'foreign key (ability_id) references ability_informations (ability_information_id));')

    cur.execute('create index on card_informations (card_name);')
    cur.execute('create index on cinderella_card_informations (cinderella_card_name);')
    cur.execute('create index on skill_informations (skill_name);')
    cur.execute('create index on ability_informations (ability_name);')


def insert_dummy_data(cur):
    with open('../json/dummy_data.json', encoding='utf-8') as f:
        dummy_data = json.load(f)

    for data in dummy_data:
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
