/* FitPlan frontend: vanilla JS, bilingual (Arabic / English). */

// ---------------------------------------------------------------- i18n
const I18N = {
  ar: {
    tagline: "نظّم تمارينك وأكلك في مكان واحد",
    login: "تسجيل الدخول", register: "إنشاء حساب", name: "الاسم", email: "البريد الإلكتروني",
    password: "كلمة المرور", noAccount: "ما عندك حساب؟", haveAccount: "عندك حساب؟",
    today: "اليوم", plan: "الجدول", food: "الأكل", profile: "ملفي",
    hello: "هلا", todaysWorkout: "تمرين اليوم", restDay: "يوم راحة", restText: "العضلات تكبر وقت الراحة. اشرب ماي ونام زين.",
    noPlan: "ما عندك جدول تمارين للحين", createPlan: "سوّ جدولك", done: "تم اليوم ✓",
    kg: "كغ", reps: "تكرار", set: "#", last: "آخر مرة", tryWeight: "جرّب", saveWorkout: "حفظ التمرين",
    saved: "تم الحفظ 💪", nutritionToday: "أكل اليوم", remaining: "باقي", of: "من", over: "زيادة",
    kcal: "سعرة", protein: "بروتين", carbs: "كارب", fat: "دهون", g: "غ",
    setupProfile: "كمّل ملفك عشان نحسب احتياجك", goProfile: "روح لملفي",
    chooseDays: "اختر أيام التمرين (من ٢ إلى ٦)", generate: "سوّ الجدول", regenerate: "جدول جديد",
    cancel: "إلغاء", addExercise: "أضف تمرين", add: "إضافة", progress: "تقدّمك", pickExercise: "اختر تمرين",
    noProgress: "سجّل هذا التمرين عشان يطلع لك التقدّم", e1rm: "أقصى وزن متوقع (1RM)",
    breakfast: "فطور", lunch: "غداء", dinner: "عشاء", snack: "سناك", nothingYet: "ما سجلت شي",
    addFood: "أضف أكل", searchFood: "ابحث: دجاج، رز، بيض…", grams: "الكمية (غرام)", meal: "الوجبة",
    customFood: "أكل مو موجود؟ أضفه بنفسك", nameAr: "الاسم بالعربي", nameEn: "الاسم بالإنجليزي",
    per100: "القيم لكل ١٠٠ غرام", createFood: "حفظ الأكل", added: "تمت الإضافة",
    yourTargets: "احتياجك اليومي", sex: "الجنس", male: "ذكر", female: "أنثى", age: "العمر",
    height: "الطول (سم)", weight: "الوزن (كغ)", activity: "النشاط", goal: "الهدف",
    sedentary: "قليل الحركة", light: "خفيف (١-٢ يوم)", moderate: "متوسط (٣-٥ أيام)", active: "عالي (٦-٧ أيام)", very_active: "عالي جداً",
    cut: "تنشيف", maintain: "ثبات", bulk: "تضخيم", save: "حفظ", logout: "تسجيل خروج",
    calories: "السعرات", tdee: "الحرق اليومي", bmr: "الحرق الأساسي",
    targetsNote: "الأرقام تقديرية (معادلة Mifflin-St Jeor). لو عندك حالة صحية، استشر مختص.",
    error: "صار خطأ، حاول مرة ثانية", deleted: "تم الحذف", fillSets: "اكتب الوزن والتكرار لمجموعة وحدة على الأقل", todayTag: "اليوم", pS: "ب", cS: "ك", fS: "د",
    days: ["الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"],
    dayOrder: [5, 6, 0, 1, 2, 3, 4],
  },
  en: {
    tagline: "Your workouts and meals, organized in one place",
    login: "Log in", register: "Sign up", name: "Name", email: "Email",
    password: "Password", noAccount: "No account?", haveAccount: "Have an account?",
    today: "Today", plan: "Plan", food: "Food", profile: "Profile",
    hello: "Hi", todaysWorkout: "Today's workout", restDay: "Rest day", restText: "Muscles grow while you rest. Hydrate and sleep well.",
    noPlan: "You don't have a workout plan yet", createPlan: "Create your plan", done: "Done today ✓",
    kg: "kg", reps: "reps", set: "#", last: "Last time", tryWeight: "Try", saveWorkout: "Save workout",
    saved: "Saved 💪", nutritionToday: "Today's nutrition", remaining: "left", of: "of", over: "over",
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
    error: "Something went wrong, please try again", deleted: "Deleted", fillSets: "Enter weight and reps for at least one set", todayTag: "Today", pS: "P", cS: "C", fS: "F",
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
  token: store.get("token"),
  tab: "today",
  authMode: "login",
  user: null,
  foodDay: localISO(),
  foodQuery: "",
  selectedFood: null,
  progressKey: null,
  editingPlan: false,
  pickedDays: [],
};
let exercisesCache = null;

const t = (k) => I18N[state.lang][k] ?? k;
const isAr = () => state.lang === "ar";
const nm = (obj, base = "name") => (isAr() ? obj[`${base}_ar`] : obj[`${base}_en`]);
const num = (n) => new Intl.NumberFormat(isAr() ? "ar-EG" : "en-US", { maximumFractionDigits: 1 }).format(n);
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

function logout() {
  state.token = null; state.user = null; store.del("token");
  render();
}

// ---------------------------------------------------------------- icons
const ICONS = {
  today: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
  plan: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 9v6M7 7v10M17 7v10M20 9v6M7 12h10"/></svg>',
  food: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M7 3v8a2 2 0 0 0 2 2v8M11 3v8M3 3v8a2 2 0 0 0 2 2M17 21V3c2 0 4 2 4 6s-2 5-4 5"/></svg>',
  profile: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="8" r="4"/><path d="M4 21c1.5-4 4.5-6 8-6s6.5 2 8 6"/></svg>',
};

// ---------------------------------------------------------------- layout
const $app = document.getElementById("app");

function header() {
  return `<div class="topbar">
    <div class="brand"><img src="/static/icon.svg" alt=""><span>Fit<b>Plan</b></span></div>
    <button class="lang-btn" data-action="lang">${isAr() ? "English" : "العربية"}</button>
  </div>`;
}

function nav() {
  return `<nav class="nav"><div class="nav-inner">
    ${["today", "plan", "food", "profile"].map((k) => `
      <button class="${state.tab === k ? "active" : ""}" data-tab="${k}">${ICONS[k]}<span>${t(k)}</span></button>`).join("")}
  </div></nav>`;
}

async function render() {
  document.documentElement.lang = state.lang;
  document.documentElement.dir = isAr() ? "rtl" : "ltr";
  if (!state.token) return renderAuth();
  try {
    if (!state.user) state.user = await api("/api/auth/me");
    const views = { today: viewToday, plan: viewPlan, food: viewFood, profile: viewProfile };
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
  $app.innerHTML = `<div class="shell"><div style="display:flex;justify-content:flex-end">
      <button class="lang-btn" data-action="lang">${isAr() ? "English" : "العربية"}</button></div>
    <div class="auth">
      <div class="brand"><img src="/static/icon.svg" alt=""><span>Fit<b>Plan</b></span></div>
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
  const r = 64, c = 2 * Math.PI * r;
  const pct = target ? Math.min(value / target, 1) : 0;
  const color = target && value > target * 1.05 ? "var(--danger)" : "var(--accent)";
  return `<svg width="150" height="150" viewBox="0 0 150 150">
    <circle cx="75" cy="75" r="${r}" fill="none" stroke="var(--surface-2)" stroke-width="12"/>
    <circle cx="75" cy="75" r="${r}" fill="none" stroke="${color}" stroke-width="12" stroke-linecap="round"
      stroke-dasharray="${c}" stroke-dashoffset="${c * (1 - pct)}"/></svg>`;
}

function bar(label, value, target, color) {
  const pct = target ? Math.min((value / target) * 100, 100) : 0;
  return `<div><div class="bar-label"><span>${label}</span><span>${num(Math.round(value))} / ${num(target)} ${t("g")}</span></div>
    <div class="bar"><i style="width:${pct}%;background:${color}"></i></div></div>`;
}

function nutritionCard(n) {
  if (!n.targets) {
    return `<div class="card"><h2>${t("nutritionToday")}</h2><p class="sub">${t("setupProfile")}</p>
      <button class="btn ghost" data-tab="profile">${t("goProfile")}</button></div>`;
  }
  const left = n.remaining.calories;
  return `<div class="card"><div class="card-head"><h2 style="margin:0">${t("nutritionToday")}</h2>
      <button class="btn small ghost" data-tab="food">+ ${t("addFood")}</button></div>
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

function workoutCard(w) {
  if (w.is_rest_day) {
    return `<div class="card"><div class="card-head"><h2 style="margin:0">${t("todaysWorkout")}</h2>
        ${w.logged ? `<span class="pill ok">${t("done")}</span>` : ""}</div>
      <div class="rest"><div class="emoji">😴</div><h3>${t("restDay")}</h3><p class="sub">${t("restText")}</p>
      <button class="btn ghost small" data-tab="plan">${t("plan")}</button></div></div>`;
  }
  const d = w.day;
  return `<div class="card"><div class="card-head">
      <div><h2 style="margin:0">${t("todaysWorkout")}</h2><div class="sub" style="margin:4px 0 0">${esc(nm(d, "title"))}</div></div>
      ${w.logged ? `<span class="pill ok">${t("done")}</span>` : `<span class="pill">${d.exercises.length} ${isAr() ? "تمارين" : "exercises"}</span>`}
    </div>
    <form id="log-form">
      ${d.exercises.map((e) => {
        const lastTxt = e.last_sets.length ? `${t("last")}: ${e.last_sets.map((s) => `${num(s.weight_kg)}×${num(s.reps)}`).join(" · ")}` : "";
        const suggested = e.suggested_weight_kg ?? "";
        const rows = Array.from({ length: e.sets }, (_, i) => `
          <span class="n">${num(i + 1)}</span>
          <input class="input" type="number" step="0.5" min="0" inputmode="decimal" name="w-${e.exercise_key}-${i + 1}" placeholder="${t("kg")}" value="${suggested}">
          <input class="input" type="number" min="0" inputmode="numeric" name="r-${e.exercise_key}-${i + 1}" placeholder="${t("reps")}" value="${topReps(e.reps)}">`).join("");
        return `<div class="ex">
          <div class="ex-head"><span class="ex-name">${esc(nm(e))}</span><span class="ex-meta">${num(e.sets)} × <bdi dir="ltr">${esc(e.reps)}</bdi></span></div>
          ${lastTxt ? `<div class="hint">${lastTxt}${e.suggested_weight_kg != null ? ` → ${t("tryWeight")} ${num(e.suggested_weight_kg)} ${t("kg")}` : ""}</div>` : ""}
          <div class="sets"><span></span><span class="sets-head">${t("kg")}</span><span class="sets-head">${t("reps")}</span>${rows}</div>
        </div>`;
      }).join("")}
      <button class="btn block" type="submit" style="margin-top:12px">${t("saveWorkout")}</button>
    </form></div>`;
}

async function viewToday() {
  const day = localISO();
  const [w, n] = await Promise.all([api(`/api/workouts/today?day=${day}`), api(`/api/meals?day=${day}`)]);
  state._today = w;
  const dateTxt = new Date().toLocaleDateString(isAr() ? "ar-SA-u-ca-gregory" : "en-US", { weekday: "long", day: "numeric", month: "long" });
  const workout = w.has_plan ? workoutCard(w) : `<div class="card"><h2>${t("todaysWorkout")}</h2><p class="sub">${t("noPlan")}</p>
      <button class="btn" data-tab="plan">${t("createPlan")}</button></div>`;
  return `<p class="sub" style="margin:0">${dateTxt}</p><h1>${t("hello")} ${esc(state.user.name)} 👋</h1><div style="height:14px"></div>
    ${workout}${nutritionCard(n)}`;
}

const afterRender = {
  today() {
    const form = document.getElementById("log-form");
    if (!form) return;
    form.onsubmit = async (ev) => {
      ev.preventDefault();
      const fd = new FormData(form);
      const sets = [];
      for (const e of state._today.day.exercises) {
        for (let i = 1; i <= e.sets; i++) {
          const w = fd.get(`w-${e.exercise_key}-${i}`), r = fd.get(`r-${e.exercise_key}-${i}`);
          if (w !== "" && r !== "" && w != null && r != null) sets.push({ exercise_key: e.exercise_key, set_number: i, weight_kg: Number(w), reps: Number(r) });
        }
      }
      if (!sets.length) return toast(t("fillSets"));
      try {
        await api("/api/workouts/logs", { method: "POST", body: { day: localISO(), plan_day_id: state._today.day.id, sets } });
        toast(t("saved")); render();
      } catch (e) { toast(e.message); }
    };
  },
  plan() {
    const sel = document.getElementById("progress-select");
    if (sel) sel.onchange = () => { state.progressKey = sel.value; render(); };
  },
  food() {
    const q = document.getElementById("food-q");
    if (q) {
      q.oninput = debounce(async () => { state.foodQuery = q.value; state.selectedFood = null; await refreshResults(); }, 250);
      refreshResults();
    }
    const dayInput = document.getElementById("food-day");
    if (dayInput) dayInput.onchange = () => { state.foodDay = dayInput.value || localISO(); render(); };
    const addForm = document.getElementById("add-food-form");
    if (addForm) addForm.onsubmit = async (ev) => {
      ev.preventDefault();
      const f = Object.fromEntries(new FormData(addForm));
      try {
        await api("/api/meals", { method: "POST", body: { day: state.foodDay, meal_type: f.meal_type, food_id: state.selectedFood.id, grams: Number(f.grams) } });
        toast(t("added")); state.selectedFood = null; render();
      } catch (e) { toast(e.message); }
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
    const form = document.getElementById("profile-form");
    form.onsubmit = async (ev) => {
      ev.preventDefault();
      const f = Object.fromEntries(new FormData(form));
      for (const k of ["age", "height_cm", "weight_kg"]) f[k] = Number(f[k]);
      try { await api("/api/profile", { method: "PUT", body: f }); toast(t("saved")); render(); }
      catch (e) { toast(e.message); }
    };
  },
};

// ---------------------------------------------------------------- plan
function dayPicker() {
  const L = I18N[state.lang];
  return `<div class="card"><h2>${t("chooseDays")}</h2>
    <div class="days">${L.dayOrder.map((d) => `<button class="day-chip ${state.pickedDays.includes(d) ? "on" : ""}" data-action="pick-day" data-day="${d}">${L.days[d]}</button>`).join("")}</div>
    <div class="row">
      <button class="btn" data-action="generate" ${state.pickedDays.length < 2 || state.pickedDays.length > 6 ? "disabled" : ""}>${t("generate")}</button>
      ${state.editingPlan ? `<button class="btn ghost" data-action="cancel-edit">${t("cancel")}</button>` : ""}
    </div></div>`;
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

async function viewPlan() {
  if (!exercisesCache) exercisesCache = await api("/api/exercises");
  const plan = await api("/api/workouts/plan").catch((e) => (e.status === 404 ? null : Promise.reject(e)));
  if (!plan || state.editingPlan) {
    if (!state.pickedDays.length && plan) state.pickedDays = plan.days.map((d) => d.weekday);
    return `<h1>${t("plan")}</h1><p class="sub">${plan ? "" : t("noPlan")}</p>${dayPicker()}`;
  }
  const L = I18N[state.lang];
  const order = (d) => L.dayOrder.indexOf(d.weekday);
  const days = [...plan.days].sort((a, b) => order(a) - order(b));
  const options = exercisesCache.map((e) => `<option value="${e.key}">${esc(isAr() ? e.ar : e.en)}</option>`).join("");

  // progress
  const logs = await api("/api/workouts/logs?limit=100");
  const logged = new Set(logs.flatMap((l) => l.sets.map((s) => s.exercise_key)));
  const progKey = state.progressKey && logged.has(state.progressKey) ? state.progressKey : [...logged][0];
  let progressHtml = "";
  if (progKey) {
    const pts = await api(`/api/workouts/progress/${progKey}`);
    progressHtml = pts.length ? `<div class="sub" style="margin:10px 0 4px">${t("e1rm")} (${t("kg")})</div>${lineChart(pts)}` : `<p class="empty" style="margin-top:10px">${t("noProgress")}</p>`;
  }
  const progOptions = exercisesCache.filter((e) => logged.has(e.key))
    .map((e) => `<option value="${e.key}" ${e.key === progKey ? "selected" : ""}>${esc(isAr() ? e.ar : e.en)}</option>`).join("");

  return `<div class="card-head"><div><h1>${t("plan")}</h1><p class="sub" style="margin:0">${esc(nm(plan, "split"))}</p></div>
      <button class="btn small ghost" data-action="edit-plan">${t("regenerate")}</button></div><div style="height:10px"></div>
    ${days.map((d) => `<div class="card plan-day">
      <div class="card-head"><h3>${L.days[d.weekday]} <span class="pill">${esc(nm(d, "title"))}</span>${d.weekday === pyWeekday(localISO()) ? `<span class="pill ok">${t("todayTag")}</span>` : ""}</h3></div>
      ${d.exercises.map((e) => `<div class="plan-ex"><span>${esc(nm(e))}<span class="meta">${num(e.sets)} × <bdi dir="ltr">${esc(e.reps)}</bdi></span></span>
        <button class="icon-btn" title="✕" data-action="del-ex" data-id="${e.id}">✕</button></div>`).join("")}
      <div class="add-row"><select class="input" id="add-${d.id}">${options}</select>
        <button class="btn small ghost" data-action="add-ex" data-day="${d.id}">${t("add")}</button></div>
    </div>`).join("")}
    <div class="card"><h2>${t("progress")}</h2>
      ${progKey ? `<select class="input" id="progress-select">${progOptions}</select>${progressHtml}` : `<p class="empty">${t("noProgress")}</p>`}</div>`;
}

// ---------------------------------------------------------------- food
const MEALS = ["breakfast", "lunch", "dinner", "snack"];

function debounce(fn, ms) { let id; return (...a) => { clearTimeout(id); id = setTimeout(() => fn(...a), ms); }; }

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
  return `<form id="add-food-form" style="margin-top:12px">
    <div class="sub" style="margin-bottom:10px"><b style="color:var(--text)">${esc(nm(f))}</b> · ${num(f.calories)} ${t("kcal")} / 100${t("g")} · ${t("protein")} ${num(f.protein)}${t("g")}</div>
    <div class="grid2">
      <div class="field"><label>${t("grams")}</label><input class="input" name="grams" type="number" min="1" step="1" value="${f.serving_g}" required inputmode="numeric"></div>
      <div class="field"><label>${t("meal")}</label><select class="input" name="meal_type">${MEALS.map((m) => `<option value="${m}" ${m === guess ? "selected" : ""}>${t(m)}</option>`).join("")}</select></div>
    </div>
    <button class="btn block" type="submit">${t("add")}</button></form>`;
}

async function viewFood() {
  const n = await api(`/api/meals?day=${state.foodDay}`);
  const byMeal = Object.fromEntries(MEALS.map((m) => [m, n.entries.filter((e) => e.meal_type === m)]));
  return `<div class="card-head"><h1>${t("food")}</h1>
      <input type="date" class="input" id="food-day" value="${state.foodDay}" style="width:auto"></div>
    ${nutritionCard(n)}
    <div class="card">
      ${MEALS.map((m) => {
        const kcal = byMeal[m].reduce((s, e) => s + e.macros.calories, 0);
        return `<div class="meal"><div class="meal-head"><h3>${t(m)}</h3><span class="kcal">${num(Math.round(kcal))} ${t("kcal")}</span></div>
          ${byMeal[m].map((e) => `<div class="entry"><div><div>${esc(isAr() ? e.food_ar : e.food_en)}</div>
            <div class="m">${num(e.grams)}${t("g")} · ${num(e.macros.calories)} ${t("kcal")} · ${t("pS")} ${num(e.macros.protein)} · ${t("cS")} ${num(e.macros.carbs)} · ${t("fS")} ${num(e.macros.fat)}</div></div>
            <button class="icon-btn" data-action="del-meal" data-id="${e.id}">✕</button></div>`).join("") || `<div class="empty">${t("nothingYet")}</div>`}
        </div>`;
      }).join("")}
    </div>
    <div class="card"><h2>${t("addFood")}</h2>
      <input class="input" id="food-q" placeholder="${t("searchFood")}" value="${esc(state.foodQuery)}" autocomplete="off">
      <div class="results" id="food-results"></div>
      ${selectedFoodForm()}
    </div>
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

// ---------------------------------------------------------------- profile
async function viewProfile() {
  const p = await api("/api/profile").catch((e) => (e.status === 404 ? null : Promise.reject(e)));
  const v = p || { sex: "male", age: "", height_cm: "", weight_kg: "", activity_level: "moderate", goal: "maintain" };
  const opt = (name, list) => `<select class="input" name="${name}">${list.map((o) => `<option value="${o}" ${v[name] === o ? "selected" : ""}>${t(o)}</option>`).join("")}</select>`;
  const targets = p ? `<div class="card"><h2>${t("yourTargets")}</h2>
      <div class="stats">
        <div class="stat"><div class="v" style="color:var(--accent)">${num(p.targets.calories)}</div><div class="l">${t("kcal")}</div></div>
        <div class="stat"><div class="v" style="color:var(--protein)">${num(p.targets.protein_g)}${t("g")}</div><div class="l">${t("protein")}</div></div>
        <div class="stat"><div class="v" style="color:var(--carbs)">${num(p.targets.carbs_g)}${t("g")}</div><div class="l">${t("carbs")}</div></div>
        <div class="stat"><div class="v" style="color:var(--fat)">${num(p.targets.fat_g)}${t("g")}</div><div class="l">${t("fat")}</div></div>
        <div class="stat"><div class="v">${num(p.targets.tdee)}</div><div class="l">${t("tdee")}</div></div>
        <div class="stat"><div class="v">${num(p.targets.bmr)}</div><div class="l">${t("bmr")}</div></div>
      </div><p class="note">${t("targetsNote")}</p></div>` : `<p class="sub">${t("setupProfile")}</p>`;
  return `<h1>${t("profile")}</h1><p class="sub">${esc(state.user.name)} · <span dir="ltr">${esc(state.user.email)}</span></p>
    ${targets}
    <form class="card" id="profile-form">
      <div class="grid2">
        <div class="field"><label>${t("sex")}</label>${opt("sex", ["male", "female"])}</div>
        <div class="field"><label>${t("age")}</label><input class="input" name="age" type="number" min="14" max="100" value="${v.age}" required></div>
        <div class="field"><label>${t("height")}</label><input class="input" name="height_cm" type="number" min="120" max="230" step="0.5" value="${v.height_cm}" required></div>
        <div class="field"><label>${t("weight")}</label><input class="input" name="weight_kg" type="number" min="35" max="300" step="0.1" value="${v.weight_kg}" required></div>
      </div>
      <div class="field"><label>${t("activity")}</label>${opt("activity_level", ["sedentary", "light", "moderate", "active", "very_active"])}</div>
      <div class="field"><label>${t("goal")}</label>${opt("goal", ["cut", "maintain", "bulk"])}</div>
      <button class="btn block" type="submit">${t("save")}</button>
    </form>
    <button class="btn ghost block" data-action="logout">${t("logout")}</button>`;
}

// ---------------------------------------------------------------- events
document.addEventListener("click", async (ev) => {
  const el = ev.target.closest("[data-action],[data-tab]");
  if (!el) return;
  if (el.dataset.tab) { state.tab = el.dataset.tab; window.scrollTo(0, 0); return render(); }
  const a = el.dataset.action;
  try {
    if (a === "lang") setLang(isAr() ? "en" : "ar");
    else if (a === "auth-switch") { state.authMode = state.authMode === "login" ? "register" : "login"; render(); }
    else if (a === "logout") logout();
    else if (a === "pick-day") {
      const d = Number(el.dataset.day);
      state.pickedDays = state.pickedDays.includes(d) ? state.pickedDays.filter((x) => x !== d) : [...state.pickedDays, d];
      render();
    } else if (a === "generate") {
      await api("/api/workouts/plan", { method: "POST", body: { weekdays: state.pickedDays } });
      state.editingPlan = false; toast(t("saved")); render();
    } else if (a === "edit-plan") { state.editingPlan = true; state.pickedDays = []; render(); }
    else if (a === "cancel-edit") { state.editingPlan = false; render(); }
    else if (a === "del-ex") { await api(`/api/workouts/plan/exercises/${el.dataset.id}`, { method: "DELETE" }); toast(t("deleted")); render(); }
    else if (a === "add-ex") {
      const key = document.getElementById(`add-${el.dataset.day}`).value;
      await api(`/api/workouts/plan/days/${el.dataset.day}/exercises`, { method: "POST", body: { exercise_key: key } });
      toast(t("added")); render();
    } else if (a === "pick-food") {
      state.selectedFood = state._foods.find((f) => f.id === Number(el.dataset.id));
      render();
    } else if (a === "del-meal") { await api(`/api/meals/${el.dataset.id}`, { method: "DELETE" }); toast(t("deleted")); render(); }
  } catch (e) { toast(e.message); }
});

render();
