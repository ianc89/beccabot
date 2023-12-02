import openai
import os

class bot(object):
	def __init__(self):
		self.api_key = ""

	def configure(self):
		return

class davinci(bot):
	def __init__(self):
		super().__init__()
		self.api_key = os.getenv("OPEN_API_KEY")
		openai.api_key = self.api_key

	def configure(self):
		self.model             = "text-davinci-003"
		self.temperature       = 0.5
		self.max_tokens        = 60
		self.top_p             = 1.0
		self.frequency_penalty = 0.5
		self.presence_penalty  = 0.0

	def prompt(self, question):
		question = " ".join(question)
		print (question)
		response = openai.Completion.create(
  			model             = self.model,
  			prompt            = f"You: {question}",
  			temperature       = self.temperature,
  			max_tokens        = self.max_tokens,
  			top_p             = self.top_p,
  			frequency_penalty = self.frequency_penalty,
  			presence_penalty  = self.presence_penalty,
  			stop              = ["You:"]
		)
		print (response)
		answer = response['choices'][0]['text']
		return response, answer
