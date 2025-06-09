class Logger:
    def log(self, message):
        print(f"[LOG] {message}")

class ErrorLogger(Logger):
    def log(self, message):
        print(f"[ERROR] {message}")


