import json
import requests

# Firebase Realtime Database URL
FIREBASE_URL = "https://commands-19fda-default-rtdb.firebaseio.com/commands"

def load_data():
    """Загружает данные из Firebase"""
    try:
        response = requests.get(f"{FIREBASE_URL}.json", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data if data else {}
        return {}
    except:
        return {}

def update_command(name, command_data):
    """Обновляет одну команду в Firebase"""
    try:
        response = requests.put(f"{FIREBASE_URL}/{name}.json", json=command_data, timeout=5)
        return response.status_code == 200
    except:
        return False

def create_command():
    """Создает новую команду"""
    data = load_data()
    
    name = input("name:").strip()
    
    if not name:
        return
    
    if name in data:
        print("уже есть")
        return
    
    while True:
        password = input("password:").strip()
        if not password:
            print("пароль обязателен")
            continue
        break
    
    command_text = input("text:").strip()
    
    if not command_text:
        return
    
    new_command = {
        "password": password,
        "text": command_text
    }
    
    if update_command(name, new_command):
        print("создано")
    else:
        print("ошибка")

def main():
    print("system commands:")
    print("- create")
    print("- list")
    
    while True:
        name = input("name:").strip()
        
        if name == "create":
            create_command()
            continue
            
        if name == "list":
            data = load_data()
            if data:
                for command_name in data.keys():
                    print(command_name)
            else:
                print("нет команд")
            continue
        
        # Загружаем данные
        data = load_data()
        
        if name in data:
            command = data[name]
            
            # Показываем текст команды
            print(command['text'])
            
            # Спрашиваем пароль для изменения
            entered_password = input("password:").strip()
            
            if entered_password == command["password"]:
                # Только при правильном пароле спрашиваем об изменении
                change = input("change? (y/n):").lower()
                if change == 'y':
                    new_text = input("new text:").strip()
                    if new_text:
                        command["text"] = new_text
                        if update_command(name, command):
                            print("изменено")
            # Если пароль неверный или пустой - ничего не происходит
        else:
            print("не найдено")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass