-- Database creation for the tournament project.
-- This file to be interpreted by psql for example by command
--     $ psql < tournament.sql

drop database if exists tournament;
create database tournament;
\c tournament

create table players (
    id  serial       primary key,
  name  varchar(50)  not null
);

create table matches (
  id      serial   primary key,
  winner  integer  not null  references players(id),
  loser   integer  not null  references players(id)
);

\dt