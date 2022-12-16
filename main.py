from coloring import GraphColoring

if __name__ == '__main__':
    app = GraphColoring(fileNameGraph='./resources/data.txt',
                        fileNameColors='./resources/vertexColor.txt')
    app.coloring()
