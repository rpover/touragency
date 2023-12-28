insert into Country (name) values ("Ukraine");
insert into Country (name) values ("USSR");
insert into Country (name) values ("Poland");
insert into Country (name) values ("China");
insert into Country (name) values ("France");
insert into Country (name) values ("Russian Empire");

insert into User (name, surname, phone) values ("Vladimir", "Lenin", "12345678910");
insert into User (name, surname, phone) values ("Nikolay", "Romanov", "13245678910");
insert into User (name, surname, phone) values ("Adolf", "Hitler", "12535678910");
insert into User (name, surname, phone, password, power_level) values ("Vladimir", "Putin", "12345678999", "1", 100);
insert into User (name, surname, phone) values ("Napoleon", "Bonaparte", "92345678910");
insert into User (name, surname, phone) values ("Ci", "Pin", "22345678910");

insert into Tour (countryId, hours, price) values (1, 744, 2500);
insert into Tour (countryId, hours, price) values (2, 72, 25);
insert into Tour (countryId, hours, price) values (3, 22, 12000);
insert into Tour (countryId, hours, price) values (4, 120, 17000);
insert into Tour (countryId, hours, price) values (5, 450, 34000);
insert into Tour (countryId, hours, price) values (6, 220, 25);

insert into Ticket (tourId, date_start, date_end, userId) values (1, '2022-22-02', '2022-22-03', 4);
insert into Ticket (tourId, date_start, date_end, userId) values (2, "1919-4-06", "1919-7-06", 1);
insert into Ticket (tourId, date_start, date_end, userId) values (3, "1939-1-01", "2003-11-09", 3);
insert into Ticket (tourId, date_start, date_end, userId) values (4, "2003-11-08", "2003-11-09", 6);
insert into Ticket (tourId, date_start, date_end, userId) values (5, "2003-11-08", "2003-11-09", 5);
insert into Ticket (tourId, date_start, date_end, userId) values (6, "2003-11-08", "2003-11-09", 2);
