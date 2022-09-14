from aiogram import types

class BarColorSet:
    def __init__(self,
                 fg_color: str,
                 bg_color: str):
        self.fg_color = fg_color
        self.bg_color = bg_color

GreenBlack = BarColorSet("🟩", "⬛️")
GreenWhite = BarColorSet("🟩", "⬜️")
RedBlack = BarColorSet("🟥", "⬛️")
RedWhite = BarColorSet("🟥", "⬜️")
BlueBlack = BarColorSet("🟦", "⬛️")
BlueWhite = BarColorSet("🟦", "⬜️")

class ProgressBar:

    def __init__(self,
                 message: types.Message,
                 name: str,
                 max_value: int,
                 min_value: int = 1,
                 step: int = 1,
                 progress_bar: BarColorSet = None):
        self._message = None
        self._chat_id = message.from_user.id
        self._bot = message.bot
        self._step = step
        self._max_value = max_value
        self._min_value = min_value
        self._name = name
        self._pos = 0
        self._ended = False
        self._progress_bar = progress_bar

        self._prev_percent = 0

    @property
    def _clock(self) -> str:
        clocks = "🕐🕑🕒🕓🕔🕕🕖🕗🕘🕙🕚🕛"
        if self._pos >= 12:
            self._pos = 0
        clock = clocks[self._pos]
        self._pos += 1
        return clock

    @property
    def _percent(self) -> str:
        return round(self._min_value * 100 / self._max_value)

    @property
    def _text(self) -> str:
        text = f"<b>{self._clock} {self._name}:<code> {self._percent}%</code></b>\n\n"
        if isinstance(self._progress_bar, BarColorSet):
            count = self._percent // 10
            text += count * self._progress_bar.fg_color
            text += (10 - count) * self._progress_bar.bg_color
        return text

    async def move(self):
        if not self._message:
            self._message = await self._bot.send_message(
                chat_id=self._chat_id,
                text=self._text
            )
        if self._prev_percent == self._percent:
            return None
        self._prev_percent = self._percent

        if self._min_value < self._max_value:
            await self._message.edit_text(
                text=self._text)
            self._min_value += self._step

        elif self._ended:
            raise TypeError("Process has been already ended!")

        else:
            await self._message.edit_text(
                text=f"<b>✅ {self._name}</b>")