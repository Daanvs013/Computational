---		Question 23 GROUP 21 
---		first check dataset in the procedure function
---		then run the entire file in batches going from top to bottom, or just run the entire file in one go

-- helper functions                    ------------------
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
go

create function dbo.turnhout_replace
(
	@inputstring nvarchar(1024),@invalidcharacters nvarchar(1024),@replacewith nvarchar(1024)
)
returns nvarchar(1024)
begin
declare @pos int
	set @pos = patindex(@invalidcharacters,@inputstring)
	while @pos >0
	begin
		set @inputstring = replace(@inputstring,substring(@inputstring,@pos,1),@replacewith)
		set @pos = patindex(@invalidcharacters,@inputstring)
	end
	return @inputstring
end;
go

create function dbo.turnhout_getAuthor 
(
	--allmost all name variants have the author name in the front of the string, so we will assume that this is the case for all
	@inputstring nvarchar(1024)
)
returns nvarchar(1024)
begin
declare @pos int
	--assume author ends with et al
	set @pos = patindex('%et al%',@inputstring)
	if (@pos < 1) --no pattern found
	begin
		--check if author name ends with :
		--assume that author name is no longer than 40 characters
		set @pos = charindex(':',substring(@inputstring,1,40))
		if (@pos < 1) -- no : found
		begin
			--check if author name ends with ,
			--assume that author name is no longer than 40 characters
			set @pos = charindex(',',substring(@inputstring,1,40))
			if (@pos <1)
				set @inputstring = @inputstring
			else
				set @inputstring = substring(@inputstring,1,@pos-1)
		end
		else
			set @inputstring = substring(@inputstring,1,@pos-1)
	end
	else
		set @inputstring = substring(@inputstring,1,@pos+4)
	return Ltrim(Rtrim(@inputstring))
end;
go

create function dbo.turnhout_getISSN
(
	@inputstring nvarchar(1024)
)
returns nvarchar(1024)
begin
declare @pos int
	set @pos = patindex('%ISSN:%',@inputstring)
	if (@pos < 1)
		set @inputstring = NULL
	else
		set @inputstring = substring(@inputstring,@pos+5,10)
	return Ltrim(Rtrim(@inputstring))
end;
go

create function dbo.turnhout_getXP
(
	@inputstring nvarchar(1024)
)
returns nvarchar(1024)
begin
declare @pos int
	set @pos = patindex('%XP00%',@inputstring)
	if (@pos < 1)
		set @inputstring = NULL
	else
		set @inputstring = substring(@inputstring,@pos,11)
	return Ltrim(Rtrim(@inputstring))
end;
go

create function dbo.turnhout_getPages
(
	@inputstring nvarchar(1024)
)
returns nvarchar(1024)
begin
declare @pos int
	set @pos = patindex('%pages%',@inputstring)
	if (@pos < 1)
	begin
		--check for NL translation
		set @pos = patindex('%bladzijde%',@inputstring)
		if (@pos <1)
			set @inputstring = null
		else
		begin
			-- we dont know how many characters the pages numbers are, for example: 10-23 is different length than 1029-1129
			-- so split string again at the whitespace
			set @inputstring = Ltrim(substring(@inputstring,@pos+9,len(@inputstring)))
			set @pos = charindex(' ',@inputstring)
			if (@pos <1)
				set @inputstring = null
			else
				set @inputstring = substring(@inputstring,1,@pos-1)
		end
	end
	else
	begin
		-- we dont know how many characters the pages numbers are, for example: 10-23 is different length than 1029-1129
		-- so split string again at the whitespace
		set @inputstring = Ltrim(substring(@inputstring,@pos+5,len(@inputstring)))
		set @pos = charindex(' ',@inputstring)
		if (@pos <1)
			set @inputstring = null
		else
			set @inputstring = substring(@inputstring,1,@pos-2)
	end
	return Ltrim(Rtrim(@inputstring))
end;
go

create function dbo.turnhout_getVolume
(
	@inputstring nvarchar(1024)
)
returns nvarchar(1024)
begin
declare @pos int
	set @pos = patindex('%vol%',@inputstring)
	if (@pos < 1)
		set @inputstring = NULL
	else
	begin
		--we dont know how many characters the volume number is, for example: vol. 2 is different length than vol. 10
		set @inputstring = Ltrim(substring(@inputstring,@pos+4,len(@inputstring)))
		set @pos = charindex(' ',@inputstring)
		if (@pos <1)
			set @inputstring = null
		else
			set @inputstring = Ltrim(substring(@inputstring,1,@pos-2))
	end
	return Ltrim(Rtrim(@inputstring))
end;
go

create function dbo.turnhout_getTitle
(
	@inputstring nvarchar(1024)
)
returns nvarchar(1024)
begin
declare @pos int
	--assume that the title is after the autor, which is thus the second information section in the string

	--firstly remove the author
	set @pos = patindex('%et al%', @inputstring)
	if (@pos > 1) -- et al inside the string
	begin
		set @inputstring = Ltrim(substring(@inputstring,@pos+7,len(@inputstring)))
		--assume that the title ends with a comma
		set @pos = charindex(',',@inputstring)
		if (@pos >1)
			set @inputstring = Rtrim(substring(@inputstring,1,@pos-1))
		else
			set @inputstring = NULL
	end
	else
	begin
		--no et al, but likely that author ends with comma or dot
		set @pos = patindex('%[.,]%', @inputstring)
		if(@pos >1)
		begin
			set @inputstring = Ltrim(substring(@inputstring,@pos+2,len(@inputstring)))
			--assume that the title ends with a comma
			set @pos = charindex(',',@inputstring)
			if (@pos >1)
				set @inputstring = Rtrim(substring(@inputstring,1,@pos-1))
			else
				set @inputstring = NULL
		end
	end
	return Ltrim(Rtrim(@inputstring))
end;
go

create function dbo.turnhout_getYear
(
	@inputstring nvarchar(1024)
)
returns nvarchar(1024)
begin
declare @pos int
	set @inputstring = Ltrim(Rtrim(@inputstring)) --trim string
	set @pos = patindex('%[1-2][0-9][0-9][0-9]%',@inputstring)  --might also be that this function returns the page number if the page numbers are 4 digits long. 
	if (@pos <1)
		set @inputstring = null
	else
		set @inputstring = Rtrim(substring(@inputstring,@pos,4))
	return @inputstring
end;
go

create function dbo.turnhout_getMonth
(
	@inputstring nvarchar(1024)
)
returns nvarchar(1024)
begin
declare @pos int
	set @inputstring = lower(Ltrim(Rtrim(@inputstring)))
	set @inputstring = case --assume english month names
		when @inputstring like '%january%' then 'january'
		when @inputstring like '%jan.%' then 'january'
		when @inputstring like '%febuary%' then 'febuary'
		when @inputstring like '%feb.%' then 'febuary'
		when @inputstring like '%march%' then 'march'
		when @inputstring like '%mar.%' then 'march'
		when @inputstring like '%april%' then 'april'
		when @inputstring like '%may%' then 'may'
		when @inputstring like '%june%' then 'june'
		when @inputstring like '%july%' then 'july'
		when @inputstring like '%august%' then 'august'
		when @inputstring like '%september%' then 'september'
		when @inputstring like '%sept.%' then 'september'
		when @inputstring like '%november%' then 'november'
		when @inputstring like '%nov.%' then 'november'
		when @inputstring like '%december%' then 'december'
		when @inputstring like '%dec.%' then 'december'
		when @inputstring like '%october%' then 'october'
		when @inputstring like '%oct.%' then 'october'
		else null
	end
	return Ltrim(Rtrim(@inputstring))
end;
go

create function dbo.getScore
(
	@inputstring nvarchar(1024)
)
returns int
begin
declare @score int
	set @score = 2
	return @score
end;
go

--------------------------------------------------------

--Procedure
create procedure turnhout
as
begin
declare @pos int
declare @id int
declare @str nvarchar(1024)

	--preclean data
	drop table if exists #turnhout_temp
	select top(1000) npl_publn_id as id, dbo.turnhout_cleanIt(Ltrim(Rtrim(npl_biblio)),'%[.@#$%^&*/\<>+=-_]%') as npl_biblio, null as cluster_id
	into #turnhout_temp
	from Patstat;

	--extract metadata
	drop table if exists #turnhout_metadata
	select id,
		dbo.turnhout_getAuthor(npl_biblio) as author,
		dbo.turnhout_getTitle(npl_biblio) as title,
		dbo.turnhout_getISSN(npl_biblio) as ISSN,
		dbo.turnhout_getXP(npl_biblio) as XP_number,
		dbo.turnhout_getPages(npl_biblio) as pages,
		dbo.turnhout_getVolume(npl_biblio) as volume,
		dbo.turnhout_getYear(npl_biblio) as publication_year,
		dbo.turnhout_getMonth(npl_biblio) as publication_month
	into #turnhout_metadata
	from #turnhout_temp;

	--display metadata table
	select *
	from #turnhout_metadata;

	--first iteration, add cluster_id 1 to a random row, we choose the first row
	set @pos = 1;
	update top(1) #turnhout_temp
	set cluster_id = 1 --@pos

	--while loop
	-- structure:
	--	1. select the first row that has a cluster_id equal to @pos, find matches (of rows that have null as cluster_id) based on rules and add the same cluster_id to these rows
	--	2. after matching, increase @pos with 1 and add that cluster_id to a random row with a null as cluster_id
	--  3. go back to first step
	--  4 stop if all rows have a non null cluster_id
	while ((select count(cluster_id) from #turnhout_temp where cluster_id = null)>0)
	begin
		--get rowid with cluster_id = @pos
		set @id = (select top(1) id from #turnhout_temp where cluster_id = @pos)
		--get corresponding row in the metadata table
		set @str = (select top(1) * from #turnhout_metadata where id = @id)

		--apply score function to all rows that have not received a cluster_id
		select *,dbo.getScore(@str) as score
		from #turnhout_temp
		where cluster_id = null
		break;
	end


	--drop all tables made in procedure
	drop table if exists #turnhout_metadata
	drop table if exists #turnhout_temp

end;
go

--execute script
exec turnhout
go

--drop all
drop procedure turnhout;
drop function dbo.turnhout_cleanIt;
drop function dbo.turnhout_replace;
drop function dbo.turnhout_getAuthor;
drop function dbo.turnhout_getISSN;
drop function dbo.turnhout_getXP;
drop function dbo.turnhout_getPages;
drop function dbo.turnhout_getVolume;
drop function dbo.turnhout_getTitle;
drop function dbo.turnhout_getYear;
drop function dbo.turnhout_getMonth;
drop function dbo.getScore;
