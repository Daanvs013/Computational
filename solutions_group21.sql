/*
 Group 21
 Daan van Turnhout 2051976
*/


------- Question 2a -------

-- 1a
select *
into #turnhout -- insert into temp table
from xemp as employee
where (employee.deptname = 'Marketing' or employee.deptname = 'Purchasing' or employee.deptname = 'Management') -- check department
and (employee.empfname like '%d' or employee.empfname like '%a%') -- check name
and employee.bossno != 0 -- check if employee has boss
order by employee.empfname asc; --sort on name

--1b
update #turnhout
set empsalary = empsalary * 1.05 -- add 5% to the salary
where empsalary >= 25000; -- check the salary condition

--1c
select *
from #turnhout;

--1d
delete from #turnhout
where empsalary < 25000;

--1e
drop table #turnhout;

--2a


--2b
select distinct * 
from xitem as items
where items.itemcolor = 'Brown' -- check item color
and items.itemname in (select sales.itemname -- check if item corresponds to a sale that is from a department from floor 1
					  from xsale as sales 
					  where sales.deptname in (select departments.deptname --check if sale is from a department from floor 1
											   from xdept as departments
											   where departments.deptfloor = 1)); -- check if floor is 1

--2c
select distinct *
from xitem as items
where items.itemcolor = 'Brown' -- check item color
and exists (select sales.itemname 
			from xsale as sales
			where sales.itemname = items.itemname -- check if itemnames in the two tables match
			and exists (select departments.deptname
						  from xdept as departments
						  where departments.deptfloor = 1 -- check if floor is 1
						  and departments.deptname = sales.deptname)); -- check if deptname in the two tables match

--3
select distinct *
from xdept as departments
where departments.deptname not in (select sales.deptname
								   from xsale as sales
								   where sales.itemname like '%compass%');

----------------
select  *
from xemp

select  *
from xdel

select  *
from xitem

select  *
from xsale

select  *
from xspl

select  *
from xdept