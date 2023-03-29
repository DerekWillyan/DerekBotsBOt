from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters

# Definindo constantes para os estados da conversa
NOME, EMAIL, SITUACAO, PLANO, PAGAMENTO = range(5)

# Função para iniciar a conversa
def start(update, context):
    update.message.reply_text(
        'Olá! Como posso ajudar? Para criar um novo bot, por favor digite seu nome.',
    )
    return NOME

# Função para obter o nome do cliente
def get_nome(update, context):
    context.user_data['nome'] = update.message.text
    update.message.reply_text(
        'Por favor, informe seu endereço de email.'
    )
    return EMAIL

# Função para obter o email do cliente
def get_email(update, context):
    context.user_data['email'] = update.message.text
    update.message.reply_text(
        'Por favor, informe a situação para a qual deseja criar o bot.'
    )
    return SITUACAO

# Função para obter a situação do cliente
def get_situacao(update, context):
    context.user_data['situacao'] = update.message.text
    reply_keyboard = [['Plano 1', 'Plano 2', 'Plano 3']]
    update.message.reply_text(
        'Para resolvermos a situação informada, oferecemos os seguintes planos mensais:\n\n'
        'Plano 1: R$ 50,00/mês\n'
        'Plano 2: R$ 100,00/mês\n'
        'Plano 3: R$ 150,00/mês\n\n'
        'Por favor, selecione um dos planos abaixo:',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return PLANO

# Função para obter o tipo de plano escolhido pelo cliente
def get_plano(update, context):
    context.user_data['plano'] = update.message.text
    reply_keyboard = [['PIX', 'Cartão de Crédito', 'Cartão de Débito']]
    update.message.reply_text(
        f'Você escolheu o {context.user_data["plano"]}.'
        '\n\nPor favor, escolha uma das opções abaixo para efetuar o pagamento:',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return PAGAMENTO

# Função para obter o tipo de pagamento escolhido pelo cliente e finalizar a conversa
def get_pagamento(update, context):
    context.user_data['pagamento'] = update.message.text
    if context.user_data['pagamento'] == 'PIX':
        update.message.reply_text(
            'Por favor, envie o valor do pagamento para a chave PIX 88998345711.'
        )
    else:
        update.message.reply_text(
            'Por favor, clique no link abaixo para efetuar o pagamento:',
            reply_markup=ReplyKeyboardRemove()
        )
        update.message.reply_text(
            'https://checkout.pagseguro.com.br/?id=ABC123'
        )
    context.bot.send_message(
        chat_id='5348472058',
        text=f'Novo cliente cadastrado'
        f'\n\nNome: {context.user_data["nome"]}'
        f'\nEmail: {context.user_data["email"]}'
        f'\nSituação: {context.user_data["situacao"]}'
        f'\nPlano: {context.user_data["plano"]}'
        f'\nPagamento: {context.user_data["pagamento"]}'
    )
    update.message.reply_text(
        'Obrigado por escolher nossos serviços. Entraremos em contato em breve!'
    )
    return ConversationHandler.END

# Função para cancelar a conversa
def cancel(update, context):
    update.message.reply_text(
        'A conversa foi cancelada.'
    )
    return ConversationHandler.END

# Criando o objeto updater e o dispatcher
updater = Updater(token='6042638645:AAHdqeeKudb8p-iPiyjMssOTKLGp1dPd7gg')
dispatcher = updater.dispatcher

# Criando o conversation handler para gerenciar a conversa
conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        NOME: [MessageHandler(Filters.text & ~Filters.command, get_nome)],
        EMAIL: [MessageHandler(Filters.text & ~Filters.command, get_email)],
        SITUACAO: [MessageHandler(Filters.text & ~Filters.command, get_situacao)],
        PLANO: [MessageHandler(Filters.regex('^(Plano 1|Plano 2|Plano 3)$'), get_plano)],
        PAGAMENTO: [MessageHandler(Filters.regex('^(PIX|Cartão de Crédito|Cartão de Débito)$'), get_pagamento)]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)

# Registrando o conversation handler no dispatcher
dispatcher.add_handler(conv_handler)

# Iniciando o bot
updater.start_polling()
updater.idle()

