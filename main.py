import pygame
import pygame.image
import json
import argparse

KEY_FIGURES = 'Figures';
KEY_SCREEN = 'Screen';
KEY_PALETTE = 'Palette';

KEY_SCREEN_WIDTH = 'width';
KEY_SCREEN_HEIGHT = 'height';
KEY_SCREEN_BG_COL = 'bg_color';
KEY_SCREEN_FG_COL = 'fg_color';

FIGURE_TYPE = 'type';
FIGURE_CIRCLE = 'circle';
FIGURE_POINT = 'point';
FIGURE_POLYGON = 'polygon';
FIGURE_RECTANGLE = 'rectangle';
FIGURE_SQUARE = 'square';

def color_to_rgba(color):
    try:
        if color[0] == '#':
            return pygame.Color(color);
        elif color[0] == '(':
            rgba = [int(val) for val in color.strip(' ')[1:-1].split(',')];
            if len(rgba) < 4: rgba.append(255);
            return pygame.Color(rgba[0], rgba[1], rgba[2], rgba[3]);
        else:
            raise Exception('Error: Color ' + str.upper(color) + ' is not defined or has invalid format');

    except ValueError:
        raise  Exception('Error: Invalid color name - ' + color);

    except Exception as e:
        raise Exception(e.args[0]);

if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser();
        parser.add_argument('file', help='Path to the JSON file', type=str);
        parser.add_argument('-o', '--output', help='Path to the PNG output file', type=str);

        args = parser.parse_args();

        INPUT_FILE = args.file;
        OUTPUT_FILE = args.output;

        with open(INPUT_FILE, 'r') as file:
            content = file.read();

        # JSON to dict
        data = json.loads(content);

        figures = data.get(KEY_FIGURES);
        screen_setup = data.get(KEY_SCREEN);
        palette = data.get(KEY_PALETTE);

        [palette.update({figure.get('color'): figure.get('color')}) for figure in figures if figure.get('color') is not None and palette.get(figure.get('color')) is None];
        [palette.update({key: color_to_rgba(palette.get(key))}) for key in palette.keys()];

        SCREEN_WIDTH = screen_setup.get(KEY_SCREEN_WIDTH);
        SCREEN_HEIGHT = screen_setup.get(KEY_SCREEN_HEIGHT);
        SCREEN_BG = palette.get(screen_setup.get(KEY_SCREEN_BG_COL));
        SCREEN_FG = palette.get(screen_setup.get(KEY_SCREEN_FG_COL));

        if SCREEN_BG is None or SCREEN_FG is None:
            raise Exception('Error: Both BG and FG color must be provided in Screen section and be defined in Palette section of JSON file..');

        pygame.init();

        screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT]);
        screen.fill(SCREEN_BG);

        for figure in figures:
            figure_type = figure.get(FIGURE_TYPE);
            try:
                if figure_type == FIGURE_CIRCLE:
                    pygame.draw.circle(screen, palette.get(figure.get('color'), SCREEN_FG), [figure.get('x'), figure.get('y')], figure.get('radius'));
                elif figure_type == FIGURE_POINT:
                    screen.set_at([figure.get('x'), figure.get('y')], palette.get(figure.get('color'), SCREEN_FG));
                elif figure_type == FIGURE_POLYGON:
                    pygame.draw.polygon(screen, palette.get(figure.get('color'), SCREEN_FG), figure.get('points'));
                elif figure_type == FIGURE_RECTANGLE:
                    width = figure.get('width');
                    height = figure.get('height');
                    center = [figure.get('x') - width >> 2, figure.get('y') - height // 2];
                    pygame.draw.rect(screen, palette.get(figure.get('color'), SCREEN_FG), center + [width] + [height]);
                elif figure_type == FIGURE_SQUARE:
                    side_len = figure.get('size');
                    center = [figure.get('x') - int(side_len // 2), figure.get('y') - int(side_len // 2)];
                    pygame.draw.rect(screen, palette.get(figure.get('color'), SCREEN_FG), center + [side_len] + [side_len]);
                else:
                    raise Exception('Error: Invalid figure type - ' + figure_type);

            except TypeError:
                raise Exception("Error: Invalid figure attributes " + str(figure));

            except Exception as e:
                raise Exception(e.args[0]);

        pygame.display.flip();

        if OUTPUT_FILE is not None:
            pygame.image.save(screen, OUTPUT_FILE + '.png');

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0);

    except FileNotFoundError:
        print('Error: Invalid path to the JSON file');
        exit(1);

    except AttributeError:
        print('Error: Missing base attributes such as [Figures, Screen, Palette]');
        exit(1);

    except Exception as e:
        print(e.args[0]);
        exit(1);