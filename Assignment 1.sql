-- Part 2: SQL programming

-- Q1
select* 
into #xemp
from xemp
where (empfname like '%a%' or empfname like '%d') and deptname in ('Management', 'Marketing', 'Purchasing') and bossno > 0
order by empfname;

select *
from #xemp

update #xemp
Set empsalary = empsalary*1.05
where empsalary >= 25000;

select *
from #xemp

select *
from #xemp
where empsalary <= 25000;

drop table #xemp

--Q2
--Join clause
select distinct a.itemname, a.itemcolor, c.deptfloor
from xitem as a
join xsale as b on a.itemname = b.itemname
join xdept as c on b.deptname = c.deptname
where c.deptfloor = 2 and a.itemcolor = 'Brown'

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

-- Q3
select distinct deptname
from xdept as a
where a.deptname not in (select b.deptname
						from xsale as b	
						where itemname = 'compass');

-- Q4
select distinct a.*, d.*
from xemp as a
inner join xdept as b on a.deptname = b.deptname
inner join xsale as c on b.deptname = c.deptname
inner join xitem as d on c.itemname = d.itemname
inner join xdel as e on d.itemname = e.itemname
inner join xspl as f on e.splno = f.splno
where b.deptname = 'Marketing' and d.itemname = 'Compass';

-- Q5
select round(avg(b.empsalary),2) as average_salariesM, 1 as ID
into #avg_marketing_table
from xdept as a
join xemp as b on b.deptname = a.deptname 
where a.deptname = 'Marketing'
group by a.deptname

select round(avg(b.empsalary),2) as average_salariesP, 1 as ID
into #avg_purchasing_table
from xdept as a
join xemp as b on b.deptname = a.deptname 
where a.deptname = 'Purchasing'
group by a.deptname

select #avg_marketing_table.average_salariesM, #avg_purchasing_table.average_salariesP, ABS(#avg_marketing_table.average_salariesM - #avg_purchasing_table.average_salariesP) as dif_salary
into #dif_salary_table
from #avg_marketing_table, #avg_purchasing_table

drop table #avg_marketing_table
drop table #avg_purchasing_table
drop table #dif_salary_table

--Q6 
select empsalary
from xemp
where empno = (select bossno
			   from xemp
			   where empno = (select bossno	
							  from xemp
							  where empfname ='Nancy'))

select empfname
from xemp
where bossno = (select empno
			    from xemp
				where empfname = 'Andrew')
order by empfname

select a.empfname, a.deptname, b.empfname as bossname, b.deptname
from xemp as a
join xemp as b on a.bossno = b.empno

select a.empno, a.empfname, (a.empsalary - b.empsalary) as salary_dif
from xemp as a
join xemp as b on a.bossno = b.empno
where a.empsalary > b.empsalary

select a.empfname, a.empsalary, b.empfname as bossname
from xemp as a
join xemp as b on a.bossno = b.empno
where a.deptname = 'Accounting' and a.empsalary > 20000

--Q7
select b.splname, count(distinct a.itemname) as total
from xdel as a
join xspl as b on a.splno = b.splno
group by b.splname
having count(distinct a.itemname) >= 5
order by b.splname;

--Q8
select a.deptname, count(b.itemname) 
from xdept as a
join xsale as b on b.deptname = a.deptname
where a.deptfloor in (1,2)
group by a.deptname
having count(b.itemname) >= 5

--Q9
select a.empfname as manager, count(b.empfname) as direct_employees
into #direct
from xemp as a
join xemp as b on a.empno = b.bossno
group by a.empfname

select *
from #direct 
where #direct.direct_employees = (select Min(#direct.direct_employees)
								  from #direct)
drop table #direct

--Q10
drop table if  exists #salary
select *
into #salary
from xemp as a
where a.deptname != 'Clothes' and empsalary > (select min(empsalary)
											   from xemp as b
											   where b.deptname = 'Clothes');

drop table if  exists #salary2
select *, dense_rank() over(order by a.empsalary desc) as ranking
into #salary2
from #salary as a
where a.deptname != 'Clothes' and empsalary > (select min(empsalary)
											   from xemp as b
											   where b.deptname = 'Clothes');

select top(3) *
from #salary2

drop table #salary
drop table #salary2

--11
select a.deptname
from xemp as a
where a.deptname in (select b.deptname
					 from xsale as b
					 where b.itemname in ('compass', 'elephant polo stick'))
group by a.deptname
having avg(empsalary) > 10000

select a.deptname
from xemp as a
group by a.deptname
having avg(empsalary) > 10000
intersect
select b.deptname
from xsale as b
where b.itemname in ('compass', 'elephant polo stick')

--Q12
select *
from xspl as a
where a.splno in (select b.splno
				  from xdel as b
				  where b.itemname != 'stetson')

select distinct a.splno, a.splname
from xspl as a
join xdel as b on a.splno = b.splno
where b.itemname != 'stetson'

--Q13
select *, rtrim(left(itemname, charindex(' ', itemname))) as itemname_firstword
from xitem
-- nu nog een functie dr van maken

--Q16
select distinct itemname
from xdel
where splno = (select splno
			   from xspl
			   where splname = 'Nepalese Corp.')
except
select itemname
from xsale
where deptname = 'Clothes'

----------
select distinct itemname
from xdel
where splno = (select splno
			   from xspl
			   where splname = 'Nepalese Corp.') and itemname not in (select itemname
																	  from xsale
																	  where deptname = 'Clothes')

--Q18
drop table if exists #cartesian_temp
select sales.saleno,sales.saleqty,sales.itemname as sale_itemname,sales.deptname, items.itemname as item_itemname,items.itemtype,items.itemcolor
into #cartesian_temp
from xsale as sales ,xitem as items;

--Cartesian product so all records are unique
drop table if exists #unique_records
select *
into #unique_records
from #cartesian_temp

-- As unique records has the same amount of rows as the cartesian product we know that there are no duplicates
delete
from #cartesian_temp

drop table #cartesian_temp
drop table #unique_records



