import pygame
import pygame_widgets
import time

from pygame_widgets.textbox import TextBox
from pygame_widgets.mouse import Mouse, MouseState


class MyTextBox(TextBox):
    NEWLINE_CHAR = "\n"

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
        """
        Initialize a text box widget.

        Args:
            win (pygame.Surface): The surface to render the text box on.
            x (int): The x-coordinate of the top-left corner.
            y (int): The y-coordinate of the top-left corner.
            width (int): The width of the text box.
            height (int): The height of the text box.
            isSubWidget (bool, optional): Specifies if this is a sub-widget. Defaults to False.
            **kwargs: Additional keyword arguments for customization.
        """
        super().__init__(win, x, y, width, height, isSubWidget, **kwargs)

        self.tab_spaces = kwargs.get("tabSpaces", 4)
        self.highlight_color = kwargs.get("highlightColor", (166, 210, 255))

        self.text = [[]]  # Multi-line text storage
        self.selected_line = 0  # Index of the currently selected line

        self.highlighted_text = [[]]
        # Highlight indexes
        self.highlight_start_line = 0
        self.highlight_end_line = 0
        self.highlight_start_inline = 0
        self.highlight_end_inline = 0

    def listen(self, events: list[pygame.event.Event]):
        """
        Listen to events.

        This method is used to listen to pygame events and update the state
        of the text box accordingly.

        Args:
            events (list[pygame.event.Event]): The list of pygame events to listen to
        """
        if not self._hidden and not self._disabled:
            if self.keyDown:
                self.updateRepeatKey()

            # Selection
            mouseState = Mouse.getMouseState()
            x, y = Mouse.getMousePos()

            if mouseState == MouseState.CLICK:
                if self.contains(x, y):
                    self.selected = True
                    self.showCursor = True
                    self.cursorTime = time.time()
                    self.update_cursor_position(x, y)

                    self.highlight_start_line = self.selected_line
                    self.highlight_start_inline = self.cursorPosition

            elif mouseState == MouseState.DRAG:
                if self.contains(x, y):
                    self.selected = True
                    self.showCursor = True
                    self.cursorTime = time.time()
                    self.update_cursor_position(x, y)

                    self.highlight_end_line = self.selected_line
                    self.highlight_end_inline = self.cursorPosition

                else:
                    self.selected = False
                    self.showCursor = False
                    self.cursorTime = time.time()

            # Keyboard Input
            if self.selected:
                for event in events:
                    if event.type == pygame.KEYDOWN:
                        self.showCursor = True
                        self.keyDown = True
                        self.repeatKey = event
                        self.repeatTime = time.time()

                        if event.key == pygame.K_BACKSPACE:
                            if not self.is_empty_highlighted_text():
                                self.erase_highlighted_text()
                                self.cursorPosition += 1
                                self.onTextChanged(*self.onTextChangedParams)

                            elif self.cursorPosition != 0:
                                self.maxLengthReached = False
                                self.text[self.selected_line].pop(self.cursorPosition - 1)
                                self.shift_lines()
                                self.onTextChanged(*self.onTextChangedParams)

                            elif self.cursorPosition == 0 and self.selected_line != 0:
                                if len(self.text[self.selected_line]) == 0:
                                    self.text.pop(self.selected_line)
                                self.selected_line -= 1
                                self.cursorPosition = (
                                    len(self.text[self.selected_line]) + 1
                                )
                                self.shift_lines()
                                self.onTextChanged(*self.onTextChangedParams)

                            self.cursorPosition = max(self.cursorPosition - 1, 0)

                        elif event.key == pygame.K_DELETE:
                            if not self.is_empty_highlighted_text():
                                self.erase_highlighted_text()
                                self.onTextChanged(*self.onTextChangedParams)

                            elif not self.cursorPosition >= len(
                                self.text[self.selected_line]
                            ):
                                self.maxLengthReached = False
                                self.text[self.selected_line].pop(self.cursorPosition)
                                self.shift_lines()
                                self.onTextChanged(*self.onTextChangedParams)

                            elif self.cursorPosition == 0 and self.selected_line != 0:
                                if len(self.text[self.selected_line]) == 0:
                                    self.text.pop(self.selected_line)
                                self.selected_line -= 1
                                self.cursorPosition = (
                                    len(self.text[self.selected_line]) + 1
                                )
                                self.onTextChanged(*self.onTextChangedParams)

                        elif event.key == pygame.K_RETURN:
                            self.onSubmit(*self.onSubmitParams)

                        elif event.key == pygame.K_UP:
                            self.selected_line = max(self.selected_line - 1, 0)

                        elif event.key == pygame.K_DOWN:
                            self.selected_line = min(
                                self.selected_line + 1, len(self.text) - 1
                            )

                        elif event.key == pygame.K_RIGHT:
                            self.cursorPosition = min(
                                self.cursorPosition + 1,
                                len(self.text[self.selected_line]),
                            )

                        elif event.key == pygame.K_LEFT:
                            self.cursorPosition = max(self.cursorPosition - 1, 0)

                        elif event.key == pygame.K_HOME:
                            self.cursorPosition = 0

                        elif event.key == pygame.K_END:
                            self.cursorPosition = len(self.text[self.selected_line])

                        elif event.key == pygame.K_TAB:
                            self.add_text(list(" " * self.tab_spaces))

                        elif event.key == pygame.K_INSERT:
                            # TODO add logic for insert. I don't really know what it do
                            pass

                        elif event.key == pygame.K_ESCAPE:
                            if not self.escape:
                                self.selected = False
                                self.showCursor = False
                                self.escape = True
                                self.repeatKey = None
                                self.keyDown = None
                                self.firstRepeat = True

                        elif not self.maxLengthReached:
                            self.add_text([event.unicode])

                    elif event.type == pygame.KEYUP:
                        self.repeatKey = None
                        self.keyDown = None
                        self.firstRepeat = True
                        self.escape = False

    def draw_border(self):
        """Draw the border of the text box.

        This method draws the border of the text box, which is the outline
        of the main body of the text box. It is drawn as a combination of
        rectangles and circles to create a rounded corner effect.
        """
        borderRects = [
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

        borderCircles = [
            (self._x + self.radius, self._y + self.radius),
            (self._x + self.radius, self._y + self._height - self.radius),
            (self._x + self._width - self.radius, self._y + self.radius),
            (self._x + self._width - self.radius, self._y + self._height - self.radius),
        ]

        for rect in borderRects:
            pygame.draw.rect(self.win, self.borderColour, rect)

        for circle in borderCircles:
            pygame.draw.circle(self.win, self.borderColour, circle, self.radius)

    def draw_background(self):
        """Draw the background of the text box.

        This method draws the main body of the text box, which is the area
        where the text is displayed. It is drawn as a rectangle with rounded
        corners.
        """
        backgroundRects = [
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

        backgroundCircles = [
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

        for rect in backgroundRects:
            pygame.draw.rect(self.win, self.colour, rect)

        for circle in backgroundCircles:
            pygame.draw.circle(self.win, self.colour, circle, self.radius)

    def draw_text(self):
        """
        Draw the text in the text box.

        This method will either draw the text in the text box or the placeholder text,
        depending on whether the text box is empty or not. The text is drawn line by line,
        with each character being rendered as a separate surface. The position of the
        text is determined by the `textOffsetLeft` and `textOffsetBottom` attributes.
        """
        if any(len(line) > 0 for line in self.text):
            text = self.text
            color = self.textColour
        else:
            text = [list(self.placeholderText)]
            color = self.placeholderTextColour

        for line_index, line in enumerate(text):
            x = [self._x + self.textOffsetLeft]
            for char in line:
                char_render = self.font.render(
                    char,
                    True,
                    color,
                )
                textRect = char_render.get_rect(
                    bottomleft=(
                        x[-1],
                        self._y
                        + self.fontSize * (line_index + 1)
                        + self.textOffsetBottom,
                    )
                )

                self.win.blit(char_render, textRect)
                x.append(x[-1] + char_render.get_width())

    def draw_cursor(self):
        """
        Draw the cursor
        The position of the cursor is determined by the `cursorPosition` attribute.
        The cursor is only displayed if the `showCursor` attribute is True.
        """
        x = self.get_line_width(self.text[self.selected_line])

        if self.showCursor:
            try:
                pygame.draw.line(
                    self.win,
                    self.cursorColour,
                    (
                        x[self.cursorPosition],
                        self._y
                        + self.textOffsetBottom
                        + self.fontSize * self.selected_line,
                    ),
                    (
                        x[self.cursorPosition],
                        self._y
                        + self.fontSize * (self.selected_line + 1)
                        + self.textOffsetBottom,
                    ),
                    width=2,
                )
            except IndexError:
                self.cursorPosition -= 1

    def draw_highlight(self) -> None:
        """
        Draw the highlighted text.

        The highlighted text is the text between the `highlight_start_line` and
        `highlight_end_line` attributes, inclusive. The text is drawn with the
        `highlight_color` attribute.

        :return: None
        """

        def draw_rect(line: int, start: int, end: int) -> None:
            """
            Draw a rectangle for a range of characters in a line.

            This method is used to draw the highlighted text. It takes a line index,
            a start character index and an end character index. It renders the text
            between the start and end character index and draws a rectangle around
            it using the `highlight_color` attribute.

            :param line: The line index
            :param start: The start character index
            :param end: The end character index
            :return: None
            """
            x = self.get_line_width(self.text[line])

            for char_index in range(start, end):
                char = self.text[line][char_index]
                char_render = self.font.render(char, True, self.highlight_color)
                rect = char_render.get_rect(
                    bottomleft=(
                        x[char_index],
                        self._y + self.fontSize * (line + 1) + self.textOffsetBottom,
                    )
                )
                pygame.draw.rect(self.win, self.highlight_color, rect)

        start_line = min(self.highlight_start_line, self.highlight_end_line)
        end_line = max(self.highlight_start_line, self.highlight_end_line)

        start_inline = self.highlight_end_inline
        end_inline = self.highlight_start_inline

        if self.highlight_start_line < self.highlight_end_line:
            start_inline = self.highlight_start_inline
            end_inline = self.highlight_end_inline

        if start_line == end_line:
            start_inline = min(self.highlight_start_inline, self.highlight_end_inline)
            end_inline = max(self.highlight_start_inline, self.highlight_end_inline)

            draw_rect(start_line, start_inline, end_inline)
            self.highlighted_text = [self.text[start_line][start_inline:end_inline]]

        else:
            draw_rect(start_line, start_inline, len(self.text[start_line]))
            self.highlighted_text = [self.text[start_line][start_inline:]]

            for line_index in range(start_line + 1, end_line):
                draw_rect(line_index, 0, len(self.text[line_index]))
                self.highlighted_text += [self.text[line_index]]

            draw_rect(end_line, 0, end_inline)
            self.highlighted_text += [self.text[end_line][:end_inline]]

    def draw(self):
        """Display to surface"""
        if not self._hidden:
            if self.selected:
                self.updateCursor()
            self.draw_border()
            self.draw_background()
            self.draw_highlight()
            self.draw_text()
            self.draw_cursor()

    def is_empty_highlighted_text(self):
        return all(len(line) == 0 for line in self.highlighted_text)

    def erase_highlighted_text(self):
        start_line = min(self.highlight_start_line, self.highlight_end_line)
        end_line = max(self.highlight_start_line, self.highlight_end_line)

        start_inline = self.highlight_end_inline
        end_inline = self.highlight_start_inline

        if self.highlight_start_line < self.highlight_end_line:
            start_inline = self.highlight_start_inline
            end_inline = self.highlight_end_inline

        if start_line == end_line:
            start_inline = min(
                self.highlight_start_inline,
                self.highlight_end_inline,
            )
            end_inline = max(
                self.highlight_start_inline,
                self.highlight_end_inline,
            )

            del self.text[start_line][start_inline:end_inline]
        else:
            del self.text[start_line][start_inline:]
            del self.text[end_line][:end_inline]
            del self.text[start_line + 1 : end_line]

        self.selected_line = start_line
        self.cursorPosition = start_inline
        self.shift_lines()

        self.highlight_start_line = self.highlight_end_line = 0
        self.highlight_start_inline = self.highlight_end_inline = 0
        self.highlighted_text = [[]]

    def update_cursor_position(self, x: float, y: float) -> None:
        """
        Update the cursor position based on the given mouse coordinates

        This method will update the `selected_line` and `cursorPosition` attributes
        based on the given mouse coordinates.

        Args:
            x (float): The x-coordinate of the mouse
            y (float): The y-coordinate of the mouse
        """
        _y = [self._y + self.textOffsetBottom]

        for i, line in enumerate(self.text):
            if _y[-1] <= y <= _y[-1] + self.fontSize:
                self.selected_line = i
                break
            _y.append(_y[-1] + self.fontSize)

        _x = [self._x + self.textOffsetLeft]

        for i, char in enumerate(self.text[self.selected_line]):
            char_render = self.font.render(char, True, self.textColour)
            if (
                _x[-1] - char_render.get_width() / 2
                <= x
                <= _x[-1] + 3 * char_render.get_width() / 2
            ):
                self.cursorPosition = i
            _x.append(_x[-1] + char_render.get_width())

        if len(_x) >= 2 and x >= _x[-1] - (_x[-1] - _x[-2]) / 2:
            self.cursorPosition = len(self.text[self.selected_line])

    def add_text(self, text: list[str]):
        """
        Add text to the text box

        This method will insert the given text into the text box at the current cursor position.
        The text will be split into individual characters and inserted one by one.
        If a line is too long, the characters will be split onto the next line.
        If the cursor is at the end of the text box, a new line will be added.

        Args:
            text (list[str]): The text to add to the text box
        """
        for char in text:
            if len(char) > 0:
                if not self.is_empty_highlighted_text():
                    self.erase_highlighted_text()

                try:
                    self.text[self.selected_line].insert(self.cursorPosition, char)

                except IndexError:
                    self.text.append([event.unicode])

                for line_index in range(self.selected_line, len(self.text)):
                    x = [self._x + self.textOffsetLeft]

                    for char1 in self.text[line_index]:
                        char_render = self.font.render(
                            char1,
                            True,
                            self.colour,
                        )

                        x.append(x[-1] + char_render.get_width())

                        if x[-1] > self._x + self._width - self.textOffsetRight:
                            try:
                                self.text[line_index + 1].insert(
                                    0, self.text[line_index].pop()
                                )
                            except IndexError:
                                self.text.insert(
                                    line_index + 1, [self.text[line_index].pop()]
                                )

                            if self.cursorPosition >= len(self.text[line_index]):
                                self.selected_line += 1
                                self.cursorPosition = 0

                self.cursorPosition += 1
                self.onTextChanged(*self.onTextChangedParams)

    def get_line_width(self, line: list[str]) -> list[float]:
        """
        Get the width of a line of text in the text box

        This method will return a list of the x-coordinates of the end of each character in the line.
        The x-coordinate is relative to the left edge of the text box.

        Args:
            line (list[str]): The line of text to get the width of

        Returns:
            list[float]: A list of the x-coordinates of the end of each character in the line
        """
        x = [self._x + self.textOffsetLeft]

        for char in line:
            char_render = self.font.render(
                char,
                True,
                self.textColour,
            )
            x.append(x[-1] + char_render.get_width())
        return x

    def shift_lines(self) -> None:
        """
        Shift lines when a line is deleted

        When a line is deleted, this method will shift all the lines below it up one line.
        """
        shift = 0
        for line in range(
            self.selected_line,
            len(self.text) - 1,
        ):
            if len(self.text[line - shift]) == 0:
                del self.text[line - shift]
                shift += 1
                continue

            x = self.get_line_width(self.text[line - shift])

            while (
                x[-1] <= self._x + self._width - self.textOffsetRight
                and len(self.text[line + 1 - shift]) > 0
            ):
                self.text[line - shift].append(self.text[line + 1 - shift].pop(0))
                x = self.get_line_width(self.text[line - shift])

    def setText(self, text: str) -> None:
        """
        Set the text of the text box.

        This method resets the text box to a single line of text and sets the cursor position to the start.

        Args:
            text (str): The text to set in the text box.
        """
        self.text = [[]]
        self.selected_line = 0
        self.cursorPosition = 0
        self.add_text(list(text))

    def getText(self) -> str:
        """
        Retrieve the complete text from the text box.

        This method concatenates all lines of text in the text box into a single string and returns it.

        Returns:
            str: The complete text from the text box.
        """
        return "".join("".join(line) for line in self.text)


if __name__ == "__main__":

    def output():
        print(textbox.getText())
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
