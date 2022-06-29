# Origin-Cover: Download Album Art
### A python script that that loops through album folders, finds exisiting yaml origin files, gets the URL for the album cover from the yaml, and then downloads the art to the album folder.

Many times when you download an album, the art is not included with the music files. Other times the art is there but small and the site has larger, higher quality art available as metadata. This script recursively looks through all the album folders in a directory for for folders with origin.yaml files.  When it finds an origin.yaml file it opens it and looks for a url to cover art. It then downloads the art as REDcover.jpg (or whatever type of image it is). If the album does not have a cover.jpg folder already, it will rename the image as cover.jpg.

It has been tuned to not download "404" or "image missing" images and will log any albums it skips and explain why: image no longer on the interenet, site no longer exists, etc.

This project has a dependency on the gazelle-origin project created by x1ppy. gazelle-origin scrapes gazelle based sites and stores the related music metadata in a yaml file in the music albums folder. For this script to work you need to use a fork that has additional metadata including the cover art. The fork that has the most additional metadata right now is: https://github.com/spinfast319/gazelle-origin

It can handle albums with artwork folders or multiple disc folders in them. It can also handle specials characters and skips and logs any albums that have characters that makes windows fail. It has been tested and works in both Ubuntu Linux and Windows 10.

## Install and set up
Clone this script where you want to run it.

Set up or specify the two directories you will be using and specify whether you albums are nested under artist or not.
1. The directory of the albums that have up to date orgin files
2. A directory to store the log files the script creates
3. Set the album_depth variable to specify whether you are using nested folders or have all albums in one directory
   - If you have all your ablums in one music directory, ie. Music/Album then set this value to 1
   - If you have all your albums nest in a Music/Artist/Album style of pattern set this value to 2

The default is 1 (Music/Album)

Then run the script from the command line.  When it finishes it will output how many album covers it downloaded.

It will also create logs of any albums it was unable to get album covers for and save to the logs folder with a short explanation of what went wrong. In some cases, connection or api issues, you might want to rerun those folders. In others, such as "the art is no longer on the internet", you will want to check in case the art is actually there and just at a weird URL. If it isn't on the site find a copy and consider adding it to the site. 
