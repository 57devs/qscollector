import os

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)


class Question(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String, unique=True, nullable=False)
	choices = db.Column(db.String, nullable=False)
	correct_choice = db.Column(db.Integer, nullable=False)
	difficulty = db.Column(db.Integer, nullable=False)
	tags = db.Column(db.String, nullable=False)

	def __repr__(self):
		return '<Question %r>' % self.title

	def to_dict(self):
		return {
			'id': self.id,
			'title': self.title,
			'choices': self.choices.split(','),
			'correct_choice': self.correct_choice,
			'difficulty': self.difficulty,
			'tags': self.tags
		}


@app.route('/question/add', methods=['GET', 'POST'])
def question():
	if request.method == 'POST':
		choices = ','.join(
			[
				request.form['choice-a'],
				request.form['choice-b'],
				request.form['choice-c'],
				request.form['choice-d']
			]
		)
		q = Question(
			title=request.form['title'],
			choices=choices,
			correct_choice=request.form['correct-choice'],
			difficulty=request.form['difficulty'],
			tags=request.form['tags']
		)
		db.session.add(q)
		db.session.commit()

	return render_template('question.html')


@app.route('/question/delete/<qid>', methods=['GET', 'POST'])
def delete(qid):
	question = Question.query.get(qid)
	if request.method == 'POST':
		if int(request.form['security-password']) != 1410:
			return render_template('delete.html')

		Question.query.filter(Question.id == qid).delete()
		db.session.commit()

		return redirect("/")

	return render_template('delete.html', q=question.to_dict())


@app.route('/', methods=['GET'])
def list():
	questions = Question.query.order_by(Question.id.desc())

	return render_template(
		'list.html', 
		q_list=[question.to_dict() for question in questions]
	)


@app.route('/question/<qid>', methods=['GET', 'POST'])
def update(qid):
	question = Question.query.get(qid)
	if request.method == 'POST':
		if int(request.form['security-password']) != 1410:
			return render_template('update.html', q=question.to_dict())

		choices = ','.join(
			[
				request.form['choice-a'],
				request.form['choice-b'],
				request.form['choice-c'],
				request.form['choice-d']
			]
		)

		question.title = request.form['title']
		question.choices = choices
		question.correct_choice = request.form['correct-choice']
		question.difficulty = request.form['difficulty']
		question.tags = request.form['tags']

		db.session.commit()

	return render_template('update.html', q=question.to_dict())


if __name__ == '__main__':
	app.run(debug=True)