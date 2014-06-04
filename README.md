questionAnsweringFamousPeople
=============================

Author: Łukasz Pawluczuk
This is homework project for "Zastosowanie informatyki w przetwarzaniu języka naturalnego" at the Adam Mickiewicz's University.



This is simple Question Answering system wich is able to answer question about birth and death of famous people. 
This works only for polish language.
This project contains also crawler to retrieve data about birth and death of famous people. It's scrapy crawler. See crawler/ directory.


Dependencies which you need to run this project:

psi-toolki: http://psi-toolkit.amu.edu.pl/
liner2.3: http://nlp.pwr.wroc.pl/en/tools-and-resources/liner2


See program.py lines 35-50 to see how ugly is the way I am running this dependencies and hopefully understand it:) 

To run this program You need to call:
python program.py --q "QUESTION IN POLISH"


You can use it freely without any restrictions if you want. Enjoy!
