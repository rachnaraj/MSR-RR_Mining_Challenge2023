Here I am tryig to use the dataset obtained in fourth phase implementation. 

I am trying to filter those conversations, where I see a version number using regex. If i find any version number, I append the whole conversations, not only one interaction (conversation).
I am also checking the occurance in prompt, answer and in code.

Known issue:

the regex is also capturing IPs.

suggestion by Prof.:

use combined conditions: regex + some relevant keyword like npm, pypi, mvn, version . (yet to think and implement)