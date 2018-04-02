#przyklad: 
#0. kim jestes?
#1. czy kupiles kiedys oprogramowanie?
#2. czy sciagnales kiedys nielegalnie oprogramowanie?


questions = ['kim jestes?','czy kupiles kiedys oprogramowanie?','czy sciagnales kiedys nielegalnie oprogramowanie?']

#[odp0, odp1, odp2]
interviewees = [
['student', 'nie', 'tak'],
['nie student', 'tak', 'tak'],
['student', 'tak', 'nie'],
['nie student', 'nie', 'nie'],
['nie student', 'nie', 'nie'],
['student', 'nie', 'tak']
]

dicts = {}
base_question = 0
number_of_questions = 3

other_questions = range(number_of_questions)
other_questions.remove(base_question)
for q in other_questions:
	dicts[q] = {}
	for interviewee in interviewees:
		if interviewee[base_question] not in dicts[q]:
			dicts[q][interviewee[base_question]] = {interviewee[q]:1}
		else:
			if interviewee[q] not in dicts[q][interviewee[base_question]]:
				dicts[q][interviewee[base_question]][interviewee[q]] = 1
			else:
				dicts[q][interviewee[base_question]][interviewee[q]] += 1
				
				
print 'pytanie bazowe: ', questions[base_question], '\n'
for q in other_questions:
	print 'pytanie', q, ':', questions[q]
	print dicts[q]
	print '\n'
	

