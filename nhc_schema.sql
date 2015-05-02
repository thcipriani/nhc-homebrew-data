-- Schema for nhc db

create table recipes (
    id           integer primary key autoincrement not null,
    year         date,
    name         text,
    style        text,
    vol          text,
    ingredients  text,
    specs        text,
    instructions text
);