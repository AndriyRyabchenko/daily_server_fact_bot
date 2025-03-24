pipeline {
    agent any

    environment {
        OPENAI_API_KEY     = credentials('openai-api-key')
        TELEGRAM_BOT_TOKEN = credentials('telegram-bot-token')
    }

    triggers {
        cron('0 9 * * *')
    }

    stages {
        stage('Install deps') {
            steps {
                sh '''
                    python3 -m venv venv
                    ./venv/bin/pip install --upgrade pip
                    ./venv/bin/pip install -r requirements.txt || ./venv/bin/pip install openai python-telegram-bot python-dotenv
                '''
            }
        }

        stage('Run bot') {
            steps {
                withCredentials([
                    string(credentialsId: 'telegram-channel-id', variable: 'TELEGRAM_CHANNEL_ID')
                ]) {
                    sh '''
                        echo "OPENAI_API_KEY=$OPENAI_API_KEY" > .env
                        echo "TELEGRAM_BOT_TOKEN=$TELEGRAM_BOT_TOKEN" >> .env
                        echo "TELEGRAM_CHANNEL_ID=$TELEGRAM_CHANNEL_ID" >> .env
                        ./venv/bin/python3 fact_bot.py
                    '''
                }
            }
        }
    }

    post {
        success {
            echo '✅ Факт успішно надіслано!'
        }
        failure {
            echo '❌ Помилка! Бот не зміг завершити роботу.'
        }
    }
}