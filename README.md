# WikipediaSkim
trying to use Wikipedia API

This was originally meant to utilize wikipedias python API because I saw someone use it for a niffty reddit post. Something about the age of italian cities. The wikipedia API
troubles with the web page I was interested in. It had some setting to block information like pictures, tables and audio. I was only interested in tables and I couldn't find
documentation on changing this behavior.


I instead used beautiful soup to grab all the data from the page and parse through it myself. Not as cool but it got it done.

This particular attempt grabbed information from the page showing deaths caused by war in the past 2000 years. This page was then parsed for every entry and then these entries were
aggregated based on 50 year periods. I then used matplot to graph the data generated/parsed. This created a nice visual graph showing that the 20th century actually sucked.
