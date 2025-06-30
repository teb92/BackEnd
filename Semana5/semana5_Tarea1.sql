CREATE TABLE lyfter_car_rental.users  (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(50) NOT NULL,
    date_of_birth DATE NOT NULL,
    account_state BOOLEAN
);

CREATE TABLE lyfter_car_rental.automoviles (
    id SERIAL PRIMARY KEY,
    car_brand VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    year INT NOT NULL,
    state VARCHAR(8) NOT NULL
);

CREATE TABLE lyfter_car_rental.rentals (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    car_id INT NOT NULL,
    rental_date DATE NOT NULL DEFAULT CURRENT_DATE,
    rental_status VARCHAR(20) NOT NULL,
    
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES lyfter_car_rental.users (id),
    CONSTRAINT fk_car FOREIGN KEY (car_id) REFERENCES lyfter_car_rental.automoviles(id)
);

insert into lyfter_car_rental.users  (id, first_name, last_name, email, password, date_of_birth, account_state) values (1, 'Donia', 'Powley', 'dpowley0@cargocollective.com', 'jB5(M3livQVNl\x', '5/2/1972', false);
insert into lyfter_car_rental.users  (id, first_name, last_name, email, password, date_of_birth, account_state) values (2, 'Deane', 'Carryer', 'dcarryer1@google.com.hk', 'cQ3${xHO', '12/17/1997', true);
insert into lyfter_car_rental.users  (id, first_name, last_name, email, password, date_of_birth, account_state) values (3, 'Hew', 'Ziem', 'hziem2@addtoany.com', 'fD7>IFxQXfdVuay', '2/26/1967', true);
insert into lyfter_car_rental.users  (id, first_name, last_name, email, password, date_of_birth, account_state) values (4, 'Di', 'Jandl', 'djandl3@deviantart.com', 'pZ6{)SzAYN3_MRQ!', '7/1/1983', false);
insert into lyfter_car_rental.users  (id, first_name, last_name, email, password, date_of_birth, account_state) values (5, 'Franchot', 'Jovanovic', 'fjovanovic4@cam.ac.uk', 'mS6,uYLbMQ!S', '5/22/1976', true);
insert into lyfter_car_rental.users  (id, first_name, last_name, email, password, date_of_birth, account_state) values (6, 'Marguerite', 'Donativo', 'mdonativo5@mediafire.com', 'wO1~\1x=s(k(_I<,', '5/1/1995', false);
insert into lyfter_car_rental.users  (id, first_name, last_name, email, password, date_of_birth, account_state) values (7, 'Paddy', 'Aveling', 'paveling6@uol.com.br', 'cJ9<HQWVYX', '1/7/1993', false);
insert into lyfter_car_rental.users  (id, first_name, last_name, email, password, date_of_birth, account_state) values (8, 'Homere', 'Morrallee', 'hmorrallee7@chron.com', 'kN2"<*2WGtj', '12/2/1965', false);
insert into lyfter_car_rental.users  (id, first_name, last_name, email, password, date_of_birth, account_state) values (9, 'Neron', 'Fishbourne', 'nfishbourne8@webeden.co.uk', 'fM9%<$E.<+', '4/21/1962', true);
insert into lyfter_car_rental.users  (id, first_name, last_name, email, password, date_of_birth, account_state) values (10, 'Gale', 'McCrillis', 'gmccrillis9@yelp.com', 'jG8?n''rI4mWp', '7/22/1985', false);
insert into lyfter_car_rental.users  (id, first_name, last_name, email, password, date_of_birth, account_state) values (11, 'Stern', 'Tankard', 'stankarda@twitpic.com', 'dU0)Bip~\b', '5/31/1963', false);
insert into lyfter_car_rental.users  (id, first_name, last_name, email, password, date_of_birth, account_state) values (12, 'Meta', 'Riguard', 'mriguardb@newyorker.com', 'oF8%d3Q*MTv%q}D', '7/15/1977', true);
insert into lyfter_car_rental.users  (id, first_name, last_name, email, password, date_of_birth, account_state) values (13, 'Mora', 'McKernan', 'mmckernanc@mozilla.org', 'nW7$.@yxi)g0k9$', '11/9/1963', false);
insert into lyfter_car_rental.users  (id, first_name, last_name, email, password, date_of_birth, account_state) values (14, 'Allister', 'Fairfoul', 'afairfould@hao123.com', 'qN8%dDbfkgJjD''', '1/3/2005', false);
insert into lyfter_car_rental.users  (id, first_name, last_name, email, password, date_of_birth, account_state) values (15, 'Eleni', 'Fattorini', 'efattorinie@ustream.tv', 'cB0}QnvYQO', '4/15/1970', true);
insert into lyfter_car_rental.users  (id, first_name, last_name, email, password, date_of_birth, account_state) values (16, 'Lilli', 'Antonijevic', 'lantonijevicf@youtube.com', 'nJ3@AS$E0MNiAeTP', '5/18/1965', false);
insert into lyfter_car_rental.users  (id, first_name, last_name, email, password, date_of_birth, account_state) values (17, 'Octavius', 'Ingman', 'oingmang@unblog.fr', 'eR5),,pDOdS2Z', '1/22/1970', true);
insert into lyfter_car_rental.users  (id, first_name, last_name, email, password, date_of_birth, account_state) values (18, 'Amelia', 'Behninck', 'abehninckh@ibm.com', 'rB9*v7$/<VvW}+O%', '2/16/1984', true);
insert into lyfter_car_rental.users  (id, first_name, last_name, email, password, date_of_birth, account_state) values (19, 'Vasilis', 'Hutchison', 'vhutchisoni@google.es', 'yI5+NR"w?4w', '4/2/1979', true);
insert into lyfter_car_rental.users  (id, first_name, last_name, email, password, date_of_birth, account_state) values (20, 'Faunie', 'Edkins', 'fedkinsj@alexa.com', 'yA5\aJZz\', '7/18/1973', false);
insert into lyfter_car_rental.users  (id, first_name, last_name, email, password, date_of_birth, account_state) values (21, 'Traver', 'Hawkridge', 'thawkridgek@hexun.com', 'uI7$q)Ka@Vk+', '3/30/1992', true);
insert into lyfter_car_rental.users  (id, first_name, last_name, email, password, date_of_birth, account_state) values (22, 'Charlotta', 'Klaffs', 'cklaffsl@goo.ne.jp', 'qY6/e"h)}.a$m5w', '1/23/1972', false);
insert into lyfter_car_rental.users  (id, first_name, last_name, email, password, date_of_birth, account_state) values (23, 'Sigfried', 'Ratt', 'srattm@jalbum.net', 'oL2!6_''$rZ@pcH', '4/26/1971', false);
insert into lyfter_car_rental.users  (id, first_name, last_name, email, password, date_of_birth, account_state) values (24, 'Cloe', 'Ilbert', 'cilbertn@zdnet.com', 'bF3''}Po0*v<EvC', '12/29/1960', true);
insert into lyfter_car_rental.users  (id, first_name, last_name, email, password, date_of_birth, account_state) values (25, 'Arleta', 'Sands', 'asandso@list-manage.com', 'jU4=.|Ca', '12/23/1973', false);
insert into lyfter_car_rental.users  (id, first_name, last_name, email, password, date_of_birth, account_state) values (26, 'Kristoffer', 'Dunn', 'kdunnp@zdnet.com', 'bM2@NAcFZ5w#@1', '5/11/1965', false);
insert into lyfter_car_rental.users  (id, first_name, last_name, email, password, date_of_birth, account_state) values (27, 'Francyne', 'O''Daly', 'fodalyq@altervista.org', 'mP9{oP!4RA(tH/', '7/15/1962', true);
insert into lyfter_car_rental.users  (id, first_name, last_name, email, password, date_of_birth, account_state) values (28, 'Hunter', 'Courtonne', 'hcourtonner@washington.edu', 'dX9<uTet0B7OtY?R', '7/9/1991', true);
insert into lyfter_car_rental.users  (id, first_name, last_name, email, password, date_of_birth, account_state) values (29, 'Gottfried', 'Janata', 'gjanatas@wikimedia.org', 'iN2!?VifvQZ', '2/26/1980', false);
insert into lyfter_car_rental.users  (id, first_name, last_name, email, password, date_of_birth, account_state) values (30, 'Cly', 'Eden', 'cedent@tumblr.com', 'wX1\G_*k', '11/13/1989', true);
insert into lyfter_car_rental.users  (id, first_name, last_name, email, password, date_of_birth, account_state) values (31, 'Alexio', 'Zelner', 'azelneru@senate.gov', 'rF1#>/2nh=.&N', '4/14/1995', false);
insert into lyfter_car_rental.users  (id, first_name, last_name, email, password, date_of_birth, account_state) values (32, 'Faye', 'Kobierra', 'fkobierrav@symantec.com', 'fU1,i{X}$', '7/16/1962', true);
insert into lyfter_car_rental.users  (id, first_name, last_name, email, password, date_of_birth, account_state) values (33, 'Kathye', 'Sidnall', 'ksidnallw@answers.com', 'dY4''}H_+CJ!E9', '9/1/1991', true);
insert into lyfter_car_rental.users  (id, first_name, last_name, email, password, date_of_birth, account_state) values (34, 'Auguste', 'Niesegen', 'aniesegenx@about.com', 'wR4/ZqBJ*JG3+ys,', '2/12/1998', true);
insert into lyfter_car_rental.users  (id, first_name, last_name, email, password, date_of_birth, account_state) values (35, 'Maxie', 'Fydo', 'mfydoy@google.pl', 'eO8+A_Xtyw{', '1/27/1985', true);
insert into lyfter_car_rental.users  (id, first_name, last_name, email, password, date_of_birth, account_state) values (36, 'Darius', 'Greeding', 'dgreedingz@mit.edu', 'aW4!eLX.', '12/15/1977', false);
insert into lyfter_car_rental.users  (id, first_name, last_name, email, password, date_of_birth, account_state) values (37, 'Ann-marie', 'Harbour', 'aharbour10@technorati.com', 'gD4&_H=a)P4', '2/14/1977', true);
insert into lyfter_car_rental.users  (id, first_name, last_name, email, password, date_of_birth, account_state) values (38, 'Rachele', 'Hutt', 'rhutt11@opera.com', 'fZ0_dwc,Zrn(aOe', '3/1/1993', false);
insert into lyfter_car_rental.users  (id, first_name, last_name, email, password, date_of_birth, account_state) values (39, 'Anthia', 'Curnock', 'acurnock12@businessweek.com', 'yH9+6Pgc', '4/29/1998', false);
insert into lyfter_car_rental.users  (id, first_name, last_name, email, password, date_of_birth, account_state) values (40, 'Jaimie', 'Canaan', 'jcanaan13@wikimedia.org', 'tJ7<Yd66v&Vrk', '10/28/2002', true);
insert into lyfter_car_rental.users  (id, first_name, last_name, email, password, date_of_birth, account_state) values (41, 'Kristy', 'Daice', 'kdaice14@census.gov', 'wG4_xmn,71', '3/29/1994', false);
insert into lyfter_car_rental.users  (id, first_name, last_name, email, password, date_of_birth, account_state) values (42, 'Alwin', 'Menere', 'amenere15@deliciousdays.com', 'yZ4?323j', '4/15/1995', true);
insert into lyfter_car_rental.users  (id, first_name, last_name, email, password, date_of_birth, account_state) values (43, 'Wolfie', 'Gosswell', 'wgosswell16@blogger.com', 'gE9!,O&bVj', '6/27/1962', true);
insert into lyfter_car_rental.users  (id, first_name, last_name, email, password, date_of_birth, account_state) values (44, 'Worth', 'Fleg', 'wfleg17@nature.com', 'jN0|k0dH=yx"', '2/29/1976', true);
insert into lyfter_car_rental.users  (id, first_name, last_name, email, password, date_of_birth, account_state) values (45, 'Morissa', 'Jenking', 'mjenking18@fda.gov', 'tJ6(=UokgvB5=', '10/20/1962', true);
insert into lyfter_car_rental.users  (id, first_name, last_name, email, password, date_of_birth, account_state) values (46, 'Anthea', 'Leitch', 'aleitch19@sina.com.cn', 'dQ9''Tt}0Rm@e+G', '4/25/2000', true);
insert into lyfter_car_rental.users  (id, first_name, last_name, email, password, date_of_birth, account_state) values (47, 'Ruthy', 'Sudell', 'rsudell1a@deviantart.com', 'dX8|3~NLLN', '12/17/1962', false);
insert into lyfter_car_rental.users  (id, first_name, last_name, email, password, date_of_birth, account_state) values (48, 'Randene', 'Seear', 'rseear1b@ebay.com', 'aE5_VTNAr', '2/16/1994', false);
insert into lyfter_car_rental.users  (id, first_name, last_name, email, password, date_of_birth, account_state) values (49, 'Babette', 'Mc Queen', 'bmcqueen1c@w3.org', 'cT8&iaYs2ld<4N', '7/4/1961', false);
insert into lyfter_car_rental.users  (id, first_name, last_name, email, password, date_of_birth, account_state) values (50, 'Madeline', 'Fenwick', 'mfenwick1d@plala.or.jp', 'wP8.l,`nj', '3/30/1991', false);



insert into lyfter_car_rental.automoviles (id, Car_Brand, Model, year, State) values (1, 'Concorde', 'Neon', 1993, 'used');
insert into lyfter_car_rental.automoviles (id, Car_Brand, Model, year, State) values (2, 'Mini Cooper', 'GTI', 1961, 'used');
insert into lyfter_car_rental.automoviles (id, Car_Brand, Model, year, State) values (3, 'T100 Xtra', 'Accord', 1996, 'repaired');
insert into lyfter_car_rental.automoviles (id, Car_Brand, Model, year, State) values (4, 'Sequoia', 'Mariner', 2011, 'new');
insert into lyfter_car_rental.automoviles (id, Car_Brand, Model, year, State) values (5, 'Golf', 'S-Class', 2006, 'used');
insert into lyfter_car_rental.automoviles (id, Car_Brand, Model, year, State) values (6, 'Colorado', 'Solstice', 2007, 'damaged');
insert into lyfter_car_rental.automoviles (id, Car_Brand, Model, year, State) values (7, 'Civic', 'Wrangler', 2010, 'damaged');
insert into lyfter_car_rental.automoviles (id, Car_Brand, Model, year, State) values (8, 'Town & Country', 'Aztek', 2005, 'damaged');
insert into lyfter_car_rental.automoviles (id, Car_Brand, Model, year, State) values (9, '929', '3 Series', 1992, 'new');
insert into lyfter_car_rental.automoviles (id, Car_Brand, Model, year, State) values (10, 'M', 'Z8', 2009, 'damaged');
insert into lyfter_car_rental.automoviles (id, Car_Brand, Model, year, State) values (11, 'Grand Prix', 'Sportvan G30', 1969, 'used');
insert into lyfter_car_rental.automoviles (id, Car_Brand, Model, year, State) values (12, 'Silverado', 'Touareg', 2007, 'damaged');
insert into lyfter_car_rental.automoviles (id, Car_Brand, Model, year, State) values (13, 'Ranger', 'Express', 2011, 'damaged');
insert into lyfter_car_rental.automoviles (id, Car_Brand, Model, year, State) values (14, 'Express 1500', 'Swift', 1998, 'damaged');
insert into lyfter_car_rental.automoviles (id, Car_Brand, Model, year, State) values (15, 'Spirit', 'S4', 1994, 'new');
insert into lyfter_car_rental.automoviles (id, Car_Brand, Model, year, State) values (16, '5 Series', 'Z4', 2006, 'new');
insert into lyfter_car_rental.automoviles (id, Car_Brand, Model, year, State) values (17, 'G-Series G20', 'LeSabre', 1992, 'repaired');
insert into lyfter_car_rental.automoviles (id, Car_Brand, Model, year, State) values (18, 'G-Series G20', 'HHR Panel', 1993, 'repaired');
insert into lyfter_car_rental.automoviles (id, Car_Brand, Model, year, State) values (19, 'Grand Caravan', 'Karif', 2012, 'damaged');
insert into lyfter_car_rental.automoviles (id, Car_Brand, Model, year, State) values (20, 'Mirage', 'Century', 1991, 'new');
insert into lyfter_car_rental.automoviles (id, Car_Brand, Model, year, State) values (21, 'G-Class', 'Mystique', 2004, 'damaged');
insert into lyfter_car_rental.automoviles (id, Car_Brand, Model, year, State) values (22, 'Envoy XL', 'Freestar', 2005, 'repaired');
insert into lyfter_car_rental.automoviles (id, Car_Brand, Model, year, State) values (23, 'Xterra', 'Civic', 2011, 'repaired');
insert into lyfter_car_rental.automoviles (id, Car_Brand, Model, year, State) values (24, 'Grand Prix', 'Maxima', 1968, 'repaired');
insert into lyfter_car_rental.automoviles (id, Car_Brand, Model, year, State) values (25, 'Explorer', 'RAV4', 2005, 'new');
insert into lyfter_car_rental.automoviles (id, Car_Brand, Model, year, State) values (26, 'Caravan', 'C70', 2001, 'used');
insert into lyfter_car_rental.automoviles (id, Car_Brand, Model, year, State) values (27, 'Classic', 'A4', 1963, 'used');
insert into lyfter_car_rental.automoviles (id, Car_Brand, Model, year, State) values (28, 'Ridgeline', '2500', 2007, 'repaired');
insert into lyfter_car_rental.automoviles (id, Car_Brand, Model, year, State) values (29, 'S10', 'Freelander', 1995, 'new');
insert into lyfter_car_rental.automoviles (id, Car_Brand, Model, year, State) values (30, 'Biturbo', 'CLK-Class', 1987, 'new');
insert into lyfter_car_rental.automoviles (id, Car_Brand, Model, year, State) values (31, 'Stratus', 'MX-5', 2002, 'used');
insert into lyfter_car_rental.automoviles (id, Car_Brand, Model, year, State) values (32, 'Venza', 'HHR', 2011, 'repaired');
insert into lyfter_car_rental.automoviles (id, Car_Brand, Model, year, State) values (33, 'Caravan', 'E-Class', 2012, 'used');
insert into lyfter_car_rental.automoviles (id, Car_Brand, Model, year, State) values (34, 'Q', 'S70', 1998, 'new');
insert into lyfter_car_rental.automoviles (id, Car_Brand, Model, year, State) values (35, '9-3', 'GS', 2011, 'new');
insert into lyfter_car_rental.automoviles (id, Car_Brand, Model, year, State) values (36, 'Clubman', 'Sunfire', 2012, 'damaged');
insert into lyfter_car_rental.automoviles (id, Car_Brand, Model, year, State) values (37, '9-3', 'Laser', 2008, 'repaired');
insert into lyfter_car_rental.automoviles (id, Car_Brand, Model, year, State) values (38, 'Lancer', 'LTD Crown Victoria', 2012, 'used');
insert into lyfter_car_rental.automoviles (id, Car_Brand, Model, year, State) values (39, 'tC', 'Highlander', 2010, 'new');
insert into lyfter_car_rental.automoviles (id, Car_Brand, Model, year, State) values (40, 'Stratus', 'Pathfinder', 2000, 'new');
insert into lyfter_car_rental.automoviles (id, Car_Brand, Model, year, State) values (41, 'Neon', 'G8', 1996, 'damaged');
insert into lyfter_car_rental.automoviles (id, Car_Brand, Model, year, State) values (42, 'E350', 'W126', 2008, 'used');
insert into lyfter_car_rental.automoviles (id, Car_Brand, Model, year, State) values (43, 'LUV', 'Countach', 1979, 'repaired');
insert into lyfter_car_rental.automoviles (id, Car_Brand, Model, year, State) values (44, 'Ram Wagon B350', '3500', 1994, 'damaged');
insert into lyfter_car_rental.automoviles (id, Car_Brand, Model, year, State) values (45, 'Reatta', 'LR4', 1990, 'new');
insert into lyfter_car_rental.automoviles (id, Car_Brand, Model, year, State) values (46, 'Mustang', 'Caliber', 1989, 'new');
insert into lyfter_car_rental.automoviles (id, Car_Brand, Model, year, State) values (47, 'Amigo', 'Elan', 1992, 'used');
insert into lyfter_car_rental.automoviles (id, Car_Brand, Model, year, State) values (48, 'Navigator', 'Topaz', 2005, 'damaged');
insert into lyfter_car_rental.automoviles (id, Car_Brand, Model, year, State) values (49, 'Expo', 'Cherokee', 1995, 'new');
insert into lyfter_car_rental.automoviles (id, Car_Brand, Model, year, State) values (50, '9000', 'Millenia', 1990, 'new');



INSERT INTO lyfter_car_rental.rentals (user_id, car_id, rental_status) VALUES (43, 20, 'active');
INSERT INTO lyfter_car_rental.rentals (user_id, car_id, rental_status) VALUES (14, 39, 'active');
INSERT INTO lyfter_car_rental.rentals (user_id, car_id, rental_status) VALUES (10, 4, 'active');
INSERT INTO lyfter_car_rental.rentals (user_id, car_id, rental_status) VALUES (36, 7, 'active');
INSERT INTO lyfter_car_rental.rentals (user_id, car_id, rental_status) VALUES (2, 2, 'cancelled');
INSERT INTO lyfter_car_rental.rentals (user_id, car_id, rental_status) VALUES (13, 42, 'completed');
INSERT INTO lyfter_car_rental.rentals (user_id, car_id, rental_status) VALUES (13, 44, 'completed');
INSERT INTO lyfter_car_rental.rentals (user_id, car_id, rental_status) VALUES (24, 7, 'cancelled');
INSERT INTO lyfter_car_rental.rentals (user_id, car_id, rental_status) VALUES (20, 27, 'cancelled');
INSERT INTO lyfter_car_rental.rentals (user_id, car_id, rental_status) VALUES (50, 29, 'cancelled');
INSERT INTO lyfter_car_rental.rentals (user_id, car_id, rental_status) VALUES (44, 9, 'completed');
INSERT INTO lyfter_car_rental.rentals (user_id, car_id, rental_status) VALUES (38, 15, 'completed');
INSERT INTO lyfter_car_rental.rentals (user_id, car_id, rental_status) VALUES (48, 36, 'completed');
INSERT INTO lyfter_car_rental.rentals (user_id, car_id, rental_status) VALUES (39, 39, 'cancelled');
INSERT INTO lyfter_car_rental.rentals (user_id, car_id, rental_status) VALUES (9, 7, 'completed');
INSERT INTO lyfter_car_rental.rentals (user_id, car_id, rental_status) VALUES (6, 4, 'cancelled');
INSERT INTO lyfter_car_rental.rentals (user_id, car_id, rental_status) VALUES (38, 34, 'active');
INSERT INTO lyfter_car_rental.rentals (user_id, car_id, rental_status) VALUES (44, 11, 'cancelled');
INSERT INTO lyfter_car_rental.rentals (user_id, car_id, rental_status) VALUES (48, 37, 'active');
INSERT INTO lyfter_car_rental.rentals (user_id, car_id, rental_status) VALUES (1, 37, 'cancelled');
INSERT INTO lyfter_car_rental.rentals (user_id, car_id, rental_status) VALUES (8, 13, 'completed');
INSERT INTO lyfter_car_rental.rentals (user_id, car_id, rental_status) VALUES (33, 47, 'completed');
INSERT INTO lyfter_car_rental.rentals (user_id, car_id, rental_status) VALUES (48, 10, 'cancelled');
INSERT INTO lyfter_car_rental.rentals (user_id, car_id, rental_status) VALUES (39, 40, 'active');
INSERT INTO lyfter_car_rental.rentals (user_id, car_id, rental_status) VALUES (10, 25, 'cancelled');
INSERT INTO lyfter_car_rental.rentals (user_id, car_id, rental_status) VALUES (38, 12, 'active');
INSERT INTO lyfter_car_rental.rentals (user_id, car_id, rental_status) VALUES (4, 19, 'completed');
INSERT INTO lyfter_car_rental.rentals (user_id, car_id, rental_status) VALUES (3, 19, 'active');
INSERT INTO lyfter_car_rental.rentals (user_id, car_id, rental_status) VALUES (7, 41, 'active');
INSERT INTO lyfter_car_rental.rentals (user_id, car_id, rental_status) VALUES (48, 8, 'active');
INSERT INTO lyfter_car_rental.rentals (user_id, car_id, rental_status) VALUES (8, 47, 'cancelled');
INSERT INTO lyfter_car_rental.rentals (user_id, car_id, rental_status) VALUES (21, 7, 'cancelled');
INSERT INTO lyfter_car_rental.rentals (user_id, car_id, rental_status) VALUES (14, 20, 'cancelled');
INSERT INTO lyfter_car_rental.rentals (user_id, car_id, rental_status) VALUES (17, 2, 'cancelled');
INSERT INTO lyfter_car_rental.rentals (user_id, car_id, rental_status) VALUES (7, 6, 'completed');
INSERT INTO lyfter_car_rental.rentals (user_id, car_id, rental_status) VALUES (2, 27, 'cancelled');
INSERT INTO lyfter_car_rental.rentals (user_id, car_id, rental_status) VALUES (20, 14, 'cancelled');
INSERT INTO lyfter_car_rental.rentals (user_id, car_id, rental_status) VALUES (14, 3, 'active');
INSERT INTO lyfter_car_rental.rentals (user_id, car_id, rental_status) VALUES (35, 13, 'completed');
INSERT INTO lyfter_car_rental.rentals (user_id, car_id, rental_status) VALUES (8, 17, 'cancelled');
INSERT INTO lyfter_car_rental.rentals (user_id, car_id, rental_status) VALUES (36, 45, 'completed');
INSERT INTO lyfter_car_rental.rentals (user_id, car_id, rental_status) VALUES (25, 35, 'active');
INSERT INTO lyfter_car_rental.rentals (user_id, car_id, rental_status) VALUES (11, 13, 'completed');
INSERT INTO lyfter_car_rental.rentals (user_id, car_id, rental_status) VALUES (45, 24, 'completed');
INSERT INTO lyfter_car_rental.rentals (user_id, car_id, rental_status) VALUES (40, 47, 'completed');
INSERT INTO lyfter_car_rental.rentals (user_id, car_id, rental_status) VALUES (20, 26, 'active');
INSERT INTO lyfter_car_rental.rentals (user_id, car_id, rental_status) VALUES (34, 9, 'active');
INSERT INTO lyfter_car_rental.rentals (user_id, car_id, rental_status) VALUES (13, 21, 'cancelled');
INSERT INTO lyfter_car_rental.rentals (user_id, car_id, rental_status) VALUES (48, 5, 'cancelled');
INSERT INTO lyfter_car_rental.rentals (user_id, car_id, rental_status) VALUES (6, 8, 'active');