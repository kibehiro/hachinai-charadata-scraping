def create_table(cur):
    cur.execute('create table card_informations('
                'card_id serial primary key,'
                'rarity varchar(5),'
                'card_name varchar(50),'
                'attribute varchar(5));')

    cur.execute('create table card_status('
                'card_status_id serial primary key,'
                'card_id integer ,'
                'parameter varchar(20),'
                'value integer,'
                'foreign key (card_id) references card_informations (card_id));')

    cur.execute('create table card_positions('
                'card_position_id serial primary key,'
                'card_id integer ,'
                'position varchar(20),'
                'level varchar (5),'
                'foreign key (card_id) references card_informations (card_id));')

    cur.execute('create table cinderella_card_informations('
                'cinderella_card_information_id serial primary key,'
                'cinderella_card_name varchar(20),'
                'card_attribute varchar (5),'
                'effect text);')

    cur.execute('create table skill_informations('
                'skill_information_id serial primary key,'
                'skill_name varchar(20),'
                'condition varchar (30),'
                'effect text);')

    cur.execute('create table ability_informations('
                'ability_information_id serial primary key,'
                'ability_name varchar(20),'
                'maxLevel smallint ,'
                'effect text);')

    cur.execute('create table card_cinderellas('
                'card_cinderella_id serial primary key,'
                'card_id integer ,'
                'cinderella_card_id integer ,'
                'foreign key (card_id) references card_informations (card_id),'
                'foreign key (cinderella_card_id) references cinderella_card_informations'
                ' (cinderella_card_information_id));')

    cur.execute('create table card_skills('
                'card_skill_id serial primary key,'
                'card_id integer ,'
                'skill_id integer ,'
                'foreign key (card_id) references card_informations (card_id),'
                'foreign key (skill_id) references skill_informations (skill_information_id));')

    cur.execute('create table card_abilities('
                'card_ability_id serial primary key,'
                'card_id integer ,'
                'ability_id integer ,'
                'foreign key (card_id) references card_informations (card_id),'
                'foreign key (ability_id) references ability_informations (ability_information_id));')

    cur.execute('create index on card_informations (card_name);')
    cur.execute('create index on cinderella_card_informations (cinderella_card_name);')
    cur.execute('create index on skill_informations (skill_name);')
    cur.execute('create index on ability_informations (ability_name);')
