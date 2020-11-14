-- Project Queries


--1.
-- for viewing different earthquakes

select
        *
from
        earthquake
;

--2.
-- for filtering earthquakes based on area

select
        datetime(e_time) as date_time,
        *
from
        earthquake,
        city,
        state
where
        e_citykey = c_citykey and
        c_statekey = s_statekey and
        s_name = 'California'
order by
        e_time asc
;

--3.
-- for filtering out earthquakes caused by nukes used for combat

select
        *
from
        nuclear
where
        ne_purpose = 'COMBAT' and
        ne_yield > 20
;

--4.
-- for filtering out earthquakes caused by nukes certified by public agencies

select
        *
from
        nuclearsource
where
        nes_ispublic = 1
;

--5.
-- earthquakes certified by Alaska Geological Survery

select
        *
from
        earthquake,
        earthquakesource,
        earthquakesourcemapping
where
        e_earthquakekey = esm_earthquakekey and
        esm_eskey = es_eskey and
        es_eskey = 'AK'
;

--6.
-- count of earthquakes in a state by year

select
        strftime('%Y', e_time) as year,
        count(*)
from
        earthquake,
        city,
        state
where
        e_citykey = c_citykey and
        c_statekey = s_statekey and
        s_name = 'Alaska'
group by
        year
;

--7.
-- count of earthquakes in a region for a given year

select
        r_name,
        count(*)
from
        earthquake,
        city,
        state,
        nation,
        region
where
        e_citykey = c_citykey and
        c_statekey = s_statekey and
        s_nationkey = n_nationkey and
        n_regionkey = r_regionkey and
        strftime('%Y', e_time) = '2010'
group by
        r_regionkey
;

--8.
-- relative number of earthquakes for state per captia

select
        s_name,
        count(*) / (s_population/1000000 + 1)
from
        earthquake,
        city,
        state,
        nation
where
        e_citykey = c_citykey and
        c_statekey = s_statekey and
        s_nationkey = n_nationkey and
        n_name = 'United States'
group by
        s_statekey
;

--9.
-- states and provinces in the world with the highest number of earthquakes

select
        state.*,
        count(*) as cnt
from
        earthquake,
        city,
        state
where
        e_citykey = c_citykey and
        c_statekey = s_statekey
group by
        s_statekey
order by
        cnt desc
limit
        10
;

--10.
-- getting closest city to certain location

select
        city.*,
        min(abs(35 - c_latitude)+abs(100 - c_longitude)) as min_diff
from
        city
;


--11.
-- inserting new earthquake into database

insert into earthquake
values('ex20201231', 24581000.646, 100, 35, -1, 5.8, 'mb', 'earthquake', 2049653)

--12.
-- relative number of earthquakes in a nation per area

select
        n_name,
        cast(count(*) * 1000000 / n_area as int) as relative_area
from
        earthquake,
        city,
        state,
        nation
where
        e_citykey = c_citykey and
        c_statekey = s_statekey and
        s_nationkey = n_nationkey
group by
        n_nationkey
order by
        relative_area desc
;

--13.
-- earthquakes occuring with certain area around a city

select
        other.c_name,
        earthquake.*
from
        earthquake,
        city as center,
        state,
        city as other
where
        e_citykey = other.c_citykey and
        center.c_name = 'Los Angeles' and
        center.c_statekey = s_statekey and
        s_name = 'California' and
        abs(center.c_latitude - other.c_latitude) < 2 and
        abs(center.c_longitude - other.c_longitude) < 2
;

--14.
-- highest magnitude earthquake before a certain date

select
        earthquake.*,
        max(e_mag)
from
        earthquake
where
        cast(strftime('%Y', e_time) as int) < 1910
;

--15.
-- for filtering earthquakes in nations with more than a million people

select
        *
from
        nation
where
        n_population > 1000000
;

--16.
-- nukes that caused earthquakes in asia

select
        nuclear.*
from
        earthquake,
        nuclear,
        city,
        state,
        nation,
        region
where
        e_citykey = c_citykey and
        e_earthquakekey = ne_earthquakekey and
        c_statekey = s_statekey and
        s_nationkey = n_nationkey and
        n_regionkey = r_regionkey and
        r_name = 'Asia'
;

--17.
-- average magnitude of earthquake caused by nukes with a certain yield

select
        avg(e_mag)
from
        earthquake,
        nuclear
where
        e_earthquakekey = ne_earthquakekey and
        ne_yield > 1000
;

--18.
-- cities with nuclear testing near them

select
        c_name,
        s_name,
        n_name,
        count(*)
from
        city,
        state,
        nation,
        nuclear,
        earthquake
where
        c_citykey = e_citykey and
        e_earthquakekey = ne_earthquakekey and
        c_statekey = s_statekey and
        s_nationkey = n_nationkey
group by
        c_citykey
;

--19.
-- earthquakes that happened in cities in Europe with less than a certain population

select
        earthquake.*
from
        city,
        state,
        nation,
        region,
        earthquake
where
        e_citykey = c_citykey and
        c_statekey = s_statekey and
        s_nationkey = n_nationkey and
        n_regionkey = r_regionkey and
        r_name = 'Europe' and
        c_population < 75000
;

--20.
-- earthquakes in a certain city

select
        *
from
        earthquake,
        city
where
        e_citykey = c_citykey and
        c_name = 'California City'
;