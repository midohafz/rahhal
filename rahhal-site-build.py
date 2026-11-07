import json, re, subprocess, os, shutil, html, urllib.parse as U

SRC = '/mnt/user-data/outputs/rahhal-index.html'
OUT = '/mnt/user-data/outputs/rahhal-site'
SITE = 'https://midohafz.github.io/rahhal/'
CJ = 'https://www.jdoqocy.com/click-101918477-14071241'   # رابط CJ العام (غيّره هنا فقط)
DATE = '2026-11-07'
OWNER = 'Mohamad Badawy Hafz'
EMAIL = 'Rahhalegypt@gmail.com'

# ---------- 1. استخراج البيانات من التطبيق ----------
js = open(SRC, encoding='utf-8').read()
js = re.search(r'<script>(.*)</script>', js, re.S).group(1)

def grab(name, opener):
    i = js.index('var %s=' % name) + len('var %s=' % name)
    close = {'[': ']', '{': '}'}[opener]
    depth = 0; j = i; ins = False; q = ''
    while True:
        c = js[j]
        if ins:
            if c == '\\': j += 1
            elif c == q: ins = False
        elif c in '"\'': ins = True; q = c
        elif c == opener: depth += 1
        elif c == close:
            depth -= 1
            if depth == 0: break
        j += 1
    return js[i:j + 1]

def evaljs(expr):
    out = subprocess.run(['node', '-e', 'console.log(JSON.stringify(' + expr + '))'], capture_output=True, text=True)
    assert out.returncode == 0, out.stderr
    return json.loads(out.stdout)

HOTELS = evaljs(grab('HOTELS', '['))
HE = evaljs(grab('HE', '{'))
HT = evaljs(grab('HT', '{'))
HE['فور سيزونز فيرست ريزيدنس'] = 'Four Seasons Cairo First Residence'

LUXN = ["فورسيزونز", "سانت ريجيس", "ريتز", "وينتر بالاس", "أولد كتراكت", "كمبينسكي", "فيرمونت", "ميناهاوس"]
FAM = ["جولي فيل", "ريكسوس", "بيراميسا", "سافوي", "جاز", "موفنبيك", "هيلتون الغردقة"]
ROM = ["ريتز", "فورسيزونز", "سانت ريجيس", "وينتر بالاس", "أولد كتراكت", "كمبينسكي"]
HIS = ["وينتر بالاس", "أولد كتراكت", "ميناهاوس"]
def has(n, a): return any(x in n for x in a)

CITYMAP = {'القاهرة': 'cairo', 'الجيزة': 'cairo', 'الأقصر': 'luxor', 'أسوان': 'aswan', 'شرم الشيخ': 'sharm',
           'الغردقة': 'hurghada', 'الإسكندرية': 'alex', 'مرسى علم': 'marsa', 'العلمين': 'alamein'}

def norm(s): return re.sub(r'\s+', '', s)
HEN = {norm(k): v for k, v in HE.items()}
HTN = {norm(k): v for k, v in HT.items()}

hotels_by_city = {}
for h in HOTELS:
    en = HE.get(h['n']) or HEN.get(norm(h['n']))
    assert en, 'no english name: ' + h['n']
    tr = HT.get(en)
    assert tr, 'no translation: ' + en
    k = CITYMAP[h['c']]
    tags = []
    if has(h['n'], FAM): tags.append('fam')
    if has(h['n'], ROM): tags.append('rom')
    if has(h['n'], HIS): tags.append('his')
    if k in ('sharm', 'hurghada', 'marsa'): tags.append('dive')
    hotels_by_city.setdefault(k, []).append({'ar': h['n'], 'en': en, 'd': {'ar': h['d'], 'en': tr[0], 'ru': tr[2]},
                                             't': {'ar': h['t'], 'en': tr[1], 'ru': tr[3]}, 'lux': has(h['n'], LUXN), 'tags': tags})
order = ['Marriott Mena House', 'Four Seasons Hotel Cairo at Nile Plaza', 'The St. Regis Cairo', 'The Nile Ritz-Carlton', 'Fairmont Nile City', 'Four Seasons Cairo First Residence']
hotels_by_city['cairo'].sort(key=lambda x: order.index(x['en']) if x['en'] in order else 99)

# ---------- 2. بيانات المدن واللغات ----------
CITIES = [
    ('cairo', 'cairo-hotels.html', 'Cairo', 'cairo',
     {'ar': ('القاهرة ومصر القديمة', 'الأزهر، خان الخليلي، قلعة صلاح الدين، وأهرامات الجيزة.', 'القاهرة'),
      'en': ('Cairo & Old Egypt', 'Al-Azhar, Khan El-Khalili, Citadel, and Giza Pyramids.', 'Cairo'),
      'ru': ('Каир', 'Аль-Азхар, Хан Эль-Халили, Цитадель и Пирамиды.', 'Каир')}),
    ('luxor', 'luxor-hotels.html', 'Luxor', 'luxor',
     {'ar': ('الأقصر', 'معبد الكرنك، معبد الأقصر، ووادي الملوك والملكات.', 'الأقصر'),
      'en': ('Luxor', 'Karnak Temple, Luxor Temple, and Valley of the Kings.', 'Luxor'),
      'ru': ('Луксор', 'Карнакский храм, Луксорский храм и Долина Царей.', 'Луксор')}),
    ('aswan', 'aswan-hotels.html', 'Aswan', 'aswan',
     {'ar': ('أسوان', 'معبد فيلة، أبو سمبل، والقرية النوبية.', 'أسوان'),
      'en': ('Aswan', 'Philae Temple, Abu Simbel, and Nubian Village.', 'Aswan'),
      'ru': ('Асуан', 'Храм Филе, Абу-Симбел и Нубийская деревня.', 'Асуан')}),
    ('sharm', 'sharm-and-taba-hotels.html', 'Sharm El Sheikh', 'sea',
     {'ar': ('شرم الشيخ', 'محمية رأس محمد، خليج نعمة، وسوهو سكوير.', 'شرم الشيخ'),
      'en': ('Sharm El Sheikh', 'Ras Mohammed, Naama Bay, and Soho Square.', 'Sharm El Sheikh'),
      'ru': ('Шарм-эль-Шейх', 'Рас-Мохаммед, Наама Бей и Сохо Сквер.', 'Шарм-эль-Шейх')}),
    ('hurghada', 'hurghada-hotels.html', 'Hurghada', 'sea',
     {'ar': ('الغردقة', 'جزيرة الجفتون، مارينا الجونة، ومتحف الأحياء المائية.', 'الغردقة'),
      'en': ('Hurghada', 'Giftun Island, El Gouna Marina, and Aquarium.', 'Hurghada'),
      'ru': ('Хургада', 'Остров Гифтун, Марина Эль-Гуна и Аквариум.', 'Хургада')}),
    ('alex', 'alexandria-hotels.html', 'Alexandria', 'sea',
     {'ar': ('الإسكندرية', 'قلعة قايتباي، مكتبة الإسكندرية، وقصر المنتزه.', 'الإسكندرية'),
      'en': ('Alexandria', 'Qaitbay Citadel, Library, and Montaza Palace.', 'Alexandria'),
      'ru': ('Александрия', 'Цитадель Кайтбей, Библиотека и Монтаза.', 'Александрия')}),
    ('marsa', 'marsa-alam-hotels.html', 'Marsa Alam', 'sea',
     {'ar': ('مرسى علم', 'محمية صمداي (بيت الدلافين) وشاطئ أبو دباب.', 'مرسى علم'),
      'en': ('Marsa Alam', 'Sataya Dolphin Reef and Abu Dabbab Beach.', 'Marsa Alam'),
      'ru': ('Марса-Алам', 'Риф Сатая и пляж Абу-Дабаб.', 'Марса-Алам')}),
    ('alamein', 'el-alamein-hotels.html', 'El Alamein', 'sea',
     {'ar': ('العلمين الجديدة', 'أبراج العلمين، الشواطئ الفيروزية الرائعة.', 'العلمين'),
      'en': ('New El Alamein', 'Alamein Towers and crystal beaches.', 'El Alamein'),
      'ru': ('Эль-Аламейн', 'Башни Аламейн и чистые пляжи.', 'Эль-Аламейн')}),
]
FOLDER = {'ar': '', 'en': 'en/', 'ru': 'ru/'}

T = {
 'ar': {'dir': 'rtl', 'home': 'رحّال', 'sub': 'دليلك لمدن مصر السياحية والفنادق وخدمات الطيران',
        'welcome': 'أهلاً بكم في مصر', 'cities': 'المدن والمعالم السياحية', 'guide': 'دليل فنادق',
        'flights': 'الطيران', 'flights_note': 'لا نبيع تذاكر الطيران. هذه مواقع الشركات الرسمية للتحقق من الرحلات والأسعار.',
        'official': 'الموقع الرسمي', 'routes': 'المسارات', 'adv': 'للتعاون والإعلان',
        'adv_text': 'تمتلك شركة سياحة أو نقل مرخّصة؟ راسلنا لمناقشة التعاون.', 'adv_btn': 'تواصل معنا',
        'search': 'ابحث عن مدينة', 'back': '← العودة إلى رحّال', 'upd': 'آخر تحديث: 7 نوفمبر 2026',
        'disc': 'إفصاح: الأزرار أدناه روابط شراكة مع Booking.com عبر شبكة CJ. إذا حجزت عبرها قد نحصل على عمولة دون أي تكلفة إضافية عليك. نختار الفنادق ولا نتلقى مقابلاً لإدراجها. الأسعار والتوفر تظهر على Booking.com وقت الحجز. تصنيف الفئة والغرض تقدير منا وليس تصنيفاً رسمياً.',
        'btn': 'تحقق من السعر على Booking.com', 'before': 'قبل أن تحجز',
        'tips': ['قارن سعر Booking.com بالموقع الرسمي للفندق.', 'اقرأ سياسة الإلغاء قبل الدفع.', 'اسأل عن الفطور والإطلالة والنقل من المطار.', 'أسماء الفنادق وإداراتها وتجديداتها تتغير، فتأكد منها وقت الحجز.'],
        'privacy': 'الخصوصية والشروط', 'foot': 'المعلومات عامة وقد تتغير، ولسنا وكالة سفر ولا مزوّد خدمات سياحية.',
        'intro': 'أبرز ما يُزار: {s}', 'intro2': 'اختر الفندق حسب قربه من الأماكن التي تريد زيارتها ووقت الطريق إليها.',
        'title': 'فنادق {c}: {n} خيارات مشهورة | رحّال', 'h1': 'فنادق {c}: {n} خيارات مشهورة',
        'desc': 'دليل مختصر لفنادق مشهورة في {c} مع ملاحظات للاختيار وروابط للتحقق من الأسعار. آخر تحديث نوفمبر 2026.',
        'lux': 'فاخر جداً', 'hi': 'راقٍ', 'tag': {'fam': 'عائلات', 'rom': 'أزواج', 'his': 'تاريخي', 'dive': 'بحر وغوص'},
        'note': 'ملاحظة', 'idx_title': 'رحّال | دليل مدن مصر السياحية والفنادق', 'idx_desc': 'دليل لمدن مصر السياحية وفنادقها وشركات الطيران، بثلاث لغات: العربية والإنجليزية والروسية.',
        'lang': 'اللغة', 'cities_n': 'عرض فنادق المدينة', 'idx_note': 'روابط الحجز في صفحات الفنادق روابط شراكة مع Booking.com عبر شبكة CJ، وقد نحصل على عمولة دون أي تكلفة إضافية عليك.'},
 'en': {'dir': 'ltr', 'home': 'Rahhal', 'sub': 'Your guide to Egypt\u2019s tourist cities, hotels and flight services',
        'welcome': 'Welcome to Egypt', 'cities': 'Cities and sights in Egypt', 'guide': 'Hotels guide',
        'flights': 'Flights', 'flights_note': 'We do not sell flight tickets. These are the airlines\u2019 official websites for checking flights and fares.',
        'official': 'Official website', 'routes': 'Routes', 'adv': 'Partnerships and advertising',
        'adv_text': 'Do you run a licensed travel or transport company? Write to us to discuss working together.', 'adv_btn': 'Contact us',
        'search': 'Search for a city', 'back': '\u2190 Back to Rahhal', 'upd': 'Last updated: 7 November 2026',
        'disc': 'Disclosure: the buttons below are affiliate links with Booking.com through the CJ network. If you book through them we may earn a commission at no extra cost to you. We choose the hotels and receive nothing for listing them. Prices and availability are shown on Booking.com at booking time. The tier and best-for labels are our own estimate, not an official rating.',
        'btn': 'Check price on Booking.com', 'before': 'Before you book',
        'tips': ['Compare the Booking.com price with the hotel\u2019s official site.', 'Read the cancellation policy before paying.', 'Ask about breakfast, the view and airport transfer.', 'Hotel names, management and renovations change, so confirm at booking time.'],
        'privacy': 'Privacy and terms', 'foot': 'The information is general and may change. We are not a travel agency or a tourism service provider.',
        'intro': 'Main sights: {s}', 'intro2': 'Choose a hotel by how close it is to the places you want to visit and the travel time to them.',
        'title': '{c} hotels: {n} well-known options | Rahhal', 'h1': '{c} hotels: {n} well-known options',
        'desc': 'A short guide to well-known hotels in {c}, with selection notes and links to check prices. Updated November 2026.',
        'lux': 'Ultra-luxury', 'hi': 'Upscale', 'tag': {'fam': 'Families', 'rom': 'Couples', 'his': 'Historic', 'dive': 'Sea and diving'},
        'note': 'Note', 'idx_title': 'Rahhal | Egypt tourist cities and hotels guide', 'idx_desc': 'A guide to Egypt\u2019s tourist cities, hotels and airlines in three languages: Arabic, English and Russian.',
        'lang': 'Language', 'cities_n': 'View city hotels', 'idx_note': 'Booking links on the hotel pages are affiliate links with Booking.com through the CJ network, and we may earn a commission at no extra cost to you.'},
 'ru': {'dir': 'ltr', 'home': 'Раххаль', 'sub': 'Ваш гид по городам Египта, отелям и авиаперелётам',
        'welcome': 'Добро пожаловать в Египет', 'cities': 'Города и достопримечательности Египта', 'guide': 'Гид по отелям',
        'flights': 'Авиаперелёты', 'flights_note': 'Мы не продаём авиабилеты. Это официальные сайты авиакомпаний для проверки рейсов и цен.',
        'official': 'Официальный сайт', 'routes': 'Маршруты', 'adv': 'Сотрудничество и реклама',
        'adv_text': 'У вас лицензированная туристическая или транспортная компания? Напишите нам, чтобы обсудить сотрудничество.', 'adv_btn': 'Связаться с нами',
        'search': 'Найти город', 'back': '\u2190 Вернуться в Раххаль', 'upd': 'Обновлено: 7 ноября 2026',
        'disc': 'Раскрытие информации: кнопки ниже — партнёрские ссылки Booking.com через сеть CJ. Если вы забронируете через них, мы можем получить комиссию без дополнительных затрат для вас. Мы сами выбираем отели и ничего не получаем за их включение. Цены и наличие мест показываются на Booking.com в момент бронирования. Класс и «Подходит для» — наша собственная оценка, а не официальный рейтинг.',
        'btn': 'Узнать цену на Booking.com', 'before': 'Перед бронированием',
        'tips': ['Сравните цену на Booking.com с официальным сайтом отеля.', 'Прочитайте условия отмены до оплаты.', 'Уточните завтрак, вид из номера и трансфер из аэропорта.', 'Названия, управление и ремонт отелей меняются, проверьте при бронировании.'],
        'privacy': 'Конфиденциальность и условия', 'foot': 'Информация общая и может меняться. Мы не турагентство и не поставщик туристических услуг.',
        'intro': 'Главное: {s}', 'intro2': 'Выбирайте отель по близости к местам, которые хотите посетить, и по времени в пути.',
        'title': 'Отели: {c} — {n} известных вариантов | Раххаль', 'h1': 'Отели: {c} — {n} известных вариантов',
        'desc': 'Краткий гид по известным отелям: {c}. Заметки для выбора и ссылки для проверки цен. Обновлено в ноябре 2026.',
        'lux': 'Люкс', 'hi': 'Высокий класс', 'tag': {'fam': 'Семьи', 'rom': 'Пары', 'his': 'Исторический', 'dive': 'Море и дайвинг'},
        'note': 'Примечание', 'idx_title': 'Раххаль | Гид по городам и отелям Египта', 'idx_desc': 'Гид по городам, отелям и авиакомпаниям Египта на трёх языках: арабском, английском и русском.',
        'lang': 'Язык', 'cities_n': 'Отели города', 'idx_note': 'Ссылки для бронирования на страницах отелей — партнёрские ссылки Booking.com через сеть CJ; мы можем получить комиссию без дополнительных затрат для вас.'},
}
LANGNAME = {'ar': 'العربية', 'en': 'English', 'ru': 'Русский'}

AIRLINES = [
    ('EgyptAir', 'https://www.egyptair.com',
     {'ar': ('مصر للطيران', 'الناقل الوطني، وله أوسع شبكة رحلات داخلية.', 'القاهرة، شرم الشيخ، الغردقة، مرسى علم، الإسكندرية، الأقصر، العلمين، أسوان، أبو سمبل'),
      'en': ('EgyptAir', 'The national carrier, with the widest domestic network.', 'Cairo, Sharm El Sheikh, Hurghada, Marsa Alam, Alexandria, Luxor, El Alamein, Aswan, Abu Simbel'),
      'ru': ('EgyptAir', 'Национальный перевозчик с самой широкой сетью внутренних рейсов.', 'Каир, Шарм-эль-Шейх, Хургада, Марса-Алам, Александрия, Луксор, Эль-Аламейн, Асуан, Абу-Симбел')}),
    ('Air Cairo', 'https://www.aircairo.com',
     {'ar': ('إير كايرو', 'شركة اقتصادية تابعة لمصر للطيران، تشغّل رحلات داخلية وإقليمية.', 'القاهرة، شرم الشيخ، الغردقة، مرسى علم، الأقصر، أسوان، أبو سمبل'),
      'en': ('Air Cairo', 'A low-cost airline owned by EgyptAir, running domestic and regional flights.', 'Cairo, Sharm El Sheikh, Hurghada, Marsa Alam, Luxor, Aswan, Abu Simbel'),
      'ru': ('Air Cairo', 'Лоукостер, принадлежащий EgyptAir, выполняет внутренние и региональные рейсы.', 'Каир, Шарм-эль-Шейх, Хургада, Марса-Алам, Луксор, Асуан, Абу-Симбел')}),
    ('Nile Air', 'https://www.nileair.com',
     {'ar': ('النيل للطيران', 'شركة خاصة تركز على الرحلات الداخلية بين المدن السياحية.', 'القاهرة، شرم الشيخ، الغردقة، الأقصر، أسوان'),
      'en': ('Nile Air', 'A private airline focused on domestic flights between tourist cities.', 'Cairo, Sharm El Sheikh, Hurghada, Luxor, Aswan'),
      'ru': ('Nile Air', 'Частная авиакомпания, специализирующаяся на внутренних рейсах между туристическими городами.', 'Каир, Шарм-эль-Шейх, Хургада, Луксор, Асуан')}),
    ('Nesma Airlines', 'https://www.nesmaairlines.com',
     {'ar': ('نسمة للطيران', 'شركة مصرية تابعة لمجموعة نسمة السعودية، برحلات داخلية وإقليمية.', 'القاهرة، شرم الشيخ، الغردقة، الأقصر، أسوان، سوهاج'),
      'en': ('Nesma Airlines', 'An Egyptian airline owned by Saudi Nesma Group, with domestic and regional flights.', 'Cairo, Sharm El Sheikh, Hurghada, Luxor, Aswan, Sohag'),
      'ru': ('Nesma Airlines', 'Египетская авиакомпания саудовской группы Nesma с внутренними и региональными рейсами.', 'Каир, Шарм-эль-Шейх, Хургада, Луксор, Асуан, Сохаг')}),
]

CSS = '''
:root{--bg:#f4f7f8;--surface:#fff;--ink:#12262e;--muted:#566b73;--line:#d8e2e6;--brand:#0b6e7a;--brand-ink:#fff;--soft:#e0f0f2;--warn:#fff4d6;--warn-ink:#4a3a00;--hero1:#0b4f63;--hero2:#0b6e7a}
@media (prefers-color-scheme:dark){:root{--bg:#0e1a20;--surface:#16262e;--ink:#e8f1f4;--muted:#9bb0b8;--line:#27404a;--brand:#4cc3d0;--brand-ink:#06242a;--soft:#1b3a42;--warn:#3a3210;--warn-ink:#f1e3a8;--hero1:#0b3a48;--hero2:#0e5560}}
*,*::before,*::after{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);font-family:"Segoe UI",Tahoma,Arial,"Noto Sans",sans-serif;font-size:17px;line-height:1.75}
.wrap{max-width:1100px;margin:0 auto;padding:20px 16px 48px}
a{color:var(--brand)}
a:focus-visible,button:focus-visible,input:focus-visible{outline:3px solid var(--brand);outline-offset:2px}
.bar{background:var(--surface);border-bottom:1px solid var(--line)}
.bar .wrap{display:flex;justify-content:space-between;align-items:center;padding-top:10px;padding-bottom:10px;gap:12px;flex-wrap:wrap}
.bar a.brand{font-weight:800;font-size:20px;text-decoration:none}
.langs a{display:inline-block;margin-inline-start:6px;padding:4px 12px;border:1px solid var(--line);border-radius:999px;text-decoration:none;font-size:15px;color:var(--ink)}
.langs a[aria-current="true"]{background:var(--brand);color:var(--brand-ink);border-color:var(--brand);font-weight:700}
.hero{background:linear-gradient(135deg,var(--hero1),var(--hero2));color:#fff;border-radius:18px;padding:28px 22px 0;margin:18px 0;overflow:hidden}
.hero h1{font-size:34px;line-height:1.3;margin:0 0 6px}
.hero p{margin:0 0 6px;font-size:18px}
.hero svg{display:block;width:100%;height:90px;margin-top:10px}
h1{font-size:28px;line-height:1.35;margin:12px 0}
h2{font-size:23px;margin:34px 0 10px}
h3{font-size:19px;margin:0 0 4px}
.note{background:var(--warn);color:var(--warn-ink);border-radius:12px;padding:10px 14px;font-size:15px;margin:16px 0}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:18px}
.card{background:var(--surface);border:1px solid var(--line);border-radius:14px;overflow:hidden;display:flex;flex-direction:column}
.card .body{padding:14px 16px 16px;flex:1;display:flex;flex-direction:column}
.card svg.art{display:block;width:100%;height:84px}
.hotel{padding:16px;margin:14px 0;background:var(--surface);border:1px solid var(--line);border-radius:14px}
.en{color:var(--muted);font-size:14px;direction:ltr}
html[dir=rtl] .en{text-align:right}
.tags span{display:inline-block;font-size:13px;border:1px solid var(--line);border-radius:999px;padding:1px 10px;margin:6px 0 0;margin-inline-end:6px;color:var(--muted)}
.tip{background:var(--soft);border-radius:10px;padding:8px 12px;font-size:15px;margin-top:10px}
.btn{display:inline-block;margin-top:12px;padding:10px 16px;border-radius:10px;background:var(--brand);color:var(--brand-ink);font-weight:700;text-decoration:none}
.card .btn{margin-top:auto;text-align:center}
.card p{margin:6px 0 12px;color:var(--muted)}
.search{width:100%;max-width:520px;padding:12px 16px;border:1px solid var(--line);border-radius:12px;background:var(--surface);color:var(--ink);font:inherit;margin:8px 0 18px}
.back{font-size:15px}
footer{margin-top:44px;font-size:14px;color:var(--muted);border-top:1px solid var(--line);padding-top:16px}
footer a{margin-inline-end:10px}
@media (max-width:520px){.hero h1{font-size:27px}}
'''

def art(kind, color):
    s = '<svg class="art" viewBox="0 0 300 64" preserveAspectRatio="none" aria-hidden="true" focusable="false"><rect width="300" height="64" fill="%s" fill-opacity=".14"/><circle cx="250" cy="18" r="9" fill="%s" fill-opacity=".55"/>' % (color, color)
    if kind == 'cairo':
        s += '<path d="M20 64L80 14l60 50zM100 64l50-34 50 34zM170 64l40-26 40 26z" fill="%s" fill-opacity=".75"/>' % color
    elif kind in ('luxor', 'aswan'):
        s += '<path d="M30 20h240v8H30zM44 28h14v36H44zM84 28h14v36H84zM124 28h14v36h-14zM164 28h14v36h-14zM204 28h14v36h-14zM244 28h14v36h-14z" fill="%s" fill-opacity=".75"/>' % color
    else:
        s += '<path d="M0 44q25-10 50 0t50 0 50 0 50 0 50 0 50 0V64H0z" fill="%s" fill-opacity=".6"/><path d="M0 54q25-8 50 0t50 0 50 0 50 0 50 0 50 0V64H0z" fill="%s" fill-opacity=".8"/>' % (color, color)
    return s + '</svg>'

COLORS = {'cairo': '#b5651d', 'luxor': '#8a3b5c', 'aswan': '#2d5fa8', 'sharm': '#0b7f9c', 'hurghada': '#0b7f9c', 'alex': '#3b7a57', 'marsa': '#0b7f9c', 'alamein': '#3b7a57'}
FAV = 'data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 64 64%27%3E%3Crect width=%2764%27 height=%2764%27 rx=%2714%27 fill=%27%230b6e7a%27/%3E%3Cpath d=%27M8 52L32 14l24 38z%27 fill=%27%23fff%27/%3E%3C/svg%3E'

def esc(s): return html.escape(s, quote=True)
def rel(frm, to_lang, file):
    if frm == to_lang: return file
    if frm == 'ar': return FOLDER[to_lang] + file
    if to_lang == 'ar': return '../' + file
    return '../' + FOLDER[to_lang] + file
def url(lang, file): return SITE + FOLDER[lang] + file

def head(lang, title, desc, file, extra=''):
    alts = ''.join('<link rel="alternate" hreflang="%s" href="%s">\n' % (l, url(l, file)) for l in ('ar', 'en', 'ru'))
    alts += '<link rel="alternate" hreflang="x-default" href="%s">\n' % url('ar', file)
    return ('<!DOCTYPE html>\n<html lang="%s" dir="%s">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '<title>%s</title>\n<meta name="description" content="%s">\n<meta name="robots" content="index,follow">\n<meta name="theme-color" content="#0b6e7a">\n'
            '<link rel="canonical" href="%s">\n%s<link rel="icon" href="%s">\n'
            '<meta property="og:type" content="website">\n<meta property="og:title" content="%s">\n<meta property="og:description" content="%s">\n<meta property="og:url" content="%s">\n<meta property="og:locale" content="%s">\n%s<style>%s</style>\n</head>\n<body>\n') % (
        lang, T[lang]['dir'], esc(title), esc(desc), url(lang, file), alts, FAV, esc(title), esc(desc), url(lang, file),
        {'ar': 'ar_EG', 'en': 'en_US', 'ru': 'ru_RU'}[lang], extra, CSS)

def topbar(lang, file):
    t = T[lang]
    sw = ''.join('<a href="%s" hreflang="%s" lang="%s"%s>%s</a>' % (rel(lang, l, file), l, l, ' aria-current="true"' if l == lang else '', LANGNAME[l]) for l in ('ar', 'en', 'ru'))
    home = 'index.html' if lang == 'ar' else 'index.html'
    return '<div class="bar"><div class="wrap"><a class="brand" href="%s">%s</a><nav class="langs" aria-label="%s">%s</nav></div></div>\n' % (home, esc(t['home']), esc(t['lang']), sw)

def footer(lang):
    t = T[lang]
    pr = ('privacy.html' if lang == 'ar' else '../privacy.html') + {'ar': '#ar', 'en': '#en', 'ru': '#ru'}[lang]
    return ('<footer><p>%s</p><p><a href="%s">%s</a><a href="mailto:%s">%s</a></p><p>\u00a9 2026 %s \u00b7 %s</p></footer>\n</div>\n') % (
        esc(t['foot']), pr, esc(t['privacy']), EMAIL, EMAIL, esc(t['home']), OWNER)

def cj_link(lang, cityk, hotel, city_en):
    slug = re.sub(r'[^a-z0-9]+', '-', hotel['en'].lower()).strip('-')[:40]
    dest = 'https://www.booking.com/searchresults.html?ss=' + U.quote_plus(hotel['en'] + ' ' + city_en)
    return '%s?sid=%s&url=%s' % (CJ, 'rahhal-%s-%s-%s' % (lang, cityk, slug), U.quote(dest, safe=''))

def build_city(lang, c):
    key, file, city_en, art_kind, names = c
    t = T[lang]; name, sights, short = names[lang]
    hs = hotels_by_city[key]; n = len(hs)
    ld = {'@context': 'https://schema.org', '@type': 'ItemList', 'name': t['h1'].format(c=short, n=n),
          'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': h['en']} for i, h in enumerate(hs)]}
    extra = '<script type="application/ld+json">%s</script>\n' % json.dumps(ld, ensure_ascii=False)
    out = head(lang, t['title'].format(c=short, n=n), t['desc'].format(c=short), file, extra)
    out += topbar(lang, file) + '<div class="wrap">\n<a class="back" href="index.html">%s</a>\n<h1>%s</h1>\n<p>%s</p>\n' % (esc(t['back']), esc(t['h1'].format(c=short, n=n)), esc(t['upd']))
    out += '<p>%s %s</p>\n<div class="note" role="note">%s</div>\n' % (esc(t['intro'].format(s=sights)), esc(t['intro2']), esc(t['disc']))
    for h in hs:
        title_main = h['ar'] if lang == 'ar' else h['en']
        sub = '<div class="en">%s</div>' % esc(h['en']) if lang == 'ar' else ''
        tags = '<span>%s</span>' % esc(t['lux'] if h['lux'] else t['hi']) + ''.join('<span>%s</span>' % esc(t['tag'][x]) for x in h['tags'])
        out += ('<article class="hotel"><h2 style="font-size:20px;margin:0 0 4px">%s</h2>%s<div class="tags">%s</div><p>%s</p><div class="tip">%s: %s</div>'
                '<a class="btn" rel="sponsored noopener" target="_blank" href="%s">%s</a></article>\n') % (
            esc(title_main), sub, tags, esc(h['d'][lang]), esc(t['note']), esc(h['t'][lang]), esc(cj_link(lang, key, h, city_en)), esc(t['btn']))
    out += '<h2>%s</h2><ul>%s</ul>\n' % (esc(t['before']), ''.join('<li>%s</li>' % esc(x) for x in t['tips']))
    return out + footer(lang) + '</body>\n</html>\n'

def build_index(lang):
    t = T[lang]; file = 'index.html'
    out = head(lang, t['idx_title'], t['idx_desc'], file)
    out += topbar(lang, file) + '<div class="wrap">\n'
    out += '<section class="hero"><h1>%s</h1><p>%s</p><p><strong>%s</strong></p>%s</section>\n' % (esc(t['home']), esc(t['sub']), esc(t['welcome']), art('cairo', '#ffffff'))
    out += '<h2>%s</h2>\n<input class="search" id="q" type="search" placeholder="%s" aria-label="%s">\n<div class="grid" id="cities">\n' % (esc(t['cities']), esc(t['search']), esc(t['search']))
    for c in CITIES:
        key, file2, city_en, kind, names = c; name, sights, short = names[lang]
        out += ('<article class="card"><a href="%s" style="text-decoration:none" tabindex="-1" aria-hidden="true">%s</a><div class="body"><h3>%s</h3><p>%s</p><a class="btn" href="%s">%s \u2014 %s</a></div></article>\n') % (
            file2, art(kind, COLORS[key]), esc(name), esc(sights), file2, esc(t['guide']), esc(short))
    out += '</div>\n<h2>%s</h2>\n<p>%s</p>\n<div class="grid">\n' % (esc(t['flights']), esc(t['flights_note']))
    for en_name, site, d in AIRLINES:
        nm, desc, routes = d[lang]
        out += '<article class="card"><div class="body"><h3>%s</h3><p>%s</p><p><strong>%s:</strong> %s</p><a class="btn" rel="noopener" target="_blank" href="%s">%s</a></div></article>\n' % (
            esc(nm), esc(desc), esc(t['routes']), esc(routes), site, esc(t['official']))
    out += '</div>\n<h2>%s</h2>\n<p>%s</p>\n<p><a class="btn" href="mailto:%s">%s</a></p>\n' % (esc(t['adv']), esc(t['adv_text']), EMAIL, esc(t['adv_btn']))
    out += '<div class="note" role="note">%s</div>\n' % esc(t['idx_note'])
    out += ('<script>(function(){var q=document.getElementById("q"),cs=document.querySelectorAll("#cities .card");'
            'q.addEventListener("input",function(){var v=q.value.trim().toLowerCase();cs.forEach(function(c){c.style.display=(!v||c.textContent.toLowerCase().indexOf(v)>-1)?"":"none"})})})();</script>\n')
    return out + footer(lang) + '</body>\n</html>\n'

def build_404():
    return ('<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>404 | رحّال</title><meta name="robots" content="noindex"><style>%s</style></head>'
            '<body><div class="wrap"><h1>404</h1><p>الصفحة غير موجودة. / Page not found. / Страница не найдена.</p><p><a class="btn" href="%s">رحّال</a></p></div></body></html>') % (CSS, SITE)

# ---------- 3. كتابة الملفات ----------
if os.path.exists(OUT): shutil.rmtree(OUT)
os.makedirs(OUT + '/en'); os.makedirs(OUT + '/ru')
pages = []
for lang in ('ar', 'en', 'ru'):
    d = OUT + '/' + FOLDER[lang]
    open(d + 'index.html', 'w', encoding='utf-8').write(build_index(lang)); pages.append((lang, 'index.html'))
    for c in CITIES:
        open(d + c[1], 'w', encoding='utf-8').write(build_city(lang, c)); pages.append((lang, c[1]))
open(OUT + '/404.html', 'w', encoding='utf-8').write(build_404())

# privacy: انسخ الصفحة السابقة وأضف canonical
pv = open('/mnt/user-data/outputs/privacy.html', encoding='utf-8').read()
if 'rel="canonical"' not in pv:
    pv = pv.replace('<meta name="robots" content="index,follow">', '<meta name="robots" content="index,follow">\n<link rel="canonical" href="%sprivacy.html">' % SITE, 1)
open(OUT + '/privacy.html', 'w', encoding='utf-8').write(pv)

urls = ''.join('<url><loc>%s</loc><lastmod>%s</lastmod></url>\n' % (url(l, f), DATE) for l, f in pages)
urls += '<url><loc>%sprivacy.html</loc><lastmod>%s</lastmod></url>\n' % (SITE, DATE)
open(OUT + '/sitemap.xml', 'w', encoding='utf-8').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + '</urlset>\n')
open(OUT + '/robots.txt', 'w').write('User-agent: *\nAllow: /\n\nSitemap: %ssitemap.xml\n' % SITE)
open(OUT + '/.nojekyll', 'w').write('')
print('pages', len(pages) + 1, 'hotels', {k: len(v) for k, v in hotels_by_city.items()})
