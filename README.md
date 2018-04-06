# facebook-messenger-parser

A Python script that parses a given Facebook conversation archive .html file into a .csv file. The generated .csv file formatted as `username,word,frequency`. Downloading your Facebook data archive is necessary.

A threshold can be set to exclude all words with frequencies lower than it, which can be helpful if you don't care about words that were used once or twice.

Since this was developed in a couple of hours intended for use by me and my friends, this isn't completely bug free (and likely will never be).
