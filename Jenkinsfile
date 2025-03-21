pipeline {
    agent any

    environment {
        // Завантажуємо змінні з .env (лише якщо Jenkins дозволяє це)
        // Інакше – прописати ключі напряму тут
        OPENAI_API_KEY     = credentials('openai-api-key')       // створити у Jenkins credentials
        TELEGRAM_BOT_TOKEN = credentials('telegram-bot-token')   // так само
        TELEGRAM_CHANNEL_ID = '@твій_канал'                      // або через credentials
    }

    triggers {
        cron('H 9 * * *')  // щодня о 9:00 ранку
    }

    stages {
        stage('Setup Python') {
            steps {
                sh '''
                python3 -m venv venv
                source venv/bin/activate
                pip install -r requirements.txt || pip install python-telegram-bot openai python-dotenv
                '''
            }
        }

        stage('Run bot') {
            steps {
                sh '''
                source venv/bin/activate
                echo "OPENAI_API_KEY=$OPENAI_API_KEY" > .env
                echo "TELEGRAM_BOT_TOKEN=$TELEGRAM_BOT_TOKEN" >> .env
                echo "TELEGRAM_CHANNEL_ID=$TELEGRAM_CHANNEL_ID" >> .env
                python3 fact_bot.py
                '''
            }
        }
    }

    post {
        failure {
            echo '❌ Помилка при запуску бота!'
        }
        success {
            echo '✅ Факт успішно надіслано!'
        }
    }
}