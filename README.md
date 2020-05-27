# Sponius (What it is)
  * sponius is a CLI lyrics service which works with [Spotify desktop app](https://www.spotify.com/us/download) and [genius.com](https://genius.com)
  * SpoNius = Spotify + geNius

# Sponius (How it works)
  * Type `sponius` in terminal and instantly get the lyrics of what you're listening on spotify. **BOOM!**
  * Type `sponius <song title> by <song aritst>` to search for a song's lyrics
  * Or Type `sponius -s <song title> -a <song artist>`

## Installation
1- clone the repository
  * `git clone https://github.com/mrtaalebi/sponius && cd sponius`
  
2- You need python development headers to build some of the requirements and few other packages
  * Linux:
    * Ubuntu/Debian: `sudo apt update && sudo apt install build-essential python-dev dbus python3-pip virtualenv build-essential python3-dev libdbus-glib-1-dev libgirepository1.0-dev`
    * Arch `sudo pacman -Sy base-devel dbus python-pip python-virtualenv`
  * macOs: **(Currently doesn't support macOS)**
    * Contribution is very pleased here!
  
3- Run install.sh
  * `./install.sh`

# ToDo
  * The lyrics search algorithm is very simple and can be improved
  * Logging and incident reporting
  * Lyrics can be printed in color

# Bugs and Reports
  * Please inform me if you see any bugs or had any bad experience using `sponius`
  * You could contact me via email: the.doors.are.locked@gmail.com or twitter DM @mrtaalebi

