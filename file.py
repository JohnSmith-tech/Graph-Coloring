class FileReader:
    def __init__(self, filename) -> None:
        self._filename: str = filename
        self._data = None

    def read_file(self):
        with open(self._filename, 'r', encoding='utf-8') as file:
            self._data = file.read()


class ReaderGraph(FileReader):
    def __init__(self, filename) -> None:
        super().__init__(filename)
        self.read_file()
        self.data = self.__create_array_of_string()
        self.v = int(self.data[0])
        self.e = int(self.data[1])
        self.edges = self.__get_graph_edges()

    def __create_array_of_string(self) -> str:
        return self._data.replace('\n', ' ').split(' ')

    def __get_graph_edges(self) -> list:
        edges = []
        for i in range(2, len(self.data)-2, 2):
            edges.append([self.data[i], self.data[i+1]])
        return edges


class ReaderColor(FileReader):
    def __init__(self, filename) -> None:
        super().__init__(filename)
        self._colors = None

    def read_file(self) -> None:
        colors = {}
        with open(self._filename, 'r', encoding='utf-8') as file:
            for line in file:
                key, value = line.strip().split(' ')
                colors[key] = value
        self._colors = colors
