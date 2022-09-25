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

