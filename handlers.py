import re

from aiogram import Router, types
from aiogram.filters import Command, CommandObject

import database as db

router = Router()

HELP_TEXT = (
    "I track your daily calories.\n\n"
    "Just send me a message with a food description and its calories, "
    "in any order. You can log several items at once by separating them "
    "with commas, e.g.:\n"
    "  chicken salad 350\n"
    "  350 chicken salad\n"
    "  250 coffee, 75 porridge\n\n"
    "/today — today's entries and total\n"
    "/week — last 7 days summary\n"
    "/undo — delete your last entry\n"
    "/goal <calories> — set your daily calorie goal\n"
    "/help — show this message"
)

CALORIE_RE = re.compile(r"\d+")


async def today_header(user_id: int) -> str:
    entries = await db.get_today_entries(user_id)
    total = sum(row[0] for row in entries)
    goal = await db.get_goal(user_id)
    header = f"Today: {total} kcal"
    if goal:
        header += f" / {goal} kcal ({max(goal - total, 0)} remaining)"
    return header


def parse_item(text: str):
    match = CALORIE_RE.search(text)
    if not match:
        return None
    calories = int(match.group())
    description = (text[: match.start()] + text[match.end() :]).strip(" -,.")
    return calories, description or "food"


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await db.ensure_user(message.from_user.id)
    await message.answer(f"Welcome! {HELP_TEXT}")


@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(HELP_TEXT)


@router.message(Command("undo"))
async def cmd_undo(message: types.Message):
    deleted = await db.delete_last_entry(message.from_user.id)
    await message.answer("Removed your last entry." if deleted else "No entries to remove.")


@router.message(Command("today"))
async def cmd_today(message: types.Message):
    entries = await db.get_today_entries(message.from_user.id)
    if not entries:
        await message.answer("No entries logged today yet.")
        return

    total = sum(row[0] for row in entries)
    lines = [f"{cal} kcal — {desc}" for cal, desc, _ in entries]

    goal = await db.get_goal(message.from_user.id)
    header = f"Total: {total} kcal"
    if goal:
        header += f" / {goal} kcal ({max(goal - total, 0)} remaining)"

    await message.answer(header + "\n\n" + "\n".join(lines))


@router.message(Command("week"))
async def cmd_week(message: types.Message):
    rows = await db.get_week_summary(message.from_user.id)
    if not rows:
        await message.answer("No entries logged in the last 7 days.")
        return

    lines = [f"{day}: {total} kcal" for day, total in rows]
    await message.answer("\n".join(lines))


@router.message(Command("goal"))
async def cmd_goal(message: types.Message, command: CommandObject):
    if not command.args or not command.args.strip().isdigit():
        await message.answer("Usage: /goal <calories>\nExample: /goal 2000")
        return

    goal = int(command.args.strip())
    await db.ensure_user(message.from_user.id)
    await db.set_goal(message.from_user.id, goal)
    await message.answer(f"Daily goal set to {goal} kcal.")


@router.message()
async def log_food(message: types.Message):
    text = (message.text or "").strip()
    chunks = [chunk.strip() for chunk in text.split(",") if chunk.strip()]

    logged = []
    failed = []
    for chunk in chunks:
        parsed = parse_item(chunk)
        if parsed is None:
            failed.append(chunk)
        else:
            logged.append(parsed)

    if not logged:
        await message.answer(
            "I couldn't find a calorie number in that message.\n"
            "Try something like: chicken salad 350\n"
            "or several at once: 250 coffee, 75 porridge"
        )
        return

    await db.ensure_user(message.from_user.id)
    for calories, description in logged:
        await db.add_entry(message.from_user.id, calories, description)

    lines = [f"Logged {cal} kcal — {desc}" for cal, desc in logged]
    if failed:
        lines.append("Couldn't parse: " + "; ".join(failed))

    header = await today_header(message.from_user.id)
    await message.answer(header + "\n\n" + "\n".join(lines))
