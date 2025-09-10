import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

TOKEN = os.getenv("BOT_TOKEN")

ECG_CASES = {
    "Normal Sinus Rhythm": "ECG طبيعي",
    "Sinus Bradycardia": "HR < 60 bpm",
    "Sinus Tachycardia": "HR > 100 bpm",
    "Atrial Fibrillation": "Irregularly irregular rhythm",
    "Atrial Flutter": "Sawtooth waves",
    "1st degree AV block": "PR interval > 200ms",
    "Mobitz I (Wenckebach)": "PR يطول تدريجياً ثم drop",
    "Mobitz II": "PR ثابت مع dropped QRS",
    "Complete Heart Block": "P و QRS غير مرتبطين",
    "STEMI": "ST elevation",
    "NSTEMI": "ST depression",
    "Ventricular Tachycardia": "Wide QRS tachycardia",
    "Ventricular Fibrillation": "Chaotic rhythm",
    "PAC": "P wave مبكرة",
    "PVC": "QRS عريض مبكر",
    "Asystole": "خط مستقيم",
    "Torsades de Pointes": "Polymorphic VT",
    "Hyperkalemia": "Tall peaked T waves",
    "Hypokalemia": "U waves",
    "WPW Syndrome": "Delta wave",
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📚 Learn", callback_data="learn")],
        [InlineKeyboardButton("📝 Quiz", callback_data="quiz")],
        [InlineKeyboardButton("📖 References", callback_data="refs")],
        [InlineKeyboardButton("🖼 Images", callback_data="images")],
        [InlineKeyboardButton("🎥 Videos", callback_data="videos")],
        [InlineKeyboardButton("🫀 Cases", callback_data="cases")],
        [InlineKeyboardButton("⚡ Practice", callback_data="practice")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("أهلاً 👋\nاختر من القائمة:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "learn":
        await query.edit_message_text("📚 قسم التعلم:\nمقدمة في ECG + أساسيات القراءة.")
    elif query.data == "quiz":
        await query.edit_message_text("📝 اختبار سريع:\nWhat is the diagnosis of this ECG?\nخيارات: Atrial Fib, VT, Normal.")
    elif query.data == "refs":
        await query.edit_message_text("📖 المراجع:\n1. Thaler - The Only EKG Book You'll Ever Need\n2. Dubin - Rapid Interpretation of EKGs")
    elif query.data == "images":
        await query.edit_message_text("🖼 صور تعليمية ECG (مثال: imgur links).")
    elif query.data == "videos":
        await query.edit_message_text("🎥 فيديوهات شرح ECG على YouTube.")
    elif query.data == "cases":
        text = "🫀 الحالات المتوفرة:\n\n" + "\n".join(f"- {case}" for case in ECG_CASES.keys())
        await query.edit_message_text(text)
    elif query.data == "practice":
        await query.edit_message_text("⚡ قسم التدريب العملي:\nاختر حالة وسيعطيك ECG عشوائي للتشخيص.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()

if __name__ == "__main__":
    main()
