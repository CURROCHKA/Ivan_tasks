import pygame

from config import (
    COLORS,
    BORDER_THICKNESS,
    FONT_NAME,
    get_font_size,
    render_text,
)


class LeaderBoard:
    def __init__(self, win: pygame.Surface, x: float, y: float, width: int, height: int, margin: float, game):
        self.win = win
        self.x = x
        self.y = y
        self.width = width
        self.height = height  # Высота одной строчки
        self.margin = margin
        self.game = game
        self.text_color = COLORS[7]
        self.border_thickness = int(self.margin / BORDER_THICKNESS)
        self.players = []  # [(player: Player, {'rank_render': pygame.Surface,
                                                # 'name_render': pygame.Surface,
                                                # 'score_render': pygame.Surface}]
        self.players_guessed = set()

        self.score_font_size = int(self.width / 15)
        self.score_font = pygame.font.SysFont(FONT_NAME, self.score_font_size)

        self.rank_font_size = int(self.height / 3)
        self.rank_font = pygame.font.SysFont(FONT_NAME, self.rank_font_size)

    def draw(self):
        for i, player_info in enumerate(self.players):
            player = player_info[0]
            rank_render = player_info[1]['rank_render']
            name_render = player_info[1]['name_render']
            score_render = player_info[1]['score_render']

            if i % 2 == 0:
                color = COLORS[0]
            elif player in self.players_guessed:
                color = COLORS[2]
            else:
                color = COLORS[8]

            pygame.draw.rect(self.win, color, (self.x, self.y + i * self.height, self.width, self.height))

            self.win.blit(rank_render, (self.x + self.margin,
                                        self.y + i * self.height + self.height / 2 - rank_render.get_height() / 2))

            self.win.blit(name_render, (self.width / 3 + self.margin,
                                        self.y + i * self.height + self.height / 2 - name_render.get_height() / 2))

            self.win.blit(score_render, (self.x + self.margin,
                                         self.y + i * self.height + (
                                                 self.height - score_render.get_height()) - self.margin * 0.1))

        pygame.draw.rect(self.win, COLORS[7], (self.x - self.border_thickness / 2,
                                               self.y - self.border_thickness / 2,
                                               self.width + self.border_thickness,
                                               self.height * len(self.players) + self.border_thickness),
                         self.border_thickness)

    def get_scores(self):
        scores = []
        for player_info in self.players:
            player = player_info[0]
            score = player.get_score()
            scores.append((player, score))
        return sorted(scores, key=lambda x: x[1], reverse=True)

    def assign_ranks(self):
        scores = self.get_scores()
        ranks = []
        current_rank = 0
        previous_score = None

        for player, score in scores:
            if score != previous_score:
                current_rank += 1
                previous_score = score

            ranks.append((player, current_rank))

        return ranks

    def player_guess(self, player):
        self.players_guessed.add(player)

    def get_rank(self, player):
        ranks = self.assign_ranks()
        for current_player, rank in ranks:
            if current_player == player:
                return rank

    def get_rank_and_score_render(self, rank: int, score: int):
        rank_render = render_text(f'# {rank}', font_size=self.rank_font_size)
        score_render = render_text(f'Счёт: {score}', font_size=self.score_font_size)
        return rank_render, score_render

    def update_rank_and_scores(self):
        for i, player_info in enumerate(self.players):
            player = player_info[0]
            rank = self.get_rank(player)
            score = player.get_score()

            rank_render, score_render = self.get_rank_and_score_render(rank, score)
            self.players[i][1]['rank_render'] = rank_render
            self.players[i][1]['score_render'] = score_render

    def add_player(self, player):
        self.players.append((player, {}))

        rank = self.get_rank(player)
        name = player.get_name()
        score = player.get_score()

        rank_render, score_render = self.get_rank_and_score_render(rank, score)

        color = COLORS[7]
        if name == self.game.name:
            name = f'{name} (Ты)'
            color = COLORS[1]

        name_font_size = get_font_size(f'{name} (Ты)', self.width - rank_render.get_width(),
                                       max_height=self.height)
        name_render = pygame.font.SysFont(FONT_NAME, name_font_size).render(name, 1, color)

        self.players[-1][1].update({'rank_render': rank_render,
                                    'name_render': name_render,
                                    'score_render': score_render})

    def remove_player(self, player):
        for player_info in self.players:
            if player_info[0] == player:
                self.players.remove(player_info)
                break
