import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Replace with your own API key and Telegram bot token
API_KEY = '76c04bb2ed09436c8d5fef2946546c61'
TELEGRAM_TOKEN = '7727269658:AAE33_AHWPdKPjCVaUsIghk4j4EJJ3H5RCw'
API_URL = 'https://api.football-data.org/v4/competitions/CL/matches'  # Updated to v4

def get_matches():
    headers = {'X-Auth-Token': API_KEY}
    response = requests.get(API_URL, headers=headers)
    return response.json()

async def matches(update: Update, context: ContextTypes.DEFAULT_TYPE):
    matches = get_matches()
    # Check if there are matches
    if 'matches' in matches and matches['matches']:
        current_matches = [match for match in matches['matches'] if match['status'] == 'IN_PLAY']
        if current_matches:
            messages = []
            for match in current_matches:
                home_team = match['homeTeam']['name']
                away_team = match['awayTeam']['name']
                home_score = match['score']['fullTime']['home'] if 'fullTime' in match['score'] else 'N/A'
                away_score = match['score']['fullTime']['away'] if 'fullTime' in match['score'] else 'N/A'
                
                # Add emojis and format the message
                message = f"⚽️ {home_team} vs {away_team} \n" \
                          f"🏟️ Score: {home_score} : {away_score} \n" \
                          f"📅 Status: In Play"
                messages.append(message)
            await update.message.reply_text("\n\n".join(messages), parse_mode='Markdown')
        else:
            await update.message.reply_text("❌ No current matches found.")
    else:
        await update.message.reply_text("❌ No matches found.")

def main():
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Add the /matches command handler
    application.add_handler(CommandHandler("matches", matches))

    application.run_polling()

if __name__ == '__main__':
    main()


