
# Used to add words to the stoplist
from nltk.corpus import stopwords
stop = stopwords.words(u'english')

# Add Stopwords
stop.append(u"of")
stop.append(u"the")
stop.append(u"not")
stop.append(u"to")
stop.append(u"or")
stop.append(u"this")
stop.append(u"all")
stop.append(u"on")
stop.append(u"with")
stop.append(u"we")
stop.append(u"in")
stop.append(u"This")
stop.append(u"The")
stop.append(u",")
stop.append(u".")
stop.append(u"..")
stop.append(u"...")
stop.append(u"...).")
stop.append(u"\")..")
stop.append(u".")
stop.append(u";")
stop.append(u"/")
stop.append(u")")
stop.append(u"(")
stop.append(u"must")
stop.append(u"system")
stop.append(u"This")
stop.append(u"The")
stop.append(u",")
stop.append(u"must")
stop.append(u"and")
stop.append(u"of")
stop.append(u"by")
stop.append(u"program")
stop.append(u"analysis")
stop.append(u"solution")
stop.append(u"stage")
stop.append(u"updated")
stop.append(u"\u2022")
stop.append(u"<h2>")
stop.append(u"</h2>")
stop.append(u"</strong></h2>")
stop.append(u"raportal")
stop.append(u"project")
stop.append(u"Project")
stop.append(u"wbs")
stop.append(u"WBS")

strp = list()
strp.append(u"<strong>")
strp.append(u"a>")
strp.append(u"<a>")
strp.append(u"<strong>")
strp.append(u"</")
strp.append(u"</h2")
strp.append(u"ttp://")
strp.append(u">")
strp.append(u"<a></a>")
strp.append(u"1>")
strp.append(u"\n")