-- Earthquake Database
-- Phase 2 Demo Queries


/*
-- viewing
1. viewing earthquakes
2. viewing earthquakes that were caused by nuclear weapons

3. filtering earthquakes based on area
4. filtering earthquakes certified by a certain source
5. filtering earthquakes based on a certain year
6. filtering earthquakes based on proximity to certain city

-- graphing
7. comparing # of earthquakes by year for a certain nation
8. comparing # of earthquakes in cities in a certain nation
9. comparing # of earthquakes per area for different nations
10. comparing # of earthquakes per capita for different regions

11. comparing most powerful earthquakes by nation
12. comparing # of earthquakes for each coordinate

13. comparing # of nuclear tests by year
14. comparing # of nuclear tests by country (location)

-- management
15. finding closest city to a certain location
16. adding in a new earthquake
17. editing previous earthquake information
18. adding in source to earthquake
19. adding in a new earthquake that was caused by a nuke + 2 source
20. editing previous nuclear bomb yield reading
*/


-- 1
select
        datetime(e_time) as date_time,
        e_longitude,
        e_latitude,
        e_mag
from
        earthquake
order by
        e_time desc
;


-- 2
select
        datetime(e_time) as date_time,
        e_longitude,
        e_latitude,
        e_mag
from
        earthquake
where
        e_type = 'nuclear explosion'
order by
        e_time desc
;


-- 3
select
        datetime(e_time) as date_time,
        c_name,
        e_longitude,
        e_latitude,
        e_mag
from
        earthquake,
        city,
        state
where
        e_type = 'earthquake' and
        e_citykey = c_citykey and
        c_statekey = s_statekey and
        s_name = 'California'
order by
        e_time desc
;


-- 4
select
        datetime(e_time) as date_time,
        c_name,
        e_longitude,
        e_latitude,
        e_mag
from
        earthquake,
        earthquakesource,
        earthquakesourcemapping,
        city
where
        e_earthquakekey = esm_earthquakekey and
        esm_eskey = es_eskey and
        es_eskey = 'AK' and
        e_citykey = c_citykey
order by
        e_time desc
;


-- 5
select
        datetime(e_time) as date_time,
        c_name || ', ' ||  s_name || ', ' || n_name as place,
        e_longitude,
        e_latitude,
        e_mag
from
        earthquake,
        city,
        state,
        nation
where
        e_type = 'earthquake' and
        e_citykey = c_citykey and
        c_statekey = s_statekey and
        s_nationkey = n_nationkey and
        strftime('%Y', e_time) = '2011'
order by
        e_mag desc
;


-- 6
select
        datetime(e_time) as date_time,
        cityother.c_name || ', ' ||  s_name as place,
        e_longitude,
        e_latitude,
        e_mag
from
        earthquake,
        city as citycenter,
        city as cityother,
        state
where
        e_type = 'earthquake' and
        e_citykey = cityother.c_citykey and
        citycenter.c_statekey = s_statekey and
        abs(e_latitude - citycenter.c_latitude) < 3 and
        abs(e_longitude - citycenter.c_longitude) < 3 and
        citycenter.c_name = 'San Francisco' and
        s_name = 'California'
order by
        e_time desc
;


-- 7
select
        strftime('%Y', e_time) as year,
        count(*) as cnt
from
        earthquake,
        city,
        state,
        nation
where
        e_type = 'earthquake' and
        e_citykey = c_citykey and
        c_statekey = s_statekey and
        s_nationkey = n_nationkey and
        n_name = 'United States'
group by
        year
order by
        year desc
;


-- 8
select
        c_name,
        s_name,
        count(*) as cnt
from
        earthquake,
        city,
        state,
        nation
where
        e_type = 'earthquake' and
        e_citykey = c_citykey and
        c_statekey = s_statekey and
        s_nationkey = n_nationkey and
        n_name = 'United States'
group by
        c_citykey,
        s_statekey
order by
        cnt desc
;


-- 9
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


-- 10
select
        r_name,
        count(*) / (r_population/1000000000 + 1) as relative_population
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
        n_regionkey = r_regionkey
group by
        r_regionkey
;


-- 11
select
        n_name,
        max(e_mag) as max_mag
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
        max_mag desc
;


-- 12
select
        cast(e_latitude / 5 as int) * 5 + 2.5 as latitude,
        cast(e_longitude / 5 as int) * 5 + 2.5 as longitude,
        count(*) as cnt
from
        earthquake
group by
        latitude,
        longitude
order by
        cnt desc
;


-- 13
select
        strftime('%Y', ne_time) as year,
        count(*) as cnt
from
        earthquake,
        nuclear
where
        e_earthquakekey = ne_earthquakekey
group by
        year
order by
        year desc
;


-- 14
select
        n_name,
        count(*) as cnt
from
        earthquake,
        nuclear,
        city,
        state,
        nation
where
        e_earthquakekey = ne_earthquakekey and
        e_citykey = c_citykey and
        c_statekey = s_statekey and
        s_nationkey = n_nationkey
group by
        n_nationkey
order by
        cnt desc
;


-- 15
select
        city.*,
        min(abs(35 - c_latitude)+abs(100 - c_longitude)) as min_diff
from
        city
;


-- 16
insert into
        earthquake
values(
        'ex11111111',
        30000000.000,
        100, 35, -1,
        5.8, 'mb',
        'earthquake',
        1788852
)
;


-- 17
update
        earthquake
set
        e_mag = 6.0,
        e_magtype = 'ml'
where
        e_earthquakekey = 'ex11111111'
;


-- 18
insert into
        earthquakesourcemapping
values(
        'ex11111111',
        'ISCGEM'
)
;


-- 19
insert into
        earthquake
values(
        'ex22222222',
        40000000.000,
        100, 35, -5,
        6.3, 'mb',
        'nuclear explosion',
        1788852
)
;
insert into
        earthquakesourcemapping
values(
        'ex22222222',
        'CI'
)
;

insert into
        nuclear
values(
        11111,
        40000000.000,
        'USA',
        'FAKESITE',
        35,
        100,
        -5,
        100.0,
        'WR',
        'AIRDROP',
        'ex22222222'
)
;
insert into
        nuclearsourcemapping
values(
        11111,
        'N'
)
;


-- 20
update
        nuclear
set
        ne_yield = 120.0,
        ne_droptype = 'TOWER'
where
        ne_nuclearkey = 11111
;
