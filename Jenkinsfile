pipeline {
    agent any

    environment {
        OPENAI_API_KEY     = credentials('openai-api-key')
        TELEGRAM_BOT_TOKEN = credentials('telegram-bot-token')
    }

    triggers {
        cron('H 9 * * *')
    }

    stages {
        stage('Run bot') {
            steps {
                withCredentials([
                    string(credentialsId: 'telegram-channel-id', variable: 'TELEGRAM_CHANNEL_ID')
                ]) {
                    sh '''
                        source venv/bin/activate || true
                        echo "OPENAI_API_KEY=$OPENAI_API_KEY" > .env
                        echo "TELEGRAM_BOT_TOKEN=$TELEGRAM_BOT_TOKEN" >> .env
                        echo "TELEGRAM_CHANNEL_ID=$TELEGRAM_CHANNEL_ID" >> .env
                        python3 fact_bot.py
                    '''
                }
            }
        }
    }
}