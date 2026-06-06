import streamlit as st

TEXTS = {
    "ar": {
        "app_title": "لوحة ذهب ذكية",
        "app_subtitle": "إدارة محفظة الذهب الشخصية",
        "language": "اللغة",
        "nav_overview": "📊 نظرة عامة",
        "nav_gold_bars": "🪙 سبائك الذهب",
        "nav_analytics": "التحليلات والرسوم",
        "nav_forecasting": "التوقعات",
        "nav_shared_ownership": "🤝 الملكية المشتركة",
        "wallet_balance": "محفظة الذهب",
        "gold_today": "سعر الذهب اليوم",
        "price_change_today": "تغير اليوم",
        "portfolio_trend": "مسار المحفظة",
        "sort_by": "ترتيب حسب",
        "sort_date": "التاريخ",
        "sort_profit": "الربح/الخسارة",
        "sort_value": "القيمة",
        "sort_grams": "الوزن",
        "export_portfolio": "تصدير المحفظة",
        "export_csv": "تحميل CSV",
        "export_excel": "تحميل Excel",
        "no_bars_title": "ابدأ محفظتك الذهبية",
        "no_bars_hint": "اضغط الزر أدناه لإضافة أول سبيكة وتتبع استثمارك",
        "add_first_bar": "➕ إضافة أول سبيكة",
        "current_gold_price": "سعر الذهب الحالي",
        "per_gram": "للغرام",
        "per_ounce": "للأونصة",
        "ounce_equals_grams": "الأونصة = {grams} جرام",
        "price_stale": "السعر قديم — آخر تحديث",
        "price_unavailable": "تعذر جلب السعر — يتم استخدام آخر سعر محفوظ",
        "total_gold": "⚖️ إجمالي الذهب",
        "total_cost": "💰 إجمالي التكلفة",
        "current_value": "💎 القيمة الحالية",
        "total_profit_loss": "📈 إجمالي الربح/الخسارة",
        "return_pct": "📊 نسبة العائد",
        "num_bars": "🪙 عدد السبائك",
        "avg_cost_per_gram": "⚖️ متوسط التكلفة للغرام",
        "grams": "الجرامات",
        "purchase_date": "تاريخ الشراء",
        "bar_type": "شكل السبيكة",
        "purchase_price": "سعر الشراء (الإجمالي)",
        "purchase_price_help": "السعر الكامل لجميع الجرامات وليس للغرام الواحد",
        "cost_per_gram": "التكلفة للغرام",
        "profit_loss": "الربح/الخسارة",
        "ownership_pct": "نسبة الملكية",
        "notes": "ملاحظات",
        "actions": "إجراءات",
        "search": "بحث",
        "filter_bar_type": "تصفية حسب الشكل",
        "all_types": "جميع الأشكال",
        "add_bar": "إضافة سبيكة",
        "edit_bar": "تعديل سبيكة",
        "delete_bar": "حذف سبيكة",
        "save": "حفظ",
        "cancel": "إلغاء",
        "delete": "حذف",
        "confirm_delete": "هل أنت متأكد من حذف هذه السبيكة؟",
        "bar_added": "تمت إضافة السبيكة بنجاح",
        "bar_updated": "تم تحديث السبيكة بنجاح",
        "bar_deleted": "تم حذف السبيكة بنجاح",
        "shared_ownership": "ملكية مشتركة",
        "participants": "المشاركون",
        "participant_name": "اسم المشارك",
        "add_participant": "إضافة مشارك",
        "remove_participant": "إزالة",
        "participants_sum_error": "يجب أن يكون مجموع نسب المشاركين 100%",
        "ownership_range_error": "نسبة الملكية يجب أن تكون بين 1 و 100",
        "required_fields_error": "يرجى ملء جميع الحقول المطلوبة",
        "no_bars": "لا توجد سبائك بعد. أضف أول سبيكة للبدء.",
        "best_performing": "أفضل سبيكة أداءً",
        "worst_performing": "أسوأ سبيكة أداءً",
        "most_expensive": "أغلى عملية شراء",
        "cheapest": "أرخص عملية شراء",
        "profit": "الربح",
        "loss": "الخسارة",
        "you_gained": "ربحت",
        "you_lost": "خسرت",
        "chart_invested_capital": "نمو رأس المال المستثمر",
        "chart_portfolio_value": "القيمة الحالية للمحفظة",
        "chart_gold_distribution": "توزيع الذهب حسب الوزن",
        "chart_shape_distribution": "توزيع الذهب حسب الشكل",
        "chart_profit_distribution": "توزيع الربح/الخسارة",
        "invested_capital": "رأس المال المستثمر",
        "portfolio_value": "قيمة المحفظة",
        "forecast_title": "سيناريوهات أسعار الذهب",
        "forecast_subtitle": "اختبر قيمة محفظتك عند أسعار مستقبلية مختلفة",
        "target_price": "السعر المستهدف (للغرام)",
        "forecast_value": "قيمة المحفظة",
        "forecast_profit": "الربح المتوقع",
        "forecast_return": "نسبة العائد",
        "custom_price": "سعر مخصص (للغرام)",
        "forecast_key_scenarios": "أبرز السيناريوهات",
        "forecast_all_scenarios": "كل الأسعار المحتملة",
        "sell_today": "لو بعت بسعر اليوم",
        "if_gold_reaches": "لو وصل الذهب إلى",
        "forecast_custom_result": "النتيجة عند سعرك المخصص",
        "at_price": "عند سعر",
        "total_invested": "إجمالي الاستثمار",
        "current_price": "السعر الحالي للغرام",
        "shared_title": "الملكية المشتركة",
        "shared_subtitle": "تفاصيل السبائك المملوكة بشكل مشترك",
        "participant": "المشارك",
        "cost": "التكلفة",
        "no_shared_bars": "لا توجد سبائك بملكية مشتركة",
        "my_share": "حصتي",
        "full_bar": "السبيكة كاملة",
        "edit": "تعديل",
        "select_bar_to_edit": "اختر سبيكة للتعديل",
        "select_bar_to_delete": "اختر سبيكة للحذف",
        "last_updated": "آخر تحديث",
        "saudi_time": "بتوقيت السعودية",
        "refresh_price": "تحديث السعر",
        "privacy_mode": "وضع الخصوصية",
        "privacy_mode_hint": "إخفاء المبالغ والأرقام الحساسة عند المشاركة",
        "privacy_active": "🔒 وضع الخصوصية مفعّل — المبالغ مخفية",
        "api_key_missing": "مفتاح API غير موجود — أضف GOLD_API_KEY في ملف .env",
        "api_quota_exceeded": "انتهت حصة GoldAPI الشهرية — يتم عرض آخر سعر محفوظ. رقّي خطتك على goldapi.io أو انتظر بداية الشهر.",
        "api_invalid_key": "مفتاح GoldAPI غير صالح — تحقق من GOLD_API_KEY في ملف .env",
        "api_network_error": "تعذر الاتصال بـ GoldAPI — تحقق من الإنترنت وحاول مرة أخرى",
        "api_fetch_failed": "تعذر جلب السعر من GoldAPI — يتم عرض آخر سعر محفوظ",
        "api_usage_title": "استخدام GoldAPI",
        "api_usage_month": "طلبات هذا الشهر",
        "api_usage_total": "إجمالي الطلبات",
        "api_usage_last_ok": "آخر طلب: نجح",
        "api_usage_last_fail": "آخر طلب: فشل",
        "api_usage_limit_hint": "الحصة المجانية تقريباً {limit} طلب/شهر",
        "monthly_sell_title": "توقعات البيع الشهرية",
        "monthly_sell_subtitle": "لو بعت في بداية كل شهر — كم كنت تملك وكم ربحت أو خسرت",
        "monthly_sell_grams": "الغرامات المملوكة",
        "monthly_sell_price": "سعر الغرام",
        "monthly_sell_value": "قيمة البيع",
        "monthly_sell_month": "الشهر",
        "monthly_sell_no_data": "لا توجد بيانات كافية لعرض التوقعات الشهرية",
        "monthly_sell_price_missing": "تعذر جلب بعض الأسعار التاريخية — تأكد من مفتاح GoldAPI",
        "month_jan": "يناير",
        "month_feb": "فبراير",
        "month_mar": "مارس",
        "month_apr": "أبريل",
        "month_may": "مايو",
        "month_jun": "يونيو",
        "month_jul": "يوليو",
        "month_aug": "أغسطس",
        "month_sep": "سبتمبر",
        "month_oct": "أكتوبر",
        "month_nov": "نوفمبر",
        "month_dec": "ديسمبر",
        "login": "تسجيل الدخول",
        "logout": "تسجيل الخروج",
        "username": "اسم المستخدم",
        "password": "كلمة المرور",
        "login_subtitle": "سجّل دخولك لإدارة محفظتك الذهبية",
        "login_required": "يرجى إدخال اسم المستخدم وكلمة المرور",
        "login_failed": "اسم المستخدم أو كلمة المرور غير صحيحة",
        "logged_in_as": "مسجّل كـ",
        "nav_admin": "⚙️ إدارة المستخدمين",
        "admin_subtitle": "إضافة وحذف المستخدمين وإدارة الحسابات",
        "admin_users_list": "المستخدمون",
        "admin_no_users": "لا يوجد مستخدمون",
        "admin_add_user": "إضافة مستخدم جديد",
        "admin_is_admin": "مدير (صلاحيات كاملة)",
        "admin_role_admin": "مدير",
        "admin_role_user": "مستخدم",
        "admin_you": "أنت",
        "admin_user_created": "تم إنشاء المستخدم بنجاح",
        "admin_user_deleted": "تم حذف المستخدم",
        "admin_username_taken": "اسم المستخدم مستخدم مسبقاً",
        "admin_password_short": "كلمة المرور يجب أن تكون 6 أحرف على الأقل",
        "admin_create_failed": "تعذر إنشاء المستخدم",
        "admin_forbidden": "ليس لديك صلاحية الوصول لهذه الصفحة",
        "admin_change_password": "تغيير كلمة المرور",
        "current_password": "كلمة المرور الحالية",
        "new_password": "كلمة المرور الجديدة",
        "confirm_password": "تأكيد كلمة المرور",
        "admin_update_password": "تحديث كلمة المرور",
        "admin_wrong_password": "كلمة المرور الحالية غير صحيحة",
        "admin_password_mismatch": "كلمتا المرور غير متطابقتين",
        "admin_password_updated": "تم تحديث كلمة المرور بنجاح",
    },
    "en": {
        "app_title": "Smart Gold Dashboard",
        "app_subtitle": "Personal gold portfolio management",
        "language": "Language",
        "nav_overview": "📊 Overview",
        "nav_gold_bars": "🪙 Gold Bars",
        "nav_analytics": "Analytics & Charts",
        "nav_forecasting": "Forecasting",
        "nav_shared_ownership": "🤝 Shared Ownership",
        "wallet_balance": "Gold Wallet",
        "gold_today": "Gold today",
        "price_change_today": "Today's change",
        "portfolio_trend": "Portfolio trend",
        "sort_by": "Sort by",
        "sort_date": "Date",
        "sort_profit": "Profit/Loss",
        "sort_value": "Value",
        "sort_grams": "Weight",
        "export_portfolio": "Export Portfolio",
        "export_csv": "Download CSV",
        "export_excel": "Download Excel",
        "no_bars_title": "Start your gold wallet",
        "no_bars_hint": "Click the button below to add your first bar and track your investment",
        "add_first_bar": "➕ Add your first bar",
        "current_gold_price": "Current Gold Price",
        "per_gram": "per gram",
        "per_ounce": "per ounce",
        "ounce_equals_grams": "1 oz = {grams} g",
        "price_stale": "Stale price — last updated",
        "price_unavailable": "Could not fetch price — using last cached value",
        "total_gold": "⚖️ Total Gold",
        "total_cost": "💰 Total Cost",
        "current_value": "💎 Current Value",
        "total_profit_loss": "📈 Total Profit/Loss",
        "return_pct": "📊 Return %",
        "num_bars": "🪙 Number of Bars",
        "avg_cost_per_gram": "⚖️ Avg Cost per Gram",
        "grams": "Grams",
        "purchase_date": "Purchase Date",
        "bar_type": "Bar Shape",
        "purchase_price": "Purchase Price (Total)",
        "purchase_price_help": "Total price for all grams, not per gram",
        "cost_per_gram": "Cost per Gram",
        "profit_loss": "Profit/Loss",
        "ownership_pct": "Ownership %",
        "notes": "Notes",
        "actions": "Actions",
        "search": "Search",
        "filter_bar_type": "Filter by shape",
        "all_types": "All shapes",
        "add_bar": "Add Gold Bar",
        "edit_bar": "Edit Gold Bar",
        "delete_bar": "Delete Gold Bar",
        "save": "Save",
        "cancel": "Cancel",
        "delete": "Delete",
        "confirm_delete": "Are you sure you want to delete this bar?",
        "bar_added": "Gold bar added successfully",
        "bar_updated": "Gold bar updated successfully",
        "bar_deleted": "Gold bar deleted successfully",
        "shared_ownership": "Shared Ownership",
        "participants": "Participants",
        "participant_name": "Participant Name",
        "add_participant": "Add Participant",
        "remove_participant": "Remove",
        "participants_sum_error": "Participant percentages must sum to 100%",
        "ownership_range_error": "Ownership must be between 1 and 100",
        "required_fields_error": "Please fill all required fields",
        "no_bars": "No gold bars yet. Add your first bar to get started.",
        "best_performing": "Best Performing Bar",
        "worst_performing": "Worst Performing Bar",
        "most_expensive": "Most Expensive Purchase",
        "cheapest": "Cheapest Purchase",
        "profit": "Profit",
        "loss": "Loss",
        "you_gained": "You gained",
        "you_lost": "You lost",
        "chart_invested_capital": "Invested Capital Growth",
        "chart_portfolio_value": "Current Portfolio Value",
        "chart_gold_distribution": "Gold Distribution by Weight",
        "chart_shape_distribution": "Gold Distribution by Shape",
        "chart_profit_distribution": "Profit/Loss Distribution",
        "invested_capital": "Invested Capital",
        "portfolio_value": "Portfolio Value",
        "forecast_title": "Gold Price Scenarios",
        "forecast_subtitle": "Test your portfolio value at different future prices",
        "target_price": "Target Price (per gram)",
        "forecast_value": "Portfolio Value",
        "forecast_profit": "Expected Profit",
        "forecast_return": "Return %",
        "custom_price": "Custom Price (per gram)",
        "forecast_key_scenarios": "Key Scenarios",
        "forecast_all_scenarios": "All Possible Prices",
        "sell_today": "If you sell at today's price",
        "if_gold_reaches": "If gold reaches",
        "forecast_custom_result": "Result at your custom price",
        "at_price": "at",
        "total_invested": "Total Invested",
        "current_price": "Current Price per Gram",
        "shared_title": "Shared Ownership",
        "shared_subtitle": "Details of jointly owned gold bars",
        "participant": "Participant",
        "cost": "Cost",
        "no_shared_bars": "No shared ownership bars",
        "my_share": "My Share",
        "full_bar": "Full Bar",
        "edit": "Edit",
        "select_bar_to_edit": "Select bar to edit",
        "select_bar_to_delete": "Select bar to delete",
        "last_updated": "Last updated",
        "saudi_time": "Saudi Arabia time",
        "refresh_price": "Refresh Price",
        "privacy_mode": "Privacy Mode",
        "privacy_mode_hint": "Hide sensitive amounts when sharing your screen",
        "privacy_active": "🔒 Privacy mode on — amounts are hidden",
        "api_key_missing": "API key missing — add GOLD_API_KEY to .env file",
        "api_quota_exceeded": "GoldAPI monthly quota exceeded — showing last cached price. Upgrade at goldapi.io or wait for next month.",
        "api_invalid_key": "Invalid GoldAPI key — check GOLD_API_KEY in your .env file",
        "api_network_error": "Could not reach GoldAPI — check your internet connection and try again",
        "api_fetch_failed": "Could not fetch price from GoldAPI — showing last cached price",
        "api_usage_title": "GoldAPI Usage",
        "api_usage_month": "Requests this month",
        "api_usage_total": "Total requests",
        "api_usage_last_ok": "Last request: success",
        "api_usage_last_fail": "Last request: failed",
        "api_usage_limit_hint": "Free tier is about {limit} requests/month",
        "monthly_sell_title": "Monthly Sell Projection",
        "monthly_sell_subtitle": "If you sold at the start of each month — grams owned and profit/loss",
        "monthly_sell_grams": "Grams Owned",
        "monthly_sell_price": "Price per Gram",
        "monthly_sell_value": "Sell Value",
        "monthly_sell_month": "Month",
        "monthly_sell_no_data": "Not enough data to show monthly projections",
        "monthly_sell_price_missing": "Could not fetch some historical prices — check your GoldAPI key",
        "month_jan": "January",
        "month_feb": "February",
        "month_mar": "March",
        "month_apr": "April",
        "month_may": "May",
        "month_jun": "June",
        "month_jul": "July",
        "month_aug": "August",
        "month_sep": "September",
        "month_oct": "October",
        "month_nov": "November",
        "month_dec": "December",
        "login": "Log in",
        "logout": "Log out",
        "username": "Username",
        "password": "Password",
        "login_subtitle": "Sign in to manage your gold portfolio",
        "login_required": "Please enter username and password",
        "login_failed": "Invalid username or password",
        "logged_in_as": "Signed in as",
        "nav_admin": "⚙️ User Management",
        "admin_subtitle": "Add, remove, and manage user accounts",
        "admin_users_list": "Users",
        "admin_no_users": "No users found",
        "admin_add_user": "Add new user",
        "admin_is_admin": "Administrator (full access)",
        "admin_role_admin": "Admin",
        "admin_role_user": "User",
        "admin_you": "You",
        "admin_user_created": "User created successfully",
        "admin_user_deleted": "User deleted",
        "admin_username_taken": "Username is already taken",
        "admin_password_short": "Password must be at least 6 characters",
        "admin_create_failed": "Could not create user",
        "admin_forbidden": "You do not have permission to access this page",
        "admin_change_password": "Change password",
        "current_password": "Current password",
        "new_password": "New password",
        "confirm_password": "Confirm password",
        "admin_update_password": "Update password",
        "admin_wrong_password": "Current password is incorrect",
        "admin_password_mismatch": "Passwords do not match",
        "admin_password_updated": "Password updated successfully",
    },
}

MONTH_KEYS = [
    "month_jan",
    "month_feb",
    "month_mar",
    "month_apr",
    "month_may",
    "month_jun",
    "month_jul",
    "month_aug",
    "month_sep",
    "month_oct",
    "month_nov",
    "month_dec",
]


def get_lang() -> str:
    if "lang" not in st.session_state:
        st.session_state.lang = "ar"
    return st.session_state.lang


def t(key: str) -> str:
    lang = get_lang()
    return TEXTS.get(lang, TEXTS["ar"]).get(key, key)


def format_month_label(month_start, lang: str | None = None) -> str:
    from datetime import date

    if lang is None:
        lang = get_lang()
    if not isinstance(month_start, date):
        return str(month_start)
    month_name = t(MONTH_KEYS[month_start.month - 1])
    return f"{month_name} {month_start.year}"


def apply_rtl_css():
    lang = get_lang()
    direction = "rtl" if lang == "ar" else "ltr"
    text_align = "right" if lang == "ar" else "left"
    flex_justify = "flex-end" if lang == "ar" else "flex-start"
    font_family = (
        "'Cairo', 'Tajawal', 'Noto Sans Arabic', sans-serif"
        if lang == "ar"
        else "'Inter', sans-serif"
    )
    sidebar_layout_css = ""
    if lang == "ar":
        sidebar_layout_css = """
        [data-testid="stAppViewContainer"] {
            flex-direction: row-reverse !important;
        }
        [data-testid="stSidebar"] {
            border-left: 1px solid rgba(250, 250, 250, 0.15);
            border-right: none !important;
        }
        [data-testid="stSidebar"][aria-expanded="false"] {
            clip-path: inset(0 100% 0 0) !important;
        }
        [data-testid="stSidebarHeader"] {
            flex-direction: row-reverse !important;
        }
        [data-testid="stSidebarCollapseButton"] {
            margin-left: 0 !important;
            margin-right: 0 !important;
        }
        [data-testid="stToolbar"] > div > div:first-child {
            order: 2 !important;
            margin-left: auto !important;
            margin-right: 0.25rem !important;
            width: auto !important;
            min-width: auto !important;
        }
        [data-testid="stToolbar"] > div > div:last-child {
            order: 3 !important;
            margin-left: 0 !important;
        }
        """

    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&family=Inter:wght@400;600;700&display=swap');
        .stApp {{
            font-family: {font_family};
            overflow-x: hidden;
        }}
        section.main,
        .main {{
            direction: {direction};
            text-align: {text_align};
        }}
        .block-container {{
            max-width: 1100px;
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }}
        {sidebar_layout_css}
        [data-testid="stSidebar"] {{
            direction: {direction};
            text-align: {text_align};
            background: linear-gradient(180deg, #12121f 0%, #1a1a2e 100%);
            overflow: hidden !important;
        }}
        [data-testid="stSidebar"] > div,
        [data-testid="stSidebarUserContent"],
        [data-testid="stSidebarContent"] {{
            overflow-x: hidden !important;
            overflow-wrap: anywhere;
            word-break: break-word;
        }}
        [data-testid="stSidebar"][aria-expanded="false"] {{
            min-width: 0 !important;
            max-width: 0 !important;
            width: 0 !important;
            overflow: hidden !important;
            border: none !important;
            padding: 0 !important;
            margin: 0 !important;
        }}
        [data-testid="stSidebar"][aria-expanded="false"] > div,
        [data-testid="stSidebar"][aria-expanded="false"] [data-testid="stSidebarUserContent"],
        [data-testid="stSidebar"][aria-expanded="false"] [data-testid="stSidebarContent"] {{
            display: none !important;
            width: 0 !important;
            min-width: 0 !important;
            overflow: hidden !important;
            opacity: 0 !important;
            pointer-events: none !important;
            visibility: hidden !important;
        }}
        h1, h2, h3, h4, h5, h6 {{
            text-align: {text_align};
            font-weight: 700;
        }}
        .block-container > div:first-child {{
            text-align: {text_align};
        }}
        .stMarkdown p {{
            text-align: {text_align};
        }}
        .section-header {{
            color: #d4af37;
            font-size: 1.15rem;
            font-weight: 700;
            margin: 1.5rem 0 1rem 0;
            padding-bottom: 0.4rem;
            border-bottom: 2px solid rgba(212, 175, 55, 0.35);
            text-align: {text_align};
        }}
        .hero-balance {{
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #1a1a2e 100%);
            border: 1px solid rgba(212, 175, 55, 0.45);
            border-radius: 18px;
            padding: 1.6rem 1.8rem;
            margin-bottom: 1rem;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35), 0 0 0 1px rgba(212, 175, 55, 0.08);
        }}
        .hero-balance-label {{
            color: #a0a0b0;
            font-size: 0.9rem;
            font-weight: 600;
            margin-bottom: 0.4rem;
            letter-spacing: 0.02em;
        }}
        .hero-balance-value {{
            color: #ffffff;
            font-size: 2.4rem;
            font-weight: 700;
            margin-bottom: 0.75rem;
            direction: ltr;
            text-align: {text_align};
            unicode-bidi: plaintext;
            line-height: 1.2;
        }}
        .hero-balance-value.profit {{
            color: #2ecc71;
        }}
        .hero-balance-value.loss {{
            color: #e74c3c;
        }}
        .hero-balance-row {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.6rem;
            align-items: center;
            margin-bottom: 0.5rem;
        }}
        .hero-gold-line {{
            color: #b0b0c0;
            font-size: 0.85rem;
            margin-top: 0.5rem;
            direction: ltr;
            text-align: {text_align};
            unicode-bidi: plaintext;
        }}
        .hero-gold-line .gold-up {{
            color: #2ecc71;
            font-weight: 600;
        }}
        .hero-gold-line .gold-down {{
            color: #e74c3c;
            font-weight: 600;
        }}
        .gold-change-line {{
            margin: 0.4rem 0 0.65rem 0;
            font-size: 0.9rem;
            color: #b0b0c0;
            direction: {direction};
            text-align: {text_align};
        }}
        .gold-change-pill {{
            display: inline-block;
            margin-top: 0.25rem;
            padding: 0.35rem 0.85rem;
            border-radius: 999px;
            font-size: 0.92rem;
            font-weight: 700;
            direction: ltr;
            unicode-bidi: plaintext;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}
        .gold-change-pill.up {{
            color: #2ecc71;
            background: rgba(46, 204, 113, 0.16);
            border: 1px solid rgba(46, 204, 113, 0.4);
            box-shadow: 0 0 14px rgba(46, 204, 113, 0.15);
        }}
        .gold-change-pill.down {{
            color: #e74c3c;
            background: rgba(231, 76, 60, 0.16);
            border: 1px solid rgba(231, 76, 60, 0.4);
            box-shadow: 0 0 14px rgba(231, 76, 60, 0.15);
        }}
        .empty-state {{
            text-align: center;
            padding: 3rem 2rem;
            background: linear-gradient(145deg, #1a1a2e 0%, #12121f 100%);
            border: 1px dashed rgba(212, 175, 55, 0.35);
            border-radius: 16px;
            margin: 2rem 0;
        }}
        .empty-state-icon {{
            font-size: 3.5rem;
            margin-bottom: 1rem;
        }}
        .empty-state-title {{
            color: #d4af37;
            font-size: 1.3rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }}
        .empty-state-hint {{
            color: #9090a0;
            font-size: 0.95rem;
        }}
        .metric-card {{
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            border-radius: 12px;
            padding: 1rem;
            border: 1px solid #d4af37;
        }}
        .gold-header {{
            color: #d4af37;
            font-weight: 700;
        }}
        .bar-card {{
            background: linear-gradient(145deg, #1a1a2e 0%, #12121f 100%);
            border: 1px solid rgba(212, 175, 55, 0.25);
            border-radius: 14px;
            padding: 1rem 1.1rem;
            margin-bottom: 1rem;
            min-height: 120px;
            transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
        }}
        .bar-card.summary-card {{
            display: flex;
            flex-direction: column;
            height: 132px;
            min-height: 132px;
            margin-bottom: 0.75rem;
            box-sizing: border-box;
        }}
        .bar-card.summary-card .bar-card-title {{
            font-size: 0.88rem;
            line-height: 1.3;
            min-height: 2.4rem;
            margin-bottom: 0.25rem;
        }}
        .bar-card.summary-card .bar-card-price {{
            flex: 1;
            display: flex;
            align-items: center;
            justify-content: {flex_justify};
            font-size: 1.35rem;
            margin-bottom: 0;
            line-height: 1.2;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            direction: ltr;
            text-align: {text_align};
            unicode-bidi: plaintext;
            width: 100%;
        }}
        .bar-card-badge-slot {{
            min-height: 1.9rem;
            display: flex;
            align-items: flex-end;
            justify-content: {flex_justify};
            width: 100%;
        }}
        .bar-card-badge-spacer {{
            display: inline-block;
            height: 1.75rem;
            visibility: hidden;
        }}
        .bar-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3), 0 0 12px rgba(212, 175, 55, 0.12);
            border-color: rgba(212, 175, 55, 0.45);
        }}
        .bar-card-title {{
            color: #e8e8e8;
            font-size: 0.95rem;
            font-weight: 600;
            margin-bottom: 0.35rem;
        }}
        .bar-card-price {{
            color: #ffffff;
            font-size: 1.65rem;
            font-weight: 700;
            margin-bottom: 0.6rem;
            direction: ltr;
            text-align: {text_align};
            unicode-bidi: plaintext;
        }}
        .bar-card-price.profit {{
            color: #2ecc71;
        }}
        .bar-card-price.loss {{
            color: #e74c3c;
        }}
        .bar-card-badge {{
            display: inline-block;
            padding: 0.3rem 0.75rem;
            border-radius: 999px;
            font-size: 0.82rem;
            font-weight: 600;
            unicode-bidi: plaintext;
        }}
        .bar-card-badge.neutral {{
            background: rgba(212, 175, 55, 0.12);
            color: #d4af37;
            border: 1px solid rgba(212, 175, 55, 0.3);
        }}
        .bar-card-badge.profit {{
            background: rgba(46, 204, 113, 0.18);
            color: #2ecc71;
            border: 1px solid rgba(46, 204, 113, 0.35);
        }}
        .bar-card-badge.loss {{
            background: rgba(231, 76, 60, 0.18);
            color: #e74c3c;
            border: 1px solid rgba(231, 76, 60, 0.35);
        }}
        .forecast-card {{
            display: flex;
            flex-direction: column;
            gap: 0.15rem;
        }}
        .forecast-card.featured {{
            border-color: rgba(212, 175, 55, 0.55);
            background: linear-gradient(145deg, #20203a 0%, #16162a 100%);
            box-shadow: 0 6px 22px rgba(0, 0, 0, 0.28), 0 0 0 1px rgba(212, 175, 55, 0.12);
        }}
        .forecast-card-tag {{
            display: inline-block;
            align-self: flex-start;
            color: #d4af37;
            background: rgba(212, 175, 55, 0.12);
            border: 1px solid rgba(212, 175, 55, 0.3);
            padding: 0.15rem 0.6rem;
            border-radius: 999px;
            font-size: 0.78rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
            unicode-bidi: plaintext;
        }}
        .forecast-card .bar-card-price {{
            font-size: 1.5rem;
            margin-bottom: 0.5rem;
        }}
        [data-testid="stMetric"] {{
            direction: {direction};
            text-align: {text_align};
        }}
        [data-testid="stMetricLabel"] {{
            text-align: {text_align};
        }}
        [data-testid="stMetricValue"] {{
            direction: ltr;
            text-align: {text_align};
            unicode-bidi: plaintext;
        }}
        [data-testid="stMetricDelta"] {{
            direction: {direction};
            text-align: {text_align};
            unicode-bidi: plaintext;
        }}
        div[data-testid="stSidebar"] .stButton > button {{
            border-radius: 10px;
            font-weight: 600;
            transition: all 0.15s ease;
        }}
        @media (max-width: 768px) {{
            .block-container {{
                padding: 1rem 0.6rem 1.5rem 0.6rem;
            }}
            .hero-balance {{
                padding: 1.1rem 1.2rem;
            }}
            .hero-balance-value {{
                font-size: 1.7rem;
            }}
            .bar-card.summary-card {{
                height: auto;
                min-height: 0;
            }}
            .bar-card.summary-card .bar-card-title {{
                min-height: 0;
            }}
            .bar-card.summary-card .bar-card-price {{
                font-size: 1.15rem;
                white-space: normal;
                overflow: visible;
                text-overflow: unset;
            }}
            .bar-card-price {{
                font-size: 1.3rem;
            }}
            .forecast-card .bar-card-price {{
                font-size: 1.2rem;
            }}
            div[data-testid="stSidebar"] .stButton > button {{
                min-height: 44px;
                font-size: 1rem;
            }}
        }}
        @media (max-width: 480px) {{
            .hero-balance-value {{
                font-size: 1.45rem;
            }}
            .section-header {{
                font-size: 1rem;
            }}
            .gold-change-pill {{
                font-size: 0.82rem;
                padding: 0.28rem 0.65rem;
            }}
            .bar-card-badge {{
                font-size: 0.75rem;
                padding: 0.25rem 0.6rem;
            }}
            .forecast-card-tag {{
                font-size: 0.72rem;
                padding: 0.12rem 0.5rem;
            }}
            .pl-box-amount {{
                font-size: 1.75rem;
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_section_header(title: str) -> None:
    st.markdown(f'<div class="section-header">{title}</div>', unsafe_allow_html=True)


def render_empty_state(title: str, hint: str) -> None:
    st.markdown(
        f"""
        <div class="empty-state">
            <div class="empty-state-icon">🥇</div>
            <div class="empty-state-title">{title}</div>
            <div class="empty-state-hint">{hint}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
