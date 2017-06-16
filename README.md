# CineFiles Backup Log Maker

This is a set of scripts that produce a CSV log of redundant backups of images for [CineFiles](bampfa.org/cinefiles) and generates an HTML table view of that CSV. The CSV generator uses imagemagick `mogrify` to produce a base64 encoded version of each image for reference.

## Usage

Run `python log.py` to create the backup CSV, which then needs to go in the `data/` folder. Right now you have to manually change the path in `index.html` to the latest log CSV.

To test it locally run `python2.7 -m SimpleHTTPServer` and go to [http://localhost:8000](http://localhost:8000)

## Ideas taken from:

The HTML portion came from Derek Eder's [csv-to-html project](https://github.com/derekeder/csv-to-html-table) (Copyright (c) 2015 Derek Eder.)

The filesize calculation came from [this stack overflow thread](http://stackoverflow.com/questions/14996453/python-libraries-to-calculate-human-readable-filesize-from-bytes).

## Dependencies

**csv-to-html** has its own dependencies (bootstrap, jquery, jquery csv, DataTables). 

The python portion requires [imagemagick](https://www.imagemagick.org/script/index.php) be installed, but uses the standard python library. Tested with python 3.5.

## TO DO

This is in progress!

The python script was originally fed into a Mac automator applet, so there's a request for the filepath to be logged. I need to make it run using crontab and the resulting html should be pushed to a static (password-protected) site. Need to figure out where to host that will be secure.

Change the html in `index.html` to look for today's date in the csv filepath to match the latest CSV.

