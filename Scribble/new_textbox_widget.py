import time
import pygame
import pyperclip
from typing import Iterable, Tuple
from functools import lru_cache

import pygame_widgets
from pygame_widgets.textbox import TextBox
from pygame_widgets.mouse import Mouse, MouseState


# TODO need to add scrolling through the text


class MyTextBox(TextBox):
    def __init__(
        self,
        win: pygame.Surface,
        x: int,
        y: int,
        width: int,
        height: int,
        isSubWidget=False,
        **kwargs
    ):
        super().__init__(win, x, y, width, height, isSubWidget, **kwargs)

        self.NEWLINE_CHAR = "\n"
        self.TAB_SPACES = 4

        self.font = kwargs.get(
            "font", pygame.font.SysFont("Consolas", self.fontSize)
        )  # Using monospaced fonts

        # self.highlighted_textColour = kwargs.get('highlighted_textColour', (33, 66, 131))  # dark theme
        self.highlighted_textColour = kwargs.get(
            "highlighted_textColour", (166, 210, 255)
        )  # light theme

        self.textOffsetTop = self.textOffsetBottom
        self.text = [[]]  # Multi-line text

        self.oldCursorPosition = self.cursorPosition  # Track old cursor position
        self.selected_line = 0  # Current line being edited
        self.highlighted_text = []  # Highlighted text details

        # Highlight ranges
        self.highlight_in_line_start = 0
        self.highlight_in_line_end = 0
        self.highlight_line_start = 0
        self.highlight_line_end = 0

        self.first_visible_line_index = 0
        self.max_visible_lines = (
            self._height - self.borderThickness * 2 - self.textOffsetTop
        ) // self.fontSize
        self.max_line_length = (
            self._width - self.borderThickness * 2 - self.radius * 2
        ) // self.font.size(" ")[0]

    def listen(self, events: list[pygame.event.Event]) -> None:
        if self._hidden or self._disabled:
            return

        if self.keyDown:
            self.updateRepeatKey()

        mouseState, (x, y) = Mouse.getMouseState(), Mouse.getMousePos()

        if mouseState in {MouseState.CLICK, MouseState.DRAG}:
            if self.contains(x, y):
                self._update_cursor_position_by_mouse(mouseState, x, y)
            elif mouseState == MouseState.CLICK:
                self.selected = self.showCursor = False

        if self.selected:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    self._handle_keydown(event)
                elif event.type == pygame.KEYUP:
                    self._reset_key_state()
                elif event.type == pygame.MOUSEWHEEL:
                    pass

    def _update_cursor_position_by_mouse(self, state, x, y):
        if state == MouseState.CLICK:
            self.selected = True
            self.showCursor = True
            self.cursorTime = time.time()
            self._set_highlight_start(x, y)
        elif state == MouseState.DRAG:
            self._set_highlight_end(x, y)
            self._highlight_text()

    def _set_highlight_start(self, x, y):
        self._set_cursor_position_after_mouse_event(x)
        self.highlight_in_line_start = self.highlight_in_line_end = self.cursorPosition

        self._set_selected_line_after_mouse_event(y)
        self.highlight_line_start = self.highlight_line_end = (
            self.selected_line - self.first_visible_line_index
        )

    def _set_highlight_end(self, x, y):
        self._set_cursor_position_after_mouse_event(x)
        self.highlight_in_line_end = self.cursorPosition

        self._set_selected_line_after_mouse_event(y)
        self.highlight_line_end = self.selected_line - self.first_visible_line_index

    def _handle_keydown(self, event):
        self.showCursor = True
        self.keyDown = True
        self.repeatKey = event
        self.repeatTime = time.time()

        key_actions = {
            pygame.K_BACKSPACE: self._handle_backspace,
            pygame.K_DELETE: self._handle_delete,
            pygame.K_RETURN: self._handle_return,
            pygame.K_RIGHT: lambda: self._move_cursor(1),
            pygame.K_LEFT: lambda: self._move_cursor(-1),
            pygame.K_UP: lambda: self._move_cursor_vertically(-1),
            pygame.K_DOWN: lambda: self._move_cursor_vertically(1),
            pygame.K_HOME: lambda: self._set_cursor_position(0),
            pygame.K_END: lambda: self._set_cursor_position(
                len(self.text[self.selected_line])
            ),
            pygame.K_ESCAPE: self._handle_escape,
        }

        if event.key in key_actions:
            key_actions[event.key]()
        else:
            self._handle_character_input(event)

    def _handle_backspace(self):
        if not self._is_empty_2D_sequence(self.highlighted_text):
            self._erase_highlighted_text()
            self.cursorPosition += 1
            self._shift_lines()
            self.onTextChanged(*self.onTextChangedParams)
        elif self.cursorPosition > 0:
            del self.text[self.selected_line][self.cursorPosition - 1]
            self._shift_lines()
            self.onTextChanged(*self.onTextChangedParams)
        elif self.selected_line > 0:
            self._merge_lines()
            self.onTextChanged(*self.onTextChangedParams)

        self.cursorPosition = max(0, self.cursorPosition - 1)

    def _handle_delete(self):
        if not self._is_empty_2D_sequence(self.highlighted_text):
            self._erase_highlighted_text()

        elif self.cursorPosition < len(self.text[self.selected_line]):
            del self.text[self.selected_line][self.cursorPosition]
            self._shift_lines()

        elif self.cursorPosition >= len(
            self.text[self.selected_line]
        ) != 0 and not self._is_special_char(
            self.text[self.selected_line][self.cursorPosition - 1]
        ):
            self._shift_lines()

        self.onTextChanged(*self.onTextChangedParams)

    def _handle_return(self):
        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
            self._insert_newline()
        else:
            self.onSubmit(*self.onSubmitParams)
        self._reset_highlight()

    def _move_cursor(self, direction):
        self.cursorPosition = max(
            0, min(self.cursorPosition + direction, len(self.text[self.selected_line]))
        )
        self._skip_special_char()
        self.oldCursorPosition = self.cursorPosition
        self._reset_highlight()

    def _move_cursor_vertically(self, direction):
        self.selected_line = max(
            0, min(len(self.text) - 1, self.selected_line + direction)
        )
        self.cursorPosition = min(
            self.oldCursorPosition, len(self.text[self.selected_line])
        )

        if self.selected_line < self.first_visible_line_index:
            self.first_visible_line_index -= 1
        elif (
            self.selected_line >= self.first_visible_line_index + self.max_visible_lines
        ):
            self.first_visible_line_index += 1

        self._skip_special_char()
        self._reset_highlight()

    def _set_cursor_position(self, position):
        self.cursorPosition = self.oldCursorPosition = position
        self._reset_highlight()

    def _handle_escape(self):
        if not self.escape:
            self.selected = False
            self.showCursor = False
            self.escape = True
            self.repeatKey = self.keyDown = None
            self.firstRepeat = True
            self._reset_highlight()

    def _handle_character_input(self, event):
        char = event.unicode
        if len(char) > 0:
            if not self._is_special_char(char):  # NOT Spec chars
                if not self._is_empty_2D_sequence(self.highlighted_text):
                    self._erase_highlighted_text()
                self._add_text(list(char))
            else:
                self._handle_special_char(event)

    def _reset_key_state(self):
        self.repeatKey = None
        self.keyDown = None
        self.firstRepeat = True
        self.escape = False

    def _merge_lines(self):
        if len(self.text[self.selected_line]) == 0 or self.text[self.selected_line] == [
            self.NEWLINE_CHAR
        ]:
            del self.text[self.selected_line]

        self.selected_line -= 1
        self.cursorPosition = len(self.text[self.selected_line])

        self._erase_special_char()
        self._shift_lines()
        self.cursorPosition += 1

        if self.selected_line < self.first_visible_line_index:
            self.first_visible_line_index -= 1

    def _insert_newline(self):
        new_line = self.text[self.selected_line][self.cursorPosition :]
        self.text[self.selected_line] = self.text[self.selected_line][
            : self.cursorPosition
        ]
        self.text[self.selected_line].append("\n")
        self.text.insert(self.selected_line + 1, new_line)
        self.selected_line += 1
        self.cursorPosition = 0
        self.onTextChanged(*self.onTextChangedParams)

    def _scroll_up(self):
        self.first_visible_line_index = max(0, self.first_visible_line_index - 1)

    def _scroll_down(self):
        max_first_line = max(0, len(self.text) - self.max_visible_lines)
        self.first_visible_line_index = min(
            max_first_line, self.first_visible_line_index + 1
        )

    @lru_cache(maxsize=1024)
    def _get_char_surface(self, char: str, color: Tuple[int, int, int]):
        return self.font.render(char, True, color)

    def _handle_special_char(self, event: pygame.event.Event) -> None:
        char_ord = ord(event.unicode)
        if char_ord == 1:  # Ctrl + A
            self.selected_line = len(self.text) - 1
            self.cursorPosition = len(self.text[self.selected_line])

            self.highlight_in_line_start = 0
            self.highlight_in_line_end = len(self.text[self.selected_line])

            self.highlight_line_start = 0
            self.highlight_line_end = len(self.text) - 1

            self._highlight_text()

        elif char_ord == 3:  # Ctrl + C
            if not self._is_empty_2D_sequence(self.highlighted_text):
                self._copy_highlighted_text()

        elif char_ord == 22:  # Ctrl + V
            self.keyDown = True
            self.repeatKey = event
            self.repeatTime = time.time()
            text = list(pyperclip.paste().replace("\t", "" * self.TAB_SPACES))
            if not self._is_empty_2D_sequence(self.highlighted_text):
                self._erase_highlighted_text()
            self._add_text(text)

        elif char_ord == 24:  # Ctrl + X
            if not self._is_empty_2D_sequence(self.highlighted_text):
                self.keyDown = True
                self.repeatKey = event
                self.repeatTime = time.time()
                self._copy_highlighted_text()
                self._erase_highlighted_text()

    def _draw_border(self):
        border_rects = [
            (
                self._x + self.radius,
                self._y,
                self._width - self.radius * 2,
                self._height,
            ),
            (
                self._x,
                self._y + self.radius,
                self._width,
                self._height - self.radius * 2,
            ),
        ]

        border_circles = [
            (self._x + self.radius, self._y + self.radius),
            (self._x + self.radius, self._y + self._height - self.radius),
            (self._x + self._width - self.radius, self._y + self.radius),
            (self._x + self._width - self.radius, self._y + self._height - self.radius),
        ]

        for rect in border_rects:
            pygame.draw.rect(self.win, self.borderColour, rect)

        for circle in border_circles:
            pygame.draw.circle(self.win, self.borderColour, circle, self.radius)

    def _draw_background(self):
        background_rects = [
            (
                self._x + self.borderThickness + self.radius,
                self._y + self.borderThickness,
                self._width - 2 * (self.borderThickness + self.radius),
                self._height - 2 * self.borderThickness,
            ),
            (
                self._x + self.borderThickness,
                self._y + self.borderThickness + self.radius,
                self._width - 2 * self.borderThickness,
                self._height - 2 * (self.borderThickness + self.radius),
            ),
        ]

        background_circles = [
            (
                self._x + self.radius + self.borderThickness,
                self._y + self.radius + self.borderThickness,
            ),
            (
                self._x + self.radius + self.borderThickness,
                self._y + self._height - self.radius - self.borderThickness,
            ),
            (
                self._x + self._width - self.radius - self.borderThickness,
                self._y + self.radius + self.borderThickness,
            ),
            (
                self._x + self._width - self.radius - self.borderThickness,
                self._y + self._height - self.radius - self.borderThickness,
            ),
        ]

        for rect in background_rects:
            pygame.draw.rect(self.win, self.colour, rect)

        for circle in background_circles:
            pygame.draw.circle(self.win, self.colour, circle, self.radius)

    def _draw_highlight(self):
        line_start, line_end = self._get_valid_highlight_line_indexes()
        inline_start, inline_end = self._get_valid_highlight_in_line_indexes()

        if self.highlight_line_start < self.highlight_line_end:
            inline_start, inline_end = (
                self.highlight_in_line_start,
                self.highlight_in_line_end,
            )

        if line_start == line_end:
            highlighted_rects = self._get_highlighted_rect(
                line_start, inline_start, inline_end
            )
        else:
            if line_start != self.highlight_line_start:
                inline_start, inline_end = (
                    self.highlight_in_line_end,
                    self.highlight_in_line_start,
                )

            highlighted_rects = self._get_highlighted_rect(
                line_start, inline_start, len(self.text[line_start])
            )
            for line in range(line_start + 1, line_end):
                highlighted_rects += self._get_highlighted_rect(
                    line, 0, len(self.text[line])
                )
            highlighted_rects += self._get_highlighted_rect(line_end, 0, inline_end)

        for rect in highlighted_rects:
            pygame.draw.rect(self.win, self.highlighted_textColour, rect)

    def _draw_cursor(self):
        if self.showCursor:
            try:
                x = self._get_line_x(self.text[self.selected_line])
                y_base = (
                    self._y
                    + self.textOffsetTop
                    + self.fontSize
                    * (self.selected_line - self.first_visible_line_index)
                )
                pygame.draw.line(
                    self.win,
                    self.cursorColour,
                    (x[self.cursorPosition], y_base),
                    (x[self.cursorPosition], y_base + self.fontSize),
                    width=2,
                )
            except IndexError:
                self.cursorPosition -= 1

    def _draw_text(
        self, string: str | list, color: tuple[int, int, int] | str, line_index: int
    ) -> None:
        x = self._get_line_x(string)

        for char_index in range(len(string)):
            char = string[char_index]

            if self._is_special_char(char):
                continue

            text = self._get_char_surface(char, color)
            text_rect = text.get_rect(
                bottomleft=(
                    x[char_index],
                    self._y
                    + self.textOffsetTop
                    + self.fontSize
                    + self.fontSize * line_index,
                )
            )
            self.win.blit(text, text_rect)

    def draw(self) -> None:
        """Display to surface"""
        if self._hidden:
            return

        if self.selected:
            self.updateCursor()

        self._draw_border()
        self._draw_background()
        self._draw_highlight()

        # Display text or placeholder text
        if self.text != [[]]:

            first_line = self.first_visible_line_index
            last_line = min(
                self.first_visible_line_index + self.max_visible_lines, len(self.text)
            )

            for line_index, line in enumerate(self.text[first_line:last_line]):
                self._draw_text(line, self.textColour, line_index)

        else:
            self._draw_text(
                self.placeholderText, self.placeholderTextColour, self.selected_line
            )

        self._draw_cursor()

    def setText(self, text: str) -> None:
        self.text = [[]]
        self.selected_line = 0
        self.cursorPosition = self.oldCursorPosition = 0
        self._add_text(list(text))

    def getText(self) -> str:
        text = ""
        for line in self.text:
            text += "".join(line)
        return text

    def _add_text(self, text: list[str]):
        for char in text:
            self._insert_char(self.selected_line, self.cursorPosition, char)

            if char == self.NEWLINE_CHAR:  # \n
                self.text.append([])
                self.selected_line += 1
                self.cursorPosition = 0
                continue

            for line_index in range(self.selected_line, len(self.text)):
                if len(self.text[line_index][:-1]) >= self.max_line_length:
                    if (
                        line_index + 1
                        >= self.first_visible_line_index + self.max_visible_lines
                    ):
                        self.first_visible_line_index += 1

                    last_char = self.text[line_index][-1]
                    del self.text[line_index][-1]

                    if last_char == self.NEWLINE_CHAR:
                        self.selected_line += 1
                        self.cursorPosition = 0
                        self.text.insert(self.selected_line, [])
                        self._insert_char(line_index + 1, 0, last_char)
                        last_char = self.text[line_index][-2]

                    self._insert_char(line_index + 1, 0, last_char)

                    if self.cursorPosition >= len(self.text[line_index]) - 1:
                        self.selected_line += 1
                        self.cursorPosition = 0

            if not self._is_special_char(char):
                self.cursorPosition += 1
                self.onTextChanged(*self.onTextChangedParams)

        self.oldCursorPosition = self.cursorPosition

    def _erase_highlighted_text(self):
        line_start, line_end = self._get_valid_highlight_line_indexes()
        inline_start, inline_end = self._get_valid_highlight_in_line_indexes()

        if line_start == line_end:  # Simple erase in line
            del self.text[self.selected_line][inline_start:inline_end]
        else:
            if line_start == self.highlight_line_start:
                inline_start, inline_end = (
                    self.highlight_in_line_start,
                    self.highlight_in_line_end,
                )
            else:
                inline_start, inline_end = (
                    self.highlight_in_line_end,
                    self.highlight_in_line_start,
                )

            del self.text[line_start][inline_start:]
            del self.text[line_end][:inline_end]
            del self.text[line_start + 1 : line_end]

            try:
                if not self.text[line_start]:
                    del self.text[line_start]
            except IndexError:
                pass

            try:
                if not self.text[line_end]:
                    del self.text[line_end]
            except IndexError:
                pass

        self.selected_line = self.first_visible_line_index + line_start
        self.cursorPosition = inline_start

        self._reset_highlight()

    def _highlight_text(self):
        line_start, line_end = self._get_valid_highlight_line_indexes()
        inline_start, inline_end = self._get_valid_highlight_in_line_indexes()

        if line_start == line_end:
            self.highlighted_text = [self.text[line_start][inline_start:inline_end]]
        else:
            if line_start == self.highlight_line_start:
                inline_start, inline_end = (
                    self.highlight_in_line_start,
                    self.highlight_in_line_end,
                )
            else:
                inline_start, inline_end = (
                    self.highlight_in_line_end,
                    self.highlight_in_line_start,
                )

            self.highlighted_text = [self.text[line_start][inline_start:]]
            self.highlighted_text += self.text[line_start + 1 : line_end]
            self.highlighted_text += [self.text[line_end][:inline_end]]

    def _reset_highlight(self) -> None:
        self.highlight_in_line_start = self.highlight_in_line_end = 0
        self.highlight_line_start = self.highlight_line_end = 0
        self.highlighted_text = []

    def _shift_lines(self) -> None:
        shift = 0
        for line in range(
            self.selected_line - self.first_visible_line_index, len(self.text) - 1
        ):
            if len(self.text[line - shift]) == 0:
                del self.text[line - shift]
                shift += 1
                continue
            if self.text[line - shift][-1] != self.NEWLINE_CHAR:
                while (
                    len(self.text[line - shift]) < self.max_line_length
                    and len(self.text[line + 1 - shift]) > 0
                ):
                    self.text[line - shift].append(self.text[line + 1 - shift][0])
                    del self.text[line + 1 - shift][0]

    def _insert_char(self, line_index: int, inline_index: int, char: str) -> None:
        try:
            self.text[line_index].insert(inline_index, char)
        except IndexError:
            self.text.append([char])

    def _erase_special_char(self):
        if self.text[self.selected_line]:
            while self.cursorPosition > 0 and self._is_special_char(
                self.text[self.selected_line][self.cursorPosition - 1]
            ):
                del self.text[self.selected_line][self.cursorPosition - 1]
                self.cursorPosition -= 1

    def _skip_special_char(self):
        if self.text[self.selected_line]:
            while self.cursorPosition > 0 and self._is_special_char(
                self.text[self.selected_line][self.cursorPosition - 1]
            ):
                self.cursorPosition = max(0, self.cursorPosition - 1)

    def _get_line_x(self, line: list[str]) -> list[float]:
        x = [self._x + self.textOffsetLeft]

        for char_index in range(len(line)):
            char = line[char_index]

            if self._is_special_char(char):
                continue

            text_width = self.font.size(line[char_index])[0]
            x.append(x[-1] + text_width)
        return x

    def _get_highlighted_rect(
        self, line_index: int, inline_start: int, inline_end: int
    ) -> list[tuple[float, float, float, float]]:
        x = self._get_line_x(self.text[line_index])

        highlighted_rects = []
        for char_index in range(len(self.text[line_index])):
            char = self.text[line_index][char_index]

            if self._is_special_char(char):
                continue

            text_width = self.font.size(char)[0]

            if inline_start <= char_index < inline_end:
                highlighted_rects.append(
                    (
                        x[char_index],
                        self._y + self.textOffsetTop + self.fontSize * line_index,
                        text_width,
                        self.fontSize,
                    )
                )

        return highlighted_rects

    def _max_width_reached(self, line: list[str]) -> bool:
        x = self._get_line_x(line)
        return (
            x[-1] > self._x + self._width - self.textOffsetRight - self.textOffsetLeft
        )

    def _set_cursor_position_after_mouse_event(self, x: int) -> None:
        coord = self._get_line_x(self.text[self.selected_line])

        for char_index in range(len(self.text[self.selected_line]) - 1):
            char1 = self.text[self.selected_line][char_index]
            char2 = self.text[self.selected_line][char_index + 1]

            if any(char for char in (char1, char2) if self._is_special_char(char)):
                continue

            char_width1 = self.font.size(char1)[0]
            char_width2 = self.font.size(char2)[0]

            x1 = char_width1 + coord[char_index]
            x2 = char_width2 + x1

            if x1 - char_width1 / 2 <= x <= x2 + char_width2 / 2:
                self.cursorPosition = char_index + 1

        if self.text[self.selected_line]:
            if x < coord[0] + self.font.size(self.text[self.selected_line][0])[0] / 2:
                self.cursorPosition = 0
            elif (
                x > coord[-1] - self.font.size(self.text[self.selected_line][-1])[0] / 2
            ):
                self.cursorPosition = len(self.text[self.selected_line])

    def _set_selected_line_after_mouse_event(self, y: int) -> None:
        coord = [self._y + self.textOffsetTop]

        for line_index in range(len(self.text)):
            if coord[-1] <= y <= coord[-1] + self.fontSize:
                self.selected_line = self.first_visible_line_index + line_index
            coord.append(coord[-1] + self.fontSize)

        if y < coord[0] + self.fontSize / 2:
            self.selected_line = self.first_visible_line_index
        elif y > coord[-1] + self.fontSize / 2:
            self.selected_line = len(self.text) - 1

    def _get_valid_highlight_line_indexes(self) -> tuple[int, int]:
        start_index = min(self.highlight_line_start, self.highlight_line_end)
        end_index = max(self.highlight_line_start, self.highlight_line_end)
        return start_index, end_index

    def _get_valid_highlight_in_line_indexes(self) -> tuple[int, int]:
        start_index = min(self.highlight_in_line_start, self.highlight_in_line_end)
        end_index = max(self.highlight_in_line_start, self.highlight_in_line_end)
        return start_index, end_index

    def _copy_highlighted_text(self) -> None:
        text = ""
        for line in self.highlighted_text:
            text += "".join(line)
        pyperclip.copy(text)

    @staticmethod
    def _is_special_char(char: str) -> bool:
        return ord(char) < 32 or ord(char) == 127

    @staticmethod
    def _is_empty_2D_sequence(
        sequence: Iterable[Iterable],
    ) -> bool:  # It's not a good name for a function.
        return not any(element for element in sequence)


if __name__ == "__main__":

    def output():
        print(len(textbox.getText()))
        textbox.setText("")

    pygame.init()
    win = pygame.display.set_mode((1000, 600))

    textbox = MyTextBox(
        win,
        100,
        100,
        800,
        400,
        fontSize=75,
        borderColour=(255, 0, 0),
        textColour=(0, 200, 0),
        onSubmit=output,
        radius=10,
        borderThickness=5,
        placeholderText="Enter something:",
    )

    run = True
    while run:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                quit()

        win.fill((255, 255, 255))

        pygame_widgets.update(events)
        pygame.display.update()
