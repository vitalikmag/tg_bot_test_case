from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from create_bot import bot, dp


# Определение состояний опроса
class CreatePollStates(StatesGroup):
    waiting_for_question = State()
    waiting_for_answer = State()


async def create_poll_handler(message: types.Message):
    # Создаем новое состояние опроса
    await CreatePollStates.waiting_for_question.set()

    # Запрашиваем первый вопрос
    await message.answer(
        'Для создания опроса отправь мне вопрос:'
    )


# Обработчик ответа на вопрос
@dp.message_handler(
    state=CreatePollStates.waiting_for_question,
    content_types=types.ContentTypes.TEXT,
)
async def process_question_answer(
        message: types.Message, state: FSMContext
):
    # Сохраняем вопрос в состоянии опроса
    async with state.proxy() as data:
        data['question'] = message.text

    # Переходим к состоянию ожидания ответов
    await CreatePollStates.waiting_for_answer.set()

    # Запрашиваем первый вариант ответа
    await message.answer(
        'Отлично! Теперь отправь мне первый вариант ответа на этот вопрос:'
    )


@dp.message_handler(
    state=CreatePollStates.waiting_for_answer,
    content_types=types.ContentTypes.TEXT,
)
async def process_answer_option(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        question = data['question']
        answer_options = data.get('answer_options', [])

    # Проверяем условия прерывая ввода ответов
    if 'Стоп'.lower() in message.text.lower() or len(answer_options) >= 10:
        if len(answer_options) < 2:
            await message.answer('Должно быть как минимум два ответа. Добавьте еще один')
        else:
            await bot.send_poll(
                chat_id=message.chat.id,
                question=question,
                options=answer_options,
                is_anonymous=True,
                type=types.PollType.REGULAR,
                correct_option_id=0,
            )
            await state.finish()
    else:
        # Добавляет новый ответ или предлагаем закончить ввод.
        answer_options.append(message.text)
        async with state.proxy() as data:
            data['answer_options'] = answer_options

        await message.answer(
            'Отлично! Теперь отправь мне следующий вариант ответа на этот вопрос '
            '(Если ответов достаточно напиши "Стоп"):'
        )
