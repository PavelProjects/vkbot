import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

main_token = '2c4afdbc583c2d03c43327bd0558790cb499cc6328e378d7928a9d1601866eb8f6e67e57cd082399a046c'
vk_session = vk_api.VkApi(token = main_token)
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

msg_hello = 'Здравствуйте, краткая справка по ценам и услугам:\n\n- Сведение 1500 руб.\n- Время сведения 1-2 дня.\n- Количество доработок - 1\n\nЭтапы нашего с вами взаимодействия:\n\n- Я получаю от вас заказ на сведение (можно без деталей или же можно примерно описать, что бы вы хотели увидеть в итоге).\n- Позже я присылаю примерный вариант сведения, после чего мы с вами обговариваем детали.\n- Далее ваш микс отправляется на доработку и потом попадает к вам в виде готовой работы.'
msg_buff = ''

def sender(id, text):
  vk_session.method('messages.send',{'user_id': id, 'message': text, 'random_id' : 0})

data = []
convs = vk_session.method('messages.searchConversations',{'q':''})
#print(convs)
for element in convs['items']:
  #vk_session.method('messages.deleteConversation',{'peer_id': element['peer']['local_id']})
  data.append(element['peer']['id'])
print(data)

for event in longpoll.listen():
  if event.type == VkEventType.USER_TYPING:   
    id = event.user_id
    if id not in data:
      print('hello')
      data.append(id)
      sender(id, msg_hello)
  if event.type == VkEventType.MESSAGE_NEW:
    if event.to_me:
      id = event.user_id
      if event.text.lower() == 'справка':
        sender(id, msg_hello)
        sender(30207458, '@id' + str(id) + ' пишет:\n' + event.text)
      elif event.text == '/change' and id == 30207458:
        sender(id, 'Напишите новую справку:')
        for event in longpoll.listen():
          if event.type == VkEventType.MESSAGE_NEW and event.user_id == 30207458:
            if event.to_me and event.user_id == 30207458:
              msg_buff = event.text
              if event.user_id == 30207458:
                msg_hello = msg_buff
                sender(id, 'Я все сделал, кожаный ублюдок')
                break

        #sender(id, 'Вам ответил бот, спасибо за сообщение, администратор скоро ответит на ваше сообщение')
        #sender(30207458, '@id' + str(id) + ' пишет:\n' + event.text)