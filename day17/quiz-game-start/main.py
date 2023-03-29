from question_model import Question
from data import question_data
from quiz_brain import QuizzBrain

question_bank = []
for q in question_data:
    question_bank.append(Question(q["question"], q["correct_answer"]))

quiz = QuizzBrain(question_bank)

while quiz.still_has_questions():
    quiz.next_question()

print("You've completed the quiz")
print(f"Your final score is: {quiz.score} out of {quiz.question_number}")