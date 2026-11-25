"""How-to guides for the built-in exercises (Arabic + English).

`primary` / `secondary` use the muscle ids drawn on the frontend body map:
chest, shoulders, rear_delts, traps, biceps, triceps, forearms, lats, lower_back,
abs, glutes, quads, hamstrings, calves.
"""

GUIDES: dict[str, dict] = {
    "bench_press": {
        "primary": ["chest"],
        "secondary": ["triceps", "shoulders"],
        "steps_ar": [
            "استلقِ على البنش وعينك تحت البار، ورجولك ثابتة على الأرض.",
            "امسك البار أعرض من كتوفك بشوي، وشد لوحات كتفك لورا وتحت.",
            "نزّل البار ببطء لين يلمس صدرك تحت الحلمة، وبعدين ادفعه لفوق.",
        ],
        "steps_en": [
            "Lie on the bench with your eyes under the bar and feet flat on the floor.",
            "Grip slightly wider than shoulder width and pull your shoulder blades back and down.",
            "Lower the bar slowly to your lower chest, then press it back up.",
        ],
        "tip_ar": "خلّ معك أحد يساعدك (سبوتر) لما تشيل أوزان ثقيلة.",
        "tip_en": "Use a spotter or safety arms when lifting heavy.",
    },
    "incline_db_press": {
        "primary": ["chest", "shoulders"],
        "secondary": ["triceps"],
        "steps_ar": [
            "اضبط البنش على ميلان 30 إلى 45 درجة واجلس ومعك الدمبلز على فخوذك.",
            "ارفع الدمبلز لمستوى صدرك وكفوفك لقدام.",
            "ادفعها لفوق لين تقرب من بعض، وبعدين نزّلها ببطء.",
        ],
        "steps_en": [
            "Set the bench to 30–45° and sit with the dumbbells on your thighs.",
            "Bring them up to chest level with palms facing forward.",
            "Press up until they nearly touch, then lower slowly.",
        ],
        "tip_ar": "لا تخلي الكوع يطلع لبرا كثير، خله بزاوية 45 درجة تقريبًا مع جسمك.",
        "tip_en": "Keep elbows at about 45° from your body, not flared out.",
    },
    "cable_fly": {
        "primary": ["chest"],
        "secondary": ["shoulders"],
        "steps_ar": [
            "اضبط البكرات على مستوى الكتف وامسك المقبضين، وخطوة لقدام.",
            "خلّ الكوع منثني شوي وثابت طول الحركة.",
            "اجمع يدينك قدام صدرك وكأنك تحضن شجرة، وبعدين ارجع ببطء.",
        ],
        "steps_en": [
            "Set the pulleys at shoulder height, grab the handles and step forward.",
            "Keep a slight, fixed bend in your elbows.",
            "Bring your hands together in front of your chest in a hugging motion, then return slowly.",
        ],
        "tip_ar": "ركّز على عصر الصدر، مو على الوزن.",
        "tip_en": "Focus on squeezing your chest, not on the weight.",
    },
    "push_up": {
        "primary": ["chest"],
        "secondary": ["triceps", "shoulders", "abs"],
        "steps_ar": [
            "حط كفوفك على الأرض أعرض من كتوفك بشوي، وجسمك خط مستقيم.",
            "نزّل صدرك لين يقرب من الأرض.",
            "ادفع لفوق وأنت شاد بطنك.",
        ],
        "steps_en": [
            "Place hands slightly wider than shoulders, body in a straight line.",
            "Lower your chest close to the floor.",
            "Push back up while keeping your core tight.",
        ],
        "tip_ar": "إذا صعب عليك، ابدأ على ركبك أو على حافة بنش.",
        "tip_en": "If it's too hard, start on your knees or with hands on a bench.",
    },
    "deadlift": {
        "primary": ["hamstrings", "glutes", "lower_back"],
        "secondary": ["traps", "forearms", "quads"],
        "steps_ar": [
            "وقّف والبار فوق منتصف قدمك، وامسكه برا ركبك.",
            "ظهرك مستقيم، وصدرك لفوق، وشد البار لين تحس بالتوتر قبل ما ترفع.",
            "ادفع الأرض برجولك ووقّف، والبار قريب من جسمك طول الوقت.",
        ],
        "steps_en": [
            "Stand with the bar over mid-foot and grip it just outside your knees.",
            "Keep your back flat and chest up; take the slack out of the bar before lifting.",
            "Push the floor away and stand up, keeping the bar close to your body.",
        ],
        "tip_ar": "لا تقوّس ظهرك أبدًا. لو انحنى، خفّف الوزن.",
        "tip_en": "Never round your back. If it rounds, lower the weight.",
    },
    "barbell_row": {
        "primary": ["lats"],
        "secondary": ["rear_delts", "biceps", "lower_back"],
        "steps_ar": [
            "امسك البار وانحنِ لقدام من الورك لين يصير جسمك قريب من 45 درجة.",
            "ظهرك مستقيم وركبك منثنية شوي.",
            "اسحب البار لبطنك، وبعدين نزّله ببطء.",
        ],
        "steps_en": [
            "Hold the bar and hinge at the hips until your torso is about 45°.",
            "Keep your back flat and knees slightly bent.",
            "Pull the bar to your belly, then lower it slowly.",
        ],
        "tip_ar": "لا تهز جسمك عشان ترفع الوزن.",
        "tip_en": "Don't swing your body to move the weight.",
    },
    "lat_pulldown": {
        "primary": ["lats"],
        "secondary": ["biceps", "rear_delts"],
        "steps_ar": [
            "اجلس وثبّت فخوذك تحت الوسادة، وامسك البار أعرض من كتوفك.",
            "ارجع لورا شوي وصدرك لفوق.",
            "اسحب البار لأعلى صدرك، وبعدين رجّعه ببطء.",
        ],
        "steps_en": [
            "Sit with thighs under the pad and grip the bar wider than shoulders.",
            "Lean back slightly with your chest up.",
            "Pull the bar to your upper chest, then let it rise slowly.",
        ],
        "tip_ar": "فكّر إنك تسحب بأكواعك، مو بيدينك.",
        "tip_en": "Think about pulling with your elbows, not your hands.",
    },
    "pull_up": {
        "primary": ["lats"],
        "secondary": ["biceps", "rear_delts", "forearms"],
        "steps_ar": [
            "تعلّق بالبار وكفوفك لقدام، أعرض من كتوفك بشوي.",
            "شد كتوفك لتحت واسحب نفسك لين يعدّي ذقنك البار.",
            "انزل ببطء لين تمد يدينك كامل.",
        ],
        "steps_en": [
            "Hang from the bar with palms forward, slightly wider than shoulders.",
            "Pull your shoulders down and pull yourself up until your chin clears the bar.",
            "Lower slowly to a full hang.",
        ],
        "tip_ar": "إذا ما تقدر، استخدم مطاط مساعد أو جهاز العقلة المساعد.",
        "tip_en": "If you can't do one yet, use an assistance band or machine.",
    },
    "seated_cable_row": {
        "primary": ["lats"],
        "secondary": ["rear_delts", "biceps", "traps"],
        "steps_ar": [
            "اجلس ورجولك على المسند وركبك منثنية شوي، وامسك المقبض.",
            "ظهرك مستقيم.",
            "اسحب المقبض لبطنك واعصر لوحات كتفك، وبعدين رجّعه ببطء.",
        ],
        "steps_en": [
            "Sit with feet on the platform, knees slightly bent, and grab the handle.",
            "Keep your back straight.",
            "Pull the handle to your belly, squeeze your shoulder blades, then return slowly.",
        ],
        "tip_ar": "لا ترجع بجسمك لورا كثير، الحركة من اليدين والظهر.",
        "tip_en": "Don't lean far back; the movement comes from your arms and back.",
    },
    "overhead_press": {
        "primary": ["shoulders"],
        "secondary": ["triceps", "traps", "abs"],
        "steps_ar": [
            "وقّف والبار على أعلى صدرك، ويدينك أعرض من كتوفك بشوي.",
            "شد بطنك ومؤخرتك.",
            "ادفع البار لفوق راسك لين تمد يدينك، وبعدين نزّله ببطء.",
        ],
        "steps_en": [
            "Stand with the bar on your upper chest, hands slightly wider than shoulders.",
            "Brace your core and glutes.",
            "Press the bar overhead to full lockout, then lower slowly.",
        ],
        "tip_ar": "لا تقوّس أسفل ظهرك وأنت تدفع.",
        "tip_en": "Don't arch your lower back as you press.",
    },
    "lateral_raise": {
        "primary": ["shoulders"],
        "secondary": ["traps"],
        "steps_ar": [
            "وقّف ومعك دمبل في كل يد جنب جسمك.",
            "ارفع يدينك على الجنب لين توصل لمستوى كتوفك، والكوع منثني شوي.",
            "نزّلها ببطء.",
        ],
        "steps_en": [
            "Stand holding a dumbbell in each hand at your sides.",
            "Raise your arms out to the side up to shoulder height, elbows slightly bent.",
            "Lower slowly.",
        ],
        "tip_ar": "استخدم وزن خفيف. هالتمرين يحتاج تحكم، مو قوة.",
        "tip_en": "Use light weights. This one is about control, not strength.",
    },
    "face_pull": {
        "primary": ["rear_delts"],
        "secondary": ["traps"],
        "steps_ar": [
            "اضبط البكرة على مستوى الوجه، وركّب الحبل.",
            "امسك الحبل وارجع خطوة.",
            "اسحب الحبل لوجهك وافتح يدينك على الجنب، وبعدين رجّعه ببطء.",
        ],
        "steps_en": [
            "Set the pulley at face height with a rope attachment.",
            "Grab the rope and step back.",
            "Pull the rope toward your face, spreading your hands apart, then return slowly.",
        ],
        "tip_ar": "ممتاز لصحة الكتف، ولا تستخدم فيه وزن ثقيل.",
        "tip_en": "Great for shoulder health. Keep the weight light.",
    },
    "squat": {
        "primary": ["quads", "glutes"],
        "secondary": ["hamstrings", "lower_back", "abs"],
        "steps_ar": [
            "حط البار على أعلى ظهرك، ورجولك بعرض كتوفك.",
            "خذ نفس وشد بطنك، وانزل كأنك بتجلس على كرسي.",
            "انزل لين يصير فخذك موازي للأرض أو أنزل، وبعدين ادفع لفوق.",
        ],
        "steps_en": [
            "Rest the bar on your upper back with feet shoulder-width apart.",
            "Breathe in, brace your core and sit down as if onto a chair.",
            "Go down until your thighs are at least parallel, then drive back up.",
        ],
        "tip_ar": "خلّ ركبك تمشي بنفس اتجاه أصابع رجلك، ولا تخليها تدخل لجوا.",
        "tip_en": "Keep your knees tracking over your toes; don't let them cave in.",
    },
    "romanian_deadlift": {
        "primary": ["hamstrings", "glutes"],
        "secondary": ["lower_back"],
        "steps_ar": [
            "وقّف وامسك البار قدام فخوذك.",
            "ادفع وركك لورا والبار ينزل قريب من رجولك، وركبك منثنية شوي.",
            "انزل لين تحس بشد خلف فخذك، وبعدين ارجع ووقّف.",
        ],
        "steps_en": [
            "Stand holding the bar in front of your thighs.",
            "Push your hips back and slide the bar down your legs, knees slightly bent.",
            "Go down until you feel a stretch in your hamstrings, then stand back up.",
        ],
        "tip_ar": "ظهرك مستقيم طول الوقت، والحركة كلها من الورك.",
        "tip_en": "Keep your back flat; the movement is all from the hips.",
    },
    "leg_press": {
        "primary": ["quads", "glutes"],
        "secondary": ["hamstrings"],
        "steps_ar": [
            "اجلس ورجولك على المنصة بعرض كتوفك.",
            "فك القفل ونزّل المنصة ببطء لين تصير ركبك بزاوية 90 درجة تقريبًا.",
            "ادفع لفوق بدون ما تقفل ركبك كامل.",
        ],
        "steps_en": [
            "Sit with feet shoulder-width apart on the platform.",
            "Release the safety and lower the platform until knees are about 90°.",
            "Push back up without fully locking your knees.",
        ],
        "tip_ar": "لا تخلي أسفل ظهرك يرتفع عن المقعد.",
        "tip_en": "Don't let your lower back lift off the seat.",
    },
    "leg_curl": {
        "primary": ["hamstrings"],
        "secondary": ["calves"],
        "steps_ar": [
            "اضبط الجهاز بحيث تكون الوسادة فوق كعبك.",
            "اثنِ ركبك واسحب الوسادة لجهة مؤخرتك.",
            "رجّعها ببطء.",
        ],
        "steps_en": [
            "Adjust the machine so the pad sits just above your heels.",
            "Bend your knees to pull the pad toward your glutes.",
            "Return slowly.",
        ],
        "tip_ar": "النزول البطيء هو اللي يفرق في هالتمرين.",
        "tip_en": "The slow lowering is what makes this exercise work.",
    },
    "leg_extension": {
        "primary": ["quads"],
        "secondary": [],
        "steps_ar": [
            "اجلس وظهرك على المسند، والوسادة فوق كاحلك.",
            "مدّ رجولك لين تصير مستقيمة.",
            "نزّلها ببطء.",
        ],
        "steps_en": [
            "Sit with your back against the pad and the roller on your ankles.",
            "Extend your legs until straight.",
            "Lower slowly.",
        ],
        "tip_ar": "اعصر عضلة الفخذ ثانية فوق قبل ما تنزل.",
        "tip_en": "Squeeze your quads for a second at the top.",
    },
    "walking_lunge": {
        "primary": ["quads", "glutes"],
        "secondary": ["hamstrings", "calves"],
        "steps_ar": [
            "وقّف ومعك دمبل في كل يد.",
            "خذ خطوة كبيرة لقدام وانزل لين تقرب ركبتك الخلفية من الأرض.",
            "ادفع بالرجل اللي قدام وكمّل بالرجل الثانية.",
        ],
        "steps_en": [
            "Stand holding a dumbbell in each hand.",
            "Take a long step forward and lower until your back knee nearly touches the floor.",
            "Push through your front foot and step into the next lunge.",
        ],
        "tip_ar": "جسمك مستقيم، والركبة اللي قدام فوق الكاحل.",
        "tip_en": "Keep your torso upright and your front knee over your ankle.",
    },
    "calf_raise": {
        "primary": ["calves"],
        "secondary": [],
        "steps_ar": [
            "وقّف على طرف درجة أو منصة، وكعبك برا.",
            "ارفع كعبك لأعلى نقطة تقدر عليها.",
            "نزّله ببطء لين تحس بشد.",
        ],
        "steps_en": [
            "Stand on the edge of a step with your heels hanging off.",
            "Rise up onto your toes as high as you can.",
            "Lower slowly into a stretch.",
        ],
        "tip_ar": "وقّف ثانية فوق وثانية تحت، بدون نطنطة.",
        "tip_en": "Pause at the top and bottom; don't bounce.",
    },
    "barbell_curl": {
        "primary": ["biceps"],
        "secondary": ["forearms"],
        "steps_ar": [
            "وقّف وامسك البار بعرض كتوفك وكفوفك لفوق.",
            "خلّ أكواعك ثابتة جنب جسمك، وارفع البار لكتوفك.",
            "نزّله ببطء.",
        ],
        "steps_en": [
            "Stand holding the bar shoulder-width with palms up.",
            "Keep your elbows pinned to your sides and curl the bar to your shoulders.",
            "Lower slowly.",
        ],
        "tip_ar": "لا تحرّك جسمك لقدام ولورا عشان ترفع.",
        "tip_en": "Don't swing your body to lift the weight.",
    },
    "hammer_curl": {
        "primary": ["biceps", "forearms"],
        "secondary": [],
        "steps_ar": [
            "امسك الدمبلز وكفوفك مقابلة لبعض.",
            "ارفعها لكتوفك والأكواع ثابتة.",
            "نزّلها ببطء.",
        ],
        "steps_en": [
            "Hold the dumbbells with palms facing each other.",
            "Curl them toward your shoulders, elbows fixed.",
            "Lower slowly.",
        ],
        "tip_ar": "تقدر تشتغل يد يد أو اليدين مع بعض.",
        "tip_en": "You can alternate arms or lift both together.",
    },
    "triceps_pushdown": {
        "primary": ["triceps"],
        "secondary": [],
        "steps_ar": [
            "وقّف قدام الكيبل وامسك البار أو الحبل.",
            "أكواعك ثابتة جنب جسمك.",
            "ادفع لتحت لين تمد يدينك كامل، وبعدين ارجع ببطء.",
        ],
        "steps_en": [
            "Stand facing the cable and grab the bar or rope.",
            "Keep your elbows pinned to your sides.",
            "Push down to full extension, then return slowly.",
        ],
        "tip_ar": "الأكواع ما تتحرك، اللي يتحرك بس الساعد.",
        "tip_en": "Only your forearms move; your elbows stay still.",
    },
    "overhead_triceps": {
        "primary": ["triceps"],
        "secondary": [],
        "steps_ar": [
            "امسك دمبل بيدينك فوق راسك.",
            "نزّله ورا راسك وأكواعك لفوق.",
            "مدّ يدينك لفوق مرة ثانية.",
        ],
        "steps_en": [
            "Hold one dumbbell overhead with both hands.",
            "Lower it behind your head, keeping elbows pointing up.",
            "Extend your arms back up.",
        ],
        "tip_ar": "خلّ أكواعك قريبة من راسك وما تفتح لبرا.",
        "tip_en": "Keep your elbows close to your head.",
    },
    "plank": {
        "primary": ["abs"],
        "secondary": ["shoulders", "glutes"],
        "steps_ar": [
            "اتّكي على ساعدك وأصابع رجلك.",
            "خلّ جسمك خط مستقيم من راسك لكعبك.",
            "شد بطنك ومؤخرتك واثبت.",
        ],
        "steps_en": [
            "Rest on your forearms and toes.",
            "Keep your body in a straight line from head to heels.",
            "Squeeze your abs and glutes and hold.",
        ],
        "tip_ar": "لا ترفع وركك ولا تنزله، وتنفّس طبيعي.",
        "tip_en": "Don't let your hips sag or pike up, and keep breathing.",
    },
    "hanging_leg_raise": {
        "primary": ["abs"],
        "secondary": ["forearms"],
        "steps_ar": [
            "تعلّق بالبار ويدينك مستقيمة.",
            "ارفع رجولك لقدام لين تصير موازية للأرض أو أعلى.",
            "نزّلها ببطء بدون ما تتمرجح.",
        ],
        "steps_en": [
            "Hang from a bar with straight arms.",
            "Raise your legs to at least parallel with the floor.",
            "Lower slowly without swinging.",
        ],
        "tip_ar": "لو صعبة عليك، ابدأ وركبك منثنية.",
        "tip_en": "If it's too hard, start with bent knees.",
    },
}


def _add_library_guides() -> None:
    """Merge the larger library's how-to text, taking each one's muscles from the exercise."""
    from app.services.exercise_guides_more import GUIDE_TEXT
    from app.services.workouts import EXERCISES

    for key, (steps_ar, steps_en, tip_ar, tip_en) in GUIDE_TEXT.items():
        ex = EXERCISES[key]
        GUIDES[key] = {
            "primary": ex["primary"],
            "secondary": ex["secondary"],
            "steps_ar": steps_ar,
            "steps_en": steps_en,
            "tip_ar": tip_ar,
            "tip_en": tip_en,
        }


_add_library_guides()
