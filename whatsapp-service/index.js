const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const axios = require('axios');

const client = new Client({
    authStrategy: new LocalAuth()
});

client.on('qr', (qr) => {
    qrcode.generate(qr, { small: true });
});

client.on('ready', () => {
    console.log('WhatsApp Ready');
});

client.on('message', async (message) => {

    try {

        console.log('Message:', message.body);

        const response = await axios.post(
            'http://127.0.0.1:8000/chat',
            {
                phone: message.from,
                text: message.body
            }
        );

        await message.reply(
            response.data.reply
        );

    } catch (error) {

    console.log(error.response?.data || error.message);

    if (error.response?.data?.reply) {

        await message.reply(error.response.data.reply);

    } else {

        await message.reply(
            "عذراً، الخدمة غير متاحة حالياً، يرجى المحاولة لاحقاً."
        );
    }
}
});

client.initialize();