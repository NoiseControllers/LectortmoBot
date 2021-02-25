class SessionModel(object):
    def __init__(self, tokens: list, user_agent: str):
        self.tokens = tokens
        self.user_agent = user_agent
