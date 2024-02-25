from PIL import Image, ImageDraw, ImageFont


class WordSearch():
    def __init__(self, board):
        self.height = len(board)
        self.width = len(board[0])
        self.board = board

    def result(self, state):
        row, col = state
        candidates = [
            ("down", (row + 1, col)),
            ("right", (row, col + 1)),
            ("left", (row, col - 1)),
            ("up", (row - 1, col))
        ]
        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width:
                result.append((action, (r, c)))
        return result

    def output_image(self, solution=None):
        cell_size = 50
        cell_border = 2
        img = Image.new(
            "RGBA",
            (self.width * cell_size, self.height * cell_size),
            "black"
        )
        draw = ImageDraw.Draw(img)
        solution = solution[1] if solution is not None else None
        for i, row in enumerate(self.board):
            for j, col in enumerate(row):
                if solution and (i, j) in solution:
                    fill = (255, 255, 0)
                else:
                    fill = (255, 255, 255)
                draw.rectangle(
                    ([(j * cell_size + cell_border, i * cell_size + cell_border),
                      ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                    fill=fill
                )
        font = ImageFont.truetype("Arial.ttf", size=25)
        for i, row in enumerate(self.board):
            for j, col in enumerate(row):
                draw.text((j * cell_size + 10, i * cell_size + 10), self.board[i][j], (20, 20, 20), font=font)
        img.show()


class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier.pop()
            return node


class Solution:
    def __init__(self, problem):
        self.problem = problem

    def exist(self, word):
        for i in range(self.problem.height):
            for j in range(self.problem.width):
                if self.problem.board[i][j] == word[0]:
                    initial_state = (i, j)
                    result = self.graph_search(initial_state, word)
                    if result is not None:
                        return result
        return None

    def graph_search(self, initial_state, word):
        frontier = StackFrontier()
        explored = set()

        initial_node = Node(initial_state, None, None)
        frontier.add(initial_node)

        while not frontier.empty():
            node = frontier.remove()
            state = node.state

            if node.action is not None:
                action_sequence = [node.action]
                path = [(state[0], state[1])]
                parent = node.parent
                while parent is not None:
                    action_sequence.append(parent.action)
                    path.append((parent.state[0], parent.state[1]))
                    parent = parent.parent

                action_sequence.reverse()
                path.reverse()
                return action_sequence, path

            explored.add(state)

            for action, neighbor_state in self.problem.result(state):
                if neighbor_state not in explored and not frontier.contains_state(neighbor_state):
                    new_node = Node(neighbor_state, node, action)
                    frontier.add(new_node)

        return None


board = [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]]
wordsearch = WordSearch(board)
word = "ABCCED"
wordsearch.output_image()

s = Solution(wordsearch)
sol = s.exist(word)
wordsearch.output_image(sol)
