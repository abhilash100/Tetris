import pygame as pg;
from TetraMinos import Tetraminos;
from ColorDictionary import Colors;
import sys;

game_settings = {
    'rows': 10,
    'cols': 10,
    'square_size': 20
}


class TetrisApp:
    def __init__(self):
        self.rows = game_settings['rows'];
        self.cols = game_settings['cols'];
        self.square_size = game_settings['square_size'];
        self.partition_size = int(game_settings['square_size'] / 10);
        self.grid = self.create_grid();
        self.initiate_pygame_params();
        self.tetraminos = Tetraminos();
        self.create_new_tetramino();
        self.pause = False;

    def initiate_pygame_params(self):
        pg.init();
        self.screen = pg.display;
        self.screen.set_mode(((self.rows * self.square_size) + (self.rows - 1) * self.partition_size,
                              self.cols * self.square_size + (self.cols - 1) * self.partition_size));
        self.screen.set_caption('Tetris');
        #pg.time.set_timer(pg.USEREVENT + 1, 750);
        clock = pg.time.Clock();
        clock.tick(30);
        pg.event.set_blocked(pg.MOUSEMOTION);

    def create_grid(self):
        grid = [];
        for i in range(self.rows):
            new_line = []
            for j in range(self.cols):
                new_line.append(0);
            grid.append(new_line);

        return grid;

    def create_new_tetramino(self):
        self.curr_tetramino = self.tetraminos.generate_random_tetramino();
        self.start_x = self.rows / 2;
        self.start_y = 0;

    def handle_event(self, event):
        """Event handler"""
        # Event handling
        shape = self.curr_tetramino.get_shape();

        if event.type == pg.QUIT:
            print("Quitting game...");
            pg.quit();
            sys.exit();
        if event.type == pg.KEYDOWN:
            print(event);
            if event.key == pg.K_LEFT:
                collision = self.is_collided(False);
                if self.start_x > 0 and not collision:
                    self.start_x -= 1;
            if event.key == pg.K_RIGHT:
                collision = self.is_collided(False);
                if self.start_x + len(shape.get_rows()) < self.cols and not collision:
                    print("Listen for event : " + str(self.start_x) + " " + str(self.start_y))
                    self.start_x += 1;
            if event.key == pg.K_UP:
                self.curr_tetramino.rotate_clockwise();
            if event.key == pg.K_DOWN:
                if not self.is_collided(True):
                    self.start_y += 1;
            if event.key == pg.K_p:
                print("Pausing game...");
                self.pause = True;
                self.pause_game();

    def draw_grid(self):
        """Draw grid defined by the 2D array. Values of the array elements indicate different colors present in the
        array """
        # Set screen to black
        self.screen.get_surface().fill(Colors.BLACK.value);

        square_size = self.square_size;
        partition_size = self.partition_size;

        # Draw grid
        for i in range(self.rows):
            for j in range(self.cols):
                xc = 0 if i == 0 else (square_size * i + i * partition_size);
                yc = 0 if j == 0 else (square_size * j + j * partition_size);

                grid_value = self.grid[i][j];
                color = GridColors.get_color(grid_value).value;
                pg.draw.rect(self.screen.get_surface(), color,
                             (xc, yc, self.square_size, self.square_size));

    def is_collided(self, lookAhead):
        """Return True/False based on whether collision has happened"""
        shape = self.curr_tetramino.get_shape();
        array2d = shape.array2d;

        for i in range(len(shape.get_rows())):
            for j in range(len(shape.get_cols())):
                pixel_value = array2d[i][j];

                xi = int(self.start_x + i);
                yi = int(self.start_y + j);

                # print("Is collided : " + str(xi) + " " + str(yi));
                # End of grid
                if yi == self.rows - 1:
                    print("Collided at 1(" + str(xi) + "," + str(yi) + ")");
                    return True;

                if lookAhead:
                    yi += 1;
                if self.grid[xi][yi] != 0 and pixel_value != 0:
                    # print(str(xi) + " " + str(yi));
                    print("Collided at 2(" + str(xi) + "," + str(yi) + ")");
                    print(str(self.grid[xi][yi]) + " " + str(pixel_value));
                    return True;

        return False;

    def draw_stone(self):
        """Draws the tetramino in the grid. Draws grid followed by tetramino"""
        self.draw_grid();
        shape = self.curr_tetramino.get_shape();

        for i in range(len(shape.get_rows())):
            for j in range(len(shape.get_cols())):
                array2d = shape.array2d
                pixel_value = array2d[i][j];
                pixel_color = GridColors.get_color(pixel_value).value;

                xi = self.start_x + i;
                yi = self.start_y + j;

                x = 0 if xi == 0 else self.square_size * xi + xi * self.partition_size;
                y = 0 if yi == 0 else self.square_size * yi + yi * self.partition_size;

                rect = (x, y, self.square_size, self.square_size);
                pg.draw.rect(self.screen.get_surface(), pixel_color, rect);

    def update_grid(self):
        """Updates the grid values. Everytime collision happens, we need to update the grid for next iteration"""
        shape = self.curr_tetramino.get_shape();

        for i in range(len(shape.get_rows())):
            for j in range(len(shape.get_cols())):
                array2d = shape.array2d
                pixel_value = array2d[i][j];

                xi = int(self.start_x + i);
                yi = int(self.start_y + j);

                print("Update grid : " + str(xi) + " " + str(yi));
                if pixel_value != 0:
                    self.grid[xi][yi] = int(pixel_value);

        ##clear_full_rows(grid);

    def pause_game(self):
        if not self.pause:
            return;
        while 1:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    print("Key pressed. Resuming game...");
                    self.pause = False;
                    return;

    def run(self):
        close = False;
        pg.event.wait();

        while not close:
            self.create_new_tetramino();
            collision = self.is_collided(True);

            if collision:
                # self.pause = True;
                # self.pause_game();
                print("Game over.... You lost");
                pg.quit();
                sys.exit(1);

            while not collision:
                pg.time.delay(1000);
                print(str(collision) + " " + str(self.start_y))

                collision = self.is_collided(True);
                self.screen.update();

                if collision:
                    self.update_grid();
                else:
                    self.draw_stone();

            for event in pg.event.get():
                self.handle_event(event);

                self.start_y += 1;


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


def game_ended(grid):
    top_row = grid[0];
    print(top_row);
    for row_value in range(len(top_row)):
        print(row_value);
        if row_value != 0:
            return True;
    return False;


def main():
    # Main method of the game
    print(game_settings)
    # Define game parameters
    app = TetrisApp();
    app.run();

# Main
main();
