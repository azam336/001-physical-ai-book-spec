/**
 * Urdu translations for all book chapters
 * Each chapter maps slug -> Urdu markdown content
 */

export const urduContent = {
  // Introduction Page (index.md)
  '/': `# فزیکل اے آئی کا تعارف

**فزیکل اے آئی کا تعارف** میں خوش آمدید، یہ ایک عملی رہنما ہے جو جسمانی دنیا کے ساتھ تعامل کرنے والے ذہین نظام بنانے کے لیے ہے۔

## اس کتاب کے بارے میں

فزیکل اے آئی - جسے Embodied AI بھی کہا جاتا ہے - مصنوعی ذہانت میں ایک بنیادی تبدیلی کی نمائندگی کرتا ہے۔

یہ کتاب آپ کو بنیادی تصورات سے لے کر اعلیٰ عنوانات تک پانچ جامع ابواب میں لے جاتی ہے:

1. **[مجسم اے آئی کا تعارف](./chapter-01-introduction-to-embodied-ai)** - فزیکل اے آئی کی منفردیت
2. **[سینسرز اور ادراک](./chapter-02-sensors-and-perception)** - روبوٹ کی نظر
3. **[حرکیات اور فعالیت](./chapter-03-kinematics-and-actuation)** - حرکت کی ریاضی
4. **[انسان نما روبوٹس کے لیے علمی فن تعمیر](./chapter-04-cognitive-architectures-for-humanoids)** - ذہین نظام
5. **[فزیکل اے آئی میں حفاظت اور اخلاقیات](./chapter-05-safety-and-ethics-in-physical-ai)** - محفوظ تعیناتی

## یہ کتاب کس کے لیے ہے

- **ابتدائی** - روبوٹکس میں دلچسپی رکھنے والے
- **سافٹ ویئر ڈویلپرز** - روبوٹکس میں منتقلی
- **طلباء** - کمپیوٹر سائنس، انجینئرنگ
- **شوقین** - روبوٹ پروجیکٹس
- **پیشہ ور** - فزیکل اے آئی کی بنیادیں

## شروع کریں

**[باب 1: مجسم اے آئی کا تعارف](./chapter-01-introduction-to-embodied-ai)** کے ساتھ اپنا سفر شروع کریں۔`,

  // Chapter 1 - Full Translation
  '/chapter-01-introduction-to-embodied-ai': `# باب 1: مجسم اے آئی کا تعارف

**تخمینی وقت**: 3-4 گھنٹے
**پیشگی ضروریات**: بنیادی Python پروگرامنگ (متغیرات، فنکشنز، لوپس)، کمانڈ لائن کے ساتھ آسانی

## سیکھنے کے نتائج

اس باب کے اختتام تک، آپ یہ قابل ہوں گے:

- Embodied AI کی تعریف کریں اور اسے disembodied AI ایپلیکیشنز سے ممتاز کریں
- ذہانت کے لیے جسمانی مجسمیت کی اہمیت کی وضاحت کریں
- Embodied AI نظاموں کی حقیقی دنیا کی ایپلیکیشنز کی شناخت کریں
- بعد کے ابواب کے لیے سمیولیشن ماحول کامیابی سے ترتیب دیں

---

## 1.1 مجسم اے آئی کیا ہے؟

### مجسمیت کا مفروضہ

Embodied AI مصنوعی ذہانت کے بارے میں ہمارے سوچنے کے طریقے میں ایک بنیادی تبدیلی کی نمائندگی کرتا ہے۔ جبکہ روایتی AI نظام مکمل طور پر ڈیجیٹل دائرے میں کام کرتے ہیں—بغیر کسی جسمانی موجودگی کے متن، تصاویر، یا ڈیٹا پر کارروائی کرتے ہوئے—Embodied AI نظام سینسرز اور ایکچویٹرز کے ذریعے براہ راست جسمانی دنیا کے ساتھ تعامل کرتے ہیں۔

**مجسمیت کا مفروضہ** یہ تجویز کرتا ہے کہ حقیقی ذہانت کے لیے ایک جسمانی جسم کی ضرورت ہوتی ہے۔ یہ خیال، جسے Rodney Brooks اور Rolf Pfeifer جیسے محققین نے فروغ دیا، یہ تجویز کرتا ہے کہ ادراک ایک ایجنٹ کے جسم اور اس کے ماحول کے درمیان مسلسل تعامل سے ابھرتا ہے۔

### Disembodied بمقابلہ Embodied AI

| پہلو | Disembodied AI | Embodied AI |
|------|----------------|-------------|
| ماحول | ڈیجیٹل/ورچوئل | جسمانی دنیا |
| ان پٹ | منظم ڈیٹا، متن، تصاویر | خام سینسر ڈیٹا (شور والا، مسلسل) |
| آؤٹ پٹ | پیشن گوئیاں، متن، درجہ بندی | جسمانی اعمال (حرکت، ہیرا پھیری) |
| وقت کی پابندیاں | اکثر batch processing | حقیقی وقت، حفاظت کے لیے اہم |
| نتائج | ڈیجیٹل غلطیاں | جسمانی نتائج (نقصان، چوٹ) |

**Disembodied AI کی مثالیں**:
- چیٹ بوٹس اور لینگویج ماڈلز
- سفارشی نظام
- تصویری classifier
- گیم کھیلنے والی AI (شطرنج، Go)

**Embodied AI کی مثالیں**:
- خود مختار گاڑیاں
- گودام کے روبوٹس
- جراحی کے روبوٹس
- ڈرونز اور UAVs
- انسان نما روبوٹس

### مجسمیت کیوں اہم ہے

جسمانی مجسمیت ایسے چیلنجز متعارف کراتی ہے جن کا خالصتاً ڈیجیٹل نظاموں کو کبھی سامنا نہیں ہوتا:

1. **سینسر کا شور اور غیر یقینی**: حقیقی سینسرز نامکمل، شور والا ڈیٹا فراہم کرتے ہیں
2. **حقیقی وقت کی پابندیاں**: جسمانی اعمال کو واپس نہیں لیا جا سکتا؛ فیصلے بروقت ہونے چاہیے
3. **حفاظت کی ضروریات**: غلطیاں جسمانی نقصان کا سبب بن سکتی ہیں
4. **ماحولیاتی تغیر پذیری**: حقیقی دنیا غیر متوقع اور مسلسل بدلتی رہتی ہے

---

## 1.2 فزیکل اے آئی پائپ لائن

ہر Embodied AI نظام ایک بنیادی پائپ لائن کی پیروی کرتا ہے: **ادراک → منصوبہ بندی → فعالیت**

### ادراک (Perception)

ادراک کا مرحلہ خام سینسر ڈیٹا کو دنیا کی معنی خیز نمائندگیوں میں تبدیل کرتا ہے۔ اس میں شامل ہیں:

- **Sensing**: کیمروں، LIDAR، ٹچ سینسرز، IMUs سے ڈیٹا جمع کرنا
- **Processing**: شور کو فلٹر کرنا، متعدد سینسرز سے ڈیٹا کو ملانا
- **Understanding**: اشیاء، رکاوٹوں، اور ماحول کے ماڈل بنانا

### منصوبہ بندی (Planning)

منصوبہ بندی کا مرحلہ محسوس شدہ معلومات کی بنیاد پر فیصلہ کرتا ہے کہ کون سے اعمال کرنے ہیں:

- **Goal representation**: یہ سمجھنا کہ کیا حاصل کرنا ہے
- **Path planning**: ماحول میں راستے تلاش کرنا
- **Decision making**: متبادل اعمال کے درمیان انتخاب کرنا
- **Prediction**: مستقبل کی حالتوں اور نتائج کی پیش گوئی کرنا

### فعالیت (Actuation)

فعالیت کا مرحلہ دنیا میں جسمانی اعمال کو انجام دیتا ہے:

- **Motor control**: موٹرز اور ایکچویٹرز کو کمانڈز بھیجنا
- **Feedback loops**: سینسر فیڈ بیک کی بنیاد پر اعمال کو ایڈجسٹ کرنا
- **Force control**: اشیاء کے ساتھ جسمانی تعاملات کا انتظام کرنا

### مسلسل لوپ

Batch-processing نظاموں کے برعکس، Embodied AI ایک مسلسل لوپ میں کام کرتا ہے۔ یہ **Perception-Cognition-Action** سائیکل مسلسل چلتا رہتا ہے، جو روبوٹ کو اپنے ماحول میں تبدیلیوں کا حقیقی وقت میں جواب دینے کے قابل بناتا ہے۔

**لوپ کے اہم پہلو:**

- **Perception** خام سینسر ڈیٹا جمع کرتا ہے اور اسے معنی خیز نمائندگیوں میں تبدیل کرتا ہے
- **Cognition** دنیا کے بارے میں استدلال کرتا ہے، اعمال کی منصوبہ بندی کرتا ہے، اور فیصلے کرتا ہے
- **Action** جسمانی حرکات کو انجام دیتا ہے جو ماحول کو تبدیل کرتی ہیں
- **Feedback** لوپ کو مکمل کرتا ہے—اعمال ماحول کو تبدیل کرتے ہیں، جو پھر دوبارہ محسوس ہوتا ہے

---

## 1.3 حقیقی دنیا کی ایپلیکیشنز

### خود مختار گاڑیاں

خود ڈرائیونگ کاریں Embodied AI کی سب سے مہتواکانکشی ایپلیکیشنز میں سے ایک ہیں:

- **Perception**: کیمرے، LIDAR، radar سڑکوں، گاڑیوں، پیدل چلنے والوں کا پتہ لگاتے ہیں
- **Planning**: راستے کی منصوبہ بندی، لین کی تبدیلی، چوراہے کی نیویگیشن
- **Actuation**: اسٹیئرنگ، رفتار، بریکنگ

### گودام کی روبوٹکس

Amazon جیسی کمپنیاں لاجسٹکس کے لیے ہزاروں موبائل روبوٹس استعمال کرتی ہیں:

- **Perception**: فرش کے نشانات، رکاوٹوں کا پتہ لگانا، پیکج کی شناخت
- **Planning**: گودام میں بہترین راستے، تصادم سے بچاؤ
- **Actuation**: نیویگیشن، شیلف اٹھانا، پیکج ہینڈلنگ

### جراحی کے روبوٹس

da Vinci جیسے نظام کم سے کم invasive سرجری کو ممکن بناتے ہیں:

- **Perception**: Stereo کیمرے، force sensing
- **Planning**: آلات کی پوزیشننگ، کانپنے کو فلٹر کرنا
- **Actuation**: سرجیکل آلات کی درست micro-movements

### زرعی روبوٹس

کھیتی باڑی اور کٹائی کے لیے خودکار نظام:

- **Perception**: فصل کا پتہ لگانا، پکنے کا اندازہ
- **Planning**: میدان کی کوریج، منتخب کٹائی کے فیصلے
- **Actuation**: نیویگیشن، چننا، سپرے کرنا

---

## 1.4 اپنے ڈیولپمنٹ ماحول کو ترتیب دینا

### سمیولیشن پہلے نقطہ نظر

جسمانی روبوٹس کے ساتھ کام کرنے سے پہلے، آپ سمیولیشن میں تیار اور ٹیسٹ کریں گے۔ یہ نقطہ نظر کئی فوائد پیش کرتا ہے:

- **حفاظت**: سامان کو نقصان پہنچانے یا چوٹ لگنے کا کوئی خطرہ نہیں
- **رفتار**: جسمانی تجربات سے تیز iteration cycles
- **تکرار پذیری**: عین حالات کو دوبارہ بنایا جا سکتا ہے
- **لاگت**: کسی مہنگے ہارڈویئر کی ضرورت نہیں

### مطلوبہ سافٹ ویئر

اس کتاب کے لیے، آپ مندرجہ ذیل ٹولز استعمال کریں گے:

1. **Python 3.9+**: بنیادی پروگرامنگ زبان
2. **PyBullet**: فزکس سمیولیشن انجن
3. **NumPy**: عددی کمپیوٹنگ لائبریری
4. **Matplotlib**: تصویری لائبریری

### انسٹالیشن کے مراحل

#### مرحلہ 1: ورچوئل ماحول بنائیں

\`\`\`python
# نیا ورچوئل ماحول بنائیں
python -m venv physical-ai-env

# ماحول کو فعال کریں (Windows)
physical-ai-env\\Scripts\\activate

# ماحول کو فعال کریں (macOS/Linux)
source physical-ai-env/bin/activate
\`\`\`

#### مرحلہ 2: مطلوبہ پیکجز انسٹال کریں

\`\`\`python
# بنیادی پیکجز انسٹال کریں
pip install pybullet numpy matplotlib

# انسٹالیشن کی تصدیق کریں
python -c "import pybullet; print('PyBullet version:', pybullet.getPhysicsEngineParameters())"
\`\`\`

#### مرحلہ 3: اپنی پہلی سمیولیشن چلائیں

\`\`\`python
import pybullet as p
import pybullet_data
import time

# GUI کے ساتھ physics server سے جڑیں
physics_client = p.connect(p.GUI)

# بلٹ ان ماڈلز کا راستہ سیٹ کریں
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# زمینی سطح لوڈ کریں
plane_id = p.loadURDF("plane.urdf")

# روبوٹ ماڈل لوڈ کریں
robot_id = p.loadURDF("r2d2.urdf", [0, 0, 0.5])

# کشش ثقل سیٹ کریں
p.setGravity(0, 0, -9.81)

# 5 سیکنڈ کے لیے سمیولیشن چلائیں
for i in range(500):
    p.stepSimulation()
    time.sleep(1./240.)

# منقطع کریں
p.disconnect()
\`\`\`

**متوقع آؤٹ پٹ**: ایک ونڈو کھلتی ہے جو R2D2 روبوٹ ماڈل کے ساتھ زمینی سطح دکھاتی ہے۔ روبوٹ کو کشش ثقل کی وجہ سے گرنا اور زمین پر بسنا چاہیے۔

---

## عملی مشقیں

### مشق 1.1: Embodied AI ایپلیکیشنز کی شناخت

ذیل میں ہر منظر نامے کے لیے، شناخت کریں کہ آیا یہ Embodied AI ہے یا Disembodied AI، اور اپنے استدلال کی وضاحت کریں:

1. ایک روبوٹ ویکیوم کلینر آپ کے گھر میں نیویگیٹ کرتا ہے
2. ایک سپیم فلٹر ای میلز کو classify کرتا ہے
3. ایک ڈرون پیکج ڈیلیور کرتا ہے
4. ایک وائس اسسٹنٹ سوالات کے جواب دیتا ہے
5. ایک روبوٹک بازو کار کے حصوں کو ویلڈ کرتا ہے

### مشق 1.2: پائپ لائن تجزیہ

ایک ڈیلیوری ڈرون کے لیے، بیان کریں کہ فزیکل AI پائپ لائن کے ہر مرحلے پر کیا ہوتا ہے:

1. یہ ادراک کے لیے کون سے سینسرز استعمال کرتا ہے؟
2. منصوبہ بندی کے مرحلے کو کون سے فیصلے کرنے ہوں گے؟
3. کون سے ایکچویٹرز جسمانی اعمال کو انجام دیتے ہیں؟

### مشق 1.3: ماحول کی تصدیق

انسٹالیشن کے مراحل مکمل کریں اور پہلی سمیولیشن چلائیں۔ دستاویز کریں:

1. آپ نے جو Python ورژن انسٹال کیا
2. کوئی خرابی کا سامنا ہوا اور آپ نے انہیں کیسے حل کیا
3. سمیولیشن ونڈو کا ایک سکرین شاٹ

---

## خلاصہ

اس باب میں، آپ نے سیکھا:

- **Embodied AI** نظام سینسرز اور ایکچویٹرز کے ذریعے جسمانی دنیا کے ساتھ تعامل کرتے ہیں
- **مجسمیت کا مفروضہ** تجویز کرتا ہے کہ جسمانی موجودگی حقیقی ذہانت کے لیے ضروری ہے
- تمام Embodied AI نظام **Perception → Planning → Actuation** پائپ لائن کی پیروی کرتے ہیں
- حقیقی دنیا کی ایپلیکیشنز میں خود مختار گاڑیاں، گودام کے روبوٹس، جراحی کے نظام، اور زرعی روبوٹس شامل ہیں
- **سمیولیشن** Embodied AI تیار کرنے کا ایک محفوظ، تیز، اور سرمایہ کاری مؤثر طریقہ فراہم کرتا ہے

---

## اہم اصطلاحات

- **Embodied AI**: جسمانی موجودگی کے ساتھ AI نظام جو حقیقی دنیا کے ساتھ تعامل کرتے ہیں
- **Perception**: سینسر ڈیٹا جمع کرنے اور تشریح کرنے کا عمل
- **Planning**: کون سے اعمال کرنے ہیں کے بارے میں فیصلہ سازی
- **Actuation**: دنیا میں جسمانی اعمال کو انجام دینا
- **Simulation**: جسمانی ہارڈویئر کے بغیر ٹیسٹنگ کے لیے ورچوئل ماحول

---

## اگلے باب کا جائزہ

باب 2 میں، آپ **سینسرز اور ادراک** میں گہرائی میں غوطہ لگائیں گے—فزیکل AI نظاموں میں استعمال ہونے والے مختلف قسم کے سینسرز اور ان کے ڈیٹا کو مفید معلومات میں کیسے پروسیس کیا جائے کے بارے میں سیکھیں گے۔`,

  // Chapter 2 - Expanded Translation
  '/chapter-02-sensors-and-perception': `# باب 2: سینسرز اور ادراک

**تخمینی وقت**: 4-5 گھنٹے
**پیشگی ضروریات**: باب 1 مکمل، بنیادی Python، NumPy کی واقفیت

## سیکھنے کے نتائج

اس باب کے اختتام تک، آپ:

- مختلف روبوٹک سینسرز کی اقسام کو سمجھیں گے (بصری، رینج، force، inertial)
- کیمرا ڈیٹا اور تصویری پروسیسنگ تکنیکوں کے ساتھ کام کریں گے
- LIDAR اور depth sensing کے اصولوں کو سمجھیں گے
- sensor fusion تکنیکوں کو نافذ کریں گے تاکہ زیادہ قابل اعتماد ادراک حاصل ہو

---

## 2.1 سینسرز کا تعارف

روبوٹس اپنے ماحول کو سینسرز کے ذریعے محسوس کرتے ہیں۔ انسانی حواس (نظر، سماعت، چھونا) کی طرح، روبوٹک سینسرز جسمانی دنیا کے بارے میں معلومات جمع کرتے ہیں اور انہیں برقی سگنلز میں تبدیل کرتے ہیں جو کمپیوٹر پروسیس کر سکتا ہے۔

### سینسرز کی اقسام

1. **بصری سینسرز** (Vision Sensors)
   - RGB کیمرے - رنگین تصاویر کیپچر کرتے ہیں
   - Depth cameras - فاصلے کی معلومات فراہم کرتے ہیں
   - Stereo cameras - گہرائی کی تخمینہ کے لیے دو کیمرے استعمال کرتے ہیں

2. **رینج سینسرز** (Range Sensors)
   - LIDAR - لیزر بیم استعمال کرتے ہوئے درست 3D نقشے بناتے ہیں
   - Ultrasonic - صوتی لہروں سے فاصلہ ماپتے ہیں
   - Radar - ریڈیو لہروں سے رفتار اور فاصلہ پتہ لگاتے ہیں

3. **Force سینسرز**
   - Touch sensors - جسمانی رابطے کا پتہ لگاتے ہیں
   - Pressure sensors - لاگو قوت کی پیمائش کرتے ہیں
   - Torque sensors - گھومنے والی قوتوں کو ماپتے ہیں

4. **Inertial سینسرز**
   - IMU (Inertial Measurement Unit) - رفتار اور سمت ٹریک کرتا ہے
   - Gyroscopes - زاویہ کی رفتار کی پیمائش کرتے ہیں
   - Accelerometers - رفتار میں تبدیلی کو محسوس کرتے ہیں

---

## 2.2 کیمرے اور بصری ادراک

کیمرے روبوٹکس میں سب سے زیادہ استعمال ہونے والے سینسرز میں سے ہیں۔ وہ ماحول کے بارے میں معلومات کی دولت فراہم کرتے ہیں، جس میں اشیاء کی شناخت، رنگ، شکل، اور بناوٹ شامل ہیں۔

### کیمرا کے بنیادی اصول

- **Resolution**: تصویر میں pixels کی تعداد (مثال: 1920x1080)
- **Frame rate**: فی سیکنڈ تصاویر کی تعداد (fps)
- **Field of view**: کیمرا کتنا وسیع علاقہ دیکھ سکتا ہے
- **Exposure**: سینسر کو روشنی کے سامنے لانے کا وقت

### تصویری پروسیسنگ کی تکنیکیں

1. **Filtering** - شور کو کم کرنا اور تصویر کو بہتر بنانا
2. **Edge detection** - اشیاء کی حدود تلاش کرنا
3. **Object detection** - تصاویر میں مخصوص اشیاء کی شناخت
4. **Segmentation** - تصویر کو معنی خیز خطوں میں تقسیم کرنا

---

## 2.3 LIDAR اور Depth Sensing

LIDAR (Light Detection and Ranging) لیزر بیم استعمال کرتے ہوئے درست 3D ماحولیاتی نقشے بناتا ہے۔

### LIDAR کیسے کام کرتا ہے

1. لیزر پلس باہر بھیجا جاتا ہے
2. روشنی اشیاء سے ٹکرا کر واپس آتی ہے
3. واپسی کا وقت فاصلے کا حساب لگانے کے لیے استعمال ہوتا ہے
4. روبوٹ کے ارد گرد 360° سکین کے لیے دہرایا جاتا ہے

### LIDAR کے فوائد

- انتہائی درست فاصلے کی پیمائش (سینٹی میٹر کی سطح)
- طویل رینج (100+ میٹر)
- کم روشنی کے حالات میں کام کرتا ہے
- 3D point cloud ڈیٹا فراہم کرتا ہے

---

## 2.4 Sensor Fusion

Sensor fusion متعدد سینسرز سے ڈیٹا کو یکجا کرتا ہے تاکہ زیادہ قابل اعتماد اور جامع ادراک حاصل ہو۔

### کیوں Sensor Fusion ضروری ہے

- کسی ایک سینسر میں کمیاں ہوتی ہیں
- متعدد سینسرز غیر یقینی کو کم کرتے ہیں
- مختلف سینسرز تکمیلی معلومات فراہم کرتے ہیں
- نقصان کے خلاف redundancy فراہم کرتا ہے

### Fusion کی تکنیکیں

1. **Kalman Filter** - شور والی پیمائشوں سے حالت کا اندازہ لگاتا ہے
2. **Weighted averaging** - سینسر کے اعتماد کی بنیاد پر ڈیٹا کو یکجا کرتا ہے
3. **Complementary filtering** - مختلف سینسرز کی طاقتوں کو یکجا کرتا ہے

---

## عملی مشقیں

### مشق 2.1: کیمرا ڈیٹا پروسیسنگ

PyBullet میں کیمرا استعمال کرتے ہوئے تصاویر کیپچر کریں اور edge detection لاگو کریں۔

### مشق 2.2: LIDAR سمیولیشن

ورچوئل LIDAR سینسر بنائیں اور رکاوٹوں کا 2D نقشہ تیار کریں۔

### مشق 2.3: Sensor Fusion

کیمرا اور LIDAR ڈیٹا کو یکجا کریں تاکہ اشیاء کی شناخت اور فاصلے کی پیمائش بہتر ہو۔

---

## خلاصہ

اس باب میں، آپ نے سیکھا:

- **سینسرز** روبوٹس کے لیے "حواس" فراہم کرتے ہیں تاکہ ماحول کو محسوس کیا جا سکے
- **کیمرے** بصری معلومات فراہم کرتے ہیں اور تصویری پروسیسنگ کی ضرورت ہوتی ہے
- **LIDAR** درست 3D ماحولیاتی نقشے بناتا ہے
- **Sensor fusion** متعدد سینسرز کو یکجا کرتا ہے تاکہ مضبوط ادراک حاصل ہو

---

## اگلے باب کا جائزہ

باب 3 میں، آپ **حرکیات اور فعالیت** کا مطالعہ کریں گے—روبوٹ کی حرکت کی ریاضی اور control نظام جو جسمانی اعمال کو ممکن بناتے ہیں۔`,

  // Chapter 3 - Expanded Translation
  '/chapter-03-kinematics-and-actuation': `# باب 3: حرکیات اور فعالیت

**تخمینی وقت**: 5-6 گھنٹے
**پیشگی ضروریات**: باب 1-2 مکمل، بنیادی trigonometry، linear algebra کا تعارف

## سیکھنے کے نتائج

اس باب کے اختتام تک، آپ:

- روبوٹک حرکیات (kinematics) کے بنیادی اصولوں کو سمجھیں گے
- Forward kinematics حل کریں گے (joint angles سے end-effector position)
- Inverse kinematics حل کریں گے (مطلوبہ position سے joint angles)
- مختلف قسم کے actuators اور control systems کے ساتھ کام کریں گے

---

## 3.1 حرکیات کا تعارف

حرکیات (Kinematics) روبوٹ کی حرکت کا مطالعہ ہے بغیر قوتوں پر غور کیے جو اسے حرکت دیتی ہیں۔ یہ سوالات کے جواب دیتا ہے جیسے:

- اگر میں joints کو مخصوص زاویوں پر سیٹ کروں، تو robot کا ہاتھ کہاں ہوگا؟ (Forward kinematics)
- robot کے ہاتھ کو مخصوص مقام تک پہنچانے کے لیے مجھے joints کو کس زاویے پر سیٹ کرنا ہوگا؟ (Inverse kinematics)

### Coordinate Frames (نقاط کے نظام)

ہر robot کے حصے کا اپنا coordinate frame ہوتا ہے:

- **World frame**: مطلق حوالہ نقطہ
- **Base frame**: robot کی بنیاد
- **Joint frames**: ہر joint کا مقامی frame
- **End-effector frame**: robot کے ہاتھ یا tool کا frame

---

## 3.2 Forward Kinematics

Forward kinematics (FK) joint angles سے end-effector کی position اور orientation کا حساب لگاتا ہے۔

### بنیادی FK مثال: 2-Link Manipulator

ایک سادہ 2-link robot arm کے لیے:

- Link 1 کی لمبائی: L1
- Link 2 کی لمبائی: L2
- Joint 1 کا زاویہ: θ1
- Joint 2 کا زاویہ: θ2

**End-effector position (x, y):**

\`\`\`
x = L1 * cos(θ1) + L2 * cos(θ1 + θ2)
y = L1 * sin(θ1) + L2 * sin(θ1 + θ2)
\`\`\`

### Transformation Matrices

زیادہ پیچیدہ robots کے لیے، ہم transformation matrices استعمال کرتے ہیں:

- **Translation**: ایک frame کو دوسرے میں منتقل کرنا
- **Rotation**: ایک frame کو گھمانا
- **Denavit-Hartenberg (DH) parameters**: robot کی جیومیٹری کو بیان کرنے کا معیاری طریقہ

---

## 3.3 Inverse Kinematics

Inverse kinematics (IK) مطلوبہ end-effector position سے joint angles کا حساب لگاتا ہے۔ یہ FK سے زیادہ مشکل ہے کیونکہ:

- متعدد حل موجود ہو سکتے ہیں (elbow up بمقابلہ elbow down)
- کوئی حل موجود نہیں ہو سکتا (goal reach سے باہر ہے)
- حساب پیچیدہ ہو سکتا ہے

### IK حل کرنے کے طریقے

1. **Analytical solutions** - بند صورت equations (صرف سادہ robots کے لیے)
2. **Numerical methods** - iterative algorithms جیسے:
   - Jacobian-based methods
   - Gradient descent
   - Cyclic Coordinate Descent (CCD)

3. **Geometric methods** - triangle حل اور trigonometry استعمال کرنا

---

## 3.4 Actuators اور Control

Actuators وہ devices ہیں جو برقی توانائی کو مکینیکل حرکت میں تبدیل کرتے ہیں۔

### Actuators کی اقسام

1. **DC Motors**
   - فوائد: سادہ، سستے، control میں آسان
   - نقصانات: محدود torque، gearing کی ضرورت

2. **Servo Motors**
   - فوائد: position control، اچھی precision
   - نقصانات: محدود رینج (عام طور پر 180°)

3. **Stepper Motors**
   - فوائد: open-loop control، اچھی positioning
   - نقصانات: torque پر محدود، زیادہ بجلی استعمال

4. **Hydraulic Actuators**
   - فوائد: بہت زیادہ قوت، سخت ماحول کے لیے اچھا
   - نقصانات: بھاری، مہنگے، دیکھ بھال کی ضرورت

### Control Loops

**PID Controller** (Proportional-Integral-Derivative) سب سے عام control algorithm ہے:

- **P (Proportional)**: موجودہ خرابی پر رد عمل
- **I (Integral)**: ماضی کی خرابیوں پر رد عمل (steady-state error کو ختم کرتا ہے)
- **D (Derivative)**: مستقبل کی خرابیوں کی پیشن گوئی (overshoot کو کم کرتا ہے)

**Control equation:**

\`\`\`
output = Kp * error + Ki * integral(error) + Kd * derivative(error)
\`\`\`

---

## عملی مشقیں

### مشق 3.1: Forward Kinematics

2-link arm کے لیے forward kinematics function لکھیں۔ مختلف joint angles کے لیے end-effector position کا حساب لگائیں۔

### مشق 3.2: Inverse Kinematics

سادہ 2D arm کے لیے analytical IK solution نافذ کریں۔ ہر goal position کے لیے دونوں ممکنہ حلوں کو تلاش کریں۔

### مشق 3.3: PID Control

PyBullet میں motor کو کنٹرول کرنے کے لیے PID controller نافذ کریں۔ مطلوبہ position پر پہنچنے کے لیے parameters کو tune کریں۔

---

## خلاصہ

اس باب میں، آپ نے سیکھا:

- **Kinematics** robot کی حرکت کی جیومیٹری کا مطالعہ ہے
- **Forward kinematics** joint angles سے end-effector position کا حساب لگاتا ہے
- **Inverse kinematics** مطلوبہ position سے joint angles تلاش کرتا ہے
- **Actuators** برقی سگنلز کو جسمانی حرکت میں تبدیل کرتے ہیں
- **PID controllers** درست position control فراہم کرتے ہیں

---

## اگلے باب کا جائزہ

باب 4 میں، آپ **انسان نما روبوٹس کے لیے علمی فن تعمیر** سیکھیں گے—perception، planning، اور action کو مربوط نظاموں میں کیسے ضم کریں جو پیچیدہ ماحول میں کام کر سکیں۔`,

  // Chapter 4 - Expanded Translation
  '/chapter-04-cognitive-architectures-for-humanoids': `# باب 4: انسان نما روبوٹس کے لیے علمی فن تعمیر

**تخمینی وقت**: 5-6 گھنٹے
**پیشگی ضروریات**: باب 1-3 مکمل، بنیادی AI/ML تصورات

## سیکھنے کے نتائج

اس باب کے اختتام تک، آپ:

- علمی فن تعمیر (cognitive architectures) کے مختلف نقطہ نظروں کو سمجھیں گے
- Perception، planning، اور action modules کو ایک مربوط نظام میں ضم کریں گے
- Behavior trees اور finite state machines استعمال کرتے ہوئے robot behavior ڈیزائن کریں گے
- انسان نما روبوٹس کے لیے پیچیدہ tasks کو توڑنے کی techniques سیکھیں گے

---

## 4.1 علمی فن تعمیر کیا ہیں؟

علمی فن تعمیر (Cognitive architecture) ایک ڈھانچہ ہے جو ذہین behavior کو منظم کرتا ہے۔ یہ بیان کرتا ہے کہ perception، decision-making، learning، اور action modules کیسے تعامل کرتے ہیں۔

### علمی فن تعمیر کیوں ضروری ہیں؟

- پیچیدہ نظاموں کو منظم طریقے سے ڈیزائن کرنے میں مدد کرتے ہیں
- modules کو دوبارہ استعمال اور testing کو آسان بناتے ہیں
- مختلف قسم کے tasks اور ماحول کو سنبھالتے ہیں
- انسانی cognition کے بارے میں theories کو implement کرنے کا طریقہ فراہم کرتے ہیں

---

## 4.2 Architecture کی اقسام

### 4.2.1 Reactive Architectures

**تعریف**: سینسر inputs پر براہ راست react کرتے ہیں بغیر internal state یا planning کے۔

**فوائد**:
- تیز رد عمل
- سادہ implementation
- robust اور predictable

**نقصانات**:
- طویل مدتی planning نہیں
- پیچیدہ tasks کو سنبھالنے میں مشکل

**مثال**: Subsumption architecture (Rodney Brooks)

### 4.2.2 Deliberative Architectures

**تعریف**: دنیا کا internal model رکھتے ہیں اور explicit planning کرتے ہیں۔

**فوائد**:
- پیچیدہ reasoning اور planning
- طویل مدتی goals کو حاصل کر سکتے ہیں
- environment کی prediction کر سکتے ہیں

**نقصانات**:
- سست ہو سکتے ہیں (planning overhead)
- model غلط ہونے پر ناکام ہو سکتے ہیں

**مثال**: STRIPS, SOAR

### 4.2.3 Hybrid Architectures

**تعریف**: Reactive اور deliberative approaches کو یکجا کرتے ہیں۔

**فوائد**:
- دونوں دنیاوں کا بہترین
- تیز reflexes + planning کی صلاحیت
- زیادہ عملی applications کے لیے

**مثال**: 3-Layer architecture (Reactive, Executive, Deliberative)

---

## 4.3 Behavior Trees

Behavior trees ایک مقبول طریقہ ہیں robot behavior کو ماڈیولر، hierarchical انداز میں منظم کرنے کا۔

### بنیادی Nodes

1. **Sequence Node** - تمام children کو ترتیب سے execute کرتا ہے
2. **Selector Node** - پہلا کامیاب child execute کرتا ہے
3. **Parallel Node** - متعدد children بیک وقت execute کرتا ہے
4. **Decorator Node** - child کی behavior کو modify کرتا ہے

### مثال: "Object Pick and Place" Task

\`\`\`
Sequence
├── Find Object
├── Navigate to Object
├── Grasp Object
├── Navigate to Goal
└── Release Object
\`\`\`

---

## 4.4 World Models اور Planning

### World Model کیا ہے؟

ایک internal representation of the environment جو robot perceive کرتا ہے اور اس کا prediction کرتا ہے۔

**شامل ہیں**:
- اشیاء کی locations اور properties
- خود robot کی state
- ماحول کی dynamics
- uncertainty estimates

### Planning Algorithms

1. **A\* Search** - optimal path planning کے لیے
2. **RRT (Rapidly-exploring Random Tree)** - high-dimensional spaces میں
3. **MPC (Model Predictive Control)** - optimization-based control
4. **Hierarchical planning** - پیچیدہ tasks کو sub-tasks میں توڑنا

---

## 4.5 انسان نما روبوٹس کے لیے خاص تحفظات

### Whole-Body Control

انسان نما روبوٹس کو متعدد limbs اور joints کو coordinate کرنا پڑتا ہے:

- **Balance maintenance** - گرنے سے بچنا
- **Posture control** - مستحکم position برقرار رکھنا
- **Multi-limb coordination** - ہاتھوں اور پیروں کو ہم آہنگ کرنا

### Human-Robot Interaction

انسانوں کے ساتھ کام کرتے وقت:

- **Intention recognition** - انسان کیا کرنا چاہتا ہے
- **Gesture understanding** - ہاتھوں کی حرکات کو سمجھنا
- **Social cues** - آنکھوں کا رابطہ، facial expressions
- **Safety** - انسانوں کو نقصان نہ پہنچانا

---

## عملی مشقیں

### مشق 4.1: Behavior Tree Implementation

PyBullet میں ایک سادہ behavior tree بنائیں جو robot کو object کی طرف navigate کرے اور pick up کرے۔

### مشق 4.2: Path Planning

A* algorithm استعمال کرتے ہوئے رکاوٹوں سے بھرے ماحول میں path plan کریں۔

### مشق 4.3: Multi-tasking

ایک controller بنائیں جو دو tasks کو بیک وقت سنبھالے: navigation اور obstacle avoidance۔

---

## خلاصہ

اس باب میں، آپ نے سیکھا:

- **علمی فن تعمیر** intelligent behavior کو منظم کرنے کے frameworks ہیں
- **Reactive architectures** تیز ہیں لیکن محدود، **deliberative** complex reasoning کرتے ہیں
- **Behavior trees** robot behavior کو ماڈیولر طریقے سے organize کرنے کا اچھا طریقہ ہیں
- **انسان نما روبوٹس** کو whole-body control اور human interaction کی خاص ضروریات ہیں

---

## اگلے باب کا جائزہ

باب 5 میں، آپ **فزیکل اے آئی میں حفاظت اور اخلاقیات** سیکھیں گے—حقیقی دنیا میں روبوٹس کو محفوظ طریقے سے تعینات کرنے کے اہم تحفظات۔`,

  // Chapter 5 - Expanded Translation
  '/chapter-05-safety-and-ethics-in-physical-ai': `# باب 5: فزیکل اے آئی میں حفاظت اور اخلاقیات

**تخمینی وقت**: 3-4 گھنٹے
**پیشگی ضروریات**: باب 1-4 مکمل، technical اور social contexts کی تفہیم

## سیکھنے کے نتائج

اس باب کے اختتام تک، آپ:

- روبوٹک حفاظت کے بنیادی اصولوں اور standards کو سمجھیں گے
- فزیکل AI نظاموں سے متعلق اخلاقی تحفظات کی شناخت اور تجزیہ کریں گے
- محفوظ تعیناتی کی حکمت عملیاں اور best practices سیکھیں گے
- risk assessment اور mitigation techniques لاگو کریں گے

---

## 5.1 روبوٹک حفاظت کے اصول

### Asimov کے تین قوانین (1942)

Isaac Asimov نے robot ethics کی بنیاد رکھی:

1. **پہلا قانون**: روبوٹ انسان کو نقصان نہیں پہنچائے گا، یا بے عملی سے انسان کو نقصان نہیں پہنچنے دے گا
2. **دوسرا قانون**: روبوٹ انسانوں کے احکامات کی پیروی کرے گا (سوائے پہلے قانون سے تصادم)
3. **تیسرا قانون**: روبوٹ اپنی موجودگی کی حفاظت کرے گا (جب تک پہلے دو قوانین سے تصادم نہ ہو)

جبکہ یہ science fiction میں دلچسپ ہیں، عملی implementation بہت پیچیدہ ہے۔

### جدید حفاظت کے اصول

1. **Physical Safety** - انسانوں اور property کو نقصان سے بچانا
2. **Functional Safety** - نظام معتبر طریقے سے کام کرتا ہے
3. **Cybersecurity** - unauthorized access سے محفوظ
4. **Privacy** - صارفین کے ڈیٹا کی حفاظت
5. **Transparency** - فیصلوں کو سمجھنے کے قابل

---

## 5.2 حفاظت کے خطرات اور Mitigation

### عام خطرات

1. **تصادم (Collision)**
   - انسان یا اشیاء سے ٹکرانا
   - **Mitigation**: Collision detection، safety zones، force limiting

2. **غیر متوقع حرکت (Unpredictable Motion)**
   - اچانک، تیز، یا غیر متوقع movements
   - **Mitigation**: Motion profiling، speed limits، emergency stop

3. **Software Failures**
   - Bugs، crashes، یا غلط behavior
   - **Mitigation**: Testing، redundancy، fail-safe defaults

4. **سینسر ناکامی (Sensor Failure)**
   - غلط یا missing sensor data
   - **Mitigation**: Sensor fusion، plausibility checks، degraded mode operation

5. **Cybersecurity Threats**
   - Hacking، malware، unauthorized control
   - **Mitigation**: Encryption، authentication، secure communication

### Safety Standards

- **ISO 13482**: Personal care robots کے لیے
- **ISO 10218**: Industrial robots کے لیے
- **IEC 61508**: Functional safety کی عمومی standard
- **UL 3300**: Service robots کے لیے

---

## 5.3 اخلاقی تحفظات

### کلیدی اخلاقی سوالات

1. **Autonomy بمقابلہ Control**
   - روبوٹس کو کتنا خود مختار ہونا چاہیے؟
   - انسانی oversight کب ضروری ہے؟

2. **جوابدہی (Accountability)**
   - اگر روبوٹ نقصان پہنچائے تو ذمہ دار کون؟
   - Manufacturer، operator، یا robot خود؟

3. **Bias اور Fairness**
   - کیا AI نظام کچھ گروپوں کے خلاف discriminate کرتے ہیں؟
   - Training data میں bias کو کیسے کم کریں؟

4. **Privacy**
   - روبوٹس جو cameras اور sensors رکھتے ہیں
   - ڈیٹا کہاں stored ہے اور کون access کر سکتا ہے؟

5. **روزگار پر اثر (Job Displacement)**
   - Automation سے ملازمتوں کا نقصان
   - معاشرے کیسے transition کو سنبھالے؟

### اخلاقی frameworks

1. **Utilitarianism** - سب سے زیادہ لوگوں کے لیے سب سے زیادہ فائدہ
2. **Deontology** - قوانین اور duties کی پیروی
3. **Virtue Ethics** - اچھے character traits پر مبنی
4. **Care Ethics** - relationships اور care پر focus

---

## 5.4 Human-Robot Interaction (HRI) Safety

### Physical HRI

انسانوں کے قریب کام کرتے وقت:

- **Power and force limiting** - زیادہ سے زیادہ قوت اور رفتار کی حدیں
- **Collision detection** - sensors استعمال کرتے ہوئے contact detect کریں
- **Compliant control** - contact پر yielding
- **Emergency stops** - فوری shut-down mechanisms

### Psychological HRI

- **Predictability** - روبوٹ کی حرکات کو سمجھنے کے قابل ہونا چاہیے
- **Communication** - واضح signals (lights، sounds، displays)
- **Trust** - معتبر اور trustworthy behavior
- **Comfort** - uncanny valley سے بچیں

---

## 5.5 محفوظ تعیناتی (Safe Deployment)

### Development Process

1. **Requirements Analysis** - safety اور performance کی واضح ضروریات
2. **Risk Assessment** - ممکنہ hazards کی شناخت
3. **Design** - safety features کو architecture میں شامل کریں
4. **Implementation** - safe coding practices
5. **Testing** - extensive testing (unit، integration، system)
6. **Validation** - حقیقی دنیا کے حالات میں verify کریں
7. **Documentation** - تمام safety measures document کریں
8. **Training** - operators اور users کی تربیت
9. **Monitoring** - deployment کے بعد مسلسل monitoring
10. **Maintenance** - باقاعدہ updates اور inspections

### Testing Strategies

- **Unit testing** - individual components
- **Integration testing** - modules کے درمیان interactions
- **System testing** - مکمل نظام
- **Stress testing** - extreme conditions میں
- **Edge case testing** - غیر معمولی scenarios
- **Simulation** - حقیقی ہارڈویئر سے پہلے virtual testing

---

## 5.6 قانونی اور ریگولیٹری مسائل

### موجودہ Regulations

- **Product liability** - manufacturers ذمہ دار ہیں
- **Insurance requirements** - کچھ applications کے لیے
- **Certification** - کچھ domains میں ضروری (medical، aviation)
- **Data protection** - GDPR، CCPA جیسے قوانین

### مستقبل کے مسائل

- **Legal personhood** - کیا روبوٹس legal entities ہو سکتے ہیں؟
- **Liability frameworks** - autonomous systems کے لیے
- **International standards** - cross-border deployment کے لیے
- **Ethics boards** - AI development کی نگرانی

---

## عملی مشقیں

### مشق 5.1: Risk Assessment

ایک delivery robot کے لیے مکمل risk assessment کریں۔ ممکنہ hazards کی شناخت اور mitigation strategies تجویز کریں۔

### مشق 5.2: Safety Features

PyBullet میں emergency stop اور collision detection features implement کریں۔

### مشق 5.3: اخلاقی Case Study

ایک اخلاقی dilemma کا تجزیہ کریں (مثال: trolley problem کا robotic version) اور مختلف ethical frameworks استعمال کرتے ہوئے evaluate کریں۔

---

## خلاصہ

اس باب میں، آپ نے سیکھا:

- **حفاظت** فزیکل AI کی تعیناتی میں سب سے اہم ہے
- **خطرات** physical، software، cybersecurity domains میں موجود ہیں
- **اخلاقی تحفظات** autonomy، accountability، bias، privacy شامل ہیں
- **محفوظ تعیناتی** careful planning، testing، اور monitoring کی ضرورت ہے
- **قانونی frameworks** ابھی evolve ہو رہے ہیں

---

## نتیجہ: فزیکل اے آئی کا مستقبل

آپ نے **Introduction to Physical AI** کے تمام پانچ ابواب مکمل کر لیے ہیں! آپ نے سیکھا:

1. Embodied AI کیا ہے اور یہ اہم کیوں ہے
2. روبوٹس اپنے ماحول کو سینسرز کے ذریعے کیسے محسوس کرتے ہیں
3. روبوٹ کی حرکت کی ریاضی اور control
4. ذہین behavior کو منظم کرنے کے architectures
5. حفاظت، اخلاقیات، اور ذمہ دارانہ تعیناتی

**اگلے قدم**:
- اپنے projects بنائیں
- Community میں شامل ہوں
- تحقیق اور development میں حصہ لیں
- Physical AI کا مستقبل بنانے میں مدد کریں

شکریہ اس سفر میں شامل ہونے کے لیے!`,

  // Glossary
  '/glossary': `# لغت

فزیکل اے آئی میں استعمال ہونے والی اہم اصطلاحات۔

## A

**Actuator (ایکچویٹر)**: ایک ڈیوائس جو توانائی کو حرکت میں تبدیل کرتی ہے۔

**AI (مصنوعی ذہانت)**: مشینوں میں انسانی ذہانت کی نقل۔

## E

**Embodied AI (مجسم اے آئی)**: AI نظام جو جسمانی دنیا کے ساتھ تعامل کرتے ہیں۔

## K

**Kinematics (حرکیات)**: حرکت کا مطالعہ۔

## S

**Sensor (سینسر)**: ایک ڈیوائس جو جسمانی مقدار کو محسوس کرتی ہے۔`,

  // Contributing
  '/contributing': `# شراکت کے رہنما خطوط

فزیکل اے آئی بک میں تعاون کرنے کا شکریہ!

## کیسے تعاون کریں

1. Repository کو Fork کریں
2. تبدیلیاں کریں
3. Pull Request جمع کرائیں

## رہنما خطوط

- واضح، جامع documentation لکھیں
- کوڈ مثالیں شامل کریں
- تمام کوڈ کی جانچ کریں`,

  // Troubleshooting
  '/resources/troubleshooting': `# مسائل کا حل

عام مسائل اور ان کے حل۔

## انسٹالیشن کے مسائل

### Python Version

یقینی بنائیں کہ Python 3.9+ انسٹال ہے۔

### Package Errors

\`\`\`bash
pip install --upgrade pip
pip install -r requirements.txt
\`\`\``,

  // Community
  '/resources/community': `# کمیونٹی پروجیکٹس

کمیونٹی کے ذریعہ بنائے گئے پروجیکٹس۔

## پروجیکٹس

کمیونٹی کے اشتراک سے پروجیکٹس یہاں شامل ہوں گے۔`,
};

export default urduContent;
