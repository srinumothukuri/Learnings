import shelve


class ShelveReadWriter:
    def __init__(self, data, file_name):
        self.data = data
        self.file_name = file_name

    def write_data(self):
        with shelve.open(self.file_name) as shelve_writer:
            try:
                for key, value in self.data:
                    shelve_writer[key] = value
            except:
                print("Error with unboxing data")

    @staticmethod
    def read_data(file_name):
        return shelve.open(file_name)
