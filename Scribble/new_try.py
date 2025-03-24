import pygame
import pygame_widgets
import time

from pygame_widgets.textbox import TextBox
from pygame_widgets.mouse import Mouse, MouseState


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

        self.text = [[]]

        self.selected_line = 0

        # TODO highlight the text

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

            elif mouseState == MouseState.DRAG:
                if self.contains(x, y):
                    self.selected = True
                    self.showCursor = True
                    self.cursorTime = time.time()
                    self.update_cursor_position(x, y)

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
                            if self.cursorPosition != 0:
                                self.maxLengthReached = False
                                self.text[self.selected_line].pop(
                                    self.cursorPosition - 1
                                )
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

                            self.cursorPosition = max(self.cursorPosition - 1, 0)

                        elif event.key == pygame.K_DELETE:
                            if not self.cursorPosition >= len(
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

    def draw(self):
        """Display to surface"""
        if not self._hidden:
            if self.selected:
                self.updateCursor()
            self.draw_border()
            self.draw_background()
            self.draw_text()
            self.draw_cursor()

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
