import asyncio

from langchain.chat_models.gigachat import GigaChat
from langchain_core.messages import SystemMessage, HumanMessage
from aiogram import Bot, Dispatcher, types

giga = GigaChat(
    profanity=False,
    credentials="MmZhMGRiZGUtMDZjOC00ZjgwLWFmM2EtYWIxZDFkMmNiYzA0Ojg0ZWM0ZWJlLTk4YmMtNDVkMy04OTljLWVkZTAxZGVmMzlkZQ====",
    scope="GIGACHAT_API_PERS",
    verify_ssl_certs=False
)

text = """
[Поддержка] Phystech GigaChat Challenge, [11/20/23 5:41PM]
 Приветствуем всех в чате хакатона Phystech GigaChat Challenge!

В разделе #General можно задать вопрос организаторам с тегом аккаунта поддержки @pgc_support и обсудить хакатон с другими участниками.

‼ Чтобы стать участником хакатона, нужно выполнить три пункта до 28 ноября, 23:59 МСК:

1 Зарегистрироваться (https://reg.gigachat-challenge.tech/register) на платформе и заполнить анкету участника (https://reg.gigachat-challenge.tech/me/0)
 (https://xn--c1ad6a.xn--80aegcbawovqtiw4l.xn--p1ai/me/0)2 Создать команду (https://reg.gigachat-challenge.tech/teams/2) (из 3-5 чел.) или присоединиться (https://reg.gigachat-challenge.tech/teams/1) к существующей
3 Подать командную заявку (https://reg.gigachat-challengetech/teams/4)
 Приглашайте в чат друзей и коллег по ссылке: https://t.me/gigachat_challenge.

[Поддержка] Phystech GigaChat Challenge, [11/20/23 5:42PM]
Уважаемые участники!

Информируем вас, что правила хакатона на сайте gigachat-challenge.tech были обновлены для внесения большей ясности в процесс получения командами призов хакатона.

Главные моменты:

1. Оператор, Заказчик и Организатор не претендует на исключительные права на Прототип, созданный в рамках участия в Хакатоне.

2. Приз победителям Хакатона будет предоставляться в виде возможности получить Инвестиции от Стартап-студии МФТИ. Общий размер инвестиций для каждой команды-победителя будет обсуждаться индивидуально после Хакатона (от 1 миллиона рублей). 

3. Инвестиция будет осуществлена в виде договора конвертируемого займа (по которому предоставляются целевые инвестиции, и которые могут быть возвращены выдавшему инвестиции лицу или переведены в долю участия в юридическом лице).

4. Процедура Инвестиций может быть осуществлена только с юридическим лицом. Если на момент окончания Хакатона у команды участников нет юридического лица, то Организаторы помогут с открытием.

5. Со стороны Стартап-студии МФТИ будет оказана дальнейшая поддержка, развитие и финансирование проектов победителей за миноритарную долю (хоть до выхода на IPO).
"""

chat_history = [text]

retriever = WikipediaRetriever()
qa = ConversationalRetrievalChain.from_llm(giga, retriever=retriever)

bot = Bot(token="5771137683:AAEbqmUH8xauH1PH-g7qcrtSIPOF5F5Bozo")
dp = Dispatcher(bot)


@dp.message_handler()
async def echo_message(message: types.Message):
    messages.append(HumanMessage(content="Оцени это сообщение: " + message.text))
    
    result = qa({"question": message, "chat_history": chat_history})
    chat_history.append((message, result["answer"]))
    print(f"-> **Question**: {message} \n")
    print(f"**Answer**: {result['answer']} \n")

    messages.append(result['answer'])
    
    await message.reply(result['answer'])


def main():
    # Start the bot
    try:
        asyncio.run(dp.start_polling())
    finally:
        dp.stop_polling()


if __name__ == '__main__':
    main()
