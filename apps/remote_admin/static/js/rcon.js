let Rcon = require('srcds-rcon');
let rcon = Rcon({
    address: '192.168.1.10',
    password: 'test'
});
rcon.connect().then(() => {
    console.log('connected');
}).catch(console.error);