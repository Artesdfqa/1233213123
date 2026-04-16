const TelegramBot = require('node-telegram-bot-api');
const https = require('https');

const TOKEN = '8790127741:AAEoajmvEvDShc7vPfrF2L9oMHpfrh2uryQ'; // Замени на свой токен от @BotFather
const bot = new TelegramBot(TOKEN, { polling: true });

// Используем picsum.photos или другой SFW API
async function getRandomGirlImage() {
  // Unsplash source - случайное фото по теме
  const randomSeed = Math.floor(Math.random() * 1000);
  return `https://picsum.photos/seed/${randomSeed}/600/800`;
}

bot.onText(/\/start/, (msg) => {
  bot.sendMessage(msg.chat.id, 
    '👋 Привет! Используй /random чтобы получить случайную картинку.'
  );
});

bot.onText(/\/random/, async (msg) => {
  const chatId = msg.chat.id;
  
  try {
    await bot.sendChatAction(chatId, 'upload_photo');
    
    const imageUrl = await getRandomGirlImage();
    
    await bot.sendPhoto(chatId, imageUrl, {
      caption: '🎲 Случайная картинка!'
    });
  } catch (error) {
    console.error('Ошибка:', error);
    bot.sendMessage(chatId, '❌ Не удалось загрузить картинку. Попробуй ещё раз.');
  }
});

console.log('Бот запущен...');
