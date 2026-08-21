const mineflayer = require('mineflayer');
const fs = require('fs');
const path = require('path');

// Парсим аргументы командной строки
const [,, ipPort, nickname, password] = process.argv;

if (!ipPort || !nickname) {
    console.error("Ошибка: Укажи IP:PORT и НИКНЕЙМ.");
    console.log("Использование: node index.js <ip:port> <nickname> [password]");
    process.exit(1);
}

// Разделяем IP и PORT
const [host, portStr] = ipPort.split(':');
const port = portStr ? parseInt(portStr) : 25565;

// Файл состояния, чтобы помнить, регистрировались ли мы уже
const stateFile = path.join(__dirname, 'bot_state.json');
let state = { registered: false };
if (fs.existsSync(stateFile)) {
    state = JSON.parse(fs.readFileSync(stateFile, 'utf8'));
}

console.log(`[INFO] Подключение к ${host}:${port} как ${nickname}...`);

const bot = mineflayer.createBot({
    host: host,
    port: port,
    username: nickname,
    version: false // Автоопределение версии
});

// Обработка спавна и авторизации
bot.on('spawn', () => {
    console.log(`[SUCCESS] Бот ${nickname} заспавнился!`);
    
    if (password) {
        if (!state.registered) {
            // Первый вход
            bot.chat(`/register ${password} ${password}`);
            state.registered = true;
            fs.writeFileSync(stateFile, JSON.stringify(state));
            console.log("[AUTH] Выполнена регистрация и сохранена в bot_state.json");
        } else {
            // Последующие входы
            bot.chat(`/login ${password}`);
            console.log("[AUTH] Выполнен вход (login)");
        }
    }
});

// Логи для отладки
bot.on('kicked', (reason) => console.log(`[KICKED] ${reason}`));
bot.on('error', (err) => console.log(`[ERROR] ${err.message}`));

// Если бота выкинуло, падаем с кодом 1, чтобы Python-скрипт понял, что нужно рестартануть
bot.on('end', () => {
    console.log("[DISCONNECT] Соединение разорвано. Завершаю процесс для авто-рестарта...");
    process.exit(1); 
});