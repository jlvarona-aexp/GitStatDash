create table repos
(
    id   integer not null
        constraint repos_pk
            primary key autoincrement,
    name text    not null
);

create unique index repos_id_uindex
    on repos (id);

create unique index repos_name_uindex
    on repos (name);

create table teams
(
    id   integer not null
        constraint teams_pk
            primary key autoincrement,
    name text    not null
);

create unique index teams_id_uindex
    on teams (id);

create unique index teams_name_uindex
    on teams (name);

create table users
(
    id       integer not null
        constraint users_pk
            primary key autoincrement,
    repo_id  text    not null,
    name     text,
    email    text,
    source   text,
    team_id  integer
        references teams,
    band     int,
    nickname text,
    platform text
);

create table CREATORS
(
    pr_id         integer not null
        constraint CREATORS_pk
            primary key autoincrement,
    id            integer not null,
    link          text,
    repo          integer
        references repos,
    name          text,
    submitted     text,
    done          text,
    state         text,
    creator       integer
        references users,
    duration      integer,
    comments      integer,
    draft         integer,
    created_at    text,
    updated_at    text,
    merged_at     text,
    closed_at     text,
    additions     integer,
    deletions     integer,
    changed_files integer
);

create index CREATORS__creator
    on CREATORS (creator, repo);

create unique index CREATORS__id
    on CREATORS (id, repo);

create unique index CREATORS_pr_id_uindex
    on CREATORS (pr_id);

create index CREATORS_submitted_id_repo_index
    on CREATORS (submitted, id, repo);

create table activity
(
    id          integer not null
        constraint activity_pk
            primary key autoincrement,
    activity_id integer not null,
    pr_id       integer not null,
    action      text,
    createdDate text,
    timestamp   integer,
    user_id     integer
        references users
);

create index activity_activity_id_createdDate_index
    on activity (activity_id, createdDate);

create unique index activity_activity_id_uindex
    on activity (activity_id);

create unique index activity_id_uindex
    on activity (id);

create index activity_user_id_activity_id_index
    on activity (user_id, activity_id);

create table reviewers
(
    pr_id    integer not null
        constraint reviewers_pk
            primary key autoincrement,
    id       integer not null,
    reviewer integer
        references users,
    repo_id  integer
);

create unique index reviewers_id_repo_id_reviewer_uindex
    on reviewers (id, repo_id, reviewer);

create unique index reviewers_pr_id_uindex
    on reviewers (pr_id);

create unique index users_id_uindex
    on users (id);

create index users_platform_index
    on users (platform, name);

create unique index users_repo_id_uindex
    on users (repo_id);

create index users_team_id_repo_id_index
    on users (team_id, repo_id);

