CREATE TABLE Users (
    id INTEGER NOT NULL,
    username VARCHAR NOT NULL,
    firstname VARCHAR NOT NULL,
    lastname VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    password VARCHAR NOT NULL,
    phone VARCHAR NOT NULL,
    userstatus INTEGER NOT NULL,
    PRIMARY KEY(id)
    );
CREATE TABLE Events (
    id_event INTEGER NOT NULL,
    name VARCHAR NOT NULL,
    status VARCHAR[],
    PRIMARY KEY(id_event)

);
CREATE TABLE Event_User (
    id_event_user INTEGER NOT NULL,
    events INTEGER[],
    users INTEGER[] ,
    access VARCHAR NOT NULL,
    PRIMARY KEY(id_event_user)

);