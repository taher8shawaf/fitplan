# FitPlan 🏋️

**[English](#english) | [العربية](#العربية)**

A bilingual (Arabic / English) web app that builds your gym schedule, tracks your lifts, and organizes your meals around your daily calorie and macro targets.

<p align="center">
  <img src="docs/today-ar.png" width="260" alt="Today screen (Arabic)">
  <img src="docs/food-ar.png" width="260" alt="Food screen (Arabic)">
  <img src="docs/plan-en.png" width="260" alt="Plan screen (English)">
</p>

---

## English

### Features
- **Clear personal targets.** Tells you exactly how many calories to eat for your goal, how far that is from your daily burn, and the expected weekly weight change. Compare cut / maintain / bulk side by side and switch with one tap.
- **Protein range.** Minimum (1.6 g/kg), best for your goal, and upper limit (2.2 g/kg), plus per-meal amounts. Uses the Mifflin-St Jeor equation, safe calorie floors, and a BMI-30 reference weight for protein at high body weights.
- **Ready-made or fully custom plans.** Pick your training days (2 to 6) and get a split that fits (Full Body, Upper/Lower, Upper/Lower + PPL, Push/Pull/Legs), or build your own from scratch.
- **Full plan editor.** Add, remove, rename and move training days; add exercises from a 102-exercise library (chest, back, shoulders, biceps, triceps, forearms, legs, core, cardio) or your own custom exercises; edit sets and reps inline; reorder exercises.
- **Today screen.** Shows today's workout or a rest day, with your sets from last time.
- **Progressive overload suggestions.** Uses double progression: if you hit the top of the rep range on every working set, it suggests adding 2.5 kg next time.
- **Progress chart.** Estimated 1RM over time per exercise (Epley formula).
- **Progress dashboard.** One page for the big picture: workout consistency (done vs planned per week), weekly average body weight and its trend, the last 7 days of calories and protein against your targets, and how much your main lifts have improved.
- **Smart meal planner.** Builds a full day (breakfast, lunch, dinner, snack) sized to your calories and protein, shows protein per meal, swaps any food for an equivalent (same protein, or same calories), and respects a budget level plus foods you like or want to avoid. Log the whole plan in one tap.
- **Meal tracking.** A built-in food database with common Arabic and Gulf foods (kabsa, foul, labneh, dates, hummus…), meal logging by day, remaining calories and macros, and private custom foods.
- **Exercise guides.** Every exercise has step-by-step instructions, a safety tip, a front/back muscle map of the muscles it works, and a link to video demos.
- **Community.** Every user gets an @username. Find friends by name or username (emails are never exposed), follow them, see their workouts in a feed with sets, total volume and best sets, and give them a 💪. A private mode hides your workouts from everyone.
- **Gym-friendly controls.** +/− steppers for weight and reps, tick off each set as you go, and a rest timer starts automatically.
- **Quick food logging.** One-tap serving sizes, live calorie/macro preview, and your recent foods for re-adding.
- **Saved meals & recipes.** Save any logged meal and re-add it in one tap. Build recipes from ingredients (with optional cooked weight) and log them by the serving.
- **Copy a previous day.** Copy all of yesterday's food, or a single meal, in one tap.
- **Quick add.** Log calories and macros directly when eating out.
- **Water tracking.** Glass/bottle buttons and a daily goal based on body weight.
- **Adaptive calories.** Log your weight and food; after ~2 weeks the app measures your *real* daily burn from your own data (food intake minus the least-squares weight trend × 7700 kcal/kg) and offers to replace the formula estimate.
- **Plate calculator.** Under every barbell exercise, a drawing shows which plates to load on each side, live as you change the weight.
- **Easy on the eyes.** An "iron & chalk" design: colours taken from competition weight plates, each with one meaning (red protein, yellow carbs, green fat, blue water), light and dark themes, large touch targets. See [docs/DESIGN.md](docs/DESIGN.md).
- **Bilingual UI.** Full Arabic (RTL) and English (LTR), switchable at any time. Numbers always use Western digits (0-9) for readability. Works on mobile and can be installed as a PWA.

### Tech stack
| Layer | Tools |
|---|---|
| Backend | Python 3.12, FastAPI, SQLModel (SQLAlchemy + Pydantic) |
| Database | SQLite locally, PostgreSQL (Supabase) in production via `DATABASE_URL` |
| Auth | JWT (PyJWT) + bcrypt password hashing |
| Frontend | Vanilla JavaScript, HTML, CSS (no build step) |
| Quality | pytest (76 tests, on SQLite and PostgreSQL), ruff, GitHub Actions CI |
| Deploy | Docker, Docker Compose |

### Run locally
```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
fastapi dev app/main.py
```
Open http://localhost:8000. The interactive API docs are at http://localhost:8000/docs.

### Deploy (Supabase + Render)
The app runs anywhere Python runs; the database can be any Postgres. A free setup:

1. **Database: Supabase.** Create a project, then copy the **session pooler** connection string from *Connect* (port `5432`, user `postgres.<project-ref>`). The session pooler works over IPv4 and supports SQLAlchemy's prepared statements.
2. **App: Render.** Push this repo to GitHub, then in Render choose *New → Blueprint* and pick the repo. `render.yaml` sets everything up; paste the Supabase URL as `DATABASE_URL` when asked. `SECRET_KEY` is generated for you.
3. Tables are created on first start (the full schema is also in `database/schema.sql`). On Postgres the app also enables Row Level Security on every table and revokes access for Supabase's public API roles (`anon`, `authenticated`), so the data is only reachable through this app.

**Or on Vercel.** Import the GitHub repo in Vercel; it detects FastAPI (`[tool.vercel] entrypoint` in `pyproject.toml`). Set `SECRET_KEY`, and set `DATABASE_URL` to Supabase's **transaction pooler** string (port `6543`). The app sees port 6543 and switches to a serverless-friendly setup: no client-side pool, no prepared statements.

Free-tier notes: Render's free web services sleep when idle (the first request after a while is slow), and free Supabase projects can be paused after a period of inactivity.

**With Docker:**
```bash
SECRET_KEY=your-long-random-secret docker compose up --build
```

### Tests
```bash
pytest -q
ruff check . && ruff format --check .
# also run the whole suite against a real Postgres:
TEST_DATABASE_URL=postgresql://user:pass@localhost:5432/fitplan_test pytest -q
```

### Project structure
```
app/
  main.py              # app setup, routers, static files
  config.py            # settings from environment variables
  database.py          # engine and session
  models.py            # database tables
  schemas.py           # request/response validation
  security.py          # password hashing, JWT
  deps.py              # auth dependency (current user)
  seed.py              # built-in foods
  routers/             # auth, profile, workouts, meals
  services/
    nutrition.py       # BMR / TDEE / macro calculations
    workouts.py        # exercise library, split templates, progression
  static/              # frontend
tests/
```

### API overview
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register` | Create an account |
| POST | `/api/auth/login` | Get an access token |
| GET / PUT | `/api/profile` | Read or update your profile and targets |
| POST | `/api/workouts/plan` | Generate a plan from training days |
| POST | `/api/workouts/plan/custom` | Start an empty plan to build by hand |
| POST | `/api/workouts/plan/days` | Add a training day |
| PATCH / DELETE | `/api/workouts/plan/days/{id}` | Rename, move or delete a day |
| POST | `/api/workouts/plan/exercises/{id}/move` | Reorder an exercise |
| GET / POST | `/api/exercises` | Exercise library, add a custom exercise |
| GET | `/api/workouts/plan` | Active plan |
| GET | `/api/workouts/today?day=` | Today's workout with suggestions |
| POST | `/api/workouts/plan/days/{id}/exercises` | Add an exercise to a day |
| PATCH / DELETE | `/api/workouts/plan/exercises/{id}` | Edit or remove an exercise |
| POST / GET | `/api/workouts/logs` | Log a workout, list history |
| GET | `/api/workouts/progress/{exercise}` | Estimated 1RM over time |
| GET / POST | `/api/foods` | Search foods, add a custom food |
| POST | `/api/meals` | Log food |
| GET | `/api/meals?day=` | A day's meals, totals and remaining macros |
| DELETE | `/api/meals/{id}` | Remove a logged food |
| POST | `/api/meals/batch` | Log several foods at once |
| GET | `/api/exercises/{key}/guide` | How-to guide and muscles for an exercise |
| POST | `/api/meals/quick` | Quick-add calories/macros |
| POST | `/api/meals/copy` | Copy a day (or one meal) to another day |
| GET / POST / DELETE | `/api/saved-meals` | Saved meals; `POST /api/saved-meals/{id}/log` to log one |
| GET / POST / DELETE | `/api/recipes` | Recipes built from ingredients |
| GET / POST | `/api/water` | Daily water intake and goal |
| GET / PUT / DELETE | `/api/weights` | Body weight (one entry per day) |
| GET | `/api/adaptive` | Measured daily burn (or progress toward enough data) |
| GET | `/api/progress?today=` | Dashboard: weekly weight, lifts, adherence, last 7 days of nutrition |
| POST | `/api/meal-plan` | Generate a day of meals for your targets |
| POST | `/api/meal-plan/alternatives` | Swaps for one food in the plan |
| GET / PUT | `/api/meal-plan/prefs` | Budget and liked / avoided foods |
| GET | `/api/meal-plan/foods` | Foods the planner can use |
| POST / DELETE | `/api/adaptive/apply` | Use the measured burn for targets / go back to the formula |
| PATCH | `/api/me/social` | Change username / private mode |
| GET | `/api/users/search?q=` | Find people by name or @username |
| GET | `/api/users/{username}` | Someone's profile and recent workouts |
| POST / DELETE | `/api/users/{username}/follow` | Follow / unfollow |
| GET | `/api/feed?before_id=` | Workouts from you and people you follow (paged) |
| POST / DELETE | `/api/workouts/logs/{id}/like` | Give / remove a 💪 |

### Design decisions
- **Users can only see their own data.** Every query is scoped to the current user, and requests for another user's resources return `404` instead of `403`, so they don't reveal that the resource exists.
- **Login errors don't reveal which accounts exist.** A wrong email and a wrong password return the same message.
- **Dates come from the client.** "Today" depends on the user's time zone, so the frontend sends its local date.
- **Old plans are kept, not deleted.** Generating a new plan deactivates the previous one, so workout history stays linked.
- **Food values are stored per 100 g.** Any amount can then be calculated the same way.
- **SQLite behaves like Postgres in tests.** Foreign keys are enforced in SQLite too, and the suite also runs against real Postgres; this caught delete-order bugs that plain SQLite would have hidden.
- **Adaptive calories are guarded.** The estimate needs at least 8 weigh-ins over 14+ days and 10 fully-logged days; days under 800 kcal are treated as incomplete and ignored, and results are clamped to ±30% of the formula so one bad week can't produce extreme targets.
- **The meal planner is rule-based, not a black box.** Each built-in food has a role (protein, carb, vegetable, fat, fruit), the meals it suits, a price tier and natural portion steps (one egg, half a pita). Protein is sized first, carbs fill the remaining calories, then portions are nudged until the day is within a few percent of the targets. Prices vary by country, so budget is only cheap / medium / any.
- **Privacy first in the social features.** Search never matches emails, a private account's workouts return `404` to others (even for likes), and the feed uses keyset paging (`before_id`) so new posts don't shift pages.

### Roadmap
- [ ] Alembic migrations and PostgreSQL in production
- [ ] Weekly meal plan generator based on targets
- [ ] Body weight tracking with charts
- [ ] Rest timer between sets
- [ ] Drag-and-drop reordering
- [ ] Refresh tokens

> Nutrition values are approximate and targets are estimates, not medical advice.

---

<div dir="rtl">

## العربية

تطبيق ويب بالعربي والإنجليزي يسوي لك جدول تمارين الجيم، ويتابع الأوزان اللي ترفعها، وينظم أكلك حسب السعرات والبروتين اللي تحتاجها يوميًا.

### المميزات
- **احتياجك بشكل واضح:** يقولك كم سعرة تاكل عشان توصل لهدفك، وكم الفرق عن حرقك اليومي، وكم بتنزل أو تزيد بالأسبوع. وتقارن بين التنشيف والثبات والتضخيم بضغطة.
- **البروتين كمدى:** أقل شي، والأفضل لهدفك، والحد الأعلى، وكم تاكل في كل وجبة.
- **طريقة الحساب:** يحسب الحرق الأساسي والحرق اليومي، والسعرات والبروتين والكارب والدهون، حسب بياناتك وهدفك (تنشيف أو ثبات أو تضخيم). الحساب بمعادلة Mifflin-St Jeor، مع حد أدنى آمن للسعرات.
- **جدول جاهز أو من الصفر:** تختار أيام تمرينك ويطلع لك جدول متكامل، أو تبني جدولك بنفسك.
- **تحكم كامل بالجدول:** تضيف أيام وتحذفها وتسميها وتغيّر يومها، وتضيف تمارين من مكتبة فيها 102 تمرين أو تمارين خاصة فيك، وتعدّل المجموعات والتكرارات، وترتب التمارين.
- **شاشة اليوم:** توريك تمرين اليوم أو إنه يوم راحة، مع أرقامك من آخر مرة.
- **اقتراح زيادة الوزن:** إذا وصلت لأعلى عدد تكرارات في كل المجموعات، يقترح عليك تزيد 2.5 كغ في التمرين الجاي.
- **رسم بياني للتقدم:** يوضح تطور أقصى وزن متوقع (1RM) لكل تمرين.
- **لوحة التقدّم:** صفحة وحدة فيها نسبة التزامك بالتمارين، ووزنك الأسبوعي واتجاهه، وسعراتك وبروتينك آخر 7 أيام مقارنة بهدفك، وكم تطورت أوزانك.
- **مخطط الوجبات الذكي:** يبني لك يوم أكل كامل على قد سعراتك وبروتينك، ويوريك البروتين بكل وجبة، وتقدر تبدّل أي أكلة ببديل يعطي نفس البروتين أو السعرات، وياخذ بعين الاعتبار ميزانيتك والأكل اللي تحبه أو ما تبيه.
- **تنظيم الأكل:** قاعدة أطعمة فيها أكلات عربية وخليجية (كبسة، فول، لبنة، تمر، حمص…)، وتسجيل الوجبات لكل يوم، ويوريك كم باقي لك. وتقدر تضيف أكلاتك الخاصة.
- **شرح التمارين:** خطوات الأداء، ونصيحة، ورسم يوضح العضلات اللي يشغّلها كل تمرين، ورابط فيديو.
- **وجبات محفوظة ووصفات:** تحفظ وجبة وتضيفها بضغطة، وتسوي وصفة من مكوناتها ويحسب لك سعرات الحصة.
- **نسخ أكل أمس:** اليوم كامل أو وجبة وحدة بضغطة.
- **إضافة سريعة:** تكتب السعرات مباشرة لما تاكل برا.
- **تتبع الماء:** أزرار كوب وقارورة، وهدف يومي حسب وزنك.
- **تعديل السعرات تلقائيًا:** تسجّل وزنك وأكلك، وبعد أسبوعين تقريبًا يحسب حرقك الحقيقي من بياناتك ويعدّل سعراتك.
- **المجتمع:** كل مستخدم له @username، تدوّر على أصحابك وتتابعهم، وتشوف تمارينهم وتعطيهم 💪، وفيه وضع خاص يخفي تمارينك.
- **حاسبة الأقراص:** تحت كل تمرين بالبار، رسم يوريك الأقراص اللي تركّبها على كل جهة.
- **سهل الاستخدام في الجيم:** أزرار + و− للوزن والتكرار، وتعلّم على كل مجموعة تخلصها، ومؤقت راحة يشتغل تلقائيًا.
- **تسجيل أكل سريع:** تختار الحصة بضغطة، وتشوف السعرات قبل ما تضيف، وأكلاتك السابقة جاهزة.
- **مريح للعين:** وضع فاتح وداكن بألوان هادئة.
- **واجهة بلغتين:** عربي (من اليمين لليسار) وإنجليزي، وتبدّل بينهم بضغطة. تشتغل على الجوال وتقدر تثبّتها كتطبيق (PWA).

### التشغيل
```bash
python -m venv .venv
source .venv/bin/activate        # ويندوز: .venv\Scripts\activate
pip install -r requirements-dev.txt
fastapi dev app/main.py
```
افتح http://localhost:8000، وتوثيق الـ API موجود على http://localhost:8000/docs.

### الاختبارات
```bash
pytest -q
```

> القيم الغذائية تقريبية، والأرقام تقديرية وما تغني عن استشارة مختص.

</div>

---

Built with the help of AI coding tools. / تم تطويره بمساعدة أدوات الذكاء الاصطناعي.
