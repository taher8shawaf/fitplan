"""How-to text for the larger exercise library (Arabic + English).

Each entry: (steps_ar, steps_en, tip_ar, tip_en). The muscles shown on the body map
come from the exercise itself (see `app.services.workouts.EXERCISES`).
"""

GUIDE_TEXT: dict[str, tuple[list[str], list[str], str, str]] = {
    # ---------------------------------------------------------------- chest
    "incline_bench_press": (
        [
            "اضبط البنش على ميلان 30 درجة تقريبًا واستلقِ وعينك تحت البار.",
            "امسك البار أعرض من كتوفك بشوي وشد كتوفك لورا.",
            "نزّل البار لأعلى صدرك ببطء، وبعدين ادفعه لفوق.",
        ],
        [
            "Set the bench to about 30° and lie with your eyes under the bar.",
            "Grip slightly wider than shoulder width and pull your shoulders back.",
            "Lower the bar slowly to your upper chest, then press it up.",
        ],
        "ميلان أكثر من 45 درجة يحول الشغل للكتف بدل الصدر.",
        "An incline steeper than 45° shifts the work from your chest to your shoulders.",
    ),
    "decline_bench_press": (
        [
            "ثبّت رجولك تحت المساند واستلقِ على البنش المنحدر.",
            "امسك البار أعرض من كتوفك بشوي وفكّه من الحامل بمساعدة.",
            "نزّله لأسفل صدرك ببطء وادفعه لفوق.",
        ],
        [
            "Hook your feet under the pads and lie back on the decline bench.",
            "Grip slightly wider than shoulder width and unrack with help.",
            "Lower the bar to your lower chest slowly, then press it up.",
        ],
        "استخدم سبوتر دايمًا، لأن الطلوع من البنش المنحدر تحت وزن صعب.",
        "Always use a spotter: getting out from under the bar on a decline is hard.",
    ),
    "db_bench_press": (
        [
            "اجلس على البنش والدمبلز على فخوذك، وبعدين استلقِ وارفعها لمستوى صدرك.",
            "خل كفوفك لقدام والكوع بزاوية 45 درجة تقريبًا مع جسمك.",
            "ادفع الدمبلز لفوق لين تقرب من بعض، ونزّلها ببطء.",
        ],
        [
            "Sit with the dumbbells on your thighs, lie back and bring them to chest level.",
            "Palms face forward, elbows about 45° from your body.",
            "Press up until they nearly touch, then lower slowly.",
        ],
        "الدمبلز تخليك تنزل أعمق من البار، استغلها بس بدون ألم بالكتف.",
        "Dumbbells let you go deeper than a bar; use it, but stop short of shoulder pain.",
    ),
    "chest_press_machine": (
        [
            "اضبط الكرسي بحيث المقابض بمستوى منتصف صدرك.",
            "اسند ظهرك كامل وامسك المقابض.",
            "ادفع لقدام بدون ما تقفل الكوع، وارجع ببطء.",
        ],
        [
            "Set the seat so the handles line up with the middle of your chest.",
            "Keep your back flat against the pad and grip the handles.",
            "Press forward without locking your elbows, then return slowly.",
        ],
        "الجهاز ممتاز لآخر التمرين لما تكون تعبان، لأنه آمن بدون سبوتر.",
        "Machines are great late in a workout when you're tired: safe without a spotter.",
    ),
    "incline_machine_press": (
        [
            "اضبط الكرسي بحيث المقابض بمستوى أعلى صدرك.",
            "اسند ظهرك وشد كتوفك لورا.",
            "ادفع لفوق ولقدام، وارجع ببطء لين تحس بتمدد بصدرك.",
        ],
        [
            "Set the seat so the handles line up with your upper chest.",
            "Keep your back on the pad and shoulders pulled back.",
            "Press up and forward, then return slowly until you feel a stretch.",
        ],
        "لا ترفع كتوفك لأذنك وانت تدفع.",
        "Don't shrug your shoulders toward your ears as you press.",
    ),
    "smith_incline_press": (
        [
            "حط بنش مائل 30 درجة تحت السميث بحيث البار ينزل على أعلى صدرك.",
            "امسك البار أعرض من كتوفك بشوي ولف البار عشان تفكه.",
            "نزّل ببطء لأعلى صدرك وادفع لفوق.",
        ],
        [
            "Place a 30° bench under the Smith bar so it lands on your upper chest.",
            "Grip slightly wider than shoulder width and twist to unrack.",
            "Lower slowly to your upper chest and press up.",
        ],
        "اضبط مكان البنش قبل ما تبدأ، لأن البار يمشي بخط ثابت.",
        "Set the bench position first: the bar moves on a fixed track.",
    ),
    "db_fly": (
        [
            "استلقِ على بنش مستوي والدمبلز فوق صدرك وكفوفك مقابل بعض.",
            "افتح ذراعيك لجنب بقوس واسع والكوع منثني شوي.",
            "نزّل لين تحس بتمدد بصدرك، وبعدين سكّر بنفس القوس.",
        ],
        [
            "Lie on a flat bench with dumbbells over your chest, palms facing each other.",
            "Open your arms in a wide arc with a slight bend in the elbows.",
            "Lower until you feel a stretch in your chest, then close along the same arc.",
        ],
        "استخدم وزن خفيف، هذا تمرين تمدد مو تمرين قوة.",
        "Go light: this is a stretch exercise, not a strength one.",
    ),
    "incline_db_fly": (
        [
            "استلقِ على بنش مائل 30 درجة والدمبلز فوق صدرك.",
            "افتح ذراعيك لجنب والكوع منثني شوي.",
            "نزّل لين تحس بتمدد بأعلى صدرك، وبعدين سكّر.",
        ],
        [
            "Lie on a 30° incline bench with dumbbells over your chest.",
            "Open your arms out to the sides, elbows slightly bent.",
            "Lower until you feel a stretch in your upper chest, then close.",
        ],
        "خل ثنية الكوع ثابتة طول الحركة.",
        "Keep the same elbow bend through the whole movement.",
    ),
    "pec_deck": (
        [
            "اضبط الكرسي بحيث المقابض بمستوى صدرك.",
            "امسك المقابض والكوع منثني شوي، وظهرك على المسند.",
            "سكّر المقابض قدامك واعصر صدرك ثانية، وارجع ببطء.",
        ],
        [
            "Set the seat so the handles are at chest height.",
            "Grip with a slight elbow bend, back against the pad.",
            "Bring the handles together, squeeze for a second, return slowly.",
        ],
        "لا ترجع لورا أكثر من اللازم، الكتف ما يحب التمدد الزايد.",
        "Don't let the handles travel too far back: shoulders dislike overstretching.",
    ),
    "low_cable_fly": (
        [
            "حط بكرات الكيبل تحت وامسك مقبض بكل يد وخطوة لقدام.",
            "ذراعيك تحت ولجنب والكوع منثني شوي.",
            "ارفع يدينك لفوق ولقدام لين يتقابلوا بمستوى كتوفك.",
        ],
        [
            "Set the pulleys low, take a handle in each hand and step forward.",
            "Start with arms low and out, elbows slightly bent.",
            "Sweep your hands up and in until they meet at shoulder height.",
        ],
        "هذا التمرين يركز على أعلى الصدر.",
        "This version targets the upper chest.",
    ),
    "chest_dip": (
        [
            "امسك المتوازي وارفع جسمك وذراعيك مستقيمة.",
            "ميّل جسمك لقدام شوي ونزّل لين الكوع يصير بزاوية 90 درجة.",
            "ادفع لفوق لين ترجع ذراعيك مستقيمة.",
        ],
        [
            "Grip the bars and lift yourself up with straight arms.",
            "Lean forward slightly and lower until your elbows reach about 90°.",
            "Press back up to straight arms.",
        ],
        "الميلان لقدام يشغل الصدر، والجسم المستقيم يشغل الترايسبس أكثر.",
        "Leaning forward works the chest; staying upright works the triceps more.",
    ),
    "db_pullover": (
        [
            "استلقِ على البنش وامسك دمبل وحدة بيدينك فوق صدرك.",
            "نزّل الدمبل لورا راسك بقوس والكوع منثني شوي.",
            "لما تحس بتمدد، ارجع بنفس القوس لفوق صدرك.",
        ],
        [
            "Lie on a bench holding one dumbbell with both hands over your chest.",
            "Lower it back behind your head in an arc, elbows slightly bent.",
            "When you feel a stretch, bring it back over your chest along the same arc.",
        ],
        "لا تنزل أبعد من ما يسمح كتفك.",
        "Don't lower further than your shoulders comfortably allow.",
    ),
    # ---------------------------------------------------------------- back
    "rack_pull": (
        [
            "حط البار على حامل بمستوى تحت الركبة أو فوقها شوي.",
            "امسك البار وظهرك مستقيم وصدرك لفوق.",
            "قوم وادفع الحوض لقدام لين توقف مستقيم، ونزّل بتحكم.",
        ],
        [
            "Set the bar on pins just below or above your knees.",
            "Grip it with a flat back and chest up.",
            "Stand up, driving your hips forward until upright, then lower with control.",
        ],
        "تقدر تشيل أوزان أثقل من الرفعة الكاملة، بس لا تقوّس ظهرك.",
        "You can lift more than a full deadlift, but never round your back.",
    ),
    "t_bar_row": (
        [
            "وقف فوق البار ومد رجولك بعرض الكتف، وانحني لقدام وظهرك مستقيم.",
            "امسك المقبض بيدينك.",
            "اسحب لصدرك واعصر ظهرك، ونزّل ببطء.",
        ],
        [
            "Straddle the bar, feet shoulder-width apart, and hinge forward with a flat back.",
            "Grip the handle with both hands.",
            "Row it to your chest, squeeze your back, then lower slowly.",
        ],
        "خل صدرك لفوق وظهرك ثابت، لا تهز جسمك عشان ترفع الوزن.",
        "Keep your chest up and torso still; don't swing to move the weight.",
    ),
    "one_arm_db_row": (
        [
            "حط ركبة ويد على البنش، والرجل الثانية على الأرض.",
            "امسك الدمبل باليد الثانية وظهرك مستقيم.",
            "اسحب الدمبل لجنب خصرك، ونزّل ببطء لين ذراعك تمتد.",
        ],
        [
            "Put one knee and hand on the bench, other foot on the floor.",
            "Hold the dumbbell in your free hand with a flat back.",
            "Pull it toward your hip, then lower slowly to a full stretch.",
        ],
        "فكّر إنك تسحب بالكوع مو باليد.",
        "Think about pulling with your elbow, not your hand.",
    ),
    "chest_supported_row": (
        [
            "استلقِ على بطنك على بنش مائل ومعك دمبلز أو على جهاز مخصص.",
            "خل ذراعيك تتدلى تحت.",
            "اسحب لفوق لين الكوع يعدي ظهرك، واعصر لوحات كتفك، ونزّل ببطء.",
        ],
        [
            "Lie chest-down on an incline bench with dumbbells, or use the machine.",
            "Let your arms hang straight down.",
            "Row up until your elbows pass your back, squeeze your shoulder blades, lower slowly.",
        ],
        "المسند يمنعك من الغش، فيشتغل ظهرك لحاله.",
        "The pad stops you cheating, so your back does all the work.",
    ),
    "machine_row": (
        [
            "اضبط الكرسي بحيث المقابض بمستوى صدرك، واسند صدرك على المسند.",
            "امسك المقابض وذراعيك ممدودة.",
            "اسحب لورا واعصر ظهرك، وارجع ببطء.",
        ],
        [
            "Set the seat so the handles are at chest height; chest against the pad.",
            "Grip the handles with arms straight.",
            "Pull back, squeeze your back, return slowly.",
        ],
        "لا تميل لورا عشان تسحب، خل صدرك على المسند.",
        "Don't lean back to pull; keep your chest on the pad.",
    ),
    "close_grip_pulldown": (
        [
            "ركّب المقبض الضيق (V) واجلس ورجولك تحت المسند.",
            "امسك المقبض وميّل لورا شوي.",
            "اسحب لأعلى صدرك والكوع لتحت، وارجع ببطء لين تمتد ذراعيك.",
        ],
        [
            "Attach a close-grip (V) handle and sit with your thighs under the pad.",
            "Grip the handle and lean back slightly.",
            "Pull to your upper chest with elbows down, return slowly to full stretch.",
        ],
        "خل التمدد كامل فوق، هذا نص فايدة التمرين.",
        "Get a full stretch at the top: that's half the benefit.",
    ),
    "straight_arm_pulldown": (
        [
            "وقف قدام الكيبل وامسك البار أو الحبل فوق، وميّل لقدام شوي.",
            "خل ذراعيك مستقيمة تقريبًا.",
            "اسحب البار لتحت لين يوصل فخوذك، وارجع ببطء.",
        ],
        [
            "Stand facing a high cable, grip the bar or rope, lean forward slightly.",
            "Keep your arms nearly straight.",
            "Pull the bar down to your thighs, then return slowly.",
        ],
        "تمرين ممتاز تحس فيه بعضلة الظهر الجانبية قبل السحب الأمامي.",
        "A good way to feel your lats working before pulldowns.",
    ),
    "chin_up": (
        [
            "امسك البار وكفوفك لوجهك بعرض الكتف.",
            "علّق جسمك وذراعيك مستقيمة.",
            "اسحب لين ذقنك يعدي البار، ونزّل ببطء لين ترجع مستقيم.",
        ],
        [
            "Grip the bar with palms facing you, shoulder-width apart.",
            "Hang with straight arms.",
            "Pull until your chin clears the bar, then lower slowly to a full hang.",
        ],
        "أسهل من العقلة العادية لأن البايسبس يساعد أكثر.",
        "Easier than a pull-up because your biceps help more.",
    ),
    "assisted_pull_up": (
        [
            "اختار وزن المساعدة على الجهاز، كل ما زاد صار أسهل.",
            "اركب على المسند وامسك المقابض أعرض من كتوفك.",
            "اسحب لين ذقنك يعدي المقابض، ونزّل ببطء.",
        ],
        [
            "Pick the assistance weight: more weight makes it easier.",
            "Kneel or stand on the pad and grip wider than your shoulders.",
            "Pull until your chin clears the handles, then lower slowly.",
        ],
        "نزّل المساعدة شوي شوي لين تقدر تسوي عقلة بدونها.",
        "Reduce the assistance over time until you can do pull-ups without it.",
    ),
    "back_extension": (
        [
            "اضبط الجهاز بحيث المسند تحت عظمة الحوض وثبّت رجولك.",
            "حط يدينك على صدرك ونزّل جسمك لقدام وظهرك مستقيم.",
            "ارفع جسمك لين يصير خط مستقيم مع رجولك، لا تكمل لورا.",
        ],
        [
            "Set the pad just below your hip bones and lock your feet in.",
            "Cross your arms on your chest and lower forward with a flat back.",
            "Rise until your body is in a straight line; don't arch past it.",
        ],
        "لما يصير سهل، امسك قرص على صدرك.",
        "When it gets easy, hold a plate against your chest.",
    ),
    "barbell_shrug": (
        [
            "وقف وامسك البار قدام فخوذك بعرض الكتف.",
            "ذراعيك مستقيمة والجسم ثابت.",
            "ارفع كتوفك لأذنك واعصر ثانية، ونزّل ببطء.",
        ],
        [
            "Stand holding the bar in front of your thighs, shoulder-width grip.",
            "Arms straight, body still.",
            "Lift your shoulders toward your ears, hold a second, lower slowly.",
        ],
        "لا تلف كتوفك، طلوع ونزول بس.",
        "Don't roll your shoulders: straight up and down.",
    ),
    "db_shrug": (
        ["وقف ودمبل بكل يد على جنبك.", "ذراعيك مستقيمة والجسم ثابت.", "ارفع كتوفك لأذنك واعصر ثانية، ونزّل ببطء."],
        [
            "Stand with a dumbbell in each hand at your sides.",
            "Arms straight, body still.",
            "Lift your shoulders toward your ears, hold a second, lower slowly.",
        ],
        "الدمبلز تعطيك حركة أطول من البار.",
        "Dumbbells give a longer range of motion than a bar.",
    ),
    # ---------------------------------------------------------------- shoulders
    "db_shoulder_press": (
        [
            "اجلس على بنش ظهره مستقيم، والدمبلز بمستوى كتوفك.",
            "كفوفك لقدام وظهرك على المسند.",
            "ادفع لفوق لين ذراعيك تقرب تستقيم، ونزّل ببطء لمستوى الكتف.",
        ],
        [
            "Sit on an upright bench with dumbbells at shoulder height.",
            "Palms forward, back against the pad.",
            "Press up until your arms are nearly straight, lower slowly to shoulder level.",
        ],
        "لا تقوّس أسفل ظهرك وانت تدفع.",
        "Don't arch your lower back as you press.",
    ),
    "arnold_press": (
        [
            "اجلس والدمبلز قدام صدرك وكفوفك لوجهك.",
            "وانت تدفع لفوق، لف كفوفك لين تصير لقدام.",
            "ارجع بنفس الحركة بالعكس لين ترجع كفوفك لوجهك.",
        ],
        [
            "Sit with dumbbells in front of your chest, palms facing you.",
            "As you press up, rotate your palms to face forward.",
            "Reverse the movement on the way down.",
        ],
        "خذ وزن أخف من ضغط الأكتاف العادي.",
        "Use a lighter weight than a regular shoulder press.",
    ),
    "machine_shoulder_press": (
        [
            "اضبط الكرسي بحيث المقابض بمستوى كتوفك.",
            "اسند ظهرك وامسك المقابض.",
            "ادفع لفوق بدون ما تقفل الكوع، ونزّل ببطء.",
        ],
        [
            "Set the seat so the handles start at shoulder height.",
            "Back against the pad, grip the handles.",
            "Press up without locking your elbows, lower slowly.",
        ],
        "خيار آمن لما تكون لحالك بدون سبوتر.",
        "A safe choice when you train alone.",
    ),
    "cable_lateral_raise": (
        [
            "حط البكرة تحت ووقف جنب الجهاز، وامسك المقبض باليد البعيدة.",
            "الكوع منثني شوي.",
            "ارفع ذراعك لجنب لمستوى الكتف، ونزّل ببطء.",
        ],
        [
            "Set the pulley low, stand side-on and take the handle in your far hand.",
            "Keep a slight bend in the elbow.",
            "Raise your arm out to shoulder height, lower slowly.",
        ],
        "الكيبل يعطي شد ثابت طول الحركة، حتى تحت.",
        "The cable keeps tension on the muscle the whole way, even at the bottom.",
    ),
    "front_raise": (
        ["وقف ودمبل بكل يد قدام فخوذك.", "الكوع منثني شوي والجسم ثابت.", "ارفع الدمبلز لقدام لمستوى الكتف، ونزّل ببطء."],
        [
            "Stand holding dumbbells in front of your thighs.",
            "Slight elbow bend, body still.",
            "Raise them forward to shoulder height, lower slowly.",
        ],
        "الكتف الأمامي يشتغل كثير بالضغط، فما يحتاج حجم كبير هنا.",
        "Front delts already work hard in pressing, so a few sets are enough.",
    ),
    "rear_delt_fly": (
        [
            "انحني لقدام وظهرك مستقيم، ودمبل خفيف بكل يد.",
            "خل ذراعيك تتدلى تحت والكوع منثني شوي.",
            "افتح ذراعيك لجنب لين مستوى كتفك، ونزّل ببطء.",
        ],
        [
            "Hinge forward with a flat back, a light dumbbell in each hand.",
            "Let your arms hang with a slight elbow bend.",
            "Raise them out to the sides to shoulder level, lower slowly.",
        ],
        "وزن خفيف وتحكم كامل، لا تهز جسمك.",
        "Light weight, full control; don't swing.",
    ),
    "reverse_pec_deck": (
        [
            "اجلس على جهاز الفراشة ووجهك للمسند.",
            "امسك المقابض وذراعيك ممدودة قدامك.",
            "افتح ذراعيك لورا لين تصير بخط واحد مع كتوفك، وارجع ببطء.",
        ],
        [
            "Sit facing the pec deck pad.",
            "Grip the handles with your arms straight out in front.",
            "Open your arms back until they line up with your shoulders, return slowly.",
        ],
        "لا تعصر لوحات كتفك بقوة، خل الشغل على الكتف الخلفي.",
        "Don't squeeze your shoulder blades hard; let the rear delts do the work.",
    ),
    "upright_row": (
        [
            "وقف وامسك البار أو الدمبلز قدام فخوذك.",
            "اسحب لفوق قريب من جسمك والكوع يقود الحركة.",
            "وقّف لما يوصل الكوع لمستوى الكتف، ونزّل ببطء.",
        ],
        [
            "Stand holding a bar or dumbbells in front of your thighs.",
            "Pull up close to your body, leading with the elbows.",
            "Stop when your elbows reach shoulder height, lower slowly.",
        ],
        "قبضة أعرض من الكتف أريح للمفصل، ووقّف إذا حسيت بألم.",
        "A wider-than-shoulder grip is easier on the joint; stop if it pinches.",
    ),
    # ---------------------------------------------------------------- biceps
    "ez_bar_curl": (
        [
            "وقف وامسك البار المتعرج على الأجزاء المايلة.",
            "الكوع ثابت جنب جسمك.",
            "ارفع البار لصدرك، ونزّل ببطء لين ذراعيك تمتد.",
        ],
        [
            "Stand holding the EZ bar on the angled grips.",
            "Keep your elbows pinned at your sides.",
            "Curl the bar up to your chest, lower slowly to full extension.",
        ],
        "أريح للرسغ من البار المستقيم.",
        "Easier on the wrists than a straight bar.",
    ),
    "db_curl": (
        ["وقف ودمبل بكل يد وكفوفك لقدام.", "الكوع ثابت جنب جسمك.", "ارفع الدمبلز لكتوفك، ونزّل ببطء."],
        [
            "Stand with a dumbbell in each hand, palms forward.",
            "Keep your elbows at your sides.",
            "Curl them up to your shoulders, lower slowly.",
        ],
        "تقدر ترفع يد بعد يد عشان تركز أكثر.",
        "You can alternate arms to focus on each side.",
    ),
    "incline_db_curl": (
        [
            "اجلس على بنش مائل 45 درجة وخل ذراعيك تتدلى.",
            "الكوع ثابت وكفوفك لقدام.",
            "ارفع الدمبلز بدون ما يتحرك الكوع لقدام، ونزّل ببطء.",
        ],
        [
            "Sit back on a 45° incline bench and let your arms hang.",
            "Elbows still, palms forward.",
            "Curl up without letting your elbows drift forward, lower slowly.",
        ],
        "الوضعية تمدد البايسبس أكثر، فخذ وزن أخف.",
        "This position stretches the biceps more, so go lighter.",
    ),
    "preacher_curl": (
        [
            "اجلس على كرسي السكوت وحط ذراعيك على المسند.",
            "امسك البار أو الدمبل وذراعيك ممدودة تقريبًا.",
            "ارفع لفوق، ونزّل ببطء بدون ما تقفل الكوع تحت.",
        ],
        [
            "Sit at the preacher bench with your upper arms on the pad.",
            "Hold the bar or dumbbell with arms nearly straight.",
            "Curl up, then lower slowly without slamming into a locked elbow.",
        ],
        "المسند يمنع الغش، فخذ وزن أخف من البار العادي.",
        "The pad stops you cheating, so use less weight than a standing curl.",
    ),
    "cable_curl": (
        ["حط البكرة تحت وامسك البار أو الحبل.", "وقف قريب والكوع ثابت جنب جسمك.", "ارفع لصدرك واعصر، ونزّل ببطء."],
        [
            "Set the pulley low and grip the bar or rope.",
            "Stand close, elbows at your sides.",
            "Curl up to your chest, squeeze, lower slowly.",
        ],
        "الكيبل يحافظ على الشد حتى تحت.",
        "The cable keeps tension even at the bottom.",
    ),
    "concentration_curl": (
        [
            "اجلس على بنش ورجولك مفتوحة، وحط ظهر ذراعك على فخذك من جوا.",
            "امسك الدمبل وذراعك ممدودة.",
            "ارفع الدمبل لكتفك، ونزّل ببطء.",
        ],
        [
            "Sit on a bench, legs apart, back of your upper arm against your inner thigh.",
            "Hold the dumbbell with your arm straight.",
            "Curl it to your shoulder, lower slowly.",
        ],
        "ركز على العصرة فوق، مو على الوزن.",
        "Focus on the squeeze at the top, not the weight.",
    ),
    # ---------------------------------------------------------------- triceps
    "rope_pushdown": (
        [
            "ركّب الحبل على البكرة فوق وامسكه بيدينك.",
            "الكوع ثابت جنب جسمك.",
            "ادفع لتحت وافتح الحبل لجنب آخر الحركة، وارجع ببطء.",
        ],
        [
            "Attach a rope to a high pulley and grip it with both hands.",
            "Pin your elbows at your sides.",
            "Push down and spread the rope apart at the bottom, return slowly.",
        ],
        "فتح الحبل تحت يعطي عصرة أقوى للترايسبس.",
        "Spreading the rope at the bottom gives a stronger triceps squeeze.",
    ),
    "cable_overhead_ext": (
        [
            "ركّب الحبل وعطي ظهرك للجهاز، وامسك الحبل ورا راسك.",
            "ميّل لقدام شوي والكوع لفوق.",
            "مد ذراعيك لقدام وفوق، وارجع ببطء لين تحس بتمدد.",
        ],
        [
            "Attach a rope, face away from the machine and hold the rope behind your head.",
            "Lean forward slightly with elbows up.",
            "Extend your arms forward and up, return slowly to a stretch.",
        ],
        "خل الكوع ثابت وما يفتح لجنب.",
        "Keep your elbows in place; don't let them flare out.",
    ),
    "skull_crusher": (
        [
            "استلقِ على البنش وامسك البار المتعرج فوق صدرك.",
            "نزّل البار لجبهتك أو ورا راسك بثني الكوع بس.",
            "مد ذراعيك لفوق، والكوع ثابت طول الحركة.",
        ],
        [
            "Lie on a bench holding an EZ bar over your chest.",
            "Lower it to your forehead or just behind your head by bending only at the elbows.",
            "Extend back up, keeping your elbows still.",
        ],
        "ابدأ بوزن خفيف، والكوع ما يتحرك لقدام أو لجنب.",
        "Start light, and don't let your elbows drift forward or out.",
    ),
    "close_grip_bench": (
        ["استلقِ على البنش وامسك البار بعرض الكتف.", "خل الكوع قريب من جسمك.", "نزّل البار لأسفل صدرك ببطء، وادفع لفوق."],
        [
            "Lie on the bench and grip the bar at shoulder width.",
            "Keep your elbows close to your body.",
            "Lower the bar slowly to your lower chest, press back up.",
        ],
        "لا تضيّق القبضة أكثر من الكتف، تتعب الرسغ.",
        "Don't grip narrower than shoulder width: it strains the wrists.",
    ),
    "triceps_dip": (
        [
            "امسك المتوازي وارفع جسمك وذراعيك مستقيمة.",
            "خل جسمك مستقيم والكوع لورا.",
            "نزّل لين الكوع 90 درجة، وادفع لفوق.",
        ],
        [
            "Grip the bars and lift yourself up with straight arms.",
            "Keep your body upright and elbows pointing back.",
            "Lower until your elbows are at 90°, then press up.",
        ],
        "إذا صعب، استخدم جهاز المساعدة أو سويه على البنش.",
        "If it's too hard, use the assisted machine or do bench dips.",
    ),
    "db_kickback": (
        [
            "انحني لقدام وظهرك مستقيم، وحط يد على البنش.",
            "ارفع الكوع لمستوى جسمك وثبته.",
            "مد ذراعك لورا لين تستقيم، وارجع ببطء.",
        ],
        [
            "Hinge forward with a flat back, one hand on the bench.",
            "Lift your elbow to torso level and keep it there.",
            "Extend your arm back until straight, return slowly.",
        ],
        "وزن خفيف وعصرة ثانية آخر الحركة.",
        "Light weight, squeeze for a second at the end.",
    ),
    # ---------------------------------------------------------------- forearms
    "wrist_curl": (
        [
            "اجلس وحط ساعدك على فخوذك أو بنش وكفوفك لفوق.",
            "خل الدمبل أو البار ينزل بأصابعك.",
            "ارفع الرسغ لفوق لأعلى نقطة، ونزّل ببطء.",
        ],
        [
            "Sit with your forearms on your thighs or a bench, palms up.",
            "Let the dumbbell or bar roll down to your fingers.",
            "Curl your wrists up as far as you can, lower slowly.",
        ],
        "عدات كثيرة (15 إلى 20) تناسب الساعد.",
        "High reps (15 to 20) suit the forearms.",
    ),
    "reverse_curl": (
        ["وقف وامسك البار وكفوفك لتحت.", "الكوع ثابت جنب جسمك.", "ارفع البار لصدرك، ونزّل ببطء."],
        [
            "Stand holding the bar with palms facing down.",
            "Keep your elbows at your sides.",
            "Curl the bar to your chest, lower slowly.",
        ],
        "خذ وزن أخف بكثير من البايسبس العادي.",
        "Use much less weight than a regular curl.",
    ),
    "farmers_walk": (
        ["امسك دمبل ثقيل بكل يد ووقف مستقيم.", "شد بطنك وكتوفك لورا.", "امشِ بخطوات قصيرة وثابتة لمسافة أو وقت محدد."],
        [
            "Pick up a heavy dumbbell in each hand and stand tall.",
            "Brace your core, shoulders back.",
            "Walk with short, steady steps for a set distance or time.",
        ],
        "يقوي القبضة والجسم كله، ويساعدك بالرفعة الميتة.",
        "Builds grip and whole-body strength, and helps your deadlift.",
    ),
    # ---------------------------------------------------------------- legs
    "front_squat": (
        [
            "حط البار على مقدمة كتوفك والكوع لفوق ولقدام.",
            "رجولك بعرض الكتف وصدرك مرفوع.",
            "انزل لين فخذك يوازي الأرض أو تحت، واطلع وصدرك لفوق.",
        ],
        [
            "Rest the bar on the front of your shoulders, elbows high.",
            "Feet shoulder-width apart, chest up.",
            "Squat to parallel or below, drive up keeping your chest high.",
        ],
        "لو صعب تمسك البار، استخدم قبضة متقاطعة أو أحزمة.",
        "If the grip is hard, use a crossed-arm grip or straps.",
    ),
    "smith_squat": (
        ["حط البار على أعلى ظهرك ورجولك لقدام شوي.", "لف البار عشان تفكه.", "انزل لين فخذك يوازي الأرض، واطلع."],
        [
            "Set the bar on your upper back with feet slightly in front of you.",
            "Twist the bar to unrack it.",
            "Squat to parallel, drive back up.",
        ],
        "مكان رجولك يغير الشغل: لقدام أكثر للأرداف، تحت البار أكثر للفخذ الأمامي.",
        "Foot position changes the work: further forward for glutes, under the bar for quads.",
    ),
    "hack_squat": (
        [
            "اسند ظهرك وكتوفك على الجهاز ورجولك بعرض الكتف على المنصة.",
            "فك الأقفال.",
            "انزل لين ركبتك 90 درجة أو أعمق، وادفع لفوق.",
        ],
        [
            "Back and shoulders against the pads, feet shoulder-width on the platform.",
            "Release the safety handles.",
            "Lower until your knees reach 90° or deeper, then push up.",
        ],
        "رجول أوطى على المنصة تشغل الفخذ الأمامي أكثر.",
        "Feet lower on the platform work the quads more.",
    ),
    "goblet_squat": (
        [
            "امسك دمبل قدام صدرك بيدينك.",
            "رجولك أعرض من الكتف شوي وأصابعك لبرا شوي.",
            "انزل بين ركبك وصدرك لفوق، واطلع.",
        ],
        [
            "Hold one dumbbell against your chest with both hands.",
            "Feet slightly wider than shoulder width, toes turned out a little.",
            "Squat down between your knees with your chest up, then stand.",
        ],
        "أحسن تمرين تتعلم فيه السكوات الصح.",
        "The best way to learn good squat form.",
    ),
    "bulgarian_split_squat": (
        [
            "حط ظهر رجلك الخلفية على بنش وراك.",
            "الرجل الأمامية لقدام بمسافة تخليك تنزل مستقيم.",
            "انزل لين ركبتك الخلفية تقرب من الأرض، وادفع بالرجل الأمامية.",
        ],
        [
            "Rest the top of your back foot on a bench behind you.",
            "Place your front foot far enough forward to lower straight down.",
            "Drop until your back knee nearly touches the floor, push through the front foot.",
        ],
        "ابدأ بوزن جسمك بس، التوازن ياخذ وقت.",
        "Start with bodyweight only: balance takes practice.",
    ),
    "step_up": (
        [
            "وقف قدام بوكس أو بنش بارتفاع الركبة تقريبًا، ودمبل بكل يد.",
            "حط رجل كاملة على البوكس.",
            "اطلع بالدفع من الرجل اللي فوق، وانزل ببطء.",
        ],
        [
            "Stand facing a box or bench about knee height, a dumbbell in each hand.",
            "Place one whole foot on the box.",
            "Step up by pushing through that foot, step down slowly.",
        ],
        "لا تدفع بالرجل اللي تحت، خل الشغل على اللي فوق.",
        "Don't push off the bottom foot; let the top leg do the work.",
    ),
    "sumo_deadlift": (
        [
            "وقف ورجولك عريضة وأصابعك لبرا، والبار فوق نص رجولك.",
            "امسك البار من جوا رجولك وظهرك مستقيم.",
            "ادفع الأرض برجولك وافتح ركبك لبرا لين توقف مستقيم.",
        ],
        [
            "Take a wide stance with toes out, the bar over mid-foot.",
            "Grip the bar inside your legs with a flat back.",
            "Push the floor away, knees out, until you stand tall.",
        ],
        "خل ركبك بنفس اتجاه أصابع رجولك.",
        "Keep your knees tracking over your toes.",
    ),
    "good_morning": (
        [
            "حط البار على أعلى ظهرك مثل السكوات، ورجولك بعرض الحوض.",
            "ركبك منثنية شوي.",
            "انحني لقدام بالحوض وظهرك مستقيم لين تحس بشد بخلفية الفخذ، وارجع.",
        ],
        [
            "Set the bar on your upper back as for a squat, feet hip-width.",
            "Soften your knees slightly.",
            "Hinge forward at the hips with a flat back until you feel your hamstrings, then stand.",
        ],
        "ابدأ بالبار فاضي، هذا تمرين تحكم مو وزن.",
        "Start with an empty bar: this is about control, not load.",
    ),
    "seated_leg_curl": (
        ["اجلس واضبط المسند فوق ركبك والمسند الثاني ورا كاحلك.", "امسك المقابض.", "اسحب رجولك لتحت ولورا، وارجع ببطء."],
        [
            "Sit and set one pad above your knees and the other behind your ankles.",
            "Hold the handles.",
            "Curl your legs down and back, return slowly.",
        ],
        "الجلوس يمدد خلفية الفخذ أكثر من الجهاز الممدد.",
        "The seated version stretches the hamstrings more than the lying one.",
    ),
    "hip_thrust": (
        [
            "اجلس على الأرض وظهرك على بنش، والبار فوق حوضك مع وسادة.",
            "رجولك على الأرض بعرض الحوض والركب منثنية.",
            "ادفع الحوض لفوق لين جسمك يصير مستقيم، واعصر الأرداف، ونزّل.",
        ],
        [
            "Sit with your upper back against a bench, the padded bar over your hips.",
            "Feet flat, hip-width apart, knees bent.",
            "Drive your hips up until your body is level, squeeze your glutes, lower.",
        ],
        "ذقنك لصدرك فوق، عشان ما تقوّس ظهرك.",
        "Tuck your chin at the top so you don't arch your back.",
    ),
    "glute_bridge": (
        [
            "استلقِ على ظهرك والركب منثنية ورجولك على الأرض.",
            "يدينك على جنبك.",
            "ارفع الحوض لفوق واعصر الأرداف، ونزّل ببطء.",
        ],
        [
            "Lie on your back, knees bent, feet flat.",
            "Arms by your sides.",
            "Lift your hips, squeeze your glutes, lower slowly.",
        ],
        "تقدر تحط دمبل أو قرص على حوضك لما يصير سهل.",
        "Rest a dumbbell or plate on your hips when it gets easy.",
    ),
    "cable_kickback": (
        [
            "ركّب حزام الكاحل على البكرة تحت، ووجهك للجهاز.",
            "امسك الجهاز وميّل لقدام شوي.",
            "ادفع رجلك لورا وفوق، واعصر الأرداف، وارجع ببطء.",
        ],
        [
            "Attach an ankle strap to a low pulley and face the machine.",
            "Hold on and lean forward slightly.",
            "Kick your leg back and up, squeeze your glutes, return slowly.",
        ],
        "لا تقوّس ظهرك عشان ترفع رجلك أعلى.",
        "Don't arch your back to kick higher.",
    ),
    "hip_abduction": (
        ["اجلس على الجهاز والمساند على جنب ركبك من برا.", "اسند ظهرك وامسك المقابض.", "افتح رجولك لبرا، وارجع ببطء."],
        [
            "Sit with the pads on the outside of your knees.",
            "Back against the pad, hold the handles.",
            "Push your legs apart, return slowly.",
        ],
        "الميلان لقدام شوي يشغل الأرداف أكثر.",
        "Leaning forward slightly works the glutes more.",
    ),
    "hip_adduction": (
        ["اجلس على الجهاز والمساند على جنب ركبك من جوا.", "اسند ظهرك وامسك المقابض.", "سكّر رجولك لجوا، وارجع ببطء."],
        [
            "Sit with the pads on the inside of your knees.",
            "Back against the pad, hold the handles.",
            "Squeeze your legs together, return slowly.",
        ],
        "ابدأ بفتحة مريحة وزيدها مع الوقت.",
        "Start with a comfortable range and widen it over time.",
    ),
    "seated_calf_raise": (
        [
            "اجلس على الجهاز والمسند فوق ركبك، وأطراف رجولك على الحافة.",
            "نزّل كعبك لتحت لين تحس بتمدد.",
            "ارفع كعبك لأعلى نقطة واعصر، ونزّل ببطء.",
        ],
        [
            "Sit with the pad over your knees and the balls of your feet on the edge.",
            "Drop your heels for a full stretch.",
            "Rise as high as you can, squeeze, lower slowly.",
        ],
        "الجلوس يشغل العضلة السفلية بالسمانة.",
        "The seated version works the lower calf muscle.",
    ),
    # ---------------------------------------------------------------- core
    "side_plank": (
        [
            "استلقِ على جنبك واسند جسمك على الكوع، والكوع تحت الكتف.",
            "ارفع الحوض لين يصير جسمك خط مستقيم.",
            "اثبت الوقت المحدد وبعدين بدّل الجهة.",
        ],
        [
            "Lie on your side propped on your elbow, elbow under your shoulder.",
            "Lift your hips so your body forms a straight line.",
            "Hold for the set time, then switch sides.",
        ],
        "لا تخلي الحوض ينزل لتحت.",
        "Don't let your hips sag.",
    ),
    "lying_leg_raise": (
        [
            "استلقِ على ظهرك ويدينك تحت أسفل ظهرك أو جنبك.",
            "رجولك مستقيمة.",
            "ارفع رجولك لفوق لين تصير عمودية، ونزّلها ببطء بدون ما تلمس الأرض.",
        ],
        [
            "Lie on your back, hands under your lower back or at your sides.",
            "Legs straight.",
            "Raise your legs until vertical, lower slowly without touching the floor.",
        ],
        "خل أسفل ظهرك لاصق بالأرض.",
        "Keep your lower back pressed into the floor.",
    ),
    "crunch": (
        [
            "استلقِ والركب منثنية ورجولك على الأرض.",
            "يدينك على صدرك أو جنب راسك بدون ما تسحب رقبتك.",
            "ارفع كتوفك عن الأرض واعصر بطنك، ونزّل ببطء.",
        ],
        [
            "Lie back with knees bent and feet flat.",
            "Hands on your chest or by your head, without pulling your neck.",
            "Curl your shoulders off the floor, squeeze your abs, lower slowly.",
        ],
        "الحركة قصيرة، المهم العصرة مو الطلوع لفوق.",
        "It's a short movement: the squeeze matters, not how high you go.",
    ),
    "cable_crunch": (
        [
            "ركّب الحبل فوق واركع قدام الجهاز، وامسك الحبل جنب راسك.",
            "الحوض ثابت.",
            "اثنِ ظهرك لتحت وقرب كوعك لركبك، وارجع ببطء.",
        ],
        [
            "Attach a rope high, kneel facing the machine, hold the rope by your head.",
            "Keep your hips still.",
            "Curl down, bringing your elbows toward your knees, return slowly.",
        ],
        "الحركة من البطن مو من الحوض.",
        "Bend through your abs, not your hips.",
    ),
    "ab_wheel": (
        [
            "اركع على الأرض وامسك العجلة قدام ركبك.",
            "شد بطنك.",
            "دحرج العجلة لقدام لأبعد مسافة تقدر تتحكم فيها، وارجع بشد البطن.",
        ],
        [
            "Kneel on the floor holding the wheel in front of your knees.",
            "Brace your abs.",
            "Roll forward as far as you can control, then pull back with your abs.",
        ],
        "ابدأ بمسافة قصيرة، وزيدها مع الوقت.",
        "Start with a short range and extend it over time.",
    ),
    "russian_twist": (
        [
            "اجلس والركب منثنية وميّل لورا شوي.",
            "امسك يدينك أو دمبل قدام صدرك.",
            "لف جسمك يمين ويسار، والحركة من الجذع مو من اليدين.",
        ],
        [
            "Sit with knees bent and lean back slightly.",
            "Hold your hands together or a dumbbell in front of your chest.",
            "Rotate side to side, turning your torso, not just your arms.",
        ],
        "ارفع رجولك عن الأرض لما يصير سهل.",
        "Lift your feet off the floor when it gets easy.",
    ),
    "mountain_climber": (
        ["ابدأ بوضعية الضغط وذراعيك مستقيمة.", "اسحب ركبة لصدرك وارجعها.", "بدّل الرجلين بسرعة والحوض ثابت."],
        [
            "Start in a push-up position with straight arms.",
            "Drive one knee toward your chest and back.",
            "Alternate legs quickly, keeping your hips level.",
        ],
        "سويه بالوقت: 30 إلى 45 ثانية.",
        "Do it for time: 30 to 45 seconds.",
    ),
    # ---------------------------------------------------------------- cardio
    "treadmill_run": (
        [
            "ابدأ بمشي 3 إلى 5 دقايق عشان تسخن.",
            "زيد السرعة لجري تقدر تتكلم فيه بصعوبة.",
            "آخر 3 دقايق خفف لمشي عشان تهدّي.",
        ],
        [
            "Walk for 3 to 5 minutes to warm up.",
            "Raise the speed to a run where talking is hard but possible.",
            "Slow to a walk for the last 3 minutes to cool down.",
        ],
        "لا تمسك المقابض وانت تجري.",
        "Don't hold the handrails while running.",
    ),
    "incline_walk": (
        ["اضبط الميلان بين 8 و 12 والسرعة بين 4.5 و 5.5 كم/س.", "امشِ وجسمك مستقيم.", "كمّل 20 إلى 30 دقيقة."],
        ["Set the incline to 8–12 and the speed to 4.5–5.5 km/h.", "Walk upright.", "Keep going for 20 to 30 minutes."],
        "لا تمسك المقابض، الشغل يروح كله.",
        "Don't hang on the rails, or you lose most of the work.",
    ),
    "stationary_bike": (
        [
            "اضبط الكرسي بحيث ركبتك منثنية شوي تحت.",
            "ابدأ بمقاومة خفيفة 3 إلى 5 دقايق.",
            "زيد المقاومة لمستوى تتعب فيه وكمّل الوقت.",
        ],
        [
            "Set the seat so your knee is slightly bent at the bottom.",
            "Start with light resistance for 3 to 5 minutes.",
            "Raise the resistance to a challenging level and keep going.",
        ],
        "أريح للركب من الجري.",
        "Easier on the knees than running.",
    ),
    "elliptical": (
        ["اطلع على الجهاز وامسك المقابض المتحركة.", "ابدأ بمقاومة خفيفة.", "زيد المقاومة وكمّل بحركة ثابتة."],
        [
            "Step on and hold the moving handles.",
            "Start with light resistance.",
            "Increase resistance and keep a steady rhythm.",
        ],
        "ادفع واسحب بيدينك عشان يشتغل جسمك كله.",
        "Push and pull with your arms to work your whole body.",
    ),
    "rowing_machine": (
        [
            "اجلس وثبّت رجولك، وامسك المقبض وذراعيك ممدودة.",
            "ادفع برجولك أول، وبعدين ميّل لورا شوي، وبعدين اسحب بيدينك.",
            "ارجع بالعكس: يدينك، جسمك، رجولك.",
        ],
        [
            "Sit, strap in your feet and hold the handle with straight arms.",
            "Push with your legs first, then lean back slightly, then pull with your arms.",
            "Return in reverse: arms, body, legs.",
        ],
        "القوة 60٪ من الرجول، مو من اليدين.",
        "About 60% of the power comes from your legs, not your arms.",
    ),
    "stair_climber": (
        ["اطلع على الجهاز واختار سرعة بطيئة.", "اطلع الدرج وجسمك مستقيم.", "زيد السرعة شوي شوي."],
        ["Step on and pick a slow speed.", "Climb with your body upright.", "Increase the speed gradually."],
        "لا تميل على المقابض، خلها للتوازن بس.",
        "Don't lean on the rails; use them only for balance.",
    ),
    "jump_rope": (
        ["امسك الحبل والكوع قريب من جسمك.", "لف الحبل بالرسغ مو بالكتف.", "انط نطات قصيرة على أطراف رجولك."],
        [
            "Hold the rope with your elbows close to your body.",
            "Turn it with your wrists, not your shoulders.",
            "Make small jumps on the balls of your feet.",
        ],
        "ابدأ بجولات 30 ثانية وراحة بينها.",
        "Start with 30-second rounds with rest in between.",
    ),
    "burpee": (
        [
            "من الوقوف، انزل وحط يدينك على الأرض.",
            "اقفز برجولك لورا لوضعية الضغط، وبعدين رجعها لقدام.",
            "قوم واقفز لفوق.",
        ],
        [
            "From standing, squat down and put your hands on the floor.",
            "Jump your feet back to a push-up position, then bring them forward.",
            "Stand up and jump.",
        ],
        "تقدر تمشي برجولك لورا بدل القفز لو كان صعب.",
        "Step your feet back instead of jumping if it's too hard.",
    ),
}
