import openai
import os
import time

# Potentially viable singleton instance
class assistant(object):
	_instance    = None
	_initialised = False

	def __new__(cls):
		if cls._instance is None:
			cls._instance = super().__new__(cls)
		return cls._instance

	def __init__(self):
		if not self._initialised:
			self.api_key = os.getenv("OPENAI_API_KEY")
			openai.api_key = self.api_key
			self.client = openai.OpenAI()
			self.configure()
			self._initialised = True

	def configure(self):
		self.threads   = {}
		assistant = self.client.beta.assistants.create(name="beccabot",
													   instructions="You are an gaming expert called BeccaBot with a range of knowledge which encompasses food, the United Kingdom, Sweden and you are an expert on the game Overwatch.",
													   tools=[],
													   model="gpt-3.5-turbo")
		self.assistant = assistant.id

	def clear_threads(self):
		self.threads = {}

	def check_user_thread(self, user):
		if user not in self.threads:
			thread             = self.client.beta.threads.create()
			self.threads[user] = thread.id

	def interact(self, user, message_in):
		self.check_user_thread(user)
		thread_id = self.threads[user]
		message = self.client.beta.threads.messages.create(thread_id=thread_id,
													  	   role="user",
												      	   content=message_in)
		run = self.client.beta.threads.runs.create(thread_id=thread_id,
												   assistant_id=self.assistant)
		time.sleep(0.5)
		while True:
			state = self.client.beta.threads.runs.retrieve(thread_id=thread_id,run_id=run.id).status
			if state == 'completed':
				break
			else:
				time.sleep(1)
		# Check output
		messages = self.client.beta.threads.messages.list(thread_id=thread_id)
		return messages.data[0].content[0].text.value



