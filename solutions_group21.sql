/*
 Group 21

*/


------- Question 2a -------

-- 1a
drop table if exists #turnhout
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
--Join clause
select distinct a.itemname, a.itemcolor, c.deptfloor
from xitem as a
join xsale as b on a.itemname = b.itemname
join xdept as c on b.deptname = c.deptname
where c.deptfloor = 2 and a.itemcolor = 'Brown' -- check deptfloor and itemcolor

--In clause
select distinct a.itemname, a.itemcolor
from xitem as a
where a.itemname in (select b.itemname
					 from xsale as b
					 where b.deptname in (select c.deptname
										  from xdept as c
										  where c.deptfloor = 2)) and a.itemcolor = 'Brown';

--Exist clause
select distinct a.itemname, a.itemcolor
from xitem as a
where exists (select b.itemname
			  from xsale as b
			  where a.itemname = b.itemname and exists (select c.deptname
														from xdept as c
														where b.deptname = c.deptname and c.deptfloor = 2)) and a.itemcolor = 'Brown';

--3
select distinct *
from xdept as departments
where departments.deptname not in (select sales.deptname
								   from xsale as sales
								   where sales.itemname like '%compass%');

-- 4
-- no results because Q3 implies that the department marketing has not sold (to a customer as a record in the xsale table) a compass.
-- So this query should result in an empty table
select distinct a.*, d.*
from xemp as a
inner join xdept as b on a.empno = b.empno
inner join xsale as c on b.deptname = c.deptname
inner join xitem as d on c.itemname = d.itemname
inner join xdel as e on d.itemname = e.itemname
inner join xspl as f on e.splno = f.splno
where b.deptname = 'Marketing' and d.itemname = 'Compass';


--5a
drop table if exists #avg_marketing_table
select avg(employee.empsalary) as avg_salary, 1 as id
into #avg_marketing_table
from xemp as employee
where employee.deptname = 'Marketing';

--5b
drop table if exists #avg_purchasing_table
select avg(employee.empsalary) as avg_salary, 1 as id
into #avg_purchasing_table
from xemp as employee
where employee.deptname = 'Purchasing';

--5cd
drop table if exists #dif_salary_table
select abs(p.avg_salary - m.avg_salary) as dif_salary -- use abs() to calculate absolute difference
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
select empsalary
from xemp
where empno = (select bossno
			   from xemp
			   where empno = (select bossno	
							  from xemp
							  where empfname ='Nancy'))
--6b
select empfname
from xemp
where bossno = (select empno
			    from xemp
				where empfname = 'Andrew')
order by empfname

--6c
select a.empfname, a.deptname, b.empfname as bossname, b.deptname
from xemp as a
join xemp as b on a.bossno = b.empno -- use a join to see who is whose boss

--6d
select a.empno, a.empfname, (a.empsalary - b.empsalary) as salary_dif
from xemp as a
join xemp as b on a.bossno = b.empno
where a.empsalary > b.empsalary -- check if salary satisfies the given condition

--6e
select a.empfname, a.empsalary, b.empfname as bossname
from xemp as a
join xemp as b on a.bossno = b.empno
where a.deptname = 'Accounting' and a.empsalary > 20000

--7
select b.splname, count(distinct a.itemname) as total
from xdel as a
join xspl as b on a.splno = b.splno
group by b.splname
having count(distinct a.itemname) >= 5
order by b.splname;

--8
-- we interpreted 'that sell at least 5 items' as: the department has made at least 5 sales in the sales table
select a.deptname, count(b.itemname) 
from xdept as a
join xsale as b on b.deptname = a.deptname
where a.deptfloor in (1,2)
group by a.deptname
having count(b.itemname) >= 5

--9a
select a.empfname as manager, count(b.empfname) as direct_employees
into #direct
from xemp as a
join xemp as b on a.empno = b.bossno
group by a.empfname

--9b
select *
from #direct 
where #direct.direct_employees = (select Min(#direct.direct_employees)
								  from #direct)
drop table #direct

--10a
drop table if exists #turnhout
select top(1000) * -- for some reason, this line was necessary to get the results ordered in a temporary table
into #turnhout
from xemp as employee
where employee.empsalary > (select max(a.empsalary) as max_salary
							from xemp as a
							where a.deptname = 'Clothes')
order by empsalary asc;

--10b
drop table if exists #turnhout_copy
select top(1000) *, rank() over(order by empsalary desc) salary_rank -- see 10a for comment on select top(1000)
into #turnhout_copy
from #turnhout
order by empsalary;

--10c
select top 3 empsalary
from #turnhout_copy
order by empsalary desc; -- since we want the highest salaries, we reverse the table

--10d
drop table #turnhout;
drop table #turnhout_copy;

--11a
select department.deptname
from xdept as department
where (select avg(employee.empsalary) as avg_salary -- find the avg salary of the department
	   from xemp as employee
	   where department.deptname = employee.deptname) > 10000 -- check avg salary 
and department.deptname in (select sales.deptname -- check if the department sells compass or elephant stick
							from xsale as sales
							where sales.itemname like '%compass%' or sales.itemname like '%elephant polo stick%');

--11b
select department.deptname
from xdept as department
where (select avg(employee.empsalary) as avg_salary -- find the avg salary of the department
	   from xemp as employee
	   where department.deptname = employee.deptname) > 10000 -- check avg salary 
intersect
select sales.deptname
from xsale as sales
where sales.itemname like '%compass%' or sales.itemname like '%elephant polo stick%';

--12a
select supplier.splname
from xspl as supplier
where supplier.splno not in (select delivery.splno
							 from xdel as delivery
							 where delivery.itemname = 'stetson');
--12b
select supplier.splname
from xspl as supplier
inner join xdel as delivery on delivery.splno = supplier.splno
where supplier.splno not in (select delivery.splno
							 from xdel as delivery
							 where delivery.itemname = 'stetson')
group by supplier.splname;

--13
create function dbo.turnhout_getFirstWord 
(
	@word varchar(248)
)
returns varchar(248)
begin
declare @output varchar(248)
	if (charindex(' ',ltrim(@word)) = 0) --meaning that there are no spaces in the string
		select @output = ltrim(@word)
	else -- there are spaces in the string
		select @output = substring(ltrim(@word),1,charindex(' ',ltrim(@word)))
	return @output
end;

select *, dbo.turnhout_getFirstWord(items.itemname) as itemname_firstword
from xitem as items;

drop function dbo.turnhout_getFirstWord;

--14abc
--first query
select 'highest_avg_salary' as type,employee.deptname as department --one single query with subqueriesssss
into #result
from xemp as employee
group by employee.deptname
having avg(employee.empsalary) = (select max(avg_salary_dept.avg) as max_avg_salary_dept -- subquery to calculate the maximum of avg_salary_dept
								  from (select avg(employee.empsalary) as avg --subquery to calculate all average salaries from each department
										from xemp as employee
										group by employee.deptname) as avg_salary_dept) -- call subquery as avg_salary_dept
union
--second query
select 'lowest_avg_salary'as type,employee.deptname as department
from xemp as employee
group by employee.deptname
having avg(employee.empsalary) = (select min(avg_salary_dept.avg) as min_avg_salary_dept -- subquery to calculate the minimum of avg_salary_dept
								  from (select avg(employee.empsalary) as avg --subquery to calculate all average salaries from each department
										from xemp as employee
										group by employee.deptname) as avg_salary_dept); -- call subquery as avg_salary_dept
--14d
drop table #result;

--15a
-- we interpret items as 'sold' as items having an entry in the sales table, so items that customers have bought
select sales.itemname
from xsale as sales
where sales.deptname = 'Clothes'
union
select delivery.itemname
from xdel as delivery
where delivery.splno in (select supplier.splno
						 from xspl as supplier
						 where supplier.splname = 'Nepalese Corp.')
order by sales.itemname asc;

--15b
select delivery.itemname
from xdel as delivery
inner join xsale as sales on delivery.deptname = sales.deptname
where delivery.splno in (select supplier.splno
						 from xspl as supplier
						 where supplier.splname = 'Nepalese Corp.')
or (sales.deptname = 'Clothes' and sales.itemname = delivery.itemname)
group by delivery.itemname;


--16a
-- we interpreted 'that  are  not  sold  in  the  Clothes department.' as: Items that have not been sold to a customer, so items that are not in the xsale table
select delivery.itemname
from xdel as delivery
where delivery.splno in (select supplier.splno
						 from xspl as supplier
						 where supplier.splname = 'Nepalese Corp.')
except
select sales.itemname
from xsale as sales
where sales.deptname = 'Clothes'
order by delivery.itemname asc;

--16b
-- we interpreted 'that  are  not  sold  in  the  Clothes department.' as: Items that have not been sold to a customer, so items that are not in the xsale table
select distinct itemname
from xdel
where splno = (select splno
			   from xspl
			   where splname = 'Nepalese Corp.') and itemname not in (select itemname
																	  from xsale
																	  where deptname = 'Clothes')


--17
-- we interpret 'sold' by the navigation department as the entries in the sales table which have department name = navigation
select sales.deptname
from xsale as sales
inner join xitem as items on items.itemname = sales.itemname
inner join xdel as delivery on delivery.itemname = items.itemname
where (items.itemtype = 'E' or items.itemtype = 'F')
and (sales.deptname = 'Navigation')
and delivery.splno in (select supplier.splno
						 from xspl as supplier
						 where supplier.splname = 'Nepalese Corp.');

 
 --18a
drop table if exists #cartesian_temp
select sales.saleno,sales.saleqty,sales.itemname as sale_itemname,sales.deptname, items.itemname as item_itemname,items.itemtype,items.itemcolor
into #cartesian_temp
from xsale as sales ,xitem as items;

--18b
--Cartesian product so all records are unique
drop table if exists #unique_records
select *
into #unique_records
from #cartesian_temp

--18c
-- As unique records has the same amount of rows as the cartesian product we know that there are no duplicates
delete
from #cartesian_temp

--18d
drop table #cartesian_temp
drop table #unique_records

--19
select * 
from xsale as sales
except 
select *
from xsale_copy as sales_copy;

------- Question 2b -------

--20a
select cluster_id, count(cluster_id) as n_pubs
from Patstat_golden_set
group by cluster_id
order by n_pubs desc;

--20b
select cluster_id, count(cluster_id) as n_pubs, 100*convert(float,count(cluster_id))/total as probability
from Patstat_golden_set, (select count(*) as total from Patstat_golden_set) as total
group by cluster_id, total
order by n_pubs desc;

--20c
drop table if exists #turnhout_result
select cluster_id, count(cluster_id) as n_pubs, 100*convert(float,count(cluster_id))/total as probability
into #turnhout_result
from Patstat_golden_set, (select count(*) as total from Patstat_golden_set) as total
group by cluster_id, total
order by n_pubs desc;

--20d
select cluster_id, count(cluster_id) as n_pubs, 100*convert(float,count(cluster_id))/total as probability, (count(cluster_id)-mean)/variance as normalized_n_pubs
from Patstat_golden_set, (select count(*) as total 
						  from Patstat_golden_set) as total, (select avg(n_pubs) as mean
															  from #turnhout_result) as mean, (select stdev(n_pubs) as variance
																							   from #turnhout_result) as variance
group by cluster_id, total, mean, variance
order by n_pubs desc;

--20e
drop table #turnhout_result

--21
drop function if exists dbo.turnhout_funcDeleteMultipleSpaces
create function dbo.turnhout_funcDeleteMultipleSpaces
(
	@inputstring nvarchar(1024)
)
returns nvarchar(1024)
begin
	set @inputstring = ltrim(@inputstring) --remove all spaces before the first word
	while charindex('  ', @inputstring) >0 --check if there exists a double space | returns 0 as index if there are no characters that match the input, in this case a double space
	begin
		set @inputstring = replace(@inputstring,'  ',' ') --if exists replace double space with single space
		--stop loop if there does not exists a double space in the string, which means that all whitespaces are replaced with a single space, or that there was no double or larger space in the inputstring
	end
	return @inputstring
end;

select dbo.turnhout_funcDeleteMultipleSpaces('   test       test       test     test test   test') as 'test';
select *, dbo.turnhout_funcDeleteMultipleSpaces(npl_biblio) as clean_npl_biblio
from Patstat;

drop function dbo.turnhout_funcDeleteMultipleSpaces;

--22
create function dbo.turnhout_cleanIt
(	
	@inputstring nvarchar(1024), @invalidcharacters  nvarchar(1024)
)
returns nvarchar(1024)
begin
declare @pos int
	-- remove all characters that are not wanted with a pattern index: returns postition in the string of a character that matches the given pattern | returns 0 if there are no more characters that matches the pattern
	set @pos = patindex(@invalidcharacters, @inputstring) -- get position of the first character that matches the pattern
	while @pos > 0 --check if position is larger than 0
	begin
		set @inputstring = concat(substring(@inputstring,1,@pos -1),substring(@inputstring,@pos +1,len(@inputstring))) --delete the character from string, based on the position where the character that needs to be deleted is
		set @pos = patindex(@invalidcharacters, @inputstring) -- update position to the next character that matches the pattern in string
	end
	return @inputstring
end;

--test cases
select dbo.turnhout_cleanIt('3567576Q7XDEWC6A871','%[^1-3A-D]%'); --would return '3DCA1'
select dbo.turnhout_cleanIt('3567576Q7XDEWC6A871','%[A-Z]%'); --would return '356757676871'
select dbo.turnhout_cleanIt('3567576Q7XDEWC6A871','%[0-9]%'); --would return 'QXDEWCA'
select dbo.turnhout_cleanIt ('64@#7*&*^6^$%Q7C6A871','%[^0-9A-Z]%'); --would return '6476Q7C6A871'
select dbo.turnhout_cleanIt('64@#7*&*^6^$%Q7C6A871','%[0-9A-Z]%'); --would return '@#*&*^^$%'
select dbo.turnhout_cleanIt('the fox ran into the forest following other foxes!','% %'); --would return 'thefoxranintotheforestfollowingotherfoxes!' [note: remove single space]
select dbo.turnhout_cleanIt('the fox ran into the forest following other foxes!','%  %'); --would return 'the fox ran into the forest following other foxes!' [note: remove doubles spaces

select *, dbo.turnhout_cleanIt(npl_biblio,'%[,.]%') as clean_npl_biblio
from Patstat;

drop function dbo.turnhout_cleanIt;
---------------------------
