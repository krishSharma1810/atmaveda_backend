// config.js
require('dotenv').config();

const config = {
    PORT: process.env.PORT || 3000,
    LANGFLOW_BASE_URL: 'https://api.langflow.astra.datastax.com',
    APPLICATION_TOKEN: process.env.APPLICATION_TOKEN,
    FLOW_ID: '382e470c-ce3e-47ca-9cde-8a011defd2e7',
    LANGFLOW_ID: 'ea20959c-e978-4007-acb6-3ef685663e7e',
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