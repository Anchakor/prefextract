= Prefextract and Learnfilter TT-RSS plugin =

Learnfilter is a intelligent filtering plugin for a Tiny Tiny RSS feed reader.

User is presented with automatically extracted keywords for each brief article abstract, which he can rate. Those ratings are then used for filtering out articles which are not interesting to the user. (Works well only with english text)

Prefextract is a backend python REST server which does most of the work and holds the ratings database.


== Installation and usage ==

  make install
to install into the default system locations. Inspect the makefile for other options. 
Prefextract requires python libraries:
  NLTK - http://nltk.org/
  topia.termextract - https://pypi.python.org/pypi/topia.termextract/

Learnfilter is a normal TT-RSS plugin. To start Prefextract, edit the conf file and either start the systemd service, or you can run it even without installing in current directory by:
  ./main.py prefextract.conf.in


For license information see LICENSE.txt

Copyright (C) 2013 Jiří Procházka; unless specified otherwise
ojirio@gmail.com
