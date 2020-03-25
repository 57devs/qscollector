from settings import TEST_QUESTION_SIZE


class Q:
	def __init__(self, i):
		self.i = i

	def to_dict(self):
		return {
			'id': self.i,
			'title': 'test title',
			'choices': list('abcd'),
			'correct_choice': 1,
			'difficulty': 3,
			'tags': ['test']
		}


def get_q(i):
	return Q(i)


def get_test_questions():
	return [get_q(i) for i in range(1, TEST_QUESTION_SIZE)]
