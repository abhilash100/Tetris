from enum import Enum;
import random as rand;
import time;

from ColorDictionary import Colors


class Shape:
    def __init__(self, array2d):
        self.array2d = array2d;

    def print_shape(self):
        for i in range(len(self.get_rows())):
            print(str(self.array2d[i]));

    def get_rows(self):
        return self.array2d;

    def get_cols(self):
        return self.array2d[0];

    # Transpose of a matrix
    def matrix_transpose(self):
        transposed_array = [];
        for x in range(len(self.get_cols())):
            new_list = [];
            for y in range(len(self.get_rows())):
                new_list.append(self.array2d[y][x])
            transposed_array.append(new_list);

        self.array2d = transposed_array;


class TetraminoType(Enum):
    I = 1;
    O = 2;
    T = 3;
    S = 4;
    Z = 5;
    J = 6;
    L = 7;



class TetraminoShape:
    Shape_I = Shape(
        [[1, 1, 1, 1]]
    );

    Shape_O = Shape(
        [[2, 2],
         [2, 2]]
    );

    Shape_T = Shape([[3, 3, 3],
                     [0, 3, 0]]);

    Shape_S = Shape([[0, 4, 4],
                     [4, 4, 0]
                     ]);

    Shape_Z = Shape([[5, 5, 0],
                     [0, 5, 5]]);

    Shape_J = Shape([[0, 6],
                     [0, 6],
                     [6, 6]]);

    Shape_L = Shape([[7, 0],
                     [7, 0],
                     [7, 7]]);

    class Tetramino:
        def __init__(self, shape, type, color):
            self.shape = shape;
            self.type = type;
            self.color = color;


class Tetramino:
    # Immutable
    def __init__(self, shape, type, color):
        self.shape = shape;
        self.type = type;
        self.color = color;

    def get_shape(self):
        return self.shape;

    def get_type(self):
        return self.type;

    def get_color(self):
        return self.color;

    def rotate_clockwise(self):
        self.shape = self.get_shape().matrix_transpose();


class Tetraminos:
    tet_I = Tetramino(TetraminoShape.Shape_I, TetraminoType.I, Colors.CYAN);
    tet_O = Tetramino(TetraminoShape.Shape_O, TetraminoType.O, Colors.YELLOW);
    tet_T = Tetramino(TetraminoShape.Shape_T, TetraminoType.T, Colors.PURPLE);
    tet_S = Tetramino(TetraminoShape.Shape_S, TetraminoType.S, Colors.GREEN);
    tet_Z = Tetramino(TetraminoShape.Shape_Z, TetraminoType.Z, Colors.RED);
    tet_J = Tetramino(TetraminoShape.Shape_J, TetraminoType.J, Colors.BLUE);
    tet_L = Tetramino(TetraminoShape.Shape_L, TetraminoType.L, Colors.ORANGE);

    tetraminos = {
        'I': tet_I,
        'O': tet_O,
        'T': tet_T,
        'S': tet_S,
        'Z': tet_Z,
        'J': tet_J,
        'L': tet_L
    };

    def generate_random_tetramino(self):
        switcher = {
            1: self.tetraminos['I'],
            2: self.tetraminos['O'],
            3: self.tetraminos['T'],
            4: self.tetraminos['S'],
            5: self.tetraminos['Z'],
            6: self.tetraminos['J'],
            7: self.tetraminos['L']
        }

        num = rand.randint(1, 7);
        return switcher[num];


tetraminos = Tetraminos();
for i in range(20):
    shape = tetraminos.generate_random_tetramino().get_shape();
    #shape.print_shape();
