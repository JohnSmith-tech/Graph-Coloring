from coloring import GraphColoring

if __name__ == '__main__':
    correct = "Раскраска правильная"
    incorrect = "Алиса пыталась обмануть"

    print('Граф №1: ', end='')
    true_graph_coloring = GraphColoring(fileNameGraph='./resources/GraphTrue.txt',
                                        fileNameColors='./resources/TrueColor.txt')

    if true_graph_coloring.coloring(alpha=5) is True:
        print(correct)
    else:
        print(incorrect)

    print('Граф №2: ', end='')

    false_graph_coloring = GraphColoring(fileNameGraph='./resources/GraphFalse.txt',
                                         fileNameColors='./resources/FalseColor.txt')

    if false_graph_coloring.coloring(alpha=5) is True:
        print(correct)
    else:
        print(incorrect)
