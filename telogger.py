import telebot
import subprocess
import os

API_TOKEN = 'TOKEN'

bot = telebot.TeleBot(API_TOKEN)
current_dir = os.path.expanduser("~")  # Начальный рабочий каталог
previous_dir = current_dir  # Для хранения предыдущего каталога

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "TeloGGer")

@bot.message_handler(func=lambda message: True)
def execute_command(message):
    global current_dir, previous_dir
    command = message.text.strip()

    # Проверка команды cd
    if command.startswith("cd "):
        try:
            target_dir = command.split(" ", 1)[1].strip()
            if target_dir == "~":
                target_dir = os.path.expanduser("~")
            elif target_dir == "-":
                target_dir, previous_dir = previous_dir, current_dir
            elif target_dir.startswith("~"):
                target_dir = os.path.expanduser(target_dir)

            new_dir = os.path.abspath(os.path.join(current_dir, target_dir))
            previous_dir = current_dir
            os.chdir(new_dir)
            current_dir = new_dir
            bot.reply_to(message, f"Текущий каталог изменен на {current_dir}")
        except Exception as e:
            bot.reply_to(message, f"Произошла ошибка при изменении каталога:\n{e}")
        return

    # Команды, требующие интерактивного ввода, не поддерживаются
    if command in ["htop", "nano"]:
        bot.reply_to(message, f"Команда {command} не поддерживается, так как требует интерактивного ввода.")
        return

    try:
        # Выполнение команды с перенаправлением вывода в файл, если это требуется
        full_command = f"source ~/.bashrc && {command}"
        result = subprocess.run(full_command, shell=True, cwd=current_dir, capture_output=True, text=True, executable='/bin/bash')
        output = result.stdout + result.stderr
        bot.reply_to(message, f'Результат:\n<pre>{output}</pre>', parse_mode="HTML")
    except Exception as e:
        bot.reply_to(message, f'Произошла ошибка при выполнении команды:\n{e}')

if __name__ == '__main__':
    bot.polling(none_stop=True)
