# Настройка интеграции терминала в VS Code

## Проблема
Сообщение об ошибке: 
```
Shell Integration Unavailable
Shell integration initialization sequence '\x1b]633;A' was not received within 14s. 
Shell integration has been disabled for this terminal instance.
```

## Решение: настройка VS Code

### 1. Откройте настройки VS Code

Есть несколько способов открыть настройки:
- Нажмите `Ctrl+,` (запятая)
- Или через меню: File → Preferences → Settings
- Или нажмите `Ctrl+Shift+P`, введите "settings" и выберите "Preferences: Open Settings (UI)"

### 2. Настройка shell integration

В поиске настроек введите "shell integration" и найдите следующие параметры:

1. **Увеличьте таймаут для интеграции оболочки**
   - Найдите `terminal.integrated.shellIntegration.timeout`
   - Увеличьте значение с 14s (по умолчанию) до 60s

2. **Убедитесь, что интеграция включена**
   - Проверьте, что `terminal.integrated.shellIntegration.enabled` установлено в `true`

### 3. Выбор правильной оболочки по умолчанию

1. Нажмите `Ctrl+Shift+P` для открытия палитры команд
2. Введите "terminal default" и выберите "Terminal: Select Default Profile"
3. Выберите подходящую оболочку из списка (рекомендуется PowerShell или cmd.exe для Windows)

### 4. Отключение декорации команд (опционально)

Если проблемы остаются:
- Найдите `terminal.integrated.shellIntegration.decorationsEnabled`
- Установите в `false`

### 5. Перезапуск

1. После внесения изменений, закройте все открытые терминалы
2. Перезапустите VS Code (`Ctrl+Shift+P` → "Developer: Reload Window")
3. Откройте новый терминал

## Альтернативное решение: настройка терминала через settings.json

Если через UI не получается, можно отредактировать файл настроек напрямую:

1. Нажмите `Ctrl+Shift+P`
2. Введите "settings json" и выберите "Preferences: Open Settings (JSON)"
3. Добавьте или измените следующие настройки:

```json
{
  "terminal.integrated.shellIntegration.enabled": true,
  "terminal.integrated.shellIntegration.timeout": 60,
  "terminal.integrated.defaultProfile.windows": "PowerShell",
  "terminal.integrated.profiles.windows": {
    "PowerShell": {
      "source": "PowerShell",
      "icon": "terminal-powershell"
    },
    "Command Prompt": {
      "path": [
        "${env:windir}\\Sysnative\\cmd.exe",
        "${env:windir}\\System32\\cmd.exe"
      ],
      "args": [],
      "icon": "terminal-cmd"
    }
  }
}
```

После внесения изменений, перезапустите VS Code и попробуйте снова использовать инструмент execute_command.