SSA Baby Names
==============

About
-----
A Python wrapper for the Social Security Administration's [Popular Baby Names service](http://www.ssa.gov/OACT/babynames/).

Provides access to the most popular names of both genders in a year of American history. Both the frequency of names and their relative frequencies (ie, percentage of all births of their gender) are available.

The top 1,000 names are available for a given gender and year; these encompass roughly 90% of all births. The earliest year in the database is 1880.

Installation
------------
`pip install ssa_baby_names`, or clone this Github repository.

Usage
-----
What was the most popular name for boys in 1985?

```
>>> from ssa_baby_names import get_top_names
>>> names = get_top_names(year=1985, name_gender_is_male=True)
>>> print(names.top().name)
Michael
```


How popular was my name in that year?

```
>>> my_name = names.lookup("Miles")
>>> print(my_name)
<BabyName for "Miles">
>>> print(my_name.rank)
396
>>> print(my_name.frequency)
497
>>> print(my_name.percentage)
0.0238
```
