import pygame as pg;
from TetraMinos import Tetraminos;
from ColorDictionary import Colors;
import sys;


def create_grid(rows, cols):
    grid = [];
    for i in range(rows):
        new_line = []
        for j in range(cols):
            new_line.append(0);
        grid.append(new_line);

    return grid;


class GridColors:
    color_dict = {
        0: Colors.GREY,
        1: Colors.CYAN,
        2: Colors.BLUE,
        3: Colors.ORANGE,
        4: Colors.YELLOW,
        5: Colors.GREEN,
        6: Colors.PURPLE,
        7: Colors.RED
    }

    def get_color(grid_value):
        if 0 <= grid_value <= 7:
            return GridColors.color_dict[grid_value];
        else:
            return Colors.BLACK;


class GameParams:
    def __init__(self, display_size, grid_size):
        self.display_size = display_size;
        self.grid_size = grid_size;

    def get_display_size(self):
        return self.display_size;

    def get_grid_size(self):
        return self.grid_size;

    def get_square_size(self):
        return self.display_size / (self.grid_size + 1);

    def get_partition_size(self):
        return (self.display_size - self.grid_size * self.get_square_size()) / (self.grid_size - 1)


def draw_grid(grid, surface, game_params):
    """Draw grid defined by the 2D array. Values of the array elements indicate different colors present in the array"""
    # Set screen to black
    surface.fill(Colors.BLACK.value);

    grid_size = game_params.get_grid_size();
    square_size = game_params.get_square_size();
    partition_size = game_params.get_partition_size();

    # Draw grid
    for i in range(grid_size):
        for j in range(grid_size):
            xc = 0 + square_size * i + (i - 1) * partition_size;
            yc = 0 + square_size * j + (j - 1) * partition_size;

            grid_value = grid[i][j];
            color = GridColors.get_color(grid_value).value;
            pg.draw.rect(surface, color,
                         (xc, yc, game_params.get_square_size(), game_params.get_square_size()));


def draw_stone(grid, surface, game_params, tetramino, pos_x, pos_y):
    """Draws the tetramino in the grid. Draws grid followed by tetramino"""
    draw_grid(grid, surface, game_params);
    shape = tetramino.get_shape();

    for i in range(len(shape.get_rows())):
        for j in range(len(shape.get_cols())):
            array2d = shape.array2d
            pixel_value = array2d[i][j];
            pixel_color = GridColors.get_color(pixel_value).value;

            xi = pos_x + i;
            yi = pos_y + j;

            x = game_params.get_square_size() * xi + (xi - 1) * game_params.get_partition_size();
            y = game_params.get_square_size() * yi + (yi - 1) * game_params.get_partition_size();

            rect = (x, y, game_params.get_square_size(), game_params.get_square_size());
            pg.draw.rect(surface, pixel_color, rect);


def update_grid(grid, param, game_params, tetramino, pos_x, pos_y):
    """Updates the grid values. Everytime collision happens, we need to update the grid for next iteration"""
    shape = tetramino.get_shape();

    for i in range(len(shape.get_rows())):
        for j in range(len(shape.get_cols())):
            array2d = shape.array2d
            pixel_value = array2d[i][j];

            xi = int(pos_x + i);
            yi = int(pos_y + j);

            # print(str(pos_x) + " " + str(pos_y) + " " + str(xi) + " " + str(yi));
            if pixel_value != 0:
                grid[xi][yi] = int(pixel_value);

    clear_full_rows(grid);


def clear_full_rows(grid):
    """When any row is completely filled, clear it"""
    for i in range(len(grid)):
        row_full = True;
        for j in range(len(grid[0])):
            if grid[i][j] == 0:
                row_full = False;
        if row_full:
            for j in range(len(grid[0])):
                grid[i][j] = 0;


def is_collided(grid, tetramino, pos_x, pos_y):
    """Return True/False based on whether collision has happened"""
    shape = tetramino.get_shape();
    array2d = shape.array2d;

    for i in range(len(shape.get_rows())):
        for j in range(len(shape.get_cols())):
            pixel_value = array2d[i][j];

            xi = int(pos_x + i);
            yi = int(pos_y + j);

            # print(str(xi) + " " + str(yi));
            if grid[xi][yi] != 0:
                # print(str(xi) + " " + str(yi));
                return True;

            if yi == (len(grid[0]) - 1):
                # print(str(xi) + " " + str(yi));
                return True;

    return False;


def listen_for_event(grid, tetramino, start_x, start_y):
    """Event handler"""
    # Event handling
    for event in pg.event.get():
        if event.type == pg.QUIT:
            print("Quitting game...");
            pg.quit();
            sys.exit();
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                if start_x > 0:
                    start_x -= 1;
                return [start_x, start_y];
            if event.key == pg.K_RIGHT:
                if start_x + len(tetramino.get_shape().get_cols()) <= len(grid[0]):
                    start_x += 1;
                return [start_x, start_y];
            if event.key == pg.K_UP:
                tetramino.get_shape().matrix_transpose();
                return [start_x, start_y];
            if event.key == pg.K_DOWN:
                if not is_collided(grid, tetramino, start_x, start_y + 1):
                    start_y += 1;
                return [start_x, start_y];

    return [start_x, start_y];


def main():
    """Main method of the game"""
    # Define game parameters
    display_size = 420;
    grid_size = 20;
    game_params = GameParams(display_size, grid_size);

    # Initialize pygame parameters
    pg.init();
    screen = pg.display;
    screen.set_mode((display_size, display_size));
    screen.set_caption('Tetris');
    clock = pg.time.Clock();
    close = False;
    pg.event.set_blocked(pg.MOUSEMOTION);

    tetraminos = Tetraminos();
    grid = create_grid(grid_size, grid_size);

    while not close:
        # Generate Tetramino
        tetramino = tetraminos.generate_random_tetramino();

        speed = 1000;
        pg.time.delay(2 * speed);

        # Print Tetramino
        start_x = grid_size / 2;
        start_y = 0;
        collision = False;

        while not collision:
            collision = is_collided(grid, tetramino, start_x, start_y + 1);
            screen.update();
            pg.time.delay(int(speed * 0.5));

            start_x, start_y = listen_for_event(grid, tetramino, start_x, start_y);

            if collision:
                update_grid(grid, screen.get_surface(), game_params, tetramino, start_x, start_y + 1);
                break;
            else:
                draw_stone(grid, screen.get_surface(), game_params, tetramino, start_x, start_y + 1);

            start_y += 1;

        clock.tick(30);

    pg.quit();


# Main
main();
