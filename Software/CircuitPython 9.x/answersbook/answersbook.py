import json
import os
import random

import hoshino

from hoshino import Service, priv
from hoshino.typing import CQEvent


sv_help = """
[问题+翻看答案] 愿一切无解都有解！解除你的迷惑，终结你的纠结！
""".strip()

sv = Service(
    name="答案之书",  # 功能名
    use_priv=priv.NORMAL,  # 使用权限
    manage_priv=priv.ADMIN,  # 管理权限
    visible=True,  # 可见性
    enable_on_default=True,  # 默认启用
    bundle="娱乐",  # 分组归类
    help_=sv_help,  # 帮助说明
)

path = os.path.join(os.path.dirname(__file__), "answersbook.json")


def get_answers():
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as dump_f:
            try:
                words = json.load(dump_f)
            except Exception as e:
                hoshino.logger.error(f"读取答案之书时发生错误{type(e)}")
                return None
    else:
        hoshino.logger.error(f"目录下未找到答案之书")
    keys = list(words.keys())
    key = random.choice(keys)
    return words[key]["answer"]


@sv.on_suffix(("翻看答案"))
@sv.on_prefix(("翻看答案"))
async def answersbook(bot, ev: CQEvent):
    msg = ev.message.extract_plain_text().strip()
    if not msg:
        await bot.finish(ev, "你想问什么问题呢？")
    answers = get_answers()
    await bot.send(ev, answers, at_sender=True)
