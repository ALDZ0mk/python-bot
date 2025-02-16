import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

TOKEN = "توكن_البوت_هنا"
OWNER_USERNAME = "@Hfddhht"  # معرف المالك
CHANNEL_ID = "@YourChannel"  # معرف القناة

bot = Bot(token=TOKEN, parse_mode=types.ParseMode.MARKDOWN)
dp = Dispatcher(bot)

# 🔹 بيانات كل دورة
courses_details = {
    "arabic": "📖 *لغة عربية - حيقون أسامة*\n\n📌 *فصل 1:* 50 ألف (مسجلة)\n📌 *فصل 2:* 60 ألف (لايف + مسجلة)\n💰 *بين زوج:* 100 ألف",
    "english": "🇬🇧 *إنجليزية - جيار*\n\n📌 *سنوي:* 100 ألف\n📌 *فصل 1:* 50 ألف\n📌 *فصل 2:* 60 ألف",
    "french": "🇫🇷 *فرنسية - نجلاء*\n\n📌 *فصل 1:* 50 ألف (مسجلة)\n📌 *فصل 2:* 60 ألف (لايف + مسجلة)\n💰 *بين زوج:* 100 ألف",
    "science": "🔬 *علوم - كتفي*\n\n📌 *ملي بدا عام:* 150 ألف (وحدات 1+2+3 + تربص)\n📌 *دورة وحدة:* 50 ألف",
    "physics": "⚡ *فيزياء - زدون*\n\n📌 *عام كامل:* 250 ألف\n📌 *ملي بدا عام:* 150 ألف\n📌 *بالوحدة:* 50 ألف",
    "math": "📏 *مرنيز*\n\n📌 *Expo + Ln + متتاليات:* 150 ألف\n📌 *للوحدة:* 60 ألف",
    "ski": "📊 *سكي رياضيات*\n\n📌 *ملي بدا عام حتى دوال أصلية:* 150 ألف\n📌 *بالوحدة:* 60 ألف"
}

# 🔹 إنشاء قائمة المواد
def get_courses_menu():
    courses_menu = InlineKeyboardMarkup(row_width=2)
    courses_menu.add(
        InlineKeyboardButton("📖 لغة عربية", callback_data="arabic"),
        InlineKeyboardButton("🇬🇧 إنجليزية", callback_data="english"),
        InlineKeyboardButton("🇫🇷 فرنسية", callback_data="french"),
        InlineKeyboardButton("🔬 علوم", callback_data="science"),
        InlineKeyboardButton("⚡ فيزياء", callback_data="physics"),
        InlineKeyboardButton("📏 مرنيز", callback_data="math"),
        InlineKeyboardButton("📊 سكي رياضيات", callback_data="ski"),
        InlineKeyboardButton("🏠 العودة إلى القائمة الرئيسية", callback_data="main_menu")
    )
    return courses_menu

# 🔹 إرسال المنشور للقناة مع تثبيته تلقائيًا
@dp.message_handler(commands=["post"])
async def send_post_to_channel(message: types.Message):
    if message.from_user.username != OWNER_USERNAME.strip("@"):
        await message.reply("❌ *ليس لديك صلاحية لاستخدام هذا الأمر.*")
        return

    post_text = "📚 *مرحبًا بكم في قائمة الدورات المتاحة!*\n\n💡 اضغط على أي دورة لرؤية التفاصيل:"
    sent_message = await bot.send_message(CHANNEL_ID, post_text, reply_markup=get_courses_menu())
    await bot.pin_chat_message(CHANNEL_ID, sent_message.message_id)  # تثبيت المنشور
    await message.reply("✅ *تم نشر القائمة في القناة وتثبيتها!*")

# 🔹 عرض قائمة الدورات عند الضغط على الزر
@dp.callback_query_handler(lambda call: call.data == "show_courses")
async def show_courses_list(call: types.CallbackQuery):
    await call.message.edit_text("📚 *اختر الدورة لعرض التفاصيل:*", reply_markup=get_courses_menu())

# 🔹 عرض تفاصيل الدورة المختارة
@dp.callback_query_handler(lambda call: call.data in courses_details)
async def show_course_details(call: types.CallbackQuery):
    course_text = courses_details[call.data]
    keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton("📩 الاشتراك", url=f"https://t.me/{OWNER_USERNAME.strip('@')}"),
        InlineKeyboardButton("🔙 رجوع", callback_data="show_courses")
    )
    await call.message.edit_text(course_text, reply_markup=keyboard)

# 🔹 العودة إلى القائمة الرئيسية
@dp.callback_query_handler(lambda call: call.data == "main_menu")
async def back_to_main(call: types.CallbackQuery):
    menu = InlineKeyboardMarkup().add(InlineKeyboardButton("📚 قائمة الدورات المتاحة", callback_data="show_courses"))
    await call.message.edit_text("👋 *مرحبًا بك في بوت الدورات التعليمية!*\n\n🔹 *اضغط على الزر أدناه لعرض القائمة:*", reply_markup=menu)

# 🔹 حماية القناة: تأكد من أن المستخدمين مشتركين قبل التفاعل مع الأزرار
async def check_subscription(user_id):
    member = await bot.get_chat_member(CHANNEL_ID, user_id)
    return member.status in ["member", "administrator", "creator"]

@dp.callback_query_handler(lambda call: call.data.startswith("show_"))
async def check_user_subscription(call: types.CallbackQuery):
    if not await check_subscription(call.from_user.id):
        await call.answer("❌ يجب عليك الاشتراك في القناة أولًا!", show_alert=True)
        return
    await show_courses_list(call)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

