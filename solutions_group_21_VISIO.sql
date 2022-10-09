---- SQL VISIO solutions GROUP 21
--business_question: What is the average salary of the cleaners that clean a double-decker
--run whole script in one go

--create all tables and populate with data

drop table if exists group21_depots;
create table group21_depots
(
	depot_num int,
	depot_name varchar(1024),
	depot_address varchar(1024),
	primary key(depot_num)
);
insert into group21_depots values (1,'MAC','Piusplein 75, 5038 WP Tilburg, Nederland');
insert into group21_depots values (2,'CUBE','Tongelresestraat 27, 5613 DA Eindhoven, Nederland');

drop table if exists group21_routes;
create table group21_routes
(
	route_num int,
	depot_num int,
	start_place varchar(1024),
	end_place varchar(1024)
	primary key (route_num),
	foreign key (depot_num) references group21_depots(depot_num)
);
insert into group21_routes values(111,1,'Tilburg','Eindhoven')
insert into group21_routes values(222,2,'Eindhoven','Amsterdam')

drop table if exists group21_employees;
create table group21_employees
(
	emp_num int,
	depot_num int,
	employee_name varchar(1024),
	salary money
	primary key (emp_num),
	foreign key (depot_num) references group21_depots(depot_num)
);
insert into group21_employees values(229,2,'Max',94000)
insert into group21_employees values(230,2,'Eric',65000)
insert into group21_employees values(231,1,'Mark',56000)
insert into group21_employees values(232,1,'Geert',86000)
insert into group21_employees values(533,2,'Dico',34000)
insert into group21_employees values(675,1,'Daan',38500)
insert into group21_employees values(334,2,'Bas',57000)
insert into group21_employees values(234,1,'Daan',67000)
insert into group21_employees values(432,2,'Klaas',14000)
insert into group21_employees values(987,1,'Tjeerd',45700)
insert into group21_employees values(573,2,'Nick',89000)

drop table if exists group21_cleaners;
create table group21_cleaners
(
	cleaner_id int,
	emp_num int,
	primary key (cleaner_id),
	foreign key (emp_num) references group21_employees(emp_num)
)
insert into group21_cleaners values(1,231)
insert into group21_cleaners values(2,232)
insert into group21_cleaners values(3,229)
insert into group21_cleaners values(4,230)

drop table if exists group21_previous_drivers;
create table group21_previous_drivers
(
	prev_drive_id int,
	route_num int,
	emp_num int,
	primary key (prev_drive_id),
	foreign key (route_num) references group21_routes(route_num),
	foreign key (emp_num) references group21_employees(emp_num)
);
insert into group21_previous_drivers values(1,111,533)
insert into group21_previous_drivers values(2,222,675)

drop table if exists group21_drivers;
create table group21_drivers
(
	driver_id int,
	emp_num int,
	date_pcv date,
	primary key (driver_id),
	foreign key (emp_num) references group21_employees(emp_num)
);
insert into group21_drivers values(1,334,'06/02/2012')
insert into group21_drivers values(2,234,'11/04/2008')
insert into group21_drivers values(3,432,'06/06/2011')
insert into group21_drivers values(4,987,'04/03/2009')
insert into group21_drivers values(5,573,'08/09/2022')

drop table if exists group21_buses;
create table group21_buses 
(
	reg_num int,
	depot_num int,
	cleaner_id int,
	model varchar(1024),
	bus_type varchar(1024),
	primary key(reg_num),
	foreign key (depot_num) references group21_depots(depot_num),
	foreign key(cleaner_id) references group21_cleaners(cleaner_id)
);
insert into group21_buses values(1,1,1,'model 1','double-decker')
insert into group21_buses values(2,2,2,'model 2','bendy')
insert into group21_buses values(3,1,1,'model 2','double-decker')
insert into group21_buses values(4,2,2,'model 1','bendy')
insert into group21_buses values(5,1,3,'model 2','double-decker')
insert into group21_buses values(6,2,3,'model 1','double-decker')
insert into group21_buses values(7,1,4,'model 2','double-decker')


drop table if exists group21_restrictions;
create table group21_restrictions
(
	restriction_id int,
	reg_num int,
	route_num int,
	primary key(restriction_id),
	foreign key (reg_num) references group21_buses(reg_num),
	foreign key (route_num) references group21_routes(route_num)
);
insert into group21_restrictions values (1,1,111)
insert into group21_restrictions values (2,4,222)

drop table if exists group21_training;
create table group21_training
(
	training_id int,
	reg_num int,
	emp_num int,
	date_completed date,
	primary key (training_id),
	foreign key (reg_num) references group21_buses(reg_num),
	foreign key (emp_num) references group21_employees(emp_num)
);
insert into group21_training values(1,1,533,'09/03/2005')
insert into group21_training values(2,2,573,'09/03/2005')

/*
--show tables
select *
from group21_buses
select *
from group21_cleaners
select *
from group21_depots
select * 
from group21_drivers
select * 
from group21_employees
select *
from group21_previous_drivers
select *
from group21_restrictions
select *
from group21_routes
select *
from group21_training
*/

--business_question: What is the average salary of the cleaners that clean a double-decker
drop table if exists #group21_business_question
select avg(salary) as avg_salary
into #group21_business_question
from group21_employees
where emp_num in (select emp_num 
				  from group21_cleaners
				  where cleaner_id in (select cleaner_id 
									   from group21_buses
									   where bus_type = 'double-decker'))
select *
from #group21_business_question


--drop all tables
drop table if exists group21_training;
drop table if exists group21_restrictions;
drop table if exists group21_buses;
drop table if exists group21_drivers;
drop table if exists group21_previous_drivers;
drop table if exists group21_cleaners;
drop table if exists group21_employees;
drop table if exists group21_routes;
drop table if exists group21_depots;
drop table if exists #group21_business_question;
