"""Built-in foods. Values are approximate, per 100 g (based on common USDA figures)."""

from sqlmodel import Session, select

from app.models import Food

# (name_ar, name_en, kcal, protein, carbs, fat, serving_g, serving_ar, serving_en)
FOODS = [
    ("رز أبيض مطبوخ", "White rice, cooked", 130, 2.7, 28.2, 0.3, 150, "صحن صغير", "small plate"),
    ("صدر دجاج مشوي", "Grilled chicken breast", 165, 31, 0, 3.6, 150, "قطعة", "piece"),
    ("بيض كامل", "Whole egg", 143, 12.6, 0.7, 9.5, 50, "حبة", "egg"),
    ("بياض بيض", "Egg white", 52, 10.9, 0.7, 0.2, 33, "حبة", "egg white"),
    ("شوفان", "Oats", 389, 16.9, 66.3, 6.9, 40, "نص كوب", "1/2 cup"),
    ("تمر", "Dates", 277, 1.8, 75, 0.2, 24, "حبة", "date"),
    ("لبنة", "Labneh", 160, 8.5, 4.5, 12, 30, "ملعقتين", "2 tbsp"),
    ("حمص", "Hummus", 166, 7.9, 14.3, 9.6, 50, "ربع كوب", "1/4 cup"),
    ("فلافل", "Falafel", 333, 13.3, 31.8, 17.8, 17, "حبة", "piece"),
    ("فول مدمس", "Foul medames", 110, 7.6, 19.6, 0.4, 150, "صحن صغير", "small bowl"),
    ("عدس مطبوخ", "Lentils, cooked", 116, 9, 20.1, 0.4, 150, "صحن صغير", "small bowl"),
    ("خبز عربي أبيض", "White pita bread", 275, 9.1, 55.7, 1.2, 60, "رغيف", "pita"),
    ("خبز عربي بر", "Whole wheat pita", 266, 9.8, 55, 2.6, 60, "رغيف", "pita"),
    ("مكرونة مطبوخة", "Pasta, cooked", 158, 5.8, 30.9, 0.9, 150, "صحن صغير", "small plate"),
    ("بطاطس مسلوقة", "Potato, boiled", 87, 1.9, 20.1, 0.1, 150, "حبة متوسطة", "medium potato"),
    ("بطاطا حلوة مسلوقة", "Sweet potato, boiled", 76, 1.4, 17.7, 0.1, 150, "حبة متوسطة", "medium"),
    ("سلمون", "Salmon", 208, 20, 0, 13, 150, "قطعة", "fillet"),
    ("تونة معلبة بالماء", "Canned tuna in water", 116, 25.5, 0, 0.8, 120, "علبة", "can"),
    ("لحم بقري مفروم مطبوخ", "Lean ground beef, cooked", 217, 26.1, 0, 11.8, 150, "حصة", "portion"),
    ("لحم غنم مطبوخ", "Lamb, cooked", 294, 25.6, 0, 20.9, 150, "حصة", "portion"),
    ("كبسة دجاج (تقريبي)", "Chicken kabsa (approx.)", 170, 9.5, 20, 5.5, 350, "صحن", "plate"),
    ("شاورما دجاج ساندويتش (تقريبي)", "Chicken shawarma wrap (approx.)", 220, 12, 22, 9, 250, "ساندويتش", "wrap"),
    ("زبادي يوناني قليل الدسم", "Greek yogurt, low fat", 59, 10.2, 3.6, 0.4, 170, "علبة", "cup"),
    ("حليب كامل الدسم", "Whole milk", 61, 3.2, 4.8, 3.3, 240, "كوب", "cup"),
    ("حليب قليل الدسم", "Low-fat milk", 42, 3.4, 5, 1, 240, "كوب", "cup"),
    ("جبن قريش", "Cottage cheese", 98, 11.1, 3.4, 4.3, 100, "نص كوب", "1/2 cup"),
    ("جبن شيدر", "Cheddar cheese", 403, 24.9, 1.3, 33.1, 28, "شريحة", "slice"),
    ("بروتين واي", "Whey protein", 400, 80, 8, 6, 30, "سكوب", "scoop"),
    ("موز", "Banana", 89, 1.1, 22.8, 0.3, 118, "حبة", "banana"),
    ("تفاح", "Apple", 52, 0.3, 13.8, 0.2, 182, "حبة", "apple"),
    ("أفوكادو", "Avocado", 160, 2, 8.5, 14.7, 100, "نص حبة", "1/2 avocado"),
    ("بروكلي مطبوخ", "Broccoli, cooked", 35, 2.4, 7.2, 0.4, 100, "كوب", "cup"),
    ("سلطة خضار", "Mixed salad (cucumber, tomato)", 18, 0.8, 3.9, 0.2, 150, "صحن", "bowl"),
    ("لوز", "Almonds", 579, 21.2, 21.6, 49.9, 28, "حفنة", "handful"),
    ("زبدة فول سوداني", "Peanut butter", 588, 25, 20, 50, 16, "ملعقة كبيرة", "tbsp"),
    ("زيت زيتون", "Olive oil", 884, 0, 0, 100, 13, "ملعقة كبيرة", "tbsp"),
    ("عسل", "Honey", 304, 0.3, 82.4, 0, 21, "ملعقة كبيرة", "tbsp"),
]


def seed_foods(session: Session) -> None:
    if session.exec(select(Food).where(Food.owner_id == None)).first():  # noqa: E711
        return
    for ar, en, kcal, p, c, f, sg, s_ar, s_en in FOODS:
        session.add(
            Food(
                name_ar=ar,
                name_en=en,
                calories=kcal,
                protein=p,
                carbs=c,
                fat=f,
                serving_g=sg,
                serving_ar=s_ar,
                serving_en=s_en,
            )
        )
    session.commit()
