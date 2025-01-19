// config.js
require('dotenv').config();

const config = {
    PORT: process.env.PORT || 3000,
    LANGFLOW_BASE_URL: 'https://api.langflow.astra.datastax.com',
    APPLICATION_TOKEN1: process.env.APPLICATION_TOKEN1,
    FLOW_ID1: '382e470c-ce3e-47ca-9cde-8a011defd2e7',
    LANGFLOW_ID1: 'ea20959c-e978-4007-acb6-3ef685663e7e',

    APPLICATION_TOKEN2: process.env.APPLICATION_TOKEN2,
    FLOW_ID2: '7dee81e7-4b0e-419c-be34-b30a22b01b2c',
    LANGFLOW_ID2: 'ea20959c-e978-4007-acb6-3ef685663e7e',

    APPLICATION_TOKEN3: process.env.APPLICATION_TOKEN3,
    FLOW_ID3: 'b3014750-9b04-4510-bfd4-00bdc2967df5',
    LANGFLOW_ID3: 'ea20959c-e978-4007-acb6-3ef685663e7e',


    TWEAKS: {
        "File-jxj7K": {},
        "SplitText-7gH6I": {},
        "ChatInput-Rpb6P": {},
        "ParseData-EJyoR": {},
        "CombineText-GqK4e": {},
        "TextInput-OUxuk": {},
        "ChatOutput-EPD4q": {},
        "AstraDB-brZ4Z": {},
        "GroqModel-SGvGQ": {}
    }
};

module.exports = config;