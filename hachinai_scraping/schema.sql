drop table if exists card_status;
drop table if exists card_positions;
drop table if exists card_cinderellas;
drop table if exists card_skills;
drop table if exists card_abilities;
drop table if exists card_informations;
drop table if exists cinderella_card_informations;
drop table if exists skill_informations;
drop table if exists ability_informations;

create table card_informations
(
    card_id   serial primary key,
    rarity    varchar(5),
    card_name varchar(50),
    attribute varchar(5)
);

create table if not exists card_status
(
    card_status_id serial primary key,
    card_id        integer,
    parameter      varchar(20),
    value          integer,
    foreign key (card_id) references card_informations (card_id)
);

create table if not exists card_positions
(
    card_position_id serial primary key,
    card_id          integer,
    position         varchar(20),
    level            varchar(5),
    foreign key (card_id) references card_informations (card_id)
);

create table if not exists cinderella_card_informations
(
    cinderella_card_information_id serial primary key,
    rank                           varchar(10),
    cinderella_card_name           varchar(20),
    card_attribute                 varchar(5),
    effect                         text
);

create table if not exists skill_informations
(
    skill_information_id serial primary key,
    rank                 varchar(10),
    skill_name           varchar(20),
    condition            varchar(30),
    effect               text
);

create table if not exists ability_informations
(
    ability_information_id serial primary key,
    ability_name           varchar(20),
    max_level              smallint,
    effect                 text
);

create table if not exists card_cinderellas
(
    card_cinderella_id serial primary key,
    card_id            integer,
    cinderella_card_id integer,
    foreign key (card_id) references card_informations (card_id),
    foreign key (cinderella_card_id) references cinderella_card_informations
        (cinderella_card_information_id)
);

create table if not exists card_skills
(
    card_skill_id serial primary key,
    card_id       integer,
    skill_id      integer,
    foreign key (card_id) references card_informations (card_id),
    foreign key (skill_id) references skill_informations (skill_information_id)
);

create table if not exists card_abilities
(
    card_ability_id serial primary key,
    card_id         integer,
    ability_id      integer,
    foreign key (card_id) references card_informations (card_id),
    foreign key (ability_id) references ability_informations (ability_information_id)
);

create index on card_informations (card_name);
create index on cinderella_card_informations (cinderella_card_name);
create index on skill_informations (skill_name);
create index on ability_informations (ability_name);