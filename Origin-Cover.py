# Download RED Cover with Origin File
# author: hypermodified
# This script uses an exisiting yaml origin file to get the URL for the cover and then download it.
# You need a fork of gazelle-origin with the extra metatdata installled for it to work.
# It takes the folder and opens the yaml to get the url. It then finds the image using the url saves the to the directory the origin file is in.
# It can handle albums with artwork folders or multiple disc folders in them. 
# It can also handle specials characters and skips and logs any characters that makes windows fail.
# It may fail if you store your music on the C: drive on Windows.
# It has been tested and works in both Ubuntu Linux and Windows 10.


# Import dependencies
import os  # Imports functionality that let's you interact with your operating system
import yaml  # Imports yaml
import shutil # Imports functionality that lets you copy files and directory
import datetime # Imports functionality that lets you make timestamps
import subprocess  # Imports functionality that let's you run command line commands in a script
import requests # Imports the ability to make web or api requests
import re # Imports regex


#  Set your directories here
album_directory = "M:\Python Test Environment\Albums" # Which directory do you want to start with?
log_directory = "M:\Python Test Environment\Logs" # Which directory do you want the log in?

# Set whether you are using nested folders or have all albums in one directory here
# If you have all your ablums in one music directory Music/Album_name then set this value to 1
# If you have all your albums nest in a Music/Artist/Album style of pattern set this value to 2
# The default is 1
album_depth = 1


# Establishes the counters for completed albums and missing origin files
count = 0
good_missing = 0
bad_missing = 0
bad_folder_name = 0
album_missing = 0
link_missing = 0
error_message = 0

# identifies location origin files are supposed to be
path_segments = album_directory.split(os.sep)
segments = len(path_segments)
origin_location = segments + album_depth

#intro text
print("")
print("To infinity...")

# A function to log events
def log_outcomes(d,p,m):
    global log_directory
    script_name = "Origin-Cover Script"
    today = datetime.datetime.now()
    log_name = p
    directory = d
    message = m
    album_name = directory.split(os.sep)
    album_name = album_name[-1]
    log_path = log_directory + os.sep + log_name + ".txt"
    with open(log_path, 'a',encoding='utf-8') as log_name:
        log_name.write("--{:%b, %d %Y}".format(today)+ " at " +"{:%H:%M:%S}".format(today)+ " from the " + script_name + ".\n")
        log_name.write("The album folder " + album_name + " " + message + ".\n")
        log_name.write("Album location: " + directory + "\n")
        log_name.write(" \n")  
        log_name.close()

#  A function that gets the url of the cover and downloads the cover into the same folder as the origin file
def download_cover(directory):
        global count
        global good_missing
        global bad_missing
        global bad_folder_name
        global album_missing
        global link_missing
        global origin_location
        print ("\n")
        #check to see if folder has bad characters and skip if it does
        #get album name from directory
        re1 = re.compile(r"[\\/:*\"<>|?]");
        name_to_check = directory.split(os.sep)
        name_to_check = name_to_check[-1]
        if re1.search(name_to_check):
            print ("Illegal windows character detected.")
            print("--Logged album skipped due to illegal characters.")
            log_name = "illegal-characters"
            log_message = "was skipped due to illegal characters"
            log_outcomes(directory,log_name,log_message)
            bad_folder_name +=1 # variable will increment every loop iteration
            
        else:
            print("Getting album cover for " + directory)
            #check to see if there is an origin file
            file_exists = os.path.exists('origin.yaml')
            #if origin file exists, load it, get url,  download and save cover
            if file_exists == True:
                #open the yaml and turn the data into variables
                with open(directory + os.sep + 'origin.yaml',encoding='utf-8') as f:
                  data = yaml.load(f, Loader=yaml.FullLoader)
                album_cover = data['Cover']
                clean_directory = data['Directory']
                f.close()
                                             
                # check to see if there is an album that exists and works
                if album_cover != None:
                    print ("--The album cover was located.")            
                    print("--The album cover is at: " + album_cover)
                    cover_format = album_cover.split(".")
                    cover_format = cover_format[-1]
                    print("--The cover is a " + cover_format)
                
                    # downloads cover as REDcover
                    redcover = requests.get(album_cover)
                    file = open(directory + os.sep + "REDcover." + cover_format, "wb")
                    file.write(redcover.content)
                    file.close()                    
                    print("--Cover downloaded and saved as REDcover." + cover_format)
                    
                    # rename REDcover to cover if there is no cover.jpg
                    
                
                    count +=1 # variable will increment every loop iteration

                else:
                    print("--The is origin file is missing a cover for the album.")
                    print("--Logged missing link.")
                    log_name = "no-link"
                    log_message = "origin file is missing a link to the album"
                    log_outcomes(directory,log_name,log_message)
                    link_missing +=1 # variable will increment every loop iteration
                    
            #otherwise log that the origin file is missing
            else:
                #split the directory to make sure that it distinguishes between folders that should and shouldn't have origin files
                current_path_segments = directory.split(os.sep)
                current_segments = len(current_path_segments)
                #create different log files depending on whether the origin file is missing somewhere it shouldn't be
                if origin_location != current_segments:
                    #log the missing origin file folders that are likely supposed to be missing
                    print ("--An origin file is missing from a folder that should not have one.")
                    print("--Logged missing origin file.")
                    log_name = "good-missing-origin"
                    log_message = "origin file is missing from a folder that should not have one.\nSince it shouldn't be there it is probably fine but you can double check"
                    log_outcomes(directory,log_name,log_message)
                    good_missing +=1 # variable will increment every loop iteration
                else:    
                    #log the missing origin file folders that are not likely supposed to be missing
                    print ("--An origin file is missing from a folder that should have one.")
                    print("--Logged missing origin file.")
                    log_name = "bad-missing-origin"
                    log_message = "origin file is missing from a folder that should have one"
                    log_outcomes(directory,log_name,log_message)
                    bad_missing +=1 # variable will increment every loop iteration
        
# Get all the subdirectories of album_directory recursively and store them in a list:
directories = [os.path.abspath(x[0]) for x in os.walk(album_directory)]
directories.remove(os.path.abspath(album_directory)) # If you don't want your main directory included

# Run a loop that goes into each directory identified and downloads the cover from the Gazelle site
for i in directories:
      os.chdir(i)         # Change working Directory
      download_cover(i)      # Run your function

# Summary text
print("")
print("...and beyond! This script downloaded " + str(count) + " album covers.")
print("This script looks for potential missing files or errors. The following messages outline whether any were found.")
if bad_folder_name >= 1:
    print("--Warning: There were " + str(bad_folder_name) + " folders with illegal characters.")
    error_message +=1 # variable will increment if statement is true
elif bad_folder_name == 0:    
    print("--Info: There were " + str(bad_folder_name) + " folders with illegal characters.")
if album_missing >= 1:
    print("--Warning: There were " + str(album_missing) + " albums no longer on the site.")
    error_message +=1 # variable will increment if statement is true
elif album_missing == 0:    
    print("--Info: There were " + str(album_missing) + " albums no longer on the site.")
if link_missing >= 1:
    print("--Warning: There were " + str(link_missing) + " origin files with a missing link to the album.")
    error_message +=1 # variable will increment if statement is true
elif link_missing == 0:    
    print("--Info: There were " + str(link_missing) + " origin files with a missing link to the album.")
if bad_missing >= 1:
    print("--Warning: There were " + str(bad_missing) + " folders missing an origin files that should have had them.")
    error_message +=1 # variable will increment if statement is true
elif bad_missing == 0:    
    print("--Info: There were " + str(bad_missing) + " folders missing an origin files that should have had them.")
if good_missing >= 1:
    print("--Info: Some folders didn't have origin files and probably shouldn't have origin files. " + str(good_missing) + " of these folders were identified.")
    error_message +=1 # variable will increment if statement is true
elif good_missing == 0:    
    print("--Info: Some folders didn't have origin files and probably shouldn't have origin files. " + str(good_missing) + " of these folders were identified.")
if error_message >= 1:
    print("Check the logs to see which folders had errors and what they were.")
else:
    print("There were no errors.")    
