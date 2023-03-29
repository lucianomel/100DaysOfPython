class QuizzBrain:
    def __init__(self, q_bank):
        self.question_number = 0
        self.question_list = q_bank
        self.score = 0

    # TODO: asking the questions
    def next_question(self):
        new_q = self.question_list[self.question_number]
        self.question_number += 1
        user_answer = input(f"Q.{self.question_number}: {new_q.text} (True/False)?: ")
        self.check_answer(user_answer, new_q.answer)

    # TODO: checking if we are at the end of the quiz
    def still_has_questions(self):
        return len(self.question_list) > self.question_number

    # TODO: checking if the answer was correct
    def check_answer(self, user_answer, correct_answer):
        if user_answer.lower() == correct_answer.lower():
            print("You got it right!")
            self.score += 1
        else:
            print("Wrong")
        print(f"The correct answer is {correct_answer}")
        print(f"Your current score is: {self.score}/{self.question_number}.\n")
