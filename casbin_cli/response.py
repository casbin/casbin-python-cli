class ResponseBody:  
    def __init__(self, allow=None, explain=None):  
        """The response body class is used to unify the JSON output format"""  
        self.allow = allow  
        self.explain = explain  
      
    def to_dict(self):  
        """Convert to dictionary format"""  
        return {  
            "allow": self.allow,  
            "explain": self.explain  
        }