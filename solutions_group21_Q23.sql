---		Question 23 GROUP 21 
---		first run all helper function
---		then run the procedure -> exec procedure -> drop all function and procedures

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


create function dbo.turnhout_getAuthor 
(
	--allmost all name variants have the author name in the front of the string, so we will assume that this is the case for all
	@inputstring nvarchar(1024)
)
returns nvarchar(1024)
begin
declare @pos int
	set @pos = patindex('%et al%:%,%',@inputstring)
	if (@pos < 1)
		set @inputstring = substring(@inputstring,1,@pos)
	else
		set @inputstring = substring(@inputstring,1,@pos-1)
	return Ltrim(Rtrim(@inputstring))
end;

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

create function dbo.turnhout_getPages
(
	@inputstring nvarchar(1024)
)
returns nvarchar(1024)
begin
declare @pos int
	set @pos = patindex('%pages%',@inputstring)
	if (@pos < 1)
		set @inputstring = NULL
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
		set @pos = patindex('%,.%', @inputstring)
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

--------------------------------------------------------

--Procedure
create procedure turnhout
as
begin
	--create helper table
	drop table if exists #turnhout_metadata
	create table #turnhout_metadata (
		id int,
		Author varchar,
		Title varchar,
		Volume int,
		Issue int,
		Pages varchar,
		Publication_year int,
		Publication_month varchar,
		ISSN int,
		ISBN int,
		DOI int,
		XP_number varchar
	)

	--preclean data
	drop table if exists #turnhout_temp
	select top(1000) npl_publn_id as id, dbo.turnhout_cleanIt(Ltrim(Rtrim(npl_biblio)),'%[.@#$%^&*/\<>+=-_]%') as npl_biblio
	into #turnhout_temp
	from Patstat

	--extract metadata
	select id,
		dbo.turnhout_getAuthor(npl_biblio) as author,
		dbo.turnhout_getTitle(npl_biblio) as title,
		dbo.turnhout_getISSN(npl_biblio) as ISSN,
		dbo.turnhout_getXP(npl_biblio) as XP_number,
		dbo.turnhout_getPages(npl_biblio) as pages,
		dbo.turnhout_getVolume(npl_biblio) as volume,
		dbo.turnhout_getIssue(npl_biblio) as issue
	--into #turnhout_metadata
	from #turnhout_temp

	select *
	from patstat

end;

--execute script
exec turnhout

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
