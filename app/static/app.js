/* FitPlan frontend: vanilla JS, bilingual (Arabic / English). */

// ---------------------------------------------------------------- i18n
const I18N = {
  ar: {
    tagline: "نظّم تمارينك وأكلك في مكان واحد",
    login: "تسجيل الدخول", register: "إنشاء حساب", name: "الاسم", email: "البريد الإلكتروني",
    password: "كلمة المرور", noAccount: "ما عندك حساب؟", haveAccount: "عندك حساب؟",
    today: "اليوم", plan: "الجدول", food: "الأكل", profile: "ملفي", social: "المجتمع",
    hello: "هلا", todaysWorkout: "تمرين اليوم", restDay: "يوم راحة", restText: "العضلات تكبر وقت الراحة. اشرب ماي ونام زين.",
    noPlan: "ما عندك جدول تمارين للحين", createPlan: "سوّ جدولك", done: "تم اليوم ✓",
    kg: "كغ", reps: "تكرار", set: "#", last: "آخر مرة", tryWeight: "جرّب", saveWorkout: "حفظ التمرين",
    saved: "تم الحفظ", nutritionToday: "أكل اليوم", remaining: "باقي", of: "من", over: "زيادة",
    kcal: "سعرة", protein: "بروتين", carbs: "كارب", fat: "دهون", g: "غ",
    setupProfile: "كمّل ملفك عشان نحسب احتياجك", goProfile: "روح لملفي",
    chooseDays: "اختر أيام التمرين (من 2 إلى 6)", generate: "سوّ الجدول", regenerate: "جدول جديد",
    cancel: "إلغاء", addExercise: "أضف تمرين", add: "إضافة", progress: "تقدّمك", pickExercise: "اختر تمرين",
    noProgress: "سجّل هذا التمرين عشان يطلع لك التقدّم", e1rm: "أقصى وزن متوقع (1RM)",
    breakfast: "فطور", lunch: "غداء", dinner: "عشاء", snack: "سناك", nothingYet: "ما سجلت شي",
    addFood: "أضف أكل", searchFood: "ابحث: دجاج، رز، بيض…", grams: "الكمية (غرام)", meal: "الوجبة",
    customFood: "أكل مو موجود؟ أضفه بنفسك", nameAr: "الاسم بالعربي", nameEn: "الاسم بالإنجليزي",
    per100: "القيم لكل 100 غرام", createFood: "حفظ الأكل", added: "تمت الإضافة",
    yourTargets: "احتياجك اليومي", sex: "الجنس", male: "ذكر", female: "أنثى", age: "العمر",
    height: "الطول (سم)", weight: "الوزن (كغ)", activity: "النشاط", goal: "الهدف",
    sedentary: "قليل الحركة", light: "خفيف (1-2 يوم)", moderate: "متوسط (3-5 أيام)", active: "عالي (6-7 أيام)", very_active: "عالي جداً",
    cut: "تنشيف", maintain: "ثبات", bulk: "تضخيم", save: "حفظ", logout: "تسجيل خروج",
    calories: "السعرات", tdee: "الحرق اليومي", bmr: "الحرق الأساسي",
    targetsNote: "الأرقام تقديرية (معادلة Mifflin-St Jeor). لو عندك حالة صحية، استشر مختص.",
    error: "صار خطأ، حاول مرة ثانية", deleted: "تم الحذف", fillSets: "اكتب الوزن والتكرار لمجموعة وحدة على الأقل",
    startOver: "ابدأ من جديد", howToStart: "كيف تبي تسوي جدولك؟",
    templateTitle: "جدول جاهز", templateDesc: "تختار أيامك ونسوي لك جدول متكامل، وبعدها تعدّل عليه براحتك.",
    customTitle: "ابنِ جدولك بنفسك", customDesc: "تبدأ من الصفر: تختار الأيام وتسميها وتحط التمارين اللي تبيها.",
    startCustom: "ابدأ من الصفر", replaceWarn: "جدولك الحالي بيتبدل (سجل تمارينك ما ينحذف).",
    dayName: "اسم اليوم (مثلاً: صدر وتراي)", deleteDay: "حذف اليوم", sure: "متأكد؟",
    addDay: "أضف يوم تمرين", allDaysUsed: "كل أيام الأسبوع مستخدمة", pickExerciseOpt: "اختر تمرين…",
    sets: "مجموعات", repsShort: "تكرار", emptyDay: "ما فيه تمارين. أضف من تحت 👇",
    customExercise: "تمرين مو موجود؟ أضفه بنفسك", muscle: "العضلة", createExercise: "حفظ التمرين",
    myExercises: "تماريني",
    theme: "تبديل المظهر", rest: "راحة", restDone: "يلا المجموعة الجاية", setsWord: "مجموعة",
    tapCheck: "اضغط ✓ بعد ما تخلص كل مجموعة", recentFoods: "أكلت قبل", serving: "حصة", total: "المجموع",
    markOne: "علّم مجموعة وحدة على الأقل ✓", warmupNote: "اقتراح",
    eatFor_cut: "عشان تنشّف، كُل", eatFor_maintain: "عشان تثبت على وزنك، كُل", eatFor_bulk: "عشان تضخّم، كُل",
    kcalPerDay: "سعرة باليوم",
    explain_cut: "هذا أقل من حرقك اليومي ({tdee} سعرة) بـ {diff} سعرة، يعني بتنزل تقريبًا {kg} كغ بالأسبوع.",
    explain_maintain: "هذا نفس حرقك اليومي، فوزنك بيثبت تقريبًا.",
    explain_bulk: "هذا أكثر من حرقك اليومي ({tdee} سعرة) بـ {diff} سعرة، يعني بتزيد تقريبًا {kg} كغ بالأسبوع.",
    floorNote: "رفعنا الرقم للحد الأدنى الآمن. لا تاكل أقل من كذا بدون إشراف مختص.",
    compareGoals: "قارن الأهداف (اضغط لتغيير هدفك)",
    proteinTitle: "البروتين", proteinMin: "أقل شي", proteinBest: "الأفضل لك", proteinMax: "الحد الأعلى",
    proteinExplain: "حاول ما تنزل عن {min} غ باليوم. {rec} غ هو الأنسب لهدفك، والزيادة فوق {max} غ ما لها فايدة واضحة للعضل.",
    perMeal: "يعني تقريبًا {n} غ بروتين في كل وجبة لو تاكل 4 وجبات.",
    proteinExample: "للمقارنة: 150 غ صدر دجاج فيها 46 غ بروتين، و3 بيضات فيها 19 غ، وعلبة زبادي يوناني فيها 17 غ.",
    carbsFat: "الكارب والدهون", fatRange: "بين {min} و{max} غ", carbsRest: "الباقي من سعراتك",
    howCalc: "كيف حسبنا هالأرقام؟",
    calcLine1: "الحرق الأساسي (جسمك وهو مرتاح): {bmr} سعرة",
    calcLine2: "× معامل نشاطك {f} = حرقك اليومي: {tdee} سعرة",
    calcLine3_cut: "− 20% عشان التنشيف = {cal} سعرة", calcLine3_maintain: "بدون تعديل = {cal} سعرة", calcLine3_bulk: "+ 10% عشان التضخيم = {cal} سعرة",
    yourInfo: "معلوماتك", saveAndCalc: "احسب احتياجي",
    howTo: "طريقة الأداء", tipTitle: "نصيحة", watchVideo: "شاهد فيديو على يوتيوب", primaryMuscles: "العضلة الأساسية", secondaryMuscles: "عضلات مساعدة",
    front: "أمام", back: "خلف", noGuide: "ما فيه شرح مكتوب لهالتمرين لأنك أضفته بنفسك، بس تقدر تشوف فيديو.", close: "إغلاق",
    mu_chest: "صدر", mu_shoulders: "أكتاف", mu_rear_delts: "كتف خلفي", mu_traps: "ترابيس", mu_biceps: "بايسبس", mu_triceps: "ترايسبس",
    mu_forearms: "ساعد", mu_lats: "ظهر (لاتس)", mu_lower_back: "أسفل الظهر", mu_abs: "بطن", mu_glutes: "مؤخرة", mu_quads: "فخذ أمامي",
    mu_hamstrings: "فخذ خلفي", mu_calves: "سمانة",
    findFriends: "ابحث بالاسم أو اسم المستخدم", follow: "تابِع", following: "تتابعه", followsYou: "يتابعك",
    followers: "متابِع", followingCount: "تتابع", workoutsCount: "تمرين", feedTitle: "آخر التمارين",
    feedEmpty: "ما فيه تمارين للحين. تابع أصحابك عشان تشوف تمارينهم هنا، وتمارينك بتطلع لهم.",
    shareHandle: "شارك اسمك", shareText: "تابعني على FitPlan: @{u}", copied: "تم النسخ", you: "أنت",
    setsLabel: "مجموعة", volumeLabel: "كغ إجمالي", exercisesLabel: "تمارين", best: "أفضل",
    todayRel: "اليوم", yesterdayRel: "أمس", daysAgo: "قبل {n} أيام", privateProfile: "هذا الحساب خاص، تمارينه مخفية.",
    socialSettings: "المجتمع والخصوصية", usernameLabel: "اسم المستخدم", privateLabel: "حساب خاص",
    privateHint: "لو فعّلته، محد يشوف تمارينك غيرك.", noResults: "ما لقينا أحد", noWorkoutsYet: "ما سجّل تمارين للحين",
    perSide: "على كل جهة", barNote: "مع بار 20 كغ", underBar: "الوزن أقل من وزن البار (20 كغ)",
    enterWeight: "اكتب الوزن ونحسب لك الأقراص", approx: "أقرب تركيبة", noPlates: "البار لحاله",
    exercisesWord: "تمارين", greeting: "هلا {name}",
    tabSearch: "بحث", tabSaved: "وجباتي", tabQuick: "سريع", addTo: "أضف إلى",
    savedMeals: "وجباتي المحفوظة", noSavedMeals: "ما عندك وجبات محفوظة. اضغط جنب أي وجبة سجّلتها عشان تحفظها.",
    items: "أصناف", recipes: "وصفاتي", noRecipes: "سوّ وصفة من مكوناتها، مثل كبسة البيت، ونحسب لك سعرات الحصة.",
    newRecipe: "+ وصفة جديدة", addServing: "+ حصة", perServing: "للحصة", servings: "عدد الحصص", servingsWord: "حصص",
    cookedWeight: "الوزن بعد الطبخ (اختياري، غ)", cookedHint: "الطبخ يغيّر الوزن (الرز يشرب ماي واللحم ينكمش). لو تعرف الوزن بعد الطبخ، الحساب يصير أدق.",
    ingredients: "المكونات", addIngredient: "ابحث عن مكوّن وأضفه…", saveRecipe: "احفظ الوصفة", recipeTotal: "المجموع",
    quickHint: "لما تاكل برا وتعرف السعرات تقريبًا، اكتبها مباشرة.", quickName: "وش أكلت؟ (اختياري)",
    saveAsMeal: "احفظ كوجبة", mealName: "اسم الوجبة", copyYesterday: "انسخ أمس", copyMealYesterday: "انسخ من أمس",
    nothingToCopy: "ما فيه شي تنسخه من أمس", copiedN: "تم نسخ {n} أصناف", yourMeals: "وجباتك",
    water: "الماء", ml: "مل", glass: "كوب", bottle: "قارورة", waterGoalDone: "وصلت هدفك اليوم",
    adaptiveTitle: "حرقك الحقيقي", adaptiveIntro: "المعادلة تقدير عام. لو تسجّل وزنك وأكلك، نحسب حرقك الحقيقي من بياناتك أنت ونعدّل سعراتك.",
    todayWeight: "وزنك اليوم (كغ)", logWeight: "سجّل", weighIns: "مرات تسجيل الوزن", loggedDays: "أيام سجّلت فيها أكلك", periodDays: "المدة (أيام)",
    adaptiveCollecting: "نحتاج بيانات أكثر شوي. وزّن نفسك الصبح قبل الأكل، وسجّل كل أكلك.",
    adaptiveReady: "حسب بياناتك، حرقك اليومي الحقيقي تقريبًا <b>{est}</b> سعرة (المعادلة كانت تقول {formula}). معدل أكلك {avg} سعرة، ووزنك يتغير {weekly} كغ بالأسبوع.",
    applyCalories: "طبّق: {cal} سعرة باليوم", appliedLabel: "مطبّق ✓ أرقامك محسوبة من بياناتك", backToFormula: "ارجع للمعادلة",
    measuredBadge: "محسوب من بياناتك",
    m_chest: "صدر", m_back: "ظهر", m_shoulders: "أكتاف", m_legs: "أرجل", m_arms: "ذراع", m_core: "بطن", m_cardio: "كارديو", m_other: "أخرى", todayTag: "اليوم",
    days: ["الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"],
    dayOrder: [5, 6, 0, 1, 2, 3, 4],
  },
  en: {
    tagline: "Your workouts and meals, organized in one place",
    login: "Log in", register: "Sign up", name: "Name", email: "Email",
    password: "Password", noAccount: "No account?", haveAccount: "Have an account?",
    today: "Today", plan: "Plan", food: "Food", profile: "Profile", social: "Community",
    hello: "Hi", todaysWorkout: "Today's workout", restDay: "Rest day", restText: "Muscles grow while you rest. Hydrate and sleep well.",
    noPlan: "You don't have a workout plan yet", createPlan: "Create your plan", done: "Done today ✓",
    kg: "kg", reps: "reps", set: "#", last: "Last time", tryWeight: "Try", saveWorkout: "Save workout",
    saved: "Saved", nutritionToday: "Today's nutrition", remaining: "left", of: "of", over: "over",
    kcal: "kcal", protein: "Protein", carbs: "Carbs", fat: "Fat", g: "g",
    setupProfile: "Complete your profile so we can calculate your needs", goProfile: "Go to profile",
    chooseDays: "Pick your training days (2 to 6)", generate: "Generate plan", regenerate: "New plan",
    cancel: "Cancel", addExercise: "Add exercise", add: "Add", progress: "Your progress", pickExercise: "Pick an exercise",
    noProgress: "Log this exercise to see your progress", e1rm: "Estimated 1RM",
    breakfast: "Breakfast", lunch: "Lunch", dinner: "Dinner", snack: "Snack", nothingYet: "Nothing logged",
    addFood: "Add food", searchFood: "Search: chicken, rice, egg…", grams: "Amount (grams)", meal: "Meal",
    customFood: "Can't find a food? Add your own", nameAr: "Arabic name", nameEn: "English name",
    per100: "Values per 100 g", createFood: "Save food", added: "Added",
    yourTargets: "Your daily targets", sex: "Sex", male: "Male", female: "Female", age: "Age",
    height: "Height (cm)", weight: "Weight (kg)", activity: "Activity", goal: "Goal",
    sedentary: "Sedentary", light: "Light (1-2 days)", moderate: "Moderate (3-5 days)", active: "Active (6-7 days)", very_active: "Very active",
    cut: "Cut", maintain: "Maintain", bulk: "Bulk", save: "Save", logout: "Log out",
    calories: "Calories", tdee: "Daily burn (TDEE)", bmr: "BMR",
    targetsNote: "Estimates based on the Mifflin-St Jeor equation. If you have a health condition, consult a professional.",
    error: "Something went wrong, please try again", deleted: "Deleted", fillSets: "Enter weight and reps for at least one set",
    startOver: "Start over", howToStart: "How do you want to build your plan?",
    templateTitle: "Ready-made plan", templateDesc: "Pick your days and get a complete plan, then edit anything you like.",
    customTitle: "Build it yourself", customDesc: "Start from scratch: choose the days, name them and add the exercises you want.",
    startCustom: "Start from scratch", replaceWarn: "Your current plan will be replaced (your workout history is kept).",
    dayName: "Day name (e.g. Chest & Triceps)", deleteDay: "Delete day", sure: "Sure?",
    addDay: "Add a training day", allDaysUsed: "Every day of the week is used", pickExerciseOpt: "Choose an exercise…",
    sets: "sets", repsShort: "reps", emptyDay: "No exercises yet. Add some below 👇",
    customExercise: "Missing an exercise? Add your own", muscle: "Muscle", createExercise: "Save exercise",
    myExercises: "My exercises",
    theme: "Toggle theme", rest: "Rest", restDone: "Next set", setsWord: "sets",
    tapCheck: "Tap ✓ after you finish each set", recentFoods: "Recent", serving: "serving", total: "Total",
    markOne: "Check off at least one set ✓", warmupNote: "Suggested",
    eatFor_cut: "To lose fat, eat", eatFor_maintain: "To keep your weight, eat", eatFor_bulk: "To build muscle, eat",
    kcalPerDay: "kcal per day",
    explain_cut: "That's {diff} kcal below your daily burn ({tdee} kcal), so you'll lose about {kg} kg per week.",
    explain_maintain: "That matches your daily burn, so your weight should stay about the same.",
    explain_bulk: "That's {diff} kcal above your daily burn ({tdee} kcal), so you'll gain about {kg} kg per week.",
    floorNote: "We raised this to the safe minimum. Don't eat less than this without professional supervision.",
    compareGoals: "Compare goals (tap to switch)",
    proteinTitle: "Protein", proteinMin: "Minimum", proteinBest: "Best for you", proteinMax: "Upper limit",
    proteinExplain: "Try not to go below {min} g a day. {rec} g suits your goal best, and going above {max} g brings no clear extra benefit for muscle.",
    perMeal: "That's about {n} g of protein per meal if you eat 4 meals.",
    proteinExample: "For reference: 150 g of chicken breast has 46 g of protein, 3 eggs have 19 g, and a cup of Greek yogurt has 17 g.",
    carbsFat: "Carbs & fat", fatRange: "between {min} and {max} g", carbsRest: "the rest of your calories",
    howCalc: "How did we calculate this?",
    calcLine1: "Resting burn (BMR): {bmr} kcal",
    calcLine2: "× your activity factor {f} = daily burn (TDEE): {tdee} kcal",
    calcLine3_cut: "− 20% to lose fat = {cal} kcal", calcLine3_maintain: "No change = {cal} kcal", calcLine3_bulk: "+ 10% to build muscle = {cal} kcal",
    yourInfo: "Your info", saveAndCalc: "Calculate my needs",
    howTo: "How to do it", tipTitle: "Tip", watchVideo: "Watch a video on YouTube", primaryMuscles: "Main muscle", secondaryMuscles: "Also works",
    front: "Front", back: "Back", noGuide: "There's no written guide for an exercise you added yourself, but you can watch a video.", close: "Close",
    mu_chest: "Chest", mu_shoulders: "Shoulders", mu_rear_delts: "Rear delts", mu_traps: "Traps", mu_biceps: "Biceps", mu_triceps: "Triceps",
    mu_forearms: "Forearms", mu_lats: "Lats", mu_lower_back: "Lower back", mu_abs: "Abs", mu_glutes: "Glutes", mu_quads: "Quads",
    mu_hamstrings: "Hamstrings", mu_calves: "Calves",
    findFriends: "Search by name or username", follow: "Follow", following: "Following", followsYou: "Follows you",
    followers: "followers", followingCount: "following", workoutsCount: "workouts", feedTitle: "Latest workouts",
    feedEmpty: "No workouts yet. Follow your friends to see their workouts here, and yours will show up for them.",
    shareHandle: "Share your username", shareText: "Follow me on FitPlan: @{u}", copied: "Copied", you: "You",
    setsLabel: "sets", volumeLabel: "kg total", exercisesLabel: "exercises", best: "best",
    todayRel: "Today", yesterdayRel: "Yesterday", daysAgo: "{n} days ago", privateProfile: "This account is private; workouts are hidden.",
    socialSettings: "Community & privacy", usernameLabel: "Username", privateLabel: "Private account",
    privateHint: "When on, nobody but you can see your workouts.", noResults: "No one found", noWorkoutsYet: "No workouts logged yet",
    perSide: "per side", barNote: "on a 20 kg bar", underBar: "Less than the bar itself (20 kg)",
    enterWeight: "Enter a weight to see the plates", approx: "closest match", noPlates: "Empty bar",
    exercisesWord: "exercises", greeting: "Hi {name}",
    tabSearch: "Search", tabSaved: "My meals", tabQuick: "Quick", addTo: "Add to",
    savedMeals: "Saved meals", noSavedMeals: "No saved meals yet. Tap next to any meal you've logged to save it.",
    items: "items", recipes: "My recipes", noRecipes: "Build a recipe from its ingredients (like your home kabsa) and we'll work out the calories per serving.",
    newRecipe: "+ New recipe", addServing: "+ Serving", perServing: "per serving", servings: "Servings", servingsWord: "servings",
    cookedWeight: "Weight after cooking (optional, g)", cookedHint: "Cooking changes weight (rice absorbs water, meat shrinks). If you know the cooked weight, the numbers are more accurate.",
    ingredients: "Ingredients", addIngredient: "Search for an ingredient to add…", saveRecipe: "Save recipe", recipeTotal: "Total",
    quickHint: "Eating out and roughly know the calories? Enter them directly.", quickName: "What did you eat? (optional)",
    saveAsMeal: "Save as meal", mealName: "Meal name", copyYesterday: "Copy yesterday", copyMealYesterday: "Copy from yesterday",
    nothingToCopy: "Nothing to copy from yesterday", copiedN: "Copied {n} items", yourMeals: "Your meals",
    water: "Water", ml: "ml", glass: "glass", bottle: "bottle", waterGoalDone: "Goal reached today",
    adaptiveTitle: "Your real burn", adaptiveIntro: "The formula is a general estimate. Log your weight and food, and we'll measure your actual burn from your own data and adjust your calories.",
    todayWeight: "Today's weight (kg)", logWeight: "Log", weighIns: "Weigh-ins", loggedDays: "Days with food logged", periodDays: "Period (days)",
    adaptiveCollecting: "We need a bit more data. Weigh yourself in the morning before eating, and log all your food.",
    adaptiveReady: "Based on your data, your real daily burn is about <b>{est}</b> kcal (the formula said {formula}). You've averaged {avg} kcal and your weight is changing {weekly} kg per week.",
    applyCalories: "Apply: {cal} kcal per day", appliedLabel: "Applied ✓ your numbers come from your own data", backToFormula: "Back to the formula",
    measuredBadge: "From your data",
    m_chest: "Chest", m_back: "Back", m_shoulders: "Shoulders", m_legs: "Legs", m_arms: "Arms", m_core: "Core", m_cardio: "Cardio", m_other: "Other", todayTag: "Today",
    days: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
    dayOrder: [0, 1, 2, 3, 4, 5, 6],
  },
};

// ---------------------------------------------------------------- storage (safe)
const store = {
  get(k) { try { return localStorage.getItem(k); } catch { return null; } },
  set(k, v) { try { localStorage.setItem(k, v); } catch { /* ignore */ } },
  del(k) { try { localStorage.removeItem(k); } catch { /* ignore */ } },
};

// ---------------------------------------------------------------- state
const state = {
  lang: store.get("lang") || "ar",
  theme: store.get("theme") || (window.matchMedia?.("(prefers-color-scheme: light)").matches ? "light" : "dark"),
  token: store.get("token"),
  tab: "today",
  authMode: "login",
  user: null,
  foodDay: localISO(),
  foodQuery: "",
  selectedFood: null,
  progressKey: null,
  planMode: null, // null = editor, "choose" = pick how to (re)start
  pickedDays: [],
  foodTab: "search", // search | saved | quick
};
let exercisesCache = null;

const t = (k) => I18N[state.lang][k] ?? k;
// A row of small facts, spaced apart (instead of joining them with dots).
const meta = (...parts) => `<span class="meta">${parts.filter(Boolean).map((p) => `<span>${p}</span>`).join("")}</span>`;
const tf = (k, vars) => t(k).replace(/\{(\w+)\}/g, (_, v) => vars[v]);
const isAr = () => state.lang === "ar";
const nm = (obj, base = "name") => (isAr() ? obj[`${base}_ar`] : obj[`${base}_en`]);
// Numbers always use Western digits (0-9), in Arabic too.
const NUMBER_FORMAT = new Intl.NumberFormat("en-US", { maximumFractionDigits: 1 });
const num = (n) => NUMBER_FORMAT.format(n);
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

function localISO(d = new Date()) {
  const x = new Date(d);
  x.setMinutes(x.getMinutes() - x.getTimezoneOffset());
  return x.toISOString().slice(0, 10);
}
const pyWeekday = (iso) => (new Date(iso + "T12:00:00").getDay() + 6) % 7; // JS Sun=0 -> Python Mon=0

// ---------------------------------------------------------------- api
async function api(path, { method = "GET", body } = {}) {
  const headers = { "Content-Type": "application/json" };
  if (state.token) headers.Authorization = `Bearer ${state.token}`;
  const res = await fetch(path, { method, headers, body: body ? JSON.stringify(body) : undefined });
  if (res.status === 401 && state.token) { logout(); throw new Error("unauthorized"); }
  if (res.status === 204) return null;
  const data = await res.json().catch(() => null);
  if (!res.ok) {
    const detail = data?.detail;
    const msg = Array.isArray(detail) ? detail.map((d) => d.msg).join("، ") : detail || t("error");
    const err = new Error(msg); err.status = res.status; throw err;
  }
  return data;
}

function toast(msg) {
  const el = document.getElementById("toast");
  el.textContent = msg; el.classList.add("show");
  clearTimeout(toast._t); toast._t = setTimeout(() => el.classList.remove("show"), 2200);
}

function setLang(lang) {
  state.lang = lang; store.set("lang", lang);
  document.documentElement.lang = lang;
  document.documentElement.dir = lang === "ar" ? "rtl" : "ltr";
  render();
}

function applyTheme() {
  document.documentElement.dataset.theme = state.theme;
  document.querySelector('meta[name="theme-color"]')?.setAttribute("content", state.theme === "light" ? "#eceeeb" : "#1b1f22");
}

function toggleTheme() {
  state.theme = state.theme === "light" ? "dark" : "light";
  store.set("theme", state.theme);
  applyTheme(); render();
}

function logout() {
  state.token = null; state.user = null; store.del("token");
  render();
}

// ---------------------------------------------------------------- icons
const ICONS = {
  bookmark: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M6 3h12v18l-6-4.5L6 21z"/></svg>',
  copy: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><rect x="8" y="8" width="12" height="13" rx="2"/><path d="M16 8V5a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v11a2 2 0 0 0 2 2h2"/></svg>',
  mark: '<svg viewBox="0 0 24 24" fill="currentColor"><rect x="2" y="9" width="3" height="6" rx="1"/><rect x="5.5" y="7" width="3" height="10" rx="1"/><rect x="15.5" y="7" width="3" height="10" rx="1"/><rect x="19" y="9" width="3" height="6" rx="1"/><rect x="8.5" y="11" width="7" height="2" rx="1"/></svg>',
  sun: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>',
  moon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>',
  check: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>',
  today: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
  plan: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 9v6M7 7v10M17 7v10M20 9v6M7 12h10"/></svg>',
  food: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M7 3v8a2 2 0 0 0 2 2v8M11 3v8M3 3v8a2 2 0 0 0 2 2M17 21V3c2 0 4 2 4 6s-2 5-4 5"/></svg>',
  social: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c1-3.5 3.5-5.5 6.5-5.5s5.5 2 6.5 5.5"/><circle cx="17" cy="9" r="2.8"/><path d="M16 14.6c2.6-.3 4.6 1.4 5.5 4.4"/></svg>',
  profile: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="8" r="4"/><path d="M4 21c1.5-4 4.5-6 8-6s6.5 2 8 6"/></svg>',
};

// ---------------------------------------------------------------- layout
const $app = document.getElementById("app");

const brand = () => `<div class="brand"><span class="brand-mark">${ICONS.mark}</span><span>Fit<b>Plan</b></span></div>`;
const topActions = () => `<div class="top-actions">
    <button class="round-btn" data-action="theme" title="${t("theme")}" aria-label="${t("theme")}">${state.theme === "light" ? ICONS.moon : ICONS.sun}</button>
    <button class="round-btn" data-action="lang" aria-label="language">${isAr() ? "EN" : "ع"}</button>
  </div>`;

function header() {
  return `<div class="topbar">${brand()}${topActions()}</div>`;
}

function nav() {
  return `<nav class="nav"><div class="nav-inner">
    ${["today", "plan", "food", "social", "profile"].map((k) => `
      <button class="${state.tab === k ? "active" : ""}" data-tab="${k}">${ICONS[k]}<span>${t(k)}</span></button>`).join("")}
  </div></nav>`;
}

async function render() {
  applyTheme();
  document.documentElement.lang = state.lang;
  document.documentElement.dir = isAr() ? "rtl" : "ltr";
  if (!state.token) return renderAuth();
  try {
    if (!state.user) state.user = await api("/api/auth/me");
    const views = { today: viewToday, plan: viewPlan, food: viewFood, social: viewSocial, profile: viewProfile };
    const body = await views[state.tab]();
    $app.innerHTML = `<div class="shell">${header()}${body}</div>${nav()}`;
    afterRender[state.tab]?.();
  } catch (e) {
    if (e.message !== "unauthorized") $app.innerHTML = `<div class="shell">${header()}<div class="card error">${esc(e.message)}</div></div>${nav()}`;
  }
}

// ---------------------------------------------------------------- auth
function renderAuth() {
  const reg = state.authMode === "register";
  $app.innerHTML = `<div class="shell"><div style="display:flex;justify-content:flex-end">${topActions()}</div>
    <div class="auth">
      ${brand()}
      <p class="tagline">${t("tagline")}</p>
      <form class="card" id="auth-form">
        ${reg ? `<div class="field"><label>${t("name")}</label><input class="input" name="name" required maxlength="80" autocomplete="name"></div>` : ""}
        <div class="field"><label>${t("email")}</label><input class="input" name="email" type="email" required autocomplete="email" dir="ltr"></div>
        <div class="field"><label>${t("password")}</label><input class="input" name="password" type="password" required minlength="${reg ? 8 : 1}" autocomplete="${reg ? "new-password" : "current-password"}" dir="ltr"></div>
        <div class="error" id="auth-error"></div>
        <button class="btn block" type="submit">${reg ? t("register") : t("login")}</button>
      </form>
      <div class="switch">${reg ? t("haveAccount") : t("noAccount")}
        <button class="link" data-action="auth-switch">${reg ? t("login") : t("register")}</button></div>
    </div></div>`;
  document.getElementById("auth-form").onsubmit = async (ev) => {
    ev.preventDefault();
    const f = Object.fromEntries(new FormData(ev.target));
    try {
      const res = await api(`/api/auth/${reg ? "register" : "login"}`, { method: "POST", body: f });
      state.token = res.access_token; store.set("token", res.access_token);
      state.tab = reg ? "profile" : "today";
      render();
    } catch (e) { document.getElementById("auth-error").textContent = e.message; }
  };
}

// ---------------------------------------------------------------- today
function ring(value, target) {
  const r = 60, c = 2 * Math.PI * r;
  const pct = target ? Math.min(value / target, 1) : 0;
  const color = target && value > target * 1.05 ? "var(--danger)" : "var(--ink)";
  return `<svg width="140" height="140" viewBox="0 0 140 140">
    <circle cx="70" cy="70" r="${r}" fill="none" stroke="var(--surface-2)" stroke-width="11"/>
    <circle cx="70" cy="70" r="${r}" fill="none" stroke="${color}" stroke-width="11" stroke-linecap="round"
      stroke-dasharray="${c}" stroke-dashoffset="${c * (1 - pct)}"/></svg>`;
}

function bar(label, value, target, color) {
  const pct = target ? Math.min((value / target) * 100, 100) : 0;
  return `<div><div class="bar-label"><span>${label}</span><span><bdi dir="ltr">${num(Math.round(value))} / ${num(target)}</bdi> ${t("g")}</span></div>
    <div class="bar"><i style="width:${pct}%;background:${color}"></i></div></div>`;
}

function nutritionCard(n) {
  if (!n.targets) {
    return `<div class="card"><h2>${t("nutritionToday")}</h2><p class="sub">${t("setupProfile")}</p>
      <button class="btn ghost" data-tab="profile">${t("goProfile")}</button></div>`;
  }
  const left = n.remaining.calories;
  return `<div class="card"><div class="card-head"><h2 style="margin:0">${t("nutritionToday")}</h2>
      ${state.tab === "food" ? "" : `<button class="btn small ghost" data-tab="food">+ ${t("addFood")}</button>`}</div>
    <div class="macros">
      <div class="ring-wrap">${ring(n.totals.calories, n.targets.calories)}
        <div class="ring-center"><div class="big">${num(Math.abs(Math.round(left)))}</div>
        <div class="small">${t("kcal")} ${left >= 0 ? t("remaining") : t("over")}</div></div></div>
      <div class="bars">
        ${bar(t("protein"), n.totals.protein, n.targets.protein_g, "var(--protein)")}
        ${bar(t("carbs"), n.totals.carbs, n.targets.carbs_g, "var(--carbs)")}
        ${bar(t("fat"), n.totals.fat, n.targets.fat_g, "var(--fat)")}
      </div>
    </div></div>`;
}

function topReps(reps) {
  const m = /^\s*(\d+)\s*(?:-\s*(\d+))?\s*$/.exec(reps);
  return m ? Number(m[2] || m[1]) : "";
}

function stepper(name, value, step, placeholder, decimal) {
  return `<div class="stepper">
    <button type="button" data-step="${-step}" aria-label="−">−</button>
    <input type="number" name="${name}" value="${value}" placeholder="${placeholder}" min="0" step="${decimal ? 0.5 : 1}" inputmode="${decimal ? "decimal" : "numeric"}">
    <button type="button" data-step="${step}" aria-label="+">+</button>
  </div>`;
}

function sessionHead(title, sub, done) {
  return `<section class="session">
    <div class="session-sub">${t("todaysWorkout")}</div>
    <div class="session-title">${title}</div>
    <div class="session-sub">${sub}${done ? ` <span class="pill ok">${t("done")}</span>` : ""}</div>
  </section>`;
}

function workoutCard(w) {
  if (w.is_rest_day) {
    return `${sessionHead(t("restDay"), t("restText"), w.logged)}
      <div style="margin:14px 0 26px"><button class="btn ghost small" data-tab="plan">${t("plan")}</button></div>`;
  }
  const d = w.day;
  const totalSets = d.exercises.reduce((n, e) => n + e.sets, 0);
  const head = sessionHead(esc(nm(d, "title")), `${num(d.exercises.length)} ${t("exercisesWord")}، ${num(totalSets)} ${t("setsWord")}`, w.logged);
  if (!d.exercises.length) {
    return `${head}<div class="card" style="margin-top:16px"><p class="empty">${t("emptyDay")}</p>
      <button class="btn ghost small" data-tab="plan">${t("plan")}</button></div>`;
  }
  return `${head}<div class="card" style="margin-top:16px">
    <div class="card-head" style="margin-bottom:10px"><span class="tip" style="margin:0">${t("tapCheck")}</span>
      ${w.logged ? "" : `<span class="pill" id="sets-count" dir="ltr">${num(0)} / ${num(totalSets)}</span>`}</div>
    <div class="progress-line"><i id="sets-bar" style="width:0%"></i></div>
    <form id="log-form">
      ${d.exercises.map((e) => {
        const last = e.last_sets.length ? `${t("last")}: <bdi dir="ltr">${e.last_sets.map((s) => `${s.weight_kg}×${s.reps}`).join("  ")}</bdi>` : "";
        const next = e.suggested_weight_kg != null ? `${t("tryWeight")} <b>${num(e.suggested_weight_kg)} ${t("kg")}</b>` : "";
        const rows = Array.from({ length: e.sets }, (_, i) => `
          <div class="set-row" data-ex="${e.exercise_key}" data-set="${i + 1}">
            <span class="n">${num(i + 1)}</span>
            ${stepper(`w-${e.exercise_key}-${i + 1}`, e.suggested_weight_kg ?? "", 2.5, t("kg"), true)}
            ${stepper(`r-${e.exercise_key}-${i + 1}`, topReps(e.reps), 1, t("reps"), false)}
            <button type="button" class="check" data-action="toggle-set" aria-label="done">${ICONS.check}</button>
          </div>`).join("");
        return `<div class="ex">
          <div class="ex-head"><button type="button" class="ex-name linkish" data-action="guide" data-key="${e.exercise_key}">${esc(nm(e))}<span class="info">i</span></button><span class="ex-meta">${num(e.sets)} × <bdi dir="ltr">${esc(e.reps)}</bdi></span></div>
          ${last ? `<div class="hint">${meta(last, next)}</div>` : ""}
          ${BARBELL_EXERCISES.has(e.exercise_key) ? `<div class="barbell" data-key="${e.exercise_key}">${barbellView(e.suggested_weight_kg)}</div>` : ""}
          <div class="set-head"><span></span><span>${t("kg")}</span><span>${t("reps")}</span><span></span></div>
          ${rows}
        </div>`;
      }).join("")}
      <button class="btn block" type="submit" style="margin-top:6px">${t("saveWorkout")}</button>
    </form></div>`;
}

// ---------------------------------------------------------------- plate calculator
const BARBELL_EXERCISES = new Set(["squat", "deadlift", "bench_press", "overhead_press", "barbell_row", "romanian_deadlift", "barbell_curl"]);
const BAR_KG = 20;
const PLATES = [25, 20, 15, 10, 5, 2.5, 1.25];
const PLATE_SIZE = { 25: [9, 52], 20: [8, 52], 15: [7, 44], 10: [6, 36], 5: [5, 26], 2.5: [4, 20], 1.25: [3, 16] };

function platesPerSide(total) {
  let rest = (total - BAR_KG) / 2;
  const plates = [];
  for (const p of PLATES) {
    while (rest >= p - 1e-9) { plates.push(p); rest -= p; }
  }
  return { plates, exact: rest < 0.01 };
}

function barbellView(weight) {
  const w = Number(weight);
  const emptyBar = `<svg viewBox="0 0 150 56" aria-hidden="true" style="opacity:.45"><rect class="bar-steel" x="0" y="26" width="150" height="4" rx="2"/><rect class="bar-steel" x="50" y="20" width="6" height="16" rx="1.5"/></svg>`;
  if (!w) return `${emptyBar}<div class="plates-text">${t("enterWeight")}</div>`;
  if (w < BAR_KG) return `${emptyBar}<div class="plates-text">${t("underBar")}</div>`;
  const { plates, exact } = platesPerSide(w);
  let x = 58;
  const shapes = plates.map((p) => {
    const [width, height] = PLATE_SIZE[p];
    const cls = p >= 10 ? `plate-${p}` : p === 5 ? "plate-5" : "plate-small";
    const rect = `<rect class="${cls}" x="${x}" y="${28 - height / 2}" width="${width}" height="${height}" rx="2"/>`;
    x += width + 2;
    return rect;
  }).join("");
  const svg = `<svg viewBox="0 0 150 56" aria-hidden="true">
    <rect class="bar-steel" x="0" y="26" width="150" height="4" rx="2"/>
    <rect class="bar-steel" x="50" y="20" width="6" height="16" rx="1.5"/>${shapes}</svg>`;
  const label = plates.length ? plates.join(" + ") : t("noPlates");
  return `${svg}<div class="plates-text"><b dir="ltr">${label}</b>${plates.length ? t("perSide") + "، " : ""}${t("barNote")}${exact ? "" : `، ${t("approx")}`}</div>`;
}

function updateBarbell(key, weight) {
  const el = document.querySelector(`.barbell[data-key="${key}"]`);
  if (el) el.innerHTML = barbellView(weight);
}

function updateSetsCount() {
  const all = document.querySelectorAll(".set-row").length;
  const done = document.querySelectorAll(".set-row.done").length;
  const label = document.getElementById("sets-count");
  if (label) label.textContent = `${num(done)} / ${num(all)}`;
  const barEl = document.getElementById("sets-bar");
  if (barEl) barEl.style.width = `${all ? (done / all) * 100 : 0}%`;
}

// Changing a set's weight fills the same weight into the later, unticked sets of that exercise.
document.addEventListener("input", (ev) => {
  const input = ev.target;
  if (!input.name?.startsWith("w-")) return;
  const row = input.closest(".set-row");
  if (!row) return;
  updateBarbell(row.dataset.ex, input.value);
  let next = row.nextElementSibling;
  while (next?.classList.contains("set-row")) {
    if (!next.classList.contains("done")) next.querySelector('input[name^="w-"]').value = input.value;
    next = next.nextElementSibling;
  }
});

// ---------------------------------------------------------------- rest timer
const REST_SECONDS = 90;
const timer = { left: 0, id: null };

function startRest(seconds = REST_SECONDS) {
  timer.left = seconds;
  clearInterval(timer.id);
  timer.id = setInterval(tickRest, 1000);
  drawRest();
}

function tickRest() {
  timer.left -= 1;
  if (timer.left <= 0) {
    clearInterval(timer.id); timer.id = null;
    try { navigator.vibrate?.([200, 100, 200]); } catch { /* ignore */ }
    drawRest(true);
    setTimeout(() => { if (!timer.id) stopRest(); }, 4000);
    return;
  }
  drawRest();
}

function stopRest() {
  clearInterval(timer.id); timer.id = null;
  document.getElementById("rest-timer")?.remove();
}

function drawRest(finished = false) {
  let el = document.getElementById("rest-timer");
  if (!el) { el = document.createElement("div"); el.id = "rest-timer"; document.body.appendChild(el); }
  const m = Math.floor(Math.max(timer.left, 0) / 60), sec = String(Math.max(timer.left, 0) % 60).padStart(2, "0");
  el.className = `timer${finished ? " finished" : ""}`;
  el.innerHTML = finished
    ? `<span class="label" style="opacity:1">${t("restDone")}</span><button data-action="rest-stop">✕</button>`
    : `<span class="label">⏱ ${t("rest")}</span><span class="time" dir="ltr">${m}:${sec}</span>
       <button data-action="rest-add">+30</button><button data-action="rest-stop" aria-label="stop">✕</button>`;
}

async function viewToday() {
  const day = localISO();
  const [w, n, water] = await Promise.all([api(`/api/workouts/today?day=${day}`), api(`/api/meals?day=${day}`), api(`/api/water?day=${day}`)]);
  state._today = w;
  const dateTxt = new Date().toLocaleDateString(isAr() ? "ar-SA-u-ca-gregory-nu-latn" : "en-US", { weekday: "long", day: "numeric", month: "long" });
  const workout = w.has_plan ? workoutCard(w)
    : `${sessionHead(t("noPlan"), "", false)}<div style="margin:14px 0 26px"><button class="btn" data-tab="plan">${t("createPlan")}</button></div>`;
  return `<p class="sub greet">${meta(tf("greeting", { name: esc(state.user.name) }), dateTxt)}</p>
    ${workout}${nutritionCard(n)}${waterCard(water, day)}`;
}

const afterRender = {
  today() {
    const form = document.getElementById("log-form");
    if (!form) return;
    updateSetsCount();
    form.onsubmit = async (ev) => {
      ev.preventDefault();
      const fd = new FormData(form);
      // Save the sets you ticked; if you didn't tick any, save every filled-in set.
      const ticked = [...form.querySelectorAll(".set-row.done")];
      const rows = ticked.length ? ticked : [...form.querySelectorAll(".set-row")];
      const sets = [];
      for (const row of rows) {
        const key = row.dataset.ex, n = Number(row.dataset.set);
        const w = fd.get(`w-${key}-${n}`), r = fd.get(`r-${key}-${n}`);
        if (w !== "" && r !== "" && w != null && r != null) sets.push({ exercise_key: key, set_number: n, weight_kg: Number(w), reps: Number(r) });
      }
      if (!sets.length) return toast(t("fillSets"));
      try {
        await api("/api/workouts/logs", { method: "POST", body: { day: localISO(), plan_day_id: state._today.day.id, sets } });
        stopRest(); toast(t("saved")); render();
      } catch (e) { toast(e.message); }
    };
  },
  plan() {
    const sel = document.getElementById("progress-select");
    if (sel) sel.onchange = () => { state.progressKey = sel.value; render(); };
    const form = document.getElementById("custom-ex-form");
    if (form) form.onsubmit = async (ev) => {
      ev.preventDefault();
      try {
        await api("/api/exercises", { method: "POST", body: Object.fromEntries(new FormData(form)) });
        exercisesCache = null; toast(t("added")); render();
      } catch (e) { toast(e.message); }
    };
  },
  food() {
    const q = document.getElementById("food-q");
    if (q) {
      q.oninput = debounce(async () => { state.foodQuery = q.value; state.selectedFood = null; await refreshResults(); }, 250);
      refreshResults();
    }
    const dayInput = document.getElementById("food-day");
    if (dayInput) dayInput.onchange = () => { state.foodDay = dayInput.value || localISO(); render(); };
    bindSelectedFood();
    const quick = document.getElementById("quick-form");
    if (quick) quick.onsubmit = async (ev) => {
      ev.preventDefault();
      const fd = new FormData(quick);
      const body = { day: state.foodDay, meal_type: fd.get("meal_type"), name: fd.get("name") || "" };
      for (const k of ["calories", "protein", "carbs", "fat"]) body[k] = Number(fd.get(k)) || 0;
      try { await api("/api/meals/quick", { method: "POST", body }); toast(t("added")); render(); }
      catch (e) { toast(e.message); }
    };
    const custom = document.getElementById("custom-food-form");
    if (custom) custom.onsubmit = async (ev) => {
      ev.preventDefault();
      const f = Object.fromEntries(new FormData(custom));
      for (const k of ["calories", "protein", "carbs", "fat", "serving_g"]) f[k] = Number(f[k]);
      try {
        const food = await api("/api/foods", { method: "POST", body: f });
        toast(t("added")); state.selectedFood = food; render();
      } catch (e) { toast(e.message); }
    };
  },
  profile() {
    const social = document.getElementById("social-form");
    social.onsubmit = async (ev) => {
      ev.preventDefault();
      const fd = new FormData(social);
      try {
        state.user = await api("/api/me/social", { method: "PATCH", body: { username: fd.get("username"), is_private: fd.get("is_private") === "on" } });
        toast(t("saved"));
      } catch (e) { toast(e.message); }
    };
    const form = document.getElementById("profile-form");
    form.onsubmit = async (ev) => {
      ev.preventDefault();
      const f = Object.fromEntries(new FormData(form));
      for (const k of ["age", "height_cm", "weight_kg"]) f[k] = Number(f[k]);
      try {
        await api("/api/profile", { method: "PUT", body: f });
        toast(t("saved")); await render(); window.scrollTo({ top: 0, behavior: "smooth" });
      }
      catch (e) { toast(e.message); }
    };
  },
};

// ---------------------------------------------------------------- plan
const MUSCLES = ["chest", "back", "shoulders", "legs", "arms", "core", "cardio", "other"];

function exerciseOptions() {
  const label = (e) => esc(isAr() ? e.ar : e.en);
  const custom = exercisesCache.filter((e) => e.custom);
  const groups = MUSCLES.map((m) => {
    const list = exercisesCache.filter((e) => !e.custom && e.muscle === m);
    return list.length ? `<optgroup label="${t("m_" + m)}">${list.map((e) => `<option value="${e.key}">${label(e)}</option>`).join("")}</optgroup>` : "";
  }).join("");
  const mine = custom.length ? `<optgroup label="${t("myExercises")}">${custom.map((e) => `<option value="${e.key}">${label(e)}</option>`).join("")}</optgroup>` : "";
  return `<option value="">${t("pickExerciseOpt")}</option>${mine}${groups}`;
}

function startChooser(hasPlan) {
  const L = I18N[state.lang];
  const n = state.pickedDays.length;
  return `<h1>${t("plan")}</h1><p class="sub">${t("howToStart")}</p>
    ${hasPlan ? `<p class="sub" style="color:var(--danger)">${t("replaceWarn")}</p>` : ""}
    <div class="card"><div class="choice-card"><div><h2 style="margin-bottom:4px">${t("templateTitle")}</h2><p class="sub">${t("templateDesc")}</p></div></div>
      <label>${t("chooseDays")}</label>
      <div class="days">${L.dayOrder.map((d) => `<button class="day-chip ${state.pickedDays.includes(d) ? "on" : ""}" data-action="pick-day" data-day="${d}">${L.days[d]}</button>`).join("")}</div>
      <button class="btn" data-action="generate" ${n < 2 || n > 6 ? "disabled" : ""}>${t("generate")}</button>
    </div>
    <div class="card"><div class="choice-card"><div><h2 style="margin-bottom:4px">${t("customTitle")}</h2><p class="sub">${t("customDesc")}</p></div></div>
      <button class="btn ghost" data-action="start-custom">${t("startCustom")}</button>
    </div>
    ${hasPlan ? `<button class="btn ghost block" data-action="cancel-edit">${t("cancel")}</button>` : ""}`;
}

function lineChart(points) {
  const W = 320, H = 150, P = 28;
  const vals = points.map((p) => p.estimated_1rm);
  const min = Math.min(...vals), max = Math.max(...vals);
  const span = max - min || 1;
  const x = (i) => (points.length === 1 ? W / 2 : P + (i * (W - 2 * P)) / (points.length - 1));
  const y = (v) => (max === min ? H / 2 : H - P - ((v - min) / span) * (H - 2 * P));
  const path = points.map((p, i) => `${i ? "L" : "M"}${x(i)},${y(p.estimated_1rm)}`).join(" ");
  return `<svg class="chart" viewBox="0 0 ${W} ${H}" preserveAspectRatio="none" direction="ltr">
    <line class="grid" x1="${P}" x2="${W - P}" y1="${H - P}" y2="${H - P}"/>
    <path class="line" d="${path}"/>
    ${points.map((p, i) => `<circle class="dot" cx="${x(i)}" cy="${y(p.estimated_1rm)}" r="4"><title>${p.day}: ${p.estimated_1rm}</title></circle>`).join("")}
    <text x="${P}" y="${H - 8}">${points[0].day.slice(5)}</text>
    ${points.length > 1 ? `<text x="${W - P}" y="${H - 8}" text-anchor="end">${points.at(-1).day.slice(5)}</text>` : ""}
    <text x="4" y="${y(max) + 4}">${max}</text>${max !== min ? `<text x="4" y="${y(min) + 4}">${min}</text>` : ""}
  </svg>`;
}

function dayCard(d, usedDays) {
  const L = I18N[state.lang];
  const template = isAr() ? d.title_ar : d.title_en;
  const weekdayOptions = L.dayOrder.map((w) =>
    `<option value="${w}" ${w === d.weekday ? "selected" : ""} ${w !== d.weekday && usedDays.has(w) ? "disabled" : ""}>${L.days[w]}</option>`).join("");
  const isToday = d.weekday === pyWeekday(localISO());
  const rows = d.exercises.map((e, i) => `
    <div class="ex-row">
      <div class="ex-order">
        <button class="mv" data-action="move-ex" data-id="${e.id}" data-dir="up" ${i === 0 ? "disabled" : ""} aria-label="up">▲</button>
        <button class="mv" data-action="move-ex" data-id="${e.id}" data-dir="down" ${i === d.exercises.length - 1 ? "disabled" : ""} aria-label="down">▼</button>
      </div>
      <button class="ex-title linkish" data-action="guide" data-key="${e.exercise_key}">${esc(nm(e))}<span class="info">i</span></button>
      <div class="ex-nums">
        <input class="input mini" type="number" min="1" max="15" inputmode="numeric" data-edit="sets" data-id="${e.id}" value="${e.sets}" aria-label="${t("sets")}">
        <span class="x">×</span>
        <input class="input mini reps" dir="ltr" maxlength="20" data-edit="reps" data-id="${e.id}" value="${esc(e.reps)}" aria-label="${t("repsShort")}">
      </div>
      <button class="icon-btn" data-action="del-ex" data-id="${e.id}" aria-label="delete">✕</button>
    </div>`).join("");
  return `<div class="card plan-day">
    <div class="day-edit">
      <select class="input day-weekday" data-edit="weekday" data-day="${d.id}">${weekdayOptions}</select>
      <input class="input" data-edit="title" data-day="${d.id}" value="${esc(d.title ?? "")}" placeholder="${esc(d.title ? t("dayName") : template)}" maxlength="40">
      <button class="icon-btn" data-action="del-day" data-id="${d.id}" title="${t("deleteDay")}">🗑</button>
    </div>
    ${isToday ? `<span class="pill ok" style="display:inline-block;margin-bottom:8px">${t("todayTag")}</span>` : ""}
    ${d.exercises.length ? `<div class="ex-cols"><span></span><span></span><span>${t("sets")} × ${t("repsShort")}</span><span></span></div>${rows}` : `<p class="empty">${t("emptyDay")}</p>`}
    <div class="add-row"><select class="input" id="add-${d.id}">${exerciseOptions()}</select>
      <button class="btn small" data-action="add-ex" data-day="${d.id}">+ ${t("add")}</button></div>
  </div>`;
}

async function viewPlan() {
  if (!exercisesCache) exercisesCache = await api("/api/exercises");
  const plan = await api("/api/workouts/plan").catch((e) => (e.status === 404 ? null : Promise.reject(e)));
  if (!plan || state.planMode === "choose") return startChooser(!!plan);

  const L = I18N[state.lang];
  const order = (d) => L.dayOrder.indexOf(d.weekday);
  const days = [...plan.days].sort((a, b) => order(a) - order(b));
  const used = new Set(days.map((d) => d.weekday));
  const free = L.dayOrder.filter((w) => !used.has(w));

  // progress
  const logs = await api("/api/workouts/logs?limit=100");
  const logged = new Set(logs.flatMap((l) => l.sets.map((s) => s.exercise_key)));
  const progKey = state.progressKey && logged.has(state.progressKey) ? state.progressKey : [...logged][0];
  let progressHtml = `<p class="empty">${t("noProgress")}</p>`;
  if (progKey) {
    const pts = await api(`/api/workouts/progress/${progKey}`);
    const progOptions = exercisesCache.filter((e) => logged.has(e.key))
      .map((e) => `<option value="${e.key}" ${e.key === progKey ? "selected" : ""}>${esc(isAr() ? e.ar : e.en)}</option>`).join("");
    progressHtml = `<select class="input" id="progress-select">${progOptions}</select>
      ${pts.length ? `<div class="sub" style="margin:10px 0 4px">${t("e1rm")} (${t("kg")})</div>${lineChart(pts)}` : ""}`;
  }

  return `<div class="page-head"><div><h1>${t("plan")}</h1><p class="sub">${esc(nm(plan, "split"))}</p></div>
      <button class="btn small ghost" data-action="start-over">${t("startOver")}</button></div>
    ${days.map((d) => dayCard(d, used)).join("")}
    <div class="card"><h2>+ ${t("addDay")}</h2>
      ${free.length ? `<div class="day-edit">
        <select class="input day-weekday" id="new-day-weekday">${free.map((w) => `<option value="${w}">${L.days[w]}</option>`).join("")}</select>
        <input class="input" id="new-day-title" placeholder="${t("dayName")}" maxlength="40">
        <button class="btn small" data-action="add-day">${t("add")}</button></div>` : `<p class="empty">${t("allDaysUsed")}</p>`}
    </div>
    <div class="card"><details><summary>${t("customExercise")}</summary>
      <form id="custom-ex-form">
        <div class="grid2">
          <div class="field"><label>${t("nameAr")}</label><input class="input" name="name_ar" required maxlength="60"></div>
          <div class="field"><label>${t("nameEn")}</label><input class="input" name="name_en" required maxlength="60" dir="ltr"></div>
        </div>
        <div class="field"><label>${t("muscle")}</label><select class="input" name="muscle">${MUSCLES.map((m) => `<option value="${m}">${t("m_" + m)}</option>`).join("")}</select></div>
        <button class="btn block ghost" type="submit">${t("createExercise")}</button>
      </form></details></div>
    <div class="card"><h2>${t("progress")}</h2>${progressHtml}</div>`;
}

// Inline edits in the plan editor save on change, without re-rendering (so focus isn't lost).
document.addEventListener("change", async (ev) => {
  const el = ev.target.closest("[data-edit]");
  if (!el) return;
  const field = el.dataset.edit;
  try {
    if (field === "sets" || field === "reps") {
      const value = field === "sets" ? Number(el.value) : el.value.trim();
      if (!value) { render(); return; }
      await api(`/api/workouts/plan/exercises/${el.dataset.id}`, { method: "PATCH", body: { [field]: value } });
      toast(t("saved"));
    } else if (field === "title") {
      await api(`/api/workouts/plan/days/${el.dataset.day}`, { method: "PATCH", body: { title: el.value } });
      toast(t("saved"));
    } else if (field === "weekday") {
      await api(`/api/workouts/plan/days/${el.dataset.day}`, { method: "PATCH", body: { weekday: Number(el.value) } });
      toast(t("saved")); render();
    }
  } catch (e) { toast(e.message); render(); }
});

// ---------------------------------------------------------------- exercise guide
// A simple, original front/back body diagram. Muscles are coloured by role.
function bodyMap(primary, secondary) {
  const fill = (m) => primary.includes(m) ? "var(--protein)" : secondary.includes(m) ? "color-mix(in srgb, var(--protein) 40%, var(--surface-3))" : "var(--surface-3)";
  const r = (m, x, y, w, h, rx = 5) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${rx}" fill="${fill(m)}"/>`;
  const e = (m, cx, cy, rx, ry) => `<ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${ry}" fill="${fill(m)}"/>`;
  const base = (c) => `<circle cx="${c}" cy="16" r="10" fill="var(--surface-3)"/><rect x="${c - 4}" y="25" width="8" height="8" fill="var(--surface-3)"/>`;
  const both = (fn) => fn(-1) + fn(1);
  const front = (c) => base(c)
    + both((s) => e("shoulders", c + s * 25, 40, 8, 7))
    + both((s) => r("chest", c + (s < 0 ? -20 : 1), 34, 19, 20, 6))
    + r("abs", c - 11, 56, 22, 36, 6)
    + both((s) => r("biceps", c + (s < 0 ? -36 : 27), 48, 9, 28))
    + both((s) => r("forearms", c + (s < 0 ? -38 : 29), 79, 9, 28))
    + both((s) => r("quads", c + (s < 0 ? -19 : 2), 96, 17, 52, 7))
    + both((s) => r("calves", c + (s < 0 ? -17 : 4), 152, 13, 42, 6));
  const back = (c) => base(c)
    + `<polygon points="${c - 17},33 ${c + 17},33 ${c},50" fill="${fill("traps")}"/>`
    + both((s) => e("rear_delts", c + s * 25, 40, 8, 7))
    + both((s) => `<polygon points="${c + s * 4},52 ${c + s * 20},44 ${c + s * 16},78 ${c + s * 6},84" fill="${fill("lats")}"/>`)
    + r("lower_back", c - 9, 78, 18, 16, 5)
    + both((s) => r("triceps", c + (s < 0 ? -36 : 27), 48, 9, 28))
    + both((s) => r("forearms", c + (s < 0 ? -38 : 29), 79, 9, 28))
    + both((s) => e("glutes", c + s * 9, 104, 10, 10))
    + both((s) => r("hamstrings", c + (s < 0 ? -19 : 2), 114, 17, 36, 7))
    + both((s) => r("calves", c + (s < 0 ? -17 : 4), 152, 13, 42, 6));
  return `<svg class="bodymap" viewBox="0 0 240 214" direction="ltr" role="img" aria-label="muscles">
    ${front(60)}${back(180)}
    <text x="60" y="210" text-anchor="middle">${t("front")}</text><text x="180" y="210" text-anchor="middle">${t("back")}</text>
  </svg>`;
}

function openSheet(html) {
  closeSheet();
  const el = document.createElement("div");
  el.id = "sheet";
  el.className = "sheet-wrap";
  el.innerHTML = `<div class="sheet" role="dialog" aria-modal="true">
    <button class="sheet-close" data-action="close-sheet" aria-label="${t("close")}">✕</button>${html}</div>`;
  el.addEventListener("click", (ev) => { if (ev.target === el) closeSheet(); });
  document.body.appendChild(el);
  document.body.style.overflow = "hidden";
}

function closeSheet() {
  document.getElementById("sheet")?.remove();
  document.body.style.overflow = "";
}

document.addEventListener("keydown", (ev) => { if (ev.key === "Escape") closeSheet(); });

async function showGuide(key) {
  const g = await api(`/api/exercises/${encodeURIComponent(key)}/guide`);
  const steps = isAr() ? g.steps_ar : g.steps_en;
  const tip = isAr() ? g.tip_ar : g.tip_en;
  const names = (list) => list.map((m) => t("mu_" + m)).join("، ");
  openSheet(`
    <h2 style="margin-bottom:4px">${esc(isAr() ? g.ar : g.en)}</h2>
    <div class="legend">
      ${g.primary.length ? `<span><i style="background:var(--protein)"></i>${t("primaryMuscles")}: ${names(g.primary)}</span>` : ""}
      ${g.secondary.length ? `<span><i style="background:color-mix(in srgb, var(--protein) 40%, var(--surface-3))"></i>${t("secondaryMuscles")}: ${names(g.secondary)}</span>` : ""}
    </div>
    ${bodyMap(g.primary, g.secondary)}
    ${steps.length ? `<h3 style="margin:14px 0 8px">${t("howTo")}</h3><ol class="steps">${steps.map((x) => `<li>${esc(x)}</li>`).join("")}</ol>` : `<p class="sub">${t("noGuide")}</p>`}
    ${tip ? `<div class="tipbox"><b>${t("tipTitle")}:</b> ${esc(tip)}</div>` : ""}
    <a class="btn block ghost" href="${esc(g.video_url)}" target="_blank" rel="noopener noreferrer" style="margin-top:14px;text-decoration:none">${t("watchVideo")}</a>`);
}

// ---------------------------------------------------------------- food
const MEALS = ["breakfast", "lunch", "dinner", "snack"];

function debounce(fn, ms) { let id; return (...a) => { clearTimeout(id); id = setTimeout(() => fn(...a), ms); }; }

// Picking a food only redraws the small form under the search box, not the whole page.
function showSelectedFood() {
  document.querySelectorAll("#food-results .result").forEach((r) =>
    r.classList.toggle("sel", Number(r.dataset.id) === state.selectedFood?.id));
  document.getElementById("selected-food").innerHTML = selectedFoodForm();
  bindSelectedFood();
  document.getElementById("add-food-form")?.scrollIntoView({ block: "nearest", behavior: "smooth" });
}

function bindSelectedFood() {
  const addForm = document.getElementById("add-food-form");
  if (!addForm) return;
  addForm.querySelector("input[name=grams]").addEventListener("input", updateFoodLive);
  updateFoodLive();
  addForm.onsubmit = async (ev) => {
    ev.preventDefault();
    const f = Object.fromEntries(new FormData(addForm));
    const btn = addForm.querySelector("button[type=submit]");
    btn.disabled = true;
    try {
      await api("/api/meals", { method: "POST", body: { day: state.foodDay, meal_type: f.meal_type, food_id: state.selectedFood.id, grams: Number(f.grams) } });
      toast(t("added")); state.selectedFood = null; render();
    } catch (e) { toast(e.message); btn.disabled = false; }
  };
}

async function refreshResults() {
  const box = document.getElementById("food-results");
  if (!box) return;
  const foods = await api(`/api/foods?q=${encodeURIComponent(state.foodQuery)}`);
  state._foods = foods;
  box.innerHTML = foods.map((f) => `<div class="result ${state.selectedFood?.id === f.id ? "sel" : ""}" data-action="pick-food" data-id="${f.id}">
      <span>${esc(nm(f))}</span><span class="m">${num(Math.round(f.calories * f.serving_g / 100))} ${t("kcal")} / ${esc(nm(f, "serving"))}</span></div>`).join("")
    || `<div class="empty">—</div>`;
}

function selectedFoodForm() {
  const f = state.selectedFood;
  if (!f) return "";
  const hour = new Date().getHours();
  const guess = hour < 11 ? "breakfast" : hour < 16 ? "lunch" : hour < 21 ? "dinner" : "snack";
  const servings = [0.5, 1, 1.5, 2];
  return `<form id="add-food-form" class="picked">
    <div class="picked-title">${esc(nm(f))}</div>
    <div class="sub">${num(Math.round(f.calories * f.serving_g / 100))} ${t("kcal")} / ${esc(nm(f, "serving"))} (${num(f.serving_g)}${t("g")})</div>
    <div class="chips" style="margin-bottom:10px">
      ${servings.map((x) => `<button type="button" class="serv ${x === 1 ? "on" : ""}" data-serv="${x}">${num(x)} ${esc(nm(f, "serving"))}</button>`).join("")}
    </div>
    <div class="field"><label>${t("grams")}</label>
      ${stepper("grams", f.serving_g, 10, t("g"), false)}
      <div class="live" id="food-live"></div>
    </div>
    <div class="field"><label>${t("meal")}</label><div class="chips">
      ${MEALS.map((m) => `<label class="chip"><input type="radio" name="meal_type" value="${m}" ${m === guess ? "checked" : ""}><span>${t(m)}</span></label>`).join("")}
    </div></div>
    <button class="btn block" type="submit">+ ${t("add")}</button></form>`;
}

function updateFoodLive() {
  const f = state.selectedFood, input = document.querySelector("#add-food-form input[name=grams]");
  const out = document.getElementById("food-live");
  if (!f || !input || !out) return;
  const g = Number(input.value) || 0, k = g / 100;
  out.innerHTML = meta(`<b>${num(Math.round(f.calories * k))} ${t("kcal")}</b>`, `${t("protein")} ${num(Math.round(f.protein * k * 10) / 10)} ${t("g")}`,
    `${t("carbs")} ${num(Math.round(f.carbs * k * 10) / 10)} ${t("g")}`, `${t("fat")} ${num(Math.round(f.fat * k * 10) / 10)} ${t("g")}`);
  document.querySelectorAll("[data-serv]").forEach((b) => b.classList.toggle("on", Math.abs(Number(b.dataset.serv) * f.serving_g - g) < 0.01));
}

function guessMeal() {
  const hour = new Date().getHours();
  return hour < 11 ? "breakfast" : hour < 16 ? "lunch" : hour < 21 ? "dinner" : "snack";
}

const mealChips = (name, current) => `<div class="chips">${MEALS.map((m) => `<label class="chip"><input type="radio" name="${name}" value="${m}" ${m === current ? "checked" : ""}><span>${t(m)}</span></label>`).join("")}</div>`;

function waterCard(w, day) {
  const glasses = Math.round(w.goal_ml / 250);
  const filled = Math.min(Math.floor(w.ml / 250), glasses);
  const done = w.ml >= w.goal_ml;
  return `<div class="card water" id="water-card" data-day="${day}">
    <div class="card-head"><h2>${t("water")}</h2><span class="pill ${done ? "ok" : ""}"><bdi>${num(w.ml)} / ${num(w.goal_ml)}</bdi> ${t("ml")}</span></div>
    <div class="glasses">${Array.from({ length: glasses }, (_, i) => `<i class="${i < filled ? "on" : ""}"></i>`).join("")}</div>
    ${done ? `<p class="sub" style="margin:0 0 10px;color:var(--water)">${t("waterGoalDone")}</p>` : ""}
    <div class="water-btns">
      <button class="btn ghost small" data-action="water" data-ml="-250" aria-label="−250">−</button>
      <button class="btn small" data-action="water" data-ml="250">+ ${t("glass")} <bdi>250</bdi></button>
      <button class="btn small" data-action="water" data-ml="500">+ ${t("bottle")} <bdi>500</bdi></button>
    </div></div>`;
}

function foodTabs() {
  return `<div class="segmented">${["search", "saved", "quick"].map((k) =>
    `<button class="${state.foodTab === k ? "on" : ""}" data-action="food-tab" data-tab-id="${k}">${t("tab" + k[0].toUpperCase() + k.slice(1))}</button>`).join("")}</div>`;
}

function savedTab(saved, recipes) {
  return `<div class="field"><label>${t("addTo")}</label>${mealChips("saved_meal_type", guessMeal())}</div>
    <h3 class="sec-title">${t("savedMeals")}</h3>
    ${saved.length ? saved.map((m) => `<div class="saved-row">
        <div class="saved-info"><b>${esc(m.name)}</b>
          ${meta(`${num(Math.round(m.totals.calories))} ${t("kcal")}`, `<span class="p">${t("protein")} ${num(Math.round(m.totals.protein))} ${t("g")}</span>`, `${num(m.items.length)} ${t("items")}`)}
          <span class="m">${m.items.map((i) => esc(isAr() ? i.food_ar : i.food_en)).join("، ")}</span></div>
        <button class="btn small" data-action="log-saved" data-id="${m.id}">+ ${t("add")}</button>
        <button class="icon-btn" data-action="del-saved" data-id="${m.id}" aria-label="delete">✕</button>
      </div>`).join("") : `<p class="empty">${t("noSavedMeals")}</p>`}
    <div class="sec-head"><h3 class="sec-title">${t("recipes")}</h3><button class="btn small ghost" data-action="new-recipe">${t("newRecipe")}</button></div>
    ${recipes.length ? recipes.map((r) => `<div class="saved-row">
        <div class="saved-info"><b>${esc(nm(r.food))}</b>
          ${meta(`${num(Math.round(r.per_serving.calories))} ${t("kcal")} ${t("perServing")}`, `<span class="p">${t("protein")} ${num(Math.round(r.per_serving.protein))} ${t("g")}</span>`, `${num(r.servings)} ${t("servingsWord")}`)}</div>
        <button class="btn small" data-action="log-recipe" data-food="${r.food.id}" data-g="${r.food.serving_g}">${t("addServing")}</button>
        <button class="icon-btn" data-action="del-recipe" data-id="${r.id}" aria-label="delete">✕</button>
      </div>`).join("") : `<p class="empty">${t("noRecipes")}</p>`}`;
}

function quickTab() {
  return `<form id="quick-form">
    <p class="sub">${t("quickHint")}</p>
    <div class="field"><input class="input" name="name" maxlength="60" placeholder="${t("quickName")}"></div>
    <div class="grid2">
      <div class="field"><label>${t("calories")} *</label><input class="input" name="calories" type="number" min="1" max="5000" inputmode="numeric" required></div>
      <div class="field"><label>${t("protein")} (${t("g")})</label><input class="input" name="protein" type="number" min="0" step="0.1" inputmode="decimal"></div>
      <div class="field"><label>${t("carbs")} (${t("g")})</label><input class="input" name="carbs" type="number" min="0" step="0.1" inputmode="decimal"></div>
      <div class="field"><label>${t("fat")} (${t("g")})</label><input class="input" name="fat" type="number" min="0" step="0.1" inputmode="decimal"></div>
    </div>
    <div class="field"><label>${t("meal")}</label>${mealChips("meal_type", guessMeal())}</div>
    <button class="btn block" type="submit">+ ${t("add")}</button></form>`;
}

function searchTab(recent) {
  return `${recent.length ? `<label>${t("recentFoods")}</label><div class="recent">${recent.map((f) => `<button data-action="pick-recent" data-id="${f.id}">${esc(nm(f))}</button>`).join("")}</div>` : ""}
      <input class="input" id="food-q" placeholder="${t("searchFood")}" value="${esc(state.foodQuery)}" autocomplete="off">
      <div class="results" id="food-results"></div>
      <div id="selected-food">${selectedFoodForm()}</div>`;
}

const yesterdayOf = (iso) => { const d = new Date(iso + "T12:00:00"); d.setDate(d.getDate() - 1); return localISO(d); };

async function viewFood() {
  const tab = state.foodTab;
  const [n, w, recent, saved, recipes] = await Promise.all([
    api(`/api/meals?day=${state.foodDay}`),
    api(`/api/water?day=${state.foodDay}`),
    tab === "search" ? api("/api/foods/recent") : [],
    tab === "saved" ? api("/api/saved-meals") : [],
    tab === "saved" ? api("/api/recipes") : [],
  ]);
  state._recent = recent;
  state._dayEntries = n.entries;
  const byMeal = Object.fromEntries(MEALS.map((m) => [m, n.entries.filter((e) => e.meal_type === m)]));
  const body = tab === "search" ? searchTab(recent) : tab === "saved" ? savedTab(saved, recipes) : quickTab();
  return `<div class="page-head"><h1>${t("food")}</h1>
      <input type="date" class="input" id="food-day" value="${state.foodDay}" style="width:auto;min-height:42px"></div>
    ${nutritionCard(n)}
    <div class="card"><h2>${t("addFood")}</h2>${foodTabs()}${body}</div>
    <div class="card">
      <div class="card-head"><h2>${t("yourMeals")}</h2><button class="btn small ghost" data-action="copy-day">${t("copyYesterday")}</button></div>
      ${MEALS.map((m) => {
        const kcal = byMeal[m].reduce((s, e) => s + e.macros.calories, 0);
        return `<div class="meal"><div class="meal-head"><h3>${t(m)}</h3>
            <div class="meal-actions"><span class="kcal">${num(Math.round(kcal))} ${t("kcal")}</span>
              ${byMeal[m].length ? `<button class="icon-btn small-ic" data-action="save-meal" data-meal="${m}" title="${t("saveAsMeal")}" aria-label="${t("saveAsMeal")}">${ICONS.bookmark}</button>`
                : `<button class="icon-btn small-ic" data-action="copy-meal" data-meal="${m}" title="${t("copyMealYesterday")}" aria-label="${t("copyMealYesterday")}">${ICONS.copy}</button>`}
            </div></div>
          ${byMeal[m].map((e) => `<div class="entry"><div><div>${esc(isAr() ? e.food_ar : e.food_en)}</div>
            ${meta(`${num(e.grams)} ${t("g")}`, `${num(Math.round(e.macros.calories))} ${t("kcal")}`, `<span class="p">${t("protein")} ${num(Math.round(e.macros.protein))} ${t("g")}</span>`)}</div>
            <button class="icon-btn" data-action="del-meal" data-id="${e.id}">✕</button></div>`).join("") || `<div class="empty">${t("nothingYet")}</div>`}
        </div>`;
      }).join("")}
    </div>
    ${waterCard(w, state.foodDay)}
    <div class="card"><details><summary>${t("customFood")}</summary>
      <form id="custom-food-form">
        <div class="grid2">
          <div class="field"><label>${t("nameAr")}</label><input class="input" name="name_ar" required maxlength="100"></div>
          <div class="field"><label>${t("nameEn")}</label><input class="input" name="name_en" required maxlength="100" dir="ltr"></div>
        </div>
        <p class="sub">${t("per100")}</p>
        <div class="grid2">
          <div class="field"><label>${t("calories")}</label><input class="input" name="calories" type="number" step="0.1" min="0" required></div>
          <div class="field"><label>${t("protein")} (${t("g")})</label><input class="input" name="protein" type="number" step="0.1" min="0" required></div>
          <div class="field"><label>${t("carbs")} (${t("g")})</label><input class="input" name="carbs" type="number" step="0.1" min="0" required></div>
          <div class="field"><label>${t("fat")} (${t("g")})</label><input class="input" name="fat" type="number" step="0.1" min="0" required></div>
        </div>
        <input type="hidden" name="serving_g" value="100">
        <button class="btn block ghost" type="submit">${t("createFood")}</button>
      </form></details></div>`;
}

// ---------------------------------------------------------------- recipe builder
const recipeDraft = { ingredients: [] };

function recipeTotals() {
  const tot = { calories: 0, protein: 0, carbs: 0, fat: 0, grams: 0 };
  for (const { food, grams } of recipeDraft.ingredients) {
    for (const k of ["calories", "protein", "carbs", "fat"]) tot[k] += (food[k] * grams) / 100;
    tot.grams += grams;
  }
  return tot;
}

function drawRecipeList() {
  const list = document.getElementById("rb-list");
  if (!list) return;
  list.innerHTML = recipeDraft.ingredients.map(({ food, grams }, i) => `<div class="ing-row">
      <div class="pi-main"><div class="pi-name">${esc(nm(food))}</div><div class="pi-kcal">${num(Math.round((food.calories * grams) / 100))} ${t("kcal")}</div></div>
      ${stepper(`rg-${i}`, grams, 10, t("g"), false)}
      <button type="button" class="icon-btn" data-action="rb-remove" data-i="${i}" aria-label="remove">✕</button></div>`).join("");
  drawRecipeTotal();
}

function drawRecipeTotal() {
  const servings = Math.max(1, Number(document.querySelector("#recipe-form [name=servings]")?.value) || 1);
  const tot = recipeTotals();
  document.getElementById("rb-total").innerHTML = recipeDraft.ingredients.length
    ? meta(`${t("recipeTotal")}: <b>${num(Math.round(tot.calories))} ${t("kcal")}</b>`, `${t("perServing")}: <b>${num(Math.round(tot.calories / servings))} ${t("kcal")}</b>`, `${t("protein")} ${num(Math.round(tot.protein / servings))} ${t("g")}`)
    : "";
}

function openRecipeBuilder() {
  recipeDraft.ingredients = [];
  openSheet(`<h2>${t("newRecipe").replace("+ ", "")}</h2>
    <form id="recipe-form">
      <div class="grid2">
        <div class="field"><label>${t("nameAr")}</label><input class="input" name="name_ar" required maxlength="100"></div>
        <div class="field"><label>${t("nameEn")}</label><input class="input" name="name_en" required maxlength="100" dir="ltr"></div>
      </div>
      <div class="grid2">
        <div class="field"><label>${t("servings")}</label>${stepper("servings", 4, 1, "", false)}</div>
        <div class="field"><label>${t("cookedWeight")}</label><input class="input" name="cooked" type="number" min="1" inputmode="numeric"></div>
      </div>
      <p class="note" style="margin-top:-6px">${t("cookedHint")}</p>
      <h3 class="sec-title">${t("ingredients")}</h3>
      <input class="input" id="rb-q" placeholder="${t("addIngredient")}" autocomplete="off">
      <div class="results" id="rb-results"></div>
      <div id="rb-list"></div>
      <p class="live" id="rb-total"></p>
      <button class="btn block" type="submit">${t("saveRecipe")}</button>
    </form>`);
  const form = document.getElementById("recipe-form");
  document.getElementById("rb-q").addEventListener("input", debounce(async (ev) => {
    const q = ev.target.value.trim();
    const box = document.getElementById("rb-results");
    if (!q) { box.innerHTML = ""; return; }
    const foods = (await api(`/api/foods?q=${encodeURIComponent(q)}`)).filter((f) => f.kind !== "recipe");
    state._rbFoods = foods;
    box.innerHTML = foods.slice(0, 8).map((f) => `<div class="result" data-action="rb-add" data-id="${f.id}"><span>${esc(nm(f))}</span><span class="m">+ ${num(f.serving_g)}${t("g")}</span></div>`).join("")
      || `<div class="empty">—</div>`;
  }, 250));
  // Grams and servings change live without redrawing the list (so the cursor stays put).
  form.addEventListener("input", (ev) => {
    const m = /^rg-(\d+)$/.exec(ev.target.name || "");
    if (m) {
      const ing = recipeDraft.ingredients[m[1]];
      ing.grams = Number(ev.target.value) || 0;
      ev.target.closest(".ing-row").querySelector(".pi-kcal").textContent = `${num(Math.round((ing.food.calories * ing.grams) / 100))} ${t("kcal")}`;
    }
    if (m || ev.target.name === "servings") drawRecipeTotal();
  });
  form.onsubmit = async (ev) => {
    ev.preventDefault();
    const ingredients = recipeDraft.ingredients.filter((i) => i.grams > 0);
    if (!ingredients.length) return toast(t("addIngredient"));
    const fd = new FormData(form);
    try {
      await api("/api/recipes", { method: "POST", body: {
        name_ar: fd.get("name_ar"), name_en: fd.get("name_en"), servings: Math.max(1, Number(fd.get("servings")) || 1),
        cooked_weight_g: Number(fd.get("cooked")) || null,
        ingredients: ingredients.map((i) => ({ food_id: i.food.id, grams: i.grams })),
      } });
      closeSheet(); toast(t("saved")); render();
    } catch (e) { toast(e.message); }
  };
}

function openSaveMeal(mealType) {
  const entries = (state._dayEntries || []).filter((e) => e.meal_type === mealType);
  openSheet(`<h2>${t("saveAsMeal")}</h2>
    <p class="sub">${entries.map((e) => esc(isAr() ? e.food_ar : e.food_en)).join("، ")}</p>
    <form id="save-meal-form"><div class="field"><label>${t("mealName")}</label>
      <input class="input" name="name" required maxlength="60" value="${esc(t(mealType))}"></div>
      <button class="btn block" type="submit">${t("save")}</button></form>`);
  document.getElementById("save-meal-form").onsubmit = async (ev) => {
    ev.preventDefault();
    const name = new FormData(ev.target).get("name");
    try {
      await api("/api/saved-meals", { method: "POST", body: { name, items: entries.map((e) => ({ food_id: e.food_id, grams: e.grams })) } });
      closeSheet(); toast(t("saved"));
    } catch (e) { toast(e.message); }
  };
}

async function copyFromYesterday(mealType = null) {
  const res = await api("/api/meals/copy", { method: "POST", body: { from_day: yesterdayOf(state.foodDay), to_day: state.foodDay, meal_type: mealType } });
  toast(res.length ? tf("copiedN", { n: num(res.length) }) : t("nothingToCopy"));
  if (res.length) render();
}

// ---------------------------------------------------------------- social
const avatar = (u, size = "") => `<button class="avatar ${size}" data-action="open-user" data-u="${esc(u.username)}" aria-label="${esc(u.name)}">${esc((u.name || "?").trim().charAt(0).toUpperCase())}</button>`;

function relDay(iso) {
  const days = Math.round((new Date(localISO() + "T12:00:00") - new Date(iso + "T12:00:00")) / 86400000);
  if (days <= 0) return t("todayRel");
  if (days === 1) return t("yesterdayRel");
  if (days < 7) return tf("daysAgo", { n: num(days) });
  return new Date(iso + "T12:00:00").toLocaleDateString(isAr() ? "ar-SA-u-ca-gregory-nu-latn" : "en-US", { day: "numeric", month: "short" });
}

function followBtn(u) {
  return `<button class="btn small ${u.is_following ? "ghost" : ""}" data-action="${u.is_following ? "unfollow" : "follow"}" data-u="${esc(u.username)}">${u.is_following ? "✓ " + t("following") : "+ " + t("follow")}</button>`;
}

function postCard(p) {
  const title = isAr() ? p.title_ar : p.title_en;
  return `<div class="card post">
    <div class="post-head">${avatar(p.user)}
      <div class="post-who"><button class="linkish" data-action="open-user" data-u="${esc(p.user.username)}"><b>${esc(p.user.name)}</b>${p.is_mine ? ` <span class="pill" style="padding:1px 8px">${t("you")}</span>` : ""}</button>
        ${meta(`<bdi dir="ltr">@${esc(p.user.username)}</bdi>`, relDay(p.day))}</div></div>
    ${title ? `<div class="post-title">${esc(title)}</div>` : ""}
    <div class="post-stats">
      <div><b>${num(p.sets_count)}</b><span>${t("setsLabel")}</span></div>
      <div><b>${num(Math.round(p.volume_kg))}</b><span>${t("volumeLabel")}</span></div>
      <div><b>${num(p.exercises.length)}</b><span>${t("exercisesLabel")}</span></div>
    </div>
    <ul class="post-ex">${p.exercises.slice(0, 5).map((e) => `<li><span>${esc(isAr() ? e.name_ar : e.name_en)}</span>
      <span class="m">${num(e.sets)} ${t("setsLabel")}، ${t("best")} <bdi dir="ltr">${e.best_weight_kg}×${e.best_reps}</bdi></span></li>`).join("")}
      ${p.exercises.length > 5 ? `<li class="m">+${num(p.exercises.length - 5)}</li>` : ""}</ul>
    <button class="like ${p.liked_by_me ? "on" : ""}" data-action="like" data-id="${p.id}" data-n="${p.likes}" ${p.is_mine ? "disabled" : ""}>💪 <span>${num(p.likes)}</span></button>
  </div>`;
}

function userRow(u) {
  return `<div class="user-row">${avatar(u)}
    <button class="linkish user-info" data-action="open-user" data-u="${esc(u.username)}"><b>${esc(u.name)}</b>${meta(`<bdi dir="ltr">@${esc(u.username)}</bdi>`, u.follows_you ? t("followsYou") : "")}</button>
    ${followBtn(u)}</div>`;
}

async function viewSocial() {
  const feed = await api("/api/feed");
  return `<div class="page-head"><div><h1>${t("social")}</h1><p class="sub"><bdi dir="ltr">@${esc(state.user.username)}</bdi></p></div>
      <button class="btn small ghost" data-action="share-handle">${t("shareHandle")}</button></div>
    <div class="card">
      <input class="input" id="user-q" placeholder="${t("findFriends")}" autocomplete="off" dir="auto">
      <div id="user-results"></div>
    </div>
    <h2 style="margin:20px 4px 12px">${t("feedTitle")}</h2>
    ${feed.length ? feed.map(postCard).join("") : `<div class="card empty-feed"><p>${t("feedEmpty")}</p>
      <button class="btn small" data-action="share-handle">${t("shareHandle")}</button></div>`}`;
}

async function searchUsers(q) {
  const box = document.getElementById("user-results");
  if (!box) return;
  if (q.trim().length < 2) { box.innerHTML = ""; return; }
  const users = await api(`/api/users/search?q=${encodeURIComponent(q.trim())}`);
  box.innerHTML = users.length ? users.map(userRow).join("") : `<p class="empty" style="padding-top:10px">${t("noResults")}</p>`;
}

async function openUser(username) {
  const p = await api(`/api/users/${encodeURIComponent(username)}`);
  const u = p.user;
  openSheet(`<div class="profile-head">${avatar(u, "lg")}
      <div><h2 style="margin:0">${esc(u.name)}</h2><div class="sub" style="margin:0">${meta(`<bdi dir="ltr">@${esc(u.username)}</bdi>`, u.follows_you ? t("followsYou") : "")}</div></div></div>
    <div class="post-stats" style="margin:16px 0">
      <div><b>${p.workouts_count == null ? "—" : num(p.workouts_count)}</b><span>${t("workoutsCount")}</span></div>
      <div><b>${num(u.followers)}</b><span>${t("followers")}</span></div>
      <div><b>${num(u.following)}</b><span>${t("followingCount")}</span></div>
    </div>
    ${p.is_me ? "" : `<div id="sheet-follow">${followBtn(u).replace("btn small", "btn block")}</div>`}
    ${p.is_private && !p.is_me ? `<p class="tipbox">${t("privateProfile")}</p>` : ""}
    <div class="sheet-posts">${p.workouts.length ? p.workouts.map(postCard).join("") : (p.is_private && !p.is_me ? "" : `<p class="empty" style="margin-top:12px">${t("noWorkoutsYet")}</p>`)}</div>`);
}

async function shareHandle() {
  const text = tf("shareText", { u: state.user.username });
  try {
    if (navigator.share) { await navigator.share({ text }); return; }
    await navigator.clipboard.writeText(text); toast(t("copied"));
  } catch { /* user cancelled */ }
}

document.addEventListener("input", debounce((ev) => { if (ev.target.id === "user-q") searchUsers(ev.target.value); }, 300));

// ---------------------------------------------------------------- profile
function targetsCards(p) {
  const T = p.targets, goal = p.goal;
  const diff = Math.abs(T.calorie_change), kg = Math.abs(T.weekly_change_kg);
  const explain = tf(`explain_${goal}`, { tdee: num(T.tdee), diff: num(diff), kg: num(kg) });

  // protein range bar: position of the recommended value between min and max
  const span = T.protein_max_g - T.protein_min_g || 1;
  const recPct = ((T.protein_g - T.protein_min_g) / span) * 100;

  return `
  <div class="card hero">
    <div class="hero-label">${t(`eatFor_${goal}`)}${T.tdee_source === "measured" ? ` <span class="pill ok">${t("measuredBadge")}</span>` : ""}</div>
    <div class="hero-num">${num(T.calories)} <span>${t("kcalPerDay")}</span></div>
    <p class="hero-text">${explain}</p>
    ${T.floor_applied ? `<p class="hero-warn">${t("floorNote")}</p>` : ""}
    <label style="margin-top:16px">${t("compareGoals")}</label>
    <div class="goal-tiles">
      ${["cut", "maintain", "bulk"].map((g) => `
        <button class="goal-tile ${g === goal ? "on" : ""}" data-action="set-goal" data-goal="${g}">
          <span class="g-name">${t(g)}</span><span class="g-kcal">${num(T.goal_calories[g])}</span><span class="g-unit">${t("kcal")}</span>
        </button>`).join("")}
    </div>
  </div>

  <div class="card">
    <h2>${t("proteinTitle")}</h2>
    <div class="range">
      <div class="range-track"><i style="inset-inline-start:${recPct}%"></i></div>
      <div class="range-labels">
        <div><span class="rl">${t("proteinMin")}</span><b>${num(T.protein_min_g)} ${t("g")}</b></div>
        <div class="best"><span class="rl">${t("proteinBest")}</span><b>${num(T.protein_g)} ${t("g")}</b></div>
        <div><span class="rl">${t("proteinMax")}</span><b>${num(T.protein_max_g)} ${t("g")}</b></div>
      </div>
    </div>
    <p class="explain">${tf("proteinExplain", { min: num(T.protein_min_g), rec: num(T.protein_g), max: num(T.protein_max_g) })}</p>
    <p class="explain">${tf("perMeal", { n: num(Math.round(T.protein_g / 4)) })}</p>
    <p class="note" style="margin-top:6px">${t("proteinExample")}</p>
  </div>

  <div class="card">
    <h2>${t("carbsFat")}</h2>
    <div class="stats two">
      <div class="stat"><div class="v" style="color:var(--carbs)">${num(T.carbs_g)} ${t("g")}</div><div class="l">${t("carbs")}<br>${t("carbsRest")}</div></div>
      <div class="stat"><div class="v" style="color:var(--fat)">${num(T.fat_g)} ${t("g")}</div><div class="l">${t("fat")}<br>${tf("fatRange", { min: num(T.fat_min_g), max: num(T.fat_max_g) })}</div></div>
    </div>
    <details style="margin-top:14px"><summary>${t("howCalc")}</summary>
      <div class="calc">
        <div>${tf("calcLine1", { bmr: num(T.bmr) })}</div>
        <div>${tf("calcLine2", { f: num(T.activity_factor), tdee: num(T.tdee) })}</div>
        <div>${tf(`calcLine3_${goal}`, { cal: num(T.goal_calories[goal]) })}</div>
      </div>
      <p class="note">${t("targetsNote")}</p>
    </details>
  </div>`;
}

function progressRow(label, have, need) {
  const pct = Math.min(100, (have / need) * 100);
  return `<div class="ad-row"><div class="bar-label"><span>${label}</span><span><bdi>${num(Math.min(have, need))} / ${num(need)}</bdi></span></div>
    <div class="bar"><i style="width:${pct}%;background:var(--ink)"></i></div></div>`;
}

function adaptiveCard(ad, weights) {
  const todayW = weights.find((w) => w.day === localISO());
  const head = `<h2>${t("adaptiveTitle")}</h2><p class="sub">${t("adaptiveIntro")}</p>
    <div class="weight-row"><label for="weight-input">${t("todayWeight")}</label>
      <div class="row"><input class="input" id="weight-input" type="number" min="30" max="300" step="0.1" inputmode="decimal" value="${todayW ? todayW.weight_kg : ""}">
      <button class="btn" data-action="log-weight" style="flex:0 0 auto">${todayW ? "✓ " : ""}${t("logWeight")}</button></div></div>`;
  if (ad.status !== "ready") {
    return `<div class="card">${head}
      ${progressRow(t("weighIns"), ad.weigh_ins, ad.weigh_ins_needed)}
      ${progressRow(t("loggedDays"), ad.logged_days, ad.logged_days_needed)}
      ${progressRow(t("periodDays"), ad.span_days, ad.span_days_needed)}
      <p class="note">${t("adaptiveCollecting")}</p></div>`;
  }
  const weekly = `${ad.weekly_change_kg > 0 ? "+" : ""}${num(ad.weekly_change_kg)}`;
  return `<div class="card">${head}
    <p class="explain">${tf("adaptiveReady", { est: num(ad.estimated_tdee), formula: num(ad.formula_tdee), avg: num(ad.avg_intake), weekly: `<bdi dir="ltr">${weekly}</bdi>` })}</p>
    ${ad.applied
      ? `<p class="pill ok" style="display:inline-block;margin:6px 0 12px">${t("appliedLabel")}</p><br><button class="btn ghost small" data-action="reset-adaptive">${t("backToFormula")}</button>`
      : `<button class="btn block" data-action="apply-adaptive">${tf("applyCalories", { cal: num(ad.suggested_calories) })}</button>`}
  </div>`;
}

function chipGroup(name, options, current) {
  return `<div class="chips">${options.map((o) => `<label class="chip"><input type="radio" name="${name}" value="${o}" ${current === o ? "checked" : ""}><span>${t(o)}</span></label>`).join("")}</div>`;
}

async function viewProfile() {
  const p = await api("/api/profile").catch((e) => (e.status === 404 ? null : Promise.reject(e)));
  state._profile = p;
  const [ad, weights] = p ? await Promise.all([api(`/api/adaptive?today=${localISO()}`), api("/api/weights?days=2")]) : [null, []];
  const v = p || { sex: "male", age: "", height_cm: "", weight_kg: "", activity_level: "moderate", goal: "cut" };
  const activity = `<select class="input" name="activity_level">${["sedentary", "light", "moderate", "active", "very_active"].map((o) => `<option value="${o}" ${v.activity_level === o ? "selected" : ""}>${t(o)}</option>`).join("")}</select>`;
  const form = `<form class="card" id="profile-form">
      <h2>${t("yourInfo")}</h2>
      <div class="field"><label>${t("goal")}</label>${chipGroup("goal", ["cut", "maintain", "bulk"], v.goal)}</div>
      <div class="field"><label>${t("sex")}</label>${chipGroup("sex", ["male", "female"], v.sex)}</div>
      <div class="grid3">
        <div class="field"><label>${t("age")}</label><input class="input" name="age" type="number" min="14" max="100" inputmode="numeric" value="${v.age}" required></div>
        <div class="field"><label>${t("height")}</label><input class="input" name="height_cm" type="number" min="120" max="230" step="0.5" inputmode="decimal" value="${v.height_cm}" required></div>
        <div class="field"><label>${t("weight")}</label><input class="input" name="weight_kg" type="number" min="35" max="300" step="0.1" inputmode="decimal" value="${v.weight_kg}" required></div>
      </div>
      <div class="field"><label>${t("activity")}</label>${activity}</div>
      <button class="btn block" type="submit">${p ? t("save") : t("saveAndCalc")}</button>
    </form>`;
  return `<h1>${t("profile")}</h1><p class="sub">${meta(esc(state.user.name), `<span dir="ltr">${esc(state.user.email)}</span>`)}</p>
    ${p ? targetsCards(p) + adaptiveCard(ad, weights) + form : `<p class="sub">${t("setupProfile")}</p>` + form}
    <form class="card" id="social-form">
      <h2>${t("socialSettings")}</h2>
      <div class="field"><label>${t("usernameLabel")}</label>
        <div class="handle-input" dir="ltr"><span>@</span><input class="input" name="username" value="${esc(state.user.username)}" maxlength="20" autocomplete="off" pattern="[a-zA-Z0-9_.]{3,20}"></div></div>
      <label class="switch-row"><span><b>${t("privateLabel")}</b><br><span class="sub" style="font-size:13px">${t("privateHint")}</span></span>
        <input type="checkbox" name="is_private" ${state.user.is_private ? "checked" : ""}><i class="switch-ui"></i></label>
      <button class="btn block ghost" type="submit">${t("save")}</button>
    </form>
    <button class="btn ghost block" data-action="logout">${t("logout")}</button>`;
}

// ---------------------------------------------------------------- events
document.addEventListener("click", async (ev) => {
  const serv = ev.target.closest("[data-serv]");
  if (serv && state.selectedFood) {
    const input = document.querySelector("#add-food-form input[name=grams]");
    input.value = Math.round(Number(serv.dataset.serv) * state.selectedFood.serving_g);
    updateFoodLive();
    return;
  }
  const stepBtn = ev.target.closest("[data-step]");
  if (stepBtn) {
    const input = stepBtn.parentElement.querySelector("input");
    const step = Number(stepBtn.dataset.step);
    const next = Math.max(0, Math.round(((Number(input.value) || 0) + step) * 10) / 10);
    input.value = next;
    input.dispatchEvent(new Event("input", { bubbles: true }));
    return;
  }
  const el = ev.target.closest("[data-action],[data-tab]");
  if (!el) return;
  if (el.dataset.tab) { closeSheet(); state.tab = el.dataset.tab; window.scrollTo(0, 0); return render(); }
  const a = el.dataset.action;
  try {
    if (a === "lang") setLang(isAr() ? "en" : "ar");
    else if (a === "theme") toggleTheme();
    else if (a === "set-goal") {
      const { targets, ...current } = state._profile;
      await api("/api/profile", { method: "PUT", body: { ...current, goal: el.dataset.goal } });
      render();
    }
    else if (a === "toggle-set") {
      const row = el.closest(".set-row");
      row.classList.toggle("done");
      updateSetsCount();
      if (row.classList.contains("done")) startRest(); else stopRest();
    }
    else if (a === "rest-add") { timer.left += 30; drawRest(); }
    else if (a === "guide") await showGuide(el.dataset.key);
    else if (a === "open-user") await openUser(el.dataset.u);
    else if (a === "food-tab") { state.foodTab = el.dataset.tabId; state.selectedFood = null; render(); }
    else if (a === "water") {
      const card = document.getElementById("water-card");
      const w = await api("/api/water", { method: "POST", body: { day: card.dataset.day, ml: Number(el.dataset.ml) } });
      card.outerHTML = waterCard(w, card.dataset.day);
    } else if (a === "log-saved") {
      const mealType = document.querySelector("input[name=saved_meal_type]:checked")?.value || guessMeal();
      await api(`/api/saved-meals/${el.dataset.id}/log`, { method: "POST", body: { day: state.foodDay, meal_type: mealType } });
      toast(t("added")); render();
    } else if (a === "log-recipe") {
      const mealType = document.querySelector("input[name=saved_meal_type]:checked")?.value || guessMeal();
      await api("/api/meals", { method: "POST", body: { day: state.foodDay, meal_type: mealType, food_id: Number(el.dataset.food), grams: Number(el.dataset.g) } });
      toast(t("added")); render();
    } else if (a === "del-saved" || a === "del-recipe") {
      if (!el.dataset.armed) { el.dataset.armed = "1"; el.textContent = t("sure"); el.classList.add("armed"); return; }
      await api(`/api/${a === "del-saved" ? "saved-meals" : "recipes"}/${el.dataset.id}`, { method: "DELETE" });
      toast(t("deleted")); render();
    } else if (a === "new-recipe") openRecipeBuilder();
    else if (a === "rb-add") {
      const food = state._rbFoods.find((f) => f.id === Number(el.dataset.id));
      recipeDraft.ingredients.push({ food, grams: food.serving_g });
      document.getElementById("rb-q").value = "";
      document.getElementById("rb-results").innerHTML = "";
      drawRecipeList();
    } else if (a === "rb-remove") { recipeDraft.ingredients.splice(Number(el.dataset.i), 1); drawRecipeList(); }
    else if (a === "save-meal") openSaveMeal(el.dataset.meal);
    else if (a === "copy-day") await copyFromYesterday();
    else if (a === "copy-meal") await copyFromYesterday(el.dataset.meal);
    else if (a === "log-weight") {
      const v = Number(document.getElementById("weight-input").value);
      if (!v) return;
      await api("/api/weights", { method: "PUT", body: { day: localISO(), weight_kg: v } });
      toast(t("saved")); render();
    } else if (a === "apply-adaptive") { await api(`/api/adaptive/apply?today=${localISO()}`, { method: "POST" }); toast(t("saved")); render(); }
    else if (a === "reset-adaptive") { await api("/api/adaptive/apply", { method: "DELETE" }); toast(t("saved")); render(); }
    else if (a === "share-handle") await shareHandle();
    else if (a === "follow" || a === "unfollow") {
      await api(`/api/users/${encodeURIComponent(el.dataset.u)}/follow`, { method: a === "follow" ? "POST" : "DELETE" });
      const nowFollowing = a === "follow";
      document.querySelectorAll(`[data-action="follow"][data-u="${el.dataset.u}"], [data-action="unfollow"][data-u="${el.dataset.u}"]`).forEach((b) => {
        b.dataset.action = nowFollowing ? "unfollow" : "follow";
        b.classList.toggle("ghost", nowFollowing);
        b.textContent = nowFollowing ? "✓ " + t("following") : "+ " + t("follow");
      });
      if (state.tab === "social" && !document.getElementById("sheet")) render();
    } else if (a === "like") {
      const liked = el.classList.contains("on");
      await api(`/api/workouts/logs/${el.dataset.id}/like`, { method: liked ? "DELETE" : "POST" });
      const n = Number(el.dataset.n) + (liked ? -1 : 1);
      el.dataset.n = n; el.classList.toggle("on", !liked); el.querySelector("span").textContent = num(n);
    }
    else if (a === "close-sheet") closeSheet();

    else if (a === "rest-stop") stopRest();
    else if (a === "auth-switch") { state.authMode = state.authMode === "login" ? "register" : "login"; render(); }
    else if (a === "logout") logout();
    else if (a === "pick-day") {
      const d = Number(el.dataset.day);
      state.pickedDays = state.pickedDays.includes(d) ? state.pickedDays.filter((x) => x !== d) : [...state.pickedDays, d];
      render();
    } else if (a === "generate") {
      await api("/api/workouts/plan", { method: "POST", body: { weekdays: state.pickedDays } });
      state.planMode = null; toast(t("saved")); render();
    } else if (a === "start-custom") {
      await api("/api/workouts/plan/custom", { method: "POST", body: { days: [] } });
      state.planMode = null; render();
    } else if (a === "start-over") { state.planMode = "choose"; state.pickedDays = []; window.scrollTo(0, 0); render(); }
    else if (a === "cancel-edit") { state.planMode = null; render(); }
    else if (a === "add-day") {
      const weekday = Number(document.getElementById("new-day-weekday").value);
      const title = document.getElementById("new-day-title").value;
      await api("/api/workouts/plan/days", { method: "POST", body: { weekday, title } });
      toast(t("added")); render();
    } else if (a === "del-day") {
      if (!el.dataset.armed) { el.dataset.armed = "1"; el.textContent = t("sure"); el.classList.add("armed"); return; }
      await api(`/api/workouts/plan/days/${el.dataset.id}`, { method: "DELETE" }); toast(t("deleted")); render();
    } else if (a === "move-ex") {
      await api(`/api/workouts/plan/exercises/${el.dataset.id}/move`, { method: "POST", body: { direction: el.dataset.dir } });
      render();
    } else if (a === "del-ex") { await api(`/api/workouts/plan/exercises/${el.dataset.id}`, { method: "DELETE" }); toast(t("deleted")); render(); }
    else if (a === "add-ex") {
      const key = document.getElementById(`add-${el.dataset.day}`).value;
      if (!key) return toast(t("pickExerciseOpt"));
      await api(`/api/workouts/plan/days/${el.dataset.day}/exercises`, { method: "POST", body: { exercise_key: key } });
      toast(t("added")); render();
    } else if (a === "pick-food") {
      state.selectedFood = state._foods.find((f) => f.id === Number(el.dataset.id));
      showSelectedFood();
    } else if (a === "pick-recent") {
      state.selectedFood = state._recent.find((f) => f.id === Number(el.dataset.id));
      showSelectedFood();
    } else if (a === "del-meal") { await api(`/api/meals/${el.dataset.id}`, { method: "DELETE" }); toast(t("deleted")); render(); }
  } catch (e) { toast(e.message); }
});

render();
