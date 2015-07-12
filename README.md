[![Build Status](https://travis-ci.org/leohemsted/gfit2mfp.svg?branch=master)](https://travis-ci.org/leohemsted/gfit2mfp) [![Coverage Status](https://coveralls.io/repos/leohemsted/gfit2mfp/badge.svg)](https://coveralls.io/r/leohemsted/gfit2mfp)

gfit2mfp = Google Fit -> My Fitness Pal
=======================================

takes excercise data from Google Fit and imports into My Fitness Pal

Edit the settings file, install the files using setup.py, and then run the module or something. i'll figure it out later

notes to self:

`google.activity.segment` returns you a two-array of values, the first of which has an `intval` key that represents the activity type, as seen here: https://developers.google.com/fit/rest/v1/reference/activity-types

The important ones:

---------------
| Running | 8 |
| Walking | 7 |
| Cycling | 1 |
| unknown | 4 |
---------------

Todo:
=====

* Make sure login works
* get posting of activities working
* Figure out what exercise_id means in mfp
* is regex the best way to get the csrf? it'll probably fall over if there's a weird line break or something. look into beautifulsoup
* get list of activity IDs
* make the type of activity configurable in the settings file
