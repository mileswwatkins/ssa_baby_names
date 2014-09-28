ssa_names
=========

Python wrapper for the Social Security Administration's ["Popular Baby Names" service] (http://www.ssa.gov/OACT/babynames/).

Provides access to the 1,000 most popular names of both genders in any year of American history, going back to 1880. Both the frequency of names and their relative frequencies (ie, percentage of all births of their gender) are available. These top 1,000 names encompass roughly 90% of all births in any given year.

===

What was the most popular name in 1985?

`>>> from ssa_names import get_top_names`

`>>> top_male_names_from_1985 = get_top_names(year=1985, name_gender_is_male=True)`

`>>> top_names[0]`

`{'percentage': 3.3742, 'frequency': 64883, 'name': 'Michael', 'rank': 1}`

How popular was my name in that year?

`>>> [name_info for name_info in top_names if name_info["name"] == "Miles"]`

`[{'percentage': 0.0238, 'frequency': 457, 'name': 'Miles', 'rank': 396}]`

