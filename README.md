[![Build Status](https://travis-ci.org/leohemsted/gfit2mfp.svg?branch=master)](https://travis-ci.org/leohemsted/gfit2mfp) [![Coverage Status](https://coveralls.io/repos/leohemsted/gfit2mfp/badge.svg)](https://coveralls.io/r/leohemsted/gfit2mfp)

gfit2mfp - Google Fit -> My Fitness Pal
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

Work out if there's a convenient way to get all activity - not just by device. what happens if i get a smart watch or brick my phone? Look at `derived:com.google.activity.segment:com.google.android.gms:merge_activity_segments`

match activity to calories before grouping the timesets - discard anything without an activity (though probably at least print out cals so I can see how much is there and work out if I want to do anything with it) - also sleepdroid reports my sleeping to google fit - creepy - probs don't want that popping up anywhere
