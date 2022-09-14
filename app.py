# -*- coding: utf-8 -*-
from utils.misc.prestart_moves import prestart_moves
from loader import dp, executor
import handlers


if __name__ == "__main__":
	executor.start_polling(dp, skip_updates=True, on_startup=prestart_moves)