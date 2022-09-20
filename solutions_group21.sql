/*
 Group 21
 Daan van Turnhout 2051976

 JOINS:
 inner join: returns entries with matching values in both tables
 left join: returns all entries from left table, and the matched entries from right table
 right join: returns all entries from right table, and the matched entries from left table
 full join: returns all entries when there is a match in either left or right table

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
select items.itemname,xdept.deptfloor,items.itemcolor
from xitem as items
inner join xsale on xsale.itemname = items.itemname --join sales and items
inner join xdept on xdept.deptname = xsale.deptname -- join department and sales
where items.itemcolor = 'Brown' -- check color
and xdept.deptfloor = 1 --check floor = 1
group by items.itemname,xdept.deptfloor,items.itemcolor; -- group by to only show unique results

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

--4
select xdept.deptname,xitem.itemname
from xdept
inner join xemp on xemp.empno = xdept.empno -- join tables on relationship between FK and PK
inner join xsale on xsale.deptname = xdept.deptname
inner join xitem on xitem.itemname = xsale.itemname
inner join xdel on xdel.deptname = xdept.deptname and xdel.itemname = xitem.itemname
inner join xspl on xdel.splno = xspl.splno
where xdept.deptname = 'Marketing' -- check department name
and xitem.itemname like '%compass%' -- check itemname
group by xdept.deptname,xitem.itemname; -- group by to show unique results
-- no results because marketing department is in Q3 table


--5a
select avg(employee.empsalary) as avg_salary, 1 as id
into #avg_marketing_table
from xemp as employee
where employee.deptname = 'Marketing';

--5b
select avg(employee.empsalary) as avg_salary, 1 as id
into #avg_purchasing_table
from xemp as employee
where employee.deptname = 'Purchasing';

--5cd
select abs(p.avg_salary - m.avg_salary) as dif_salary
into #dif_salary_table
from #avg_marketing_table as m
join #avg_purchasing_table as p on p.id = m.id;

select *
from #dif_salary_table;

--5e
drop table #avg_marketing_table;
drop table #avg_purchasing_table;
drop table #dif_salary_table;

--6a
select employee.empfname
from xemp as employee
where ;


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