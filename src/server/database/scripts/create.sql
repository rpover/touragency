drop table if exists Tour;
drop table if exists Country;
drop table if exists User;
drop table if exists Ticket;

create table Country(
	id integer primary key autoincrement,
	name varchar(256) not null unique
);

create table Tour(
	id integer primary key autoincrement,
	countryId integer not null,
	hours integer not null,
	price integer not null,
	foreign key (countryId) references Country(id)	
);

create table User(
	id integer primary key autoincrement,
	name varchar(256) not null,
	surname varchar(256) not null,
	phone varchar(12) not null unique,
	password varchar(16),
	power_level integer not null default 1
);

create table Ticket(
	id integer primary key autoincrement,
	tourId integer not null,
	date_start date,
	date_end date,
	userId integer not null,
	foreign key (tourId) references Tour(id),
	foreign key (userId) references User(id) 
);