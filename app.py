import sys
import shutil
import zipfile
import asyncio
import logging
from os import getenv
from pathlib import Path

from aiogram.filters import CommandStart
from aiogram.utils.markdown import hbold
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, FSInputFile

from utils.tg_file_context import tmp_datafolder
from utils.locale_svc import prepare_default_xlsx_file, get_back_prepared_xlsx_files_to_json, get_back_single_xlsx_file_to_json

# Bot token can be obtained via https://t.me/BotFather
TOKEN = getenv("TG_BOT_TOKEN")
TG_BOT = Bot(TOKEN)

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()


def solve_doc_from_msg(msg: Message) -> str:
    return


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    print(message)
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


async def is_message_with_file(message: types.Message, err_answer_str: str):
    if message.document is None:
        await message.answer(err_answer_str)
        return False
    return True


def detect_root_localization_folder(path: Path, deep=0) -> Path:
    for i in path.iterdir():
        if i.is_dir():
            return detect_root_localization_folder(i, deep + 1)
        return (path / '..').resolve()


async def download_and_unzip_file(message: types.Message, tmp_folder) -> Path:
    await message.answer("Start download your file")
    file = await TG_BOT.get_file(message.document.file_id)
    file_path = tmp_folder / message.document.file_name
    await TG_BOT.download_file(file.file_path, destination=file_path, timeout=120)
    await message.answer("Download successfully")
    if file_path.suffix == ".zip":
        unzip_file_path = tmp_folder / message.document.file_name[:-4]
        with zipfile.ZipFile(file_path, mode="r") as archive:
            archive.extractall(unzip_file_path)
        return detect_root_localization_folder(unzip_file_path)
    else:
        return file_path.resolve()


async def upload_file_to_tg(message: types.Message, file_path: Path):
    await message.answer("Start sending file to you")
    upload_file = FSInputFile(file_path)
    await message.answer_document(document=upload_file)


@dp.message()
async def echo_handler(message: types.Message) -> None:
    action = message.text or message.html_text or message.caption
    with tmp_datafolder() as tmp_folder:
        match action:
            case "1":
                if await is_message_with_file(message, "Don't receive zip with data for prepare xlsx from json"):
                    prepared_localization_path = await download_and_unzip_file(message, tmp_folder)
                    prepare_default_xlsx_file(prepared_localization_path)
                    new_zip_file_path = shutil.make_archive(tmp_folder / (message.document.file_name[:-4] + "_prepared"), 'zip', prepared_localization_path)
                    await upload_file_to_tg(message, new_zip_file_path)
            case "2":
                if await is_message_with_file(message, "Don't receive zip with data for prepare xlsx to new json"):
                    prepared_localization_path = await download_and_unzip_file(message, tmp_folder)
                    get_back_prepared_xlsx_files_to_json(prepared_localization_path)
                    new_zip_file_path = shutil.make_archive(tmp_folder / (message.document.file_name[:-4] + "_finally"), 'zip', prepared_localization_path)
                    await upload_file_to_tg(message, new_zip_file_path)
            case "3":
                if await is_message_with_file(message, "Don't receive xlsx file for make new json"):
                    prepared_localization_path = await download_and_unzip_file(message, tmp_folder)
                    new_json_path = (prepared_localization_path / f"../{prepared_localization_path.stem}_new.json").resolve()
                    get_back_single_xlsx_file_to_json(prepared_localization_path, new_json_path)
                    await upload_file_to_tg(message, new_json_path)
            # case "4":
            #     await message.answer("4")
            case _:
                answer = [
                    '1 - load zip with json to xlsx',
                    '2 - load proofreaded zip xslx to new_json',
                    '3 - load proofreaded xlsx to new_json',
                ]
                await message.answer(',\n'.join(answer))


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    # And the run events dispatching
    await dp.start_polling(TG_BOT)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
