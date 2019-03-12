/* Table creation */
CREATE TABLE IF NOT EXISTS Nurse
(
  id                  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  access_id           TEXT NOT NULL,
  first_name          TEXT    NOT NULL,
  last_name           TEXT    NOT NULL,
  password TEXT NOT NULL
);


CREATE TABLE IF NOT EXISTS Admin
(
    id          INTEGER    NOT NULL PRIMARY KEY AUTOINCREMENT,
    email       TEXT        NOT NULL,
    password    TEXT        NOT NULL

);

CREATE TABLE IF NOT EXISTS Doctor
(
  id                  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  physician_permit_nb INTEGER NOT NULL,
  first_name          TEXT    NOT NULL,
  last_name           TEXT    NOT NULL,
  specialty           TEXT    NOT NULL,
  city                TEXT    NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Patient
(
  id             INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  health_card_nb TEXT    NOT NULL,
  date_of_birth  TEXT    NOT NULL,
  gender         TEXT    NOT NULL,
  phone_nb       TEXT    NOT NULL,
  home_address   TEXT    NOT NULL,
  email          TEXT    NOT NULL,
  first_name     TEXT    NOT NULL,
  last_name      TEXT    NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Availability
(
  id        INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  doctor_id INTEGER NOT NULL,
  start     INTEGER NOT NULL,
  room      TEXT    NOT NULL,
  free      INTEGER NOT NULL,
  year      INTEGER NOT NULL,
  month     INTEGER NOT NULL,
  day       INTEGER NOT NULL,
  booking_type TEXT NOT NULL,
  FOREIGN KEY (doctor_id) REFERENCES Doctor (id)
);

CREATE TABLE IF NOT EXISTS Booking
(
  id              INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  availability_id INTEGER NOT NULL,
  doctor_id       INTEGER NOT NULL,
  patient_id      INTEGER NOT NULL,
  FOREIGN KEY (availability_id) REFERENCES Availability (id),
  FOREIGN KEY (doctor_id) REFERENCES Doctor (id),
  FOREIGN KEY (patient_id) REFERENCES Patient (id)
);

/* Fake tuple insertion using Mockaroo */
/* Nurse */
insert into Nurse (id, access_id, first_name, last_name, password)
values (1, "ABC 12345", 'Nurse', 'Jackie', 'password');
insert into Nurse (id, access_id, first_name, last_name, password)
values (2, "DEF 12345", 'Nurse', 'Tony', 'password');
insert into Nurse (id, access_id, first_name, last_name, password)
values (3, "XYZ 12345", 'Nurse', 'Laurent', 'password');


/* Admin - make only one */
insert into Admin (id, email, password)
values (1, 'admin@ubersante.com', 'admin');

/* Doctor */
insert into Doctor (id, physician_permit_nb, first_name, last_name, specialty, city, password)
values (1, 1406023, 'Nestor', 'Gonnel', 'cardiologist', 'gatineau', 'password');
insert into Doctor (id, physician_permit_nb, first_name, last_name, specialty, city, password)
values (2, 5454131, 'Bentlee', 'Swainger', 'dermatologist', 'montreal', 'password');
insert into Doctor (id, physician_permit_nb, first_name, last_name, specialty, city, password)
values (3, 7840255, 'Joyce', 'Calkin', 'family physician', 'laval', 'password');
insert into Doctor (id, physician_permit_nb, first_name, last_name, specialty, city, password)
values (4, 5153071, 'Coleman', 'Iannitti', 'emergency medicine', 'montreal', 'password');
insert into Doctor (id, physician_permit_nb, first_name, last_name, specialty, city, password)
values (5, 8312731, 'Dannel', 'Creddon', 'cardiologist', 'montreal', 'password');
insert into Doctor (id, physician_permit_nb, first_name, last_name, specialty, city, password)
values (6, 3342889, 'Mei', 'Ollerton', 'hematologist', 'montreal', 'password');
insert into Doctor (id, physician_permit_nb, first_name, last_name, specialty, city, password)
values (7, 6210479, 'Evy', 'Fligg', 'neurologist', 'longueil', 'password');
insert into Doctor (id, physician_permit_nb, first_name, last_name, specialty, city, password)
values (8, 1418384, 'Dacie', 'Dufton', 'oncologist', 'montreal', 'password');
insert into Doctor (id, physician_permit_nb, first_name, last_name, specialty, city, password)
values (9, 2074325, 'Dyan', 'Andryushin', 'gynecologist', 'laval', 'password');
insert into Doctor (id, physician_permit_nb, first_name, last_name, specialty, city, password)
values (10, 3678983, 'Nichols', 'Fesby', 'cardiologist', 'montreal', 'password');
insert into Doctor (id, physician_permit_nb, first_name, last_name, specialty, city, password)
values (11, 2675194, 'Hildagarde', 'Willis', 'family physician', 'quebec city', 'password');
insert into Doctor (id, physician_permit_nb, first_name, last_name, specialty, city, password)
values (12, 7813950, 'Ugo', 'Pobjay', 'plastic surgeon', 'montreal', 'password');
insert into Doctor (id, physician_permit_nb, first_name, last_name, specialty, city, password)
values (13, 7187092, 'Jolyn', 'O''Lunney', 'family physician', 'quebec city', 'password');
insert into Doctor (id, physician_permit_nb, first_name, last_name, specialty, city, password)
values (14, 2320880, 'Obadias', 'Densumbe', 'cardiologist', 'sherbrooke', 'password');
insert into Doctor (id, physician_permit_nb, first_name, last_name, specialty, city, password)
values (15, 7908275, 'Sharon', 'Lartice', 'podiatrist', 'longueil', 'password');
insert into Doctor (id, physician_permit_nb, first_name, last_name, specialty, city, password)
values (16, 2712541, 'Andrew', 'Zamudio', 'physiatrist', 'laval', 'password');
insert into Doctor (id, physician_permit_nb, first_name, last_name, specialty, city, password)
values (17, 6680877, 'Selie', 'Cahen', 'pathologist', 'montreal', 'password');
insert into Doctor (id, physician_permit_nb, first_name, last_name, specialty, city, password)
values (18, 8407636, 'Ali', 'Sives', 'family physician', 'quebec city', 'password');
insert into Doctor (id, physician_permit_nb, first_name, last_name, specialty, city, password)
values (19, 4760117, 'Kurtis', 'Wiper', 'pathologist', 'montreal', 'password');
insert into Doctor (id, physician_permit_nb, first_name, last_name, specialty, city, password)
values (20, 7928709, 'Amata', 'Drewet', 'dermatologist', 'montreal', 'password');

/* Patient */
insert into Patient (id, health_card_nb, date_of_birth, gender, phone_nb, home_address, email, first_name, last_name, password)
values (1, 'XGCB 1090 0810', '1958-01-31', 'F', '514-699-7660', '61 Gale Alley', 'setridge0@ucsd.edu', 'Sigrid',
        'Etridge', 'password');
insert into Patient (id, health_card_nb, date_of_birth, gender, phone_nb, home_address, email, first_name, last_name, password)
values (2, 'NPAL 9661 6734', '1988-08-13', 'M', '514-078-4930', '39802 Drewry Junction', 'oheinschke1@bloomberg.com',
        'Ozzie', 'Heinschke', 'password');
insert into Patient (id, health_card_nb, date_of_birth, gender, phone_nb, home_address, email, first_name, last_name, password)
values (3, 'STCG 9070 8994', '1965-05-09', 'M', '514-459-4060', '0 School Trail', 'zjeromson2@nbcnews.com', 'Zerk',
        'Jeromson', 'password');
insert into Patient (id, health_card_nb, date_of_birth, gender, phone_nb, home_address, email, first_name, last_name, password)
values (4, 'ADYU 1682 7209', '1976-11-14', 'M', '514-591-0844', '27 Oakridge Point', 'mkneale3@merriam-webster.com',
        'Merle', 'Kneale', 'password');
insert into Patient (id, health_card_nb, date_of_birth, gender, phone_nb, home_address, email, first_name, last_name, password)
values (5, 'UXKY 2976 6574', '1984-04-29', 'F', '514-834-3343', '28 Merrick Trail', 'sarlidge4@1688.com', 'Sylvia',
        'Arlidge', 'password');
insert into Patient (id, health_card_nb, date_of_birth, gender, phone_nb, home_address, email, first_name, last_name, password)
values (6, 'DWYZ 4748 5154', '1964-09-01', 'M', '514-856-8742', '8121 Lakewood Drive', 'ohunnisett5@harvard.edu',
        'Ollie', 'Hunnisett', 'password');
insert into Patient (id, health_card_nb, date_of_birth, gender, phone_nb, home_address, email, first_name, last_name, password)
values (7, 'OKCQ 2078 2295', '1974-04-10', 'M', '514-008-3285', '333 Trailsway Avenue', 'mboarleyson6@geocities.com',
        'Miner', 'Boarleyson', 'password');
insert into Patient (id, health_card_nb, date_of_birth, gender, phone_nb, home_address, email, first_name, last_name, password)
values (8, 'HALR 0914 0725', '1958-11-22', 'F', '514-408-4233', '7515 Gale Terrace', 'acroxley7@printfriendly.com',
        'Aurelea', 'Croxley', 'password');
insert into Patient (id, health_card_nb, date_of_birth, gender, phone_nb, home_address, email, first_name, last_name, password)
values (9, 'NCMX 0378 5850', '1995-01-20', 'M', '514-183-2737', '9116 Fair Oaks Road', 'mbloss8@earthlink.net', 'Mata',
        'Bloss', 'password');
insert into Patient (id, health_card_nb, date_of_birth, gender, phone_nb, home_address, email, first_name, last_name, password)
values (10, 'HAKI 0952 3402', '1964-06-28', 'F', '514-530-1096', '5877 Brentwood Park', 'mhamberstone9@washington.edu',
        'Modesty', 'Hamberstone', 'password');
insert into Patient (id, health_card_nb, date_of_birth, gender, phone_nb, home_address, email, first_name, last_name, password)
values (11, 'EYOS 6626 1609', '1973-04-02', 'M', '514-698-4259', '73286 Graceland Lane', 'bsorrella@java.com', 'Blaine',
        'Sorrell', 'password');
insert into Patient (id, health_card_nb, date_of_birth, gender, phone_nb, home_address, email, first_name, last_name, password)
values (12, 'KQVZ 9169 9184', '1970-09-09', 'M', '514-794-5975', '6 Farwell Lane', 'gbeaglesb@virginia.edu', 'Gothart',
        'Beagles', 'password');
insert into Patient (id, health_card_nb, date_of_birth, gender, phone_nb, home_address, email, first_name, last_name, password)
values (13, 'BGHY 4546 6221', '1995-10-29', 'M', '514-771-1173', '6 Judy Parkway', 'gcasettic@columbia.edu', 'Georgi',
        'Casetti', 'password');
insert into Patient (id, health_card_nb, date_of_birth, gender, phone_nb, home_address, email, first_name, last_name, password)
values (14, 'BGAP 4559 3259', '1990-10-18', 'M', '514-503-0322', '4933 Ridge Oak Lane', 'bwinsperd@usgs.gov', 'Baxy',
        'Winsper', 'password');
insert into Patient (id, health_card_nb, date_of_birth, gender, phone_nb, home_address, email, first_name, last_name, password)
values (15, 'KWPX 7136 4744', '1998-12-07', 'F', '514-565-7705', '4 Sugar Park', 'lgarvane@twitter.com', 'Lucita',
        'Garvan', 'password');
insert into Patient (id, health_card_nb, date_of_birth, gender, phone_nb, home_address, email, first_name, last_name, password)
values (16, 'DRSJ 9971 0157', '1966-12-29', 'M', '514-546-0527', '4883 Saint Paul Circle', 'eewertf@digg.com', 'Eliot',
        'Ewert', 'password');
insert into Patient (id, health_card_nb, date_of_birth, gender, phone_nb, home_address, email, first_name, last_name, password)
values (17, 'CDQU 5941 3609', '1986-05-24', 'M', '514-434-0643', '402 Eggendart Place', 'glockyerg@ted.com', 'Garry',
        'Lockyer', 'password');
insert into Patient (id, health_card_nb, date_of_birth, gender, phone_nb, home_address, email, first_name, last_name, password)
values (18, 'KDLY 7854 3649', '1988-06-04', 'M', '514-650-2415', '93492 Memorial Place', 'jbulledh@cnbc.com', 'Job',
        'Bulled', 'password');
insert into Patient (id, health_card_nb, date_of_birth, gender, phone_nb, home_address, email, first_name, last_name, password)
values (19, 'QOGU 7257 5077', '1968-03-07', 'F', '514-107-8253', '953 Hagan Way', 'cdraudei@usa.gov', 'Corly',
        'Draude', 'password');
insert into Patient (id, health_card_nb, date_of_birth, gender, phone_nb, home_address, email, first_name, last_name, password)
values (20, 'YSRT 5881 3753', '1991-01-10', 'F', '514-968-7811', '7 Fordem Park', 'dsichardtj@tinyurl.com', 'Dorothee',
        'Sichardt', 'password');
insert into Patient (id, health_card_nb, date_of_birth, gender, phone_nb, home_address, email, first_name, last_name, password)
values (21, 'XPKR 2916 3203', '1954-04-29', 'M', '514-613-9013', '09738 Hoard Pass', 'hmonkemank@edublogs.org',
        'Hurley', 'Monkeman', 'password');
insert into Patient (id, health_card_nb, date_of_birth, gender, phone_nb, home_address, email, first_name, last_name, password)
values (22, 'JHAC 3558 9162', '2000-03-21', 'M', '514-580-9311', '7843 Harper Court', 'lroufl@sfgate.com', 'Logan',
        'Rouf', 'password');
insert into Patient (id, health_card_nb, date_of_birth, gender, phone_nb, home_address, email, first_name, last_name, password)
values (23, 'FBZI 8689 3106', '1955-07-06', 'F', '514-321-7127', '69 Forest Circle', 'abickerstassem@infoseek.co.jp',
        'Annnora', 'Bickerstasse', 'password');
insert into Patient (id, health_card_nb, date_of_birth, gender, phone_nb, home_address, email, first_name, last_name, password)
values (24, 'DAYH 3249 0984', '1970-05-28', 'M', '514-148-0244', '0417 Basil Center', 'mrabbn@ucsd.edu', 'Markos',
        'Rabb', 'password');
insert into Patient (id, health_card_nb, date_of_birth, gender, phone_nb, home_address, email, first_name, last_name, password)
values (25, 'GBYD 1888 1831', '1971-03-24', 'M', '514-934-0511', '57 Donald Park', 'jrealffo@archive.org', 'John',
        'Realff', 'password');
insert into Patient (id, health_card_nb, date_of_birth, gender, phone_nb, home_address, email, first_name, last_name, password)
values (26, 'MKEB 3843 8074', '1988-07-26', 'M', '514-128-0969', '5755 Lakewood Street', 'adawsp@cocolog-nifty.com',
        'Adolpho', 'Daws', 'password');
insert into Patient (id, health_card_nb, date_of_birth, gender, phone_nb, home_address, email, first_name, last_name, password)
values (27, 'RMHY 2658 8600', '1988-04-14', 'M', '514-954-2022', '09492 South Lane', 'brodieq@usa.gov', 'Brennan',
        'Rodie', 'password');
insert into Patient (id, health_card_nb, date_of_birth, gender, phone_nb, home_address, email, first_name, last_name, password)
values (28, 'PEUI 6591 6654', '1957-07-12', 'M', '514-782-3956', '01 Muir Crossing', 'kainleyr@artisteer.com', 'Keenan',
        'Ainley', 'password');
insert into Patient (id, health_card_nb, date_of_birth, gender, phone_nb, home_address, email, first_name, last_name, password)
values (29, 'GXAL 9357 5760', '1993-08-07', 'M', '514-710-0835', '95456 Sutteridge Parkway', 'cporchers@xrea.com',
        'Ced', 'Porcher', 'password');
insert into Patient (id, health_card_nb, date_of_birth, gender, phone_nb, home_address, email, first_name, last_name, password)
values (30, 'ZIJC 7759 2238', '1983-10-18', 'F', '514-036-6490', '0 Norway Maple Plaza', 'awoffindent@mediafire.com',
        'Addie', 'Woffinden', 'password');
insert into Patient (id, health_card_nb, date_of_birth, gender, phone_nb, home_address, email, first_name, last_name, password)
values (31, 'KCBP 4250 7937', '1952-08-14', 'F', '514-730-9483', '944 Mosinee Way', 'agallopu@bloomberg.com', 'Ardelle',
        'Gallop', 'password');
insert into Patient (id, health_card_nb, date_of_birth, gender, phone_nb, home_address, email, first_name, last_name, password)
values (32, 'XTDN 4432 9193', '1956-07-02', 'F', '514-336-7588', '50 Anhalt Circle', 'ggerredv@netscape.com',
        'Gratiana', 'Gerred', 'password');
insert into Patient (id, health_card_nb, date_of_birth, gender, phone_nb, home_address, email, first_name, last_name, password)
values (33, 'XCNT 7826 0247', '1961-07-08', 'M', '514-580-9633', '16 Washington Place', 'wiggow@blogger.com', 'Waite',
        'Iggo', 'password');
insert into Patient (id, health_card_nb, date_of_birth, gender, phone_nb, home_address, email, first_name, last_name, password)
values (34, 'EPSF 7237 5052', '1999-02-24', 'M', '514-122-9214', '11 John Wall Circle', 'gplowmanx@uol.com.br',
        'Griswold', 'Plowman', 'password');
insert into Patient (id, health_card_nb, date_of_birth, gender, phone_nb, home_address, email, first_name, last_name, password)
values (35, 'YSBA 7121 6210', '1956-01-23', 'F', '514-638-9880', '3646 Ridgeview Drive', 'mehraty@bloglines.com',
        'Melesa', 'Ehrat', 'password');
insert into Patient (id, health_card_nb, date_of_birth, gender, phone_nb, home_address, email, first_name, last_name, password)
values (36, 'KGPW 9742 5736', '1972-10-19', 'M', '514-870-4791', '98 Mifflin Alley', 'gdeaguirrez@un.org', 'Garek',
        'de Aguirre', 'password');
insert into Patient (id, health_card_nb, date_of_birth, gender, phone_nb, home_address, email, first_name, last_name, password)
values (37, 'CBFA 9649 6766', '1973-02-12', 'F', '514-778-6053', '3 Havey Place', 'shambridge10@blogs.com', 'Shelli',
        'Hambridge', 'password');
insert into Patient (id, health_card_nb, date_of_birth, gender, phone_nb, home_address, email, first_name, last_name, password)
values (38, 'YZGW 8529 2871', '1999-05-23', 'M', '514-216-7622', '58495 Fuller Lane', 'ftwelve11@mysql.com', 'Flinn',
        'Twelve', 'password');
insert into Patient (id, health_card_nb, date_of_birth, gender, phone_nb, home_address, email, first_name, last_name, password)
values (39, 'PJSZ 3833 8509', '1967-10-17', 'M', '514-399-0744', '96778 Novick Street', 'gvautier12@artisteer.com',
        'Glyn', 'Vautier', 'password');
insert into Patient (id, health_card_nb, date_of_birth, gender, phone_nb, home_address, email, first_name, last_name, password)
values (40, 'JOWX 6551 4478', '1987-09-23', 'M', '514-971-7063', '4126 Caliangt Lane', 'gclapshaw13@desdev.cn',
        'Gustave', 'Clapshaw', 'password');
insert into Patient (id, health_card_nb, date_of_birth, gender, phone_nb, home_address, email, first_name, last_name, password)
values (41, 'BJOP 8707 2683', '1997-08-22', 'F', '514-826-1865', '3855 Holmberg Junction', 'dpointin14@yahoo.com',
        'Deanna', 'Pointin', 'password');
insert into Patient (id, health_card_nb, date_of_birth, gender, phone_nb, home_address, email, first_name, last_name, password)
values (42, 'BTKD 8701 4327', '1958-03-31', 'M', '514-428-2134', '93221 Artisan Alley', 'bmcgraw15@ezinearticles.com',
        'Baxy', 'McGraw', 'password');
insert into Patient (id, health_card_nb, date_of_birth, gender, phone_nb, home_address, email, first_name, last_name, password)
values (43, 'SLUR 4194 1628', '1986-05-20', 'F', '514-903-4051', '859 Bashford Alley', 'pbarwis16@europa.eu', 'Pearla',
        'Barwis', 'password');
insert into Patient (id, health_card_nb, date_of_birth, gender, phone_nb, home_address, email, first_name, last_name, password)
values (44, 'XNWS 9252 7238', '1964-05-20', 'F', '514-954-9906', '5600 Holmberg Circle', 'nblackborne17@infoseek.co.jp',
        'Nicolette', 'Blackborne', 'password');
insert into Patient (id, health_card_nb, date_of_birth, gender, phone_nb, home_address, email, first_name, last_name, password)
values (45, 'VMZX 9489 1398', '1957-03-08', 'M', '514-617-2584', '56244 Melvin Point', 'kjanoschek18@fotki.com',
        'Karlens', 'Janoschek', 'password');
insert into Patient (id, health_card_nb, date_of_birth, gender, phone_nb, home_address, email, first_name, last_name, password)
values (46, 'EZDX 0884 2147', '1990-01-04', 'F', '514-392-3785', '78623 Alpine Park', 'pswayne19@senate.gov', 'Prisca',
        'Swayne', 'password');
insert into Patient (id, health_card_nb, date_of_birth, gender, phone_nb, home_address, email, first_name, last_name, password)
values (47, 'DWXE 1226 5191', '1952-06-15', 'M', '514-053-3690', '33771 Birchwood Avenue', 'hmaltster1a@cisco.com',
        'Hayward', 'Maltster', 'password');
insert into Patient (id, health_card_nb, date_of_birth, gender, phone_nb, home_address, email, first_name, last_name, password)
values (48, 'YDPU 3555 4753', '1952-11-28', 'F', '514-011-2485', '9562 Bartelt Plaza', 'llevins1b@quantcast.com',
        'Lorain', 'Levins', 'password');
insert into Patient (id, health_card_nb, date_of_birth, gender, phone_nb, home_address, email, first_name, last_name, password)
values (49, 'FUGE 1387 8350', '1979-02-15', 'F', '514-524-5317', '252 Gulseth Terrace', 'mblaes1c@fastcompany.com',
        'Maurita', 'Blaes', 'password');
insert into Patient (id, health_card_nb, date_of_birth, gender, phone_nb, home_address, email, first_name, last_name, password)
values (50, 'JSWA 8200 1562', '1971-04-20', 'F', '514-957-0686', '67 Moland Hill', 'wvallentin1d@chron.com', 'Willette',
        'Vallentin', 'password');

/* Availability */
insert into Availability (id, doctor_id, start, room, free, year, month, day, booking_type)
values (1, 1, 32400, '103', 1, 2019, 2, 26, "ANNUAL");
insert into Availability (id, doctor_id, start, room, free, year, month, day, booking_type)
values (2, 2, 32400, '104', 1, 2019, 3, 31, "ANNUAL");
insert into Availability (id, doctor_id, start, room, free, year, month, day, booking_type)
values (3, 3, 32400, '105', 1, 2019,2,16, "ANNUAL");
insert into Availability (id, doctor_id, start, room, free, year, month, day, booking_type)
values (4, 4, 32400, '101', 1, 2019,2,18, "ANNUAL");
insert into Availability (id, doctor_id, start, room, free, year, month, day, booking_type)
values (5, 5, 32400, '102', 1, 2019,3,31, "WALKIN");
insert into Availability (id, doctor_id, start, room, free, year, month, day, booking_type)
values (6, 6, 32400, '103', 1, 2019,4,3, "WALKIN");
insert into Availability (id, doctor_id, start, room, free, year, month, day, booking_type)
values (7, 7, 32400, '104', 1, 2019, 2, 23, "ANNUAL");
insert into Availability (id, doctor_id, start, room, free, year, month, day, booking_type)
values (8, 8, 32400, '103', 1, 2019, 3, 8, "ANNUAL");
insert into Availability (id, doctor_id, start, room, free, year, month, day, booking_type)
values (9, 9, 32400, '105', 1, 2019, 3, 22, "ANNUAL");
insert into Availability (id, doctor_id, start, room, free, year, month, day, booking_type)
values (10, 10, 32400, '102', 1, 2019, 4, 1, "ANNUAL");
insert into Availability (id, doctor_id, start, room, free, year, month, day, booking_type)
values (11, 11, 32400, '101', 1, 2019, 3, 1, "ANNUAL");
insert into Availability (id, doctor_id, start, room, free, year, month, day, booking_type)
values (12, 12, 32400, '103', 1, 2019, 3, 27, "ANNUAL");
insert into Availability (id, doctor_id, start, room, free, year, month, day, booking_type)
values (13, 13, 32400, '104', 1, 2019, 3, 26, "ANNUAL");
insert into Availability (id, doctor_id, start, room, free, year, month, day, booking_type)
values (14, 14, 32400, '102', 1, 2019, 2, 23, "ANNUAL");
insert into Availability (id, doctor_id, start, room, free, year, month, day, booking_type)
values (15, 15, 32400, '105', 1, 2019, 4, 04, "ANNUAL");
insert into Availability (id, doctor_id, start, room, free, year, month, day, booking_type)
values (16, 16, 32400, '104', 1, 2019, 2, 26, "WALKIN");
insert into Availability (id, doctor_id, start, room, free, year, month, day, booking_type)
values (17, 17, 32400, '104', 1, 2019, 2, 14, "WALKIN");
insert into Availability (id, doctor_id, start, room, free, year, month, day, booking_type)
values (18, 18, 32400, '103', 1, 2019, 4, 8, "WALKIN");
insert into Availability (id, doctor_id, start, room, free, year, month, day, booking_type)
values (19, 19, 32400, '102', 1, 2019, 4, 2, "WALKIN");
insert into Availability (id, doctor_id, start, room, free, year, month, day, booking_type)
values (20, 20, 32400, '101', 1, 2019, 4, 8, "WALKIN");

/* Booking */
insert into Booking (id, availability_id, doctor_id, patient_id) values (1, 1, 1, 19);
insert into Booking (id, availability_id, doctor_id, patient_id) values (2, 2, 2, 4);
insert into Booking (id, availability_id, doctor_id, patient_id) values (3, 3, 3, 31);
insert into Booking (id, availability_id, doctor_id, patient_id) values (4, 4, 4, 13);
insert into Booking (id, availability_id, doctor_id, patient_id) values (5, 5, 5, 23);
insert into Booking (id, availability_id, doctor_id, patient_id) values (6, 6, 6, 28);
insert into Booking (id, availability_id, doctor_id, patient_id) values (7, 7, 7, 2);
insert into Booking (id, availability_id, doctor_id, patient_id) values (8, 8, 8, 17);
insert into Booking (id, availability_id, doctor_id, patient_id) values (9, 9, 9, 40);
insert into Booking (id, availability_id, doctor_id, patient_id) values (10, 10, 10, 36);
insert into Booking (id, availability_id, doctor_id, patient_id) values (11, 11, 11, 35);
insert into Booking (id, availability_id, doctor_id, patient_id) values (12, 12, 12, 15);
insert into Booking (id, availability_id, doctor_id, patient_id) values (13, 13, 13, 20);
insert into Booking (id, availability_id, doctor_id, patient_id) values (14, 14, 14, 2);
insert into Booking (id, availability_id, doctor_id, patient_id) values (15, 15, 15, 41);
insert into Booking (id, availability_id, doctor_id, patient_id) values (16, 16, 16, 36);
insert into Booking (id, availability_id, doctor_id, patient_id) values (17, 17, 17, 20);
