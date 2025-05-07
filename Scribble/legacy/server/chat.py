class Chat:
    def __init__(self, rnd):
        self.content = []
        self.new_content = []
        self.receiver_count = 0
        self.round = rnd

    def update_chat(self, player_name: str, msg: str, guess: bool, is_sys_msg: bool) -> None:
        content = (player_name, msg, guess, is_sys_msg)
        self.content.append(content)
        self.new_content.append(content)

    def get_new_content(self) -> list[tuple[str, str, bool, bool]]:
        new_content = self.new_content[:]
        self.new_content = []
        # TODO сделать так, чтобы новые сообщения "сбрасывались"
        return new_content

    def get_chat(self) -> list[tuple[str, str, bool, bool]]:
        return self.content
