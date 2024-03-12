import nltk

# nltk.download('punkt')  # Download the punkt tokenizer if you haven't already
# nltk.download('stopwords')  # Download the stopwords if you haven't already
from Speaking import Speaking

class QuestionAnswer:

    def __init__(self, questions, stop_words):
        self.questions = questions
        self.stop_words = stop_words

    # Define a function to remove stopwords from a given text
    def remove_stopwords(self, text):
        words = nltk.word_tokenize(text)
        words_filtered = [word.lower() for word in words if word.lower() not in self.stop_words]
        return ' '.join(words_filtered)

    # Define a function to handle user input and generate responses
    def respond(self, user_input):
        # Remove stopwords from user input
        user_input = self.remove_stopwords(user_input)

        tokens = nltk.word_tokenize(user_input.lower())
        for question in self.questions:
            # Remove stopwords from system questions
            q = self.remove_stopwords(question)
            if all(word in tokens for word in nltk.word_tokenize(q.lower())):
                return self.questions[question]
        return "I'm sorry, I don't understand what you're asking."

    # Main program loop
    def init(self, user_query):
        response = self.respond(user_query)
        print("Response:", response)
        objSpeak = Speaking()
        objSpeak.speak(response)
