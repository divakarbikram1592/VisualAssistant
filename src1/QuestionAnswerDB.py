from nltk.corpus import stopwords

from QuestionAnswerModel import QuestionAnswer

class QuestionAnswerDB:
    questions = {
        "what is your name": "I unable to identify",
        "how old are you": "I am an artificial intelligence and do not have an age.",
        "what is the meaning of life": "The meaning of life is subjective and varies from person to person.",
        "what is the capital of france": "The capital of France is Paris.",
    }



    def init(self, query, name="I unable to identify"):
        # Define a set of stopwords
        self.questions['what is your name'] = name
        stop_words = set(stopwords.words('english'))
        objQA = QuestionAnswer(self.questions, stop_words)
        objQA.init(query)