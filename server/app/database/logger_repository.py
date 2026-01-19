from app.config import directory_log

class LoggerRepository():
    FOLDER = directory_log()

    def __init__(self):
        pass
    
    def read_log(self, filename):
        self.filepath = self.FOLDER + "\\" + filename

        with open(self.filepath, "r") as f:
            self.file = f.read()

        return {"message": self.file}, 200

    def write_log(self, filename, loglevel, message, date = None):
        self.filepath = self.FOLDER + "\\" + filename

        with open(self.filepath, "a") as f:
            if not date:
                f.write(f"[{loglevel}] {message}\n")
            else:
                f.write(f"[{loglevel} | {date}] {message}\n")