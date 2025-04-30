
import telebot
bot = telebot.TeleBot(token)

user_states = {}
user_routes = {}

from geopy.distance import great_circle  # Для расчета расстояний между городами
import logging
import itertools
from itertools import permutations
from telebot import types
import folium
from telebot import TeleBot, types


regions = ['central', 'northwest', 'south', 'volga', 'ural', 'sibirsk', 'daln', 'kavkaz']
cities = {
    'central': ['Москва', 'Тула', 'Рязань', 'Владимир', 'Воронеж', 'Иваново', 'Липецк', 'Орел', 'Ярославль'],
    'northwest': ['Санкт-Петербург', 'Калининград', 'Архангельск'],
    'south': ['Астрахань','Краснодар','Сочи'],
    'volga': ['Уфа','Казань','Оренбург'],
    'ural': ['Салехард','Екатеринбург','Тюмень'],
    'sibirsk':['Новосибирск','Омск','Норильск'],
    'daln':['Благовещенск','Хабаровск','Владивосток'],
    'kavkaz':['Грозный','Махачкала','Владикавказ']
}

# Достопримечательности по городам с описанием и фото
attractions = {
    "Москва": {
        "Долина реки Битцы": {
            "description": "Маршрут проложен вдоль левого берега реки Битцы, мимо заболоченной поймы, болота, памятника природы «Старый ельник в Знаменском-Садках». Посетители познакомятся с экосистемой рек, их флорой и фауной.",
            "photo": "https://ic.pics.livejournal.com/anton_i_masha/74760968/910048/910048_2000.jpg"
        },
        "Экотропа в природно-историческом парке «Кузьминки-Люблино»": {
            "description": "На этот маршрут можно попасть, войдя в отдаленную часть лесопарка. Посетителям по пути попадутся березы, сосны, рябины, черноольшаники. Из животных можно увидеть крота, ласку, лису.",
        },
        "«У истоков рек» в ландшафтном заказнике «Теплый Стан»": {
            "description": "Экотропа состоит из 11 участков с точками-остановками, среди которых Теплостанская возвышенность, овражно-балочная сеть, родник «Холодный» (памятник природы) и другие интересные объекты.",
        },
        "«В гармонии с природой» в Серебряном бору": {
            "description": "Чтобы пройти через весь Серебряный бор, можно воспользоваться тропой «В гармонии с природой», которая пролегает мимо заливов озера Бездонного, через заповедный лес, сосняки и опушки. (Подробнее https://www.mos.ru/news/item/97366073/)",
        }
    },
    "Тула":{
        "Малиновая засека":{
            "description": "Древний лесной массив, расположенный неподалеку от южной окраины областного центра. Пешком от Косой Горы где начинается экотропа, можно спокойно добраться до Ясной поляны. (Подробнее https://myslo.ru/news/company/2020-02-05-ekotropa-v-malinovoj-zaseke-progulki-po-istoricheskim-mestam-tuly)",
            "photo": "https://avatars.mds.yandex.net/i?id=aa933014fca04f145d485edaba864e51_l-11869273-images-thumbs&n=13"
        }
    },
    "Рязань":{
        "Тропа Паустовского":{
            "description": " Всего 7 вариантов маршрутов туристических протяженностью от 7 до 50 километров. Каждый маршрут промаркирован и оборудован информационными стендами, где можно отсканировать QR и начать своё сказочное путешествие по свежему воздуху.(Подробнее: https://www.tourister.ru/world/europe/russia/city/solotcha/placeofinterest/33933)",
            "photo": "https://avatars.mds.yandex.net/i?id=99745c40b911f423d32529db8501aaf0_l-5869166-images-thumbs&n=13"
        }
    },
    "Владимир": {
        "Боголюбовский луг": {
            "description": "На Боголюбовский луг можно ходить хоть каждый месяц. И раз от разу картинка будет другая, так как постоянно идет смена растительности. На лугу произрастает более 290 видов различных растений, некоторые из них занесены в Красную книгу.",
            "photo": "https://avatars.dzeninfra.ru/get-zen_doc/271828/pub_659aecba16f1ad2e39b1f677_659aed4895509b2d84332255/scale_1200"
        },
        "Дендрарий в парке «Дружба»": {
            "description": "Протяженность всесезонного маршрута составляет 6 километров. К слову, это расстояние равно необходимой суточной норме прогулки, по мнению врачей. Общедоступную «Тропу Дружбы» могут посещать как организованные группы школьников, так и простые горожане.",
        },
        "Дюкинские карьеры": {
            "description": "Маршрут экотропы проходит по каменистым склонам и террасам старого известнякового карьера… Туристы пройдут по дну древнего моря, где увидят уникальные палеонтологические объекты: остатки раковин древних моллюсков, отпечатки кораллов, относящихся к каменноугольному периоду развития нашей планеты.",
        }
    },
    "Воронеж": {
        "Заповедная сказка": {
            "description": "Специально оборудованный лесной маршрут находится в шаговой доступности от Центральной площади. На небольшой территории можно увидеть типичных представителей флоры Усманского бора.",
            "photo": "https://cdn.culture.ru/images/53e82bf7-a9d8-5bd3-ace2-dd21600172ef"
        },
        "Черепахинская": {
            "description": "Живописный маршрут среди сосен. Дает возможность окунуться в природу, без страха заблудиться. Маршрут разделен на длительные и короткие прогулки.",
        }
    },
     "Ярославль": {
        "Заповедная сказка": {
            "description": "Специально оборудованный лесной маршрут находится в шаговой доступности от Центральной площади. На небольшой территории можно увидеть типичных представителей флоры Усманского бора.",
            "photo": "https://avatars.dzeninfra.ru/get-zen_doc/5098316/pub_6398c30799b73029a4f9b1fe_639a1c08d5ce4f7656eac402/scale_1200"
        },
        "Черепахинская": {
            "description": "Живописный маршрут среди сосен. Дает возможность окунуться в природу, без страха заблудиться. Маршрут разделен на длительные и короткие прогулки.",
        }
    },

    "Санкт-Петербург":{
        "Сестрорецкое болото":{
            "description": "е площадки, мостики, а также инфостенды о флоре и фауне заказника.",
            "photo": "https://avatars.yandex.net/get-music-content/9837520/67df1b93.t.127523348-1/m1000x1000?webp=false"
        },
        "Комаровский берег": {
            "description": "На маршруте длинной 2,8 км. встретятся беседки, пруды, мостики, а также большие муравейники. Тропинки проходят по красивейшему сосновому лесу и выходят на Финский залив.",
        },
        "Линдуловская роща": {
            "description": "Маршрут проходит по красивому лесу, выходит к речке с порогами, по маршруту есть деревянные настилы, беседки, указатели и много других замечательных мест. Длина маршрута составляет 5.5 км.",

        },
        "Дудергофские высоты": {
            "description": "Экотропа начинается от станции Можайская и заканчивается у мемориала морякам-авроровцам. На маршруте вы узнаете информацию об истории этих мест с 15 века. Протяжённость тропы: 2,5 км. (Подробнее обо всех экотропах: https://dzen.ru/a/ZjKW1ZlDKSNPz3nd)",

        }
    },
    "Калининград":{
        "Высота Эфа":{
            "description": "Проходит через песчаные дюны Куршской косы. Длина тропы — примерно 3 км, на ней есть две обзорные площадки. (Подробнее: https://eco-trails.ru/catalog/kaliningradskaya-oblast/vysota-efa/)",
            "photo": "https://avatars.mds.yandex.net/i?id=a5910c3ae3d72cdfcc18ebc75b4b24c5_l-8494143-images-thumbs&n=13"
        },
        "Танцующий лес": {
            "description": "Находится в национальном парке «Куршская коса», в посёлке Рыбачий. Длина маршрута — 0,8 км. ",
        },
        "Сказки Куршской косы": {
            "description": "Пешеходный маршрут по парку длиной 2 км покрыт высокотехнологичным нетканым полотном — геотекстилем, поверх которого насыпана песчано-гравийная смесь. Со временем дорожка уплотнится, и это спасет почву от разрушения. (Подробнее: https://www.kp.ru/russia/kaliningrad/mesta/kurshskaya-kosa/ekologicheskaya-tropa/)",

        }
    },
    "Архангельск":{
        "К Сийским озёрам":{
            "description": "5 км экотропы предоставляют отличную возможность насладиться атмосферой соснового леса, восхититься красотой Сийских озёр и просто пообщаться с природой. ",
            "photo": "https://avatars.dzeninfra.ru/get-zen_doc/3986710/pub_608aa5ee9b8b9a4212897308_6094f13f4fade3788bc8c917/scale_1200"
        },
        "Мудьюг": {
            "description": "Кольцевой маршрут тропы подготовлен исключительно для пешего передвижения и имеет протяженность около 5 км.",
        },
        "По следам Грина": {
            "description": "Экотропа знакомит с уникальностью и ценностями заказника «Железные Ворота», с впечатлениями от жизни в архангельской ссылке А.С. Грина и его жены В.П. Гриневской. (Подробнее обо всех экотропах: https://travel.eco29.ru/ecotropi/)  ",

        }
    },
    "Астрахань":{
        "Обретенная дельта":{
            "description": "Маршрут проходит через 4 острова, каждый из которых позволяет познакомиться с различными заповедными биотопами и их обитателями. (Подробнее: https://astrakhanzapoved.ru/экотуризм-1/экскурсии-и-туры/экологическая-тропа-обретённая-дель/)",
            "photo": "https://s1.stc.all.kpcdn.net/russia/wp-content/uploads/2023/09/Astrahanskij-kreml-1330.jpg"
        }
    },
    "Ростов-на-Дону":{
        "Щепкинский лес":{
            "description": "В Щепкинском лесу распространены как пешеходные прогулки, так и велосипедные. На въезде в лес со стороны поселка Темерницкий находится пункт проката велосипедов.",
            "photo": "https://titam.ru/wp-content/uploads/2022/11/Театр-Драмы.jpg"
        },
        "Тайны дельты Дона": {
            "description": "Дельта Дона это - дивный уголок живой природы с десятками островов, сотнями километров речных проток, утопающих в причудливом зеленом убранстве.",
        }
    },
    "Сочи":{
        "Тропа здоровья":{
            "description": "Тропа, проложенная по южным склонам горы Псехако, находится на территории Сочинского национального парка и относится к категории терренкуров. Подробнее: https://rosakhutor.ru/what-to-do/tropa-zdorovya-bolshoe-koltso/?ysclid=m7ai5gt29b413689051",
            "photo": "https://a.d-cd.net/REAAAgJItuA-1920.jpg"
        },
        "Реликтовый лес": {
            "description": "Несложная пологая тропа идет по тенистому буковому лесу среди необхватных многовековых пихт и редких растений-эндемиков, которые не встречаются нигде больше кроме Западного Кавказа. Протяженность около 1 км.",
        }
    },
    "Уфа":{
        "Таллы":{
            "description": "Несложная пологая тропа идет по тенистому буковому лесу среди необхватных многовековых пихт и редких растений-эндемиков, которые не встречаются нигде больше кроме Западного Кавказа. Протяженность 3,5 км. (Подробнее: https://trekkingmania.ru/ekotropa_tallyi/)",
            "photo": "https://avatars.mds.yandex.net/i?id=127c0c328f8acd32741adacad23f6c38_l-12323132-images-thumbs&n=13"
        },
        "Нарыштау": {
            "description": "Маршрут подойдет любителям несложных пеших прогулок. По всей тропе есть указатели, которые четко проведут до вершины. На смотровых площадках установлены скамейки. (Подробнее: https://dzen.ru/a/Y0vhgPZU1nV5b89C)",
        }
    },
    "Казань":{
        "Маршрут Лисы":{
            "description": "Маршрут спроектирован в виде познавательной прогулки-игры, в ходе которой пешеходов ждут семь контрольных точек-остановок — специальных локаций со стендами и полезной информацией о лесе.",
            "photo": "https://xcourse.me/images/showplaces/484/55674e061a45015a287e9d46598e2ab8.jpg"
        },
        "Обитатели озера Кабан": {
            "description": "На экологической тропе, проходящей по набережной озера Нижний Кабан в Казани, можно познакомиться с птицами, обитающими в водоеме. Протяженность маршрута составляет около 1,5 километра.",
        }
    },
    "Оренбург":{
        "Дыхание степи":{
            "description": "Экологическая тропа ведет посетителей к Центру реинтродукции лошади Пржевальского (тропу посетители проходят в составе группы в сопровождении рассказа экскурсовода - сотрудника заповедника).",
            "photo": "https://avatars.mds.yandex.net/i?id=02bf38b8a0ac8beadfab518990c5c54b_l-5220281-images-thumbs&n=13"
        },
        "Путь к Цапле": {
            "description": "На этой экотропе вы можете насладиться пением птиц, свежим воздухом, просторными пейзажами, увидеть степных пресмыкающихся и, возможно, сурков и околоводных и водных птиц ",
        }
    },
    "Челябинск":{
        "Тайны Озера":{
            "description": "Протяженность нового маршрута составляет 2,6 км, тропа ведет вдоль озера Зюраткуль от плотины к Каменному мысу и в обратном направлении.",
            "photo": "https://cdn.culture.ru/images/e82aad8c-5a97-507b-944b-3487cdba6166"
        },
        "Жукова Шишка": {
            "description": "Жукова шишка состоит из известняка и покрыта реликтовыми соснами, елями и пихтами. Живописна с любого ракурса и в любое время года. Протяженность тропы 1400 м. Подробнее: https://clck.ru/3LB9eB",
        },
        "Лесные сказки": {
            "description": "Маршрут проходит по существующей лесной тропе Челябинского городского бора и в увлекательной форме знакомит детей и подростков с его флорой и фауной. (Подробнее о других экотропах: https://ura.news/news/1052796747)",

        }
    },
    "Екатеринбург":{
        "Каменная Чаша":{
            "description": "Проходит вокруг скал около посёлка Палкино.",
            "photo": "https://avatars.mds.yandex.net/i?id=4855a983f46c838dfedacb739fbde104_l-10952687-images-thumbs&n=13"
        },
        "«Щелкунская экотропа»": {
            "description": "Маршрут проходит вдоль берега озера, пересекает старый Челябинский тракт, проходит мимо «Экодома» в селе Никольское.",
        },
        "Авроринская экотропа": {
            "description": "Протяжённость маршрута — 3,5 км. Тропа проходит по лесу среди кедров и елей, огибает Средний пруд против часовой стрелки, проходит по восточной окраине посёлка Уралец и возвращается в точке старта.",

        }
    },
    "Тюмень":{
        "Лукашино":{
            "description": "«Лукашино» находится у озера Полушинского на Ирбитском тракте в Тюменском районе. Она разделена на два маршрута: на 3,9 км и 4,7 км.",
            "photo": "https://www.sayanring.ru/static/images/tour/0443/tyumen.naberezhnaya.-most-vlyublennyx.jpg"
        },
        "В гостях у леса": {
            "description": "Лес смешанный, далеко от крупных городов. Так что воздух свежий. Много разной растительности, даже есть краснокнижные растения. (Подробнее: https://72.ru/text/ecology/2024/06/17/73704563/)",
        }
    },
    "Новосибирск":{
        "Берёзовские скалы":{
            "description": "Тропа начинается у высокой скалы, которая выходит к берегу реки Бердь. Протяженость маршрута около километра.",
            "photo": "https://cdn.culture.ru/images/9b01c3e6-9d6c-54b2-9898-d0cd2a6841ab"
        },
        "Бердские скалы": {
            "description": "К смотровой площадке проложена благоустроенная экотропа длиной 7 км: для туристов установлены указатели, информационные стенды о животном и растительном мире Бердских скал.",
        },
        "Таёжник": {
            "description": "Тропа представленна как кольцевой маршрут, на маршруте есть места отдыха, смотровые площадки и указатели. (Подробнее: https://welcome-novosibirsk.ru/articles/acts/ekotropy-novosibirska-i-oblasti/)",

        }
    },
    "Омск":{
        "Екатерининский бор":{
            "description": "Протяжённость тропы — 2 км. Она представляет собой кольцевой маршрут по живописным местам омского севера.",
            "photo": "https://s13.stc.yc.kpcdn.net/share/i/12/13195326/wr-960.webp"
        },
        "Озеро Ленёво": {
            "description": "Экологическая тропа вдоль оз. Ленево располагается на территории Муромцевского района протяжённостью около 3 км.",
        },
        "Озеро Эбейты": {
            "description": "Посетители могут узнать о озере, свойствах его воды и рапы, а также о семи легендах о происхождении водоёма. (Подробнее: https://omskzdes.ru/society/85349.html)",

        }
    },
    "Норильск":{
        "Красные камни":{
            "description": "Маршрут проходит вдоль дачного массива, подъемника горнолыжной трассы, вентиляционного ствола шахты, параллельно проселочной дороге в направлении реки Валек.",
            "photo": "https://avatars.mds.yandex.net/i?id=513cae48d1b8083f07c55c9f0f72564e_l-9233306-images-thumbs&n=13"
        }
    },
    "Благовещенск":{
        "Спортивный":{
            "description": "Кольцевой маршрут протяжённостью 3620 метров, карта тропы расположена у центрального входа спорткомплекса «Юность».",
            "photo": "https://avatars.mds.yandex.net/i?id=2df2fd08d7d2ef414829efdcc0dd56aa_l-5233303-images-thumbs&n=13"
        }
    },
    "Хабаровск":{
        "Путём Арсеньева":{
            "description": "Тропа проходит вдоль побережья Татарского пролива, начинается в хвойном лесу. Расстояние маршрута — 3,64 км.",
            "photo": "https://avatars.dzeninfra.ru/get-zen_doc/9736637/pub_6440e7aa09e9480c41a2cf5a_6443d2ae6da6c90a85b1e80b/scale_1200"
        }
    },
    "Владивосток":{
        "Волшебный лес":{
            "description": "На высоте 280 м. от уровня моря открывается шикарный вид на Уссурийский залив, бухту Маньчжур и мыс Вилково.",
            "photo": "https://avatars.mds.yandex.net/i?id=84d1e4300537e74430105147eb6d03a1_l-5288833-images-thumbs&n=13"
        },
        "Капище Перуна": {
            "description": "Капище Перуна — это место, где можно почувствовать дух древних славян и насладиться красотой природы.",
        },
        "Цветущие сады Вир": {
            "description": "На протяжении всего маршрута вас будет окружать сладкий запах цветов. Весной, когда расцветают все деревья, тропа становится особенно красивым местом для прогулки. (Подробнее: https://www.openstreetmap.org/way/842297136)",

        }
    },
    "Грозный":{
        "Вокруг моря":{
            "description": "Вокруг моря это 7.2 km (10 000 шагов) маршрут проходит вокруг Грознецкого моря, вы можете встретить множество разных птиц и увидеть красивые пейзажи",
            "photo": "https://avatars.mds.yandex.net/i?id=57c5d23aa4d025891c71ec3bbc5f1fab_l-5499599-images-thumbs&n=13"
        }
    },
    "Махачкала":{
        "Сарыкум бархан":{
            "description": "Тропа примечательно своей живописностью и обилием пустынной фауны. Встречаются эти животные, только в данной локации.",
            "photo": "https://avatars.dzeninfra.ru/get-zen_doc/1861837/pub_61e6a1fd2fca5f51d869c76c_61e869d6134195771cf7a9a1/scale_1200"
        },
        "Пещера Нохъю": {
            "description": "Пройдя самый длинный подвесной мост в Дагестане вы попадете в пещеры Нохъо.",
        }
    },
    "Владикавказ":{
        "Цейский ледник":{
            "description": "Цейский ледник — это удивительное место, которое поражает своей красотой и мощью. По пути следования экологической тропы можно встретить множество ручьёв, которые протекают прямо по лесу. (Подробнее: https://club-voshod.com/info/pohodnoe_info/dostoprimechatelnosti/severnaya_osetiya/ceyskiy_lednik/)",
            "photo": "https://avatars.mds.yandex.net/i?id=8f3a22e72c0562dfb44a7931bf409da6_l-5378240-images-thumbs&n=13"
        },
        "Экотропа к водопаду Шагацикондон": {
            "description": "Экотропа к водопаду Шагацикондон — это живописный маршрут, который проходит через горный лес и приводит к двум водопадам.",
        }
    }

}


city_coordinates = {
    'Москва': (55.7522, 37.6156),
    'Тула': (54.1961, 37.6182),
    'Рязань': (54.6269, 39.6916),
    'Владимир':(56.1366, 40.3966),
    'Воронеж':(51.672, 39.1843),
    'Ярославль':(57.6299, 39.8737),
    'Санкт-Петербург': (59.9386, 30.3141),
    'Калининград': (54.7065, 20.511),
    'Архангельск': (64.5401, 40.5433),
    'Астрахань': (46.3497, 48.0408),
    'Ростов-на-Дону': (47.2313, 39.7233),
    'Сочи': (43.5992, 39.7257),
    'Уфа': (54.7431, 55.9678),
    'Казань': (55.7887, 49.1221),
    'Оренбург': (51.7727, 55.0988),
    'Челябинск': (66.53, 66.6019),
    'Екатеринбург': (56.8519, 60.6122),
    'Тюмень': (57.1522, 65.5272),
    'Новосибирск': (55.0415, 82.9346),
    'Омск': (54.9924, 73.3686),
    'Норильск': (69.3535, 88.2027),
    'Благовещенск': (50.2796, 127.54),
    'Хабаровск': (48.4827, 135.084),
    'Владивосток': (43.1056, 131.874),
    'Грозный': (43.312, 45.6889),
    'Махачкала': (42.9764, 47.5024),
    'Владикавказ': (43.0367, 44.6678)
    }
city_trails = {
    "Москва": {
        "У истоков рек": (55.641402, 37.486701),
        "Долина реки Битцы": (55.584208, 37.546483),
        "Кузьминки-Люблино": (55.685969, 37.810547),
        "В гармонии с природой": (55.780678, 37.436257)
    },
    "Санкт-Петербург": {
        "Сестрорецкое болото": (60.123434, 30.002491),
        "Комаровский берег": (60.180116, 29.798947),
        "Линдуловская роща": (60.249524, 29.575095),
        "Дудергофские высоты": (59.7024, 30.1199)
    },
    "Тула": {
        "Малиновая засека": (54.111294, 37.520373)
    },
    "Рязань": {
        "Тропа Паустовского": (54.792426, 39.835495)
    },
    "Владимир": {
        "Боголюбовский луг":  (56.19517, 40.54076),
        "Тропа Дружбы": (56.105360, 40.311530),
        "Дюкинские карьеры": (56.007906, 41.064872)
    },
    "Воронеж": {
        "Заповедная Сказка": (51.875606, 39.652246),
        "Черепахинская": (51.875572, 39.653044)
    },
    "Архангельск": {
        "К Сийским озёрам": (63.570667, 41.654194),
        "Мудьюг": (64.852167, 40.289639),
        "По следам Грина": (64.797389, 43.340417)
    },
    "Калининград": {
        "Высота Эфа": (55.222255, 20.891544),
        "Танцующий лес": (55.18266, 20.85949),
        "Сказки Куршской косы": (55.02017, 20.62236)
    },
    "Астрахань": {
        "Обретенная дельта": (46.311334 , 48.014001)
    },
    "Ростов-на-Дону": {
        "Щепкинский лес": (47.339900, 39.736919),
        "Тайны дельты Дона": (47.183275, 39.337785)
    },
    "Сочи": {
        "Тропа здоровья": (43.632117, 40.316111),
        "Реликтовый лес": (43.65888, 40.2509)
    },
    "Уфа": {
        "Таллы": (53.0390, 56.4209),
        "Нарыштау": (54.495835, 53.462941)
    },
    "Казань": {
        "Маршрут Лисы": (55.820718, 49.042095),
        "Обитатели озера Кабан":(55.775889, 49.126267)
    },
     "Оренбург": {
        "Дыхание степи": (51.195697, 56.192556),
        "Путь к Цапле": (51.150231, 56.094853)
    },
     "Челябинск": {
        "Лесные сказки": (54.974089, 57.678620),
        "Тайны Озера": (54.916625, 59.227319),
        "Жукова Шишка": (54.974089, 57.678620)
    },
     "Екатеринбург": {
        "Авроринская экотропа": (57.66356, 59.67698),
        "Каменная Чаша": (56.866547, 60.378334),
        "Щелкунская": (56.283316, 60.940922)
    },
     "Тюмень": {
        "Лукашино": (57.315070, 65.009125),
        "В гостях у леса": (56.985499, 63.731113),
    },
     "Новосибирск": {
        "Таёжник": (54.553282, 84.053825),
        "Бердские скалы": (54.620984, 83.984150)
    },
     "Омск": {
        "Екатерининский бор": (56.885293, 74.601715),
        "Озеро Ленёво": (56.40465, 75.62037),
        "Озеро Эбейты": (54.644530, 71.738300)
    },
     "Норильск": {
        "Красные камни": (69.480384, 88.531666)
    },
     "Благовещенск": {
        "Спортивный": (50.249549, 127.566993)
    },
     "Хабаровск": {
        "Путём Арсеньева": (48.935391, 140.348181)
    },
    "Владивосток": {
        "Волшебнфй лес": (43.230213, 132.220117),
        "Капище Перуна": (43.07792, 131.91018),
        "Сады Вир": (43.243436463895,132.06346392632)

    },
    "Грозный": {
        "Вокруг моря": (43.260274, 45.673225)
    },
    "Махачкала": {
        "Сарыкум бархан": (43.00302, 47.238025),
        "Пещера Нохъю": (43.064364, 46.829543)
    },
    "Владикавказ": {
        "Цейский ледник": (42.775086, 43.860499),
        "К водопаду Шагацикондон": (42.793357, 43.922480),
    },






}


# Функция для создания карты
def create_map(city_name):
    # Получаем координаты экотроп для выбранного города
    trails = city_trails.get(city_name, {})

    # Если экотропы есть, берем координаты первого для центра карты
    if trails:
        first_trail_coords = list(trails.values())[0]
        center_lat, center_lon = first_trail_coords
    else:
        center_lat, center_lon = 0, 0  # Если нет экотроп, центрируем на нуле

    zoom_level = 10
    # Создаем карту
    m = folium.Map(location=[center_lat, center_lon], zoom_start=zoom_level)

    # Добавление маркеров для каждой экотропы
    for trail_name, coords in trails.items():
        folium.Marker(
            location=coords,
            popup=trail_name,
            tooltip='Нажмите для подробностей'
        ).add_to(m)

    # Сохранение карты в HTML-файл
    m.save('map.html')

# Функция для отправки карты
def send_map(chat_id, city_name):
    create_map(city_name)  # Создаем карту для выбранного города
    with open("map.html", "rb") as map_file:
        bot.send_document(chat_id, map_file)

user_states = {}
user_routes = {}
user_start_city = {}
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Что ты умеешь?")
    btn2 = types.KeyboardButton("Мой маршрут 🗺️")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, text="Привет, {0.first_name}! Это бот для составления маршрутов по экотропам  России. У меня широкий выбор экологических троп во многих городах нашей страны! Надеюсь, тебе понравится!🦋".format(message.from_user), reply_markup=markup)

@bot.message_handler(content_types=['text'])
def handle_text_messages(message):
    if message.text == "Что ты умеешь?":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        b1 = types.KeyboardButton("Ответить на вопросы 💡")
        back = types.KeyboardButton("Вернуться в главное меню ↩")
        markup.add(b1, back)
        bot.send_message(message.chat.id, text="Я могу предложить тебе варианты экотроп в различных городах России.🧸 Позволь мне задать тебе пару вопросов для уточнения твоих предпочтений", reply_markup=markup)

    elif message.text == "Ответить на вопросы 💡":
        show_regions(message.chat.id)

    elif message.text == "Вернуться в главное меню ↩":
        start(message)

    elif message.text == "Мой маршрут 🗺️":
        ask_departure_city(message)  # Запрашиваем город отправления

    elif message.text in city_trails.keys():  # Проверяем, является ли введенный текст названием города
        send_map(message.chat.id, message.text)  # Отправляем карту для выбранного города

    elif message.text == "Очистить маршрут ❌":
        clear_user_route(message)
def ask_departure_city(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, 'Пожалуйста, введите город отправления:')
    bot.register_next_step_handler(msg, process_departure_city)

# Обработка ответа с городом отправления
def process_departure_city(message):
    departure_city = message.text.strip()
    chat_id = message.chat.id

    if departure_city in city_coordinates:
        if chat_id not in user_routes:
            user_routes[chat_id] = []

        if departure_city in user_routes[chat_id]:
            # Если город уже в маршруте, перемещаем его в начало
            user_routes[chat_id].remove(departure_city)
            user_routes[chat_id].insert(0, departure_city)  # Перемещаем в начало
            bot.send_message(chat_id, f'Город отправления "{departure_city}" уже добавлен в маршрут и был перемещен в начало.')
        else:
            # Добавляем город отправления в маршрут пользователя
            user_start_city[chat_id] = departure_city
            user_routes[chat_id].insert(0, departure_city)
            bot.send_message(chat_id, f'Город отправления "{departure_city}" успешно добавлен.')
        show_user_route_menu(chat_id)
    else:
        bot.send_message(chat_id, 'Не удалось распознать город.')
        msg = bot.send_message(chat_id, 'Пожалуйста, попробуйте снова.')
        bot.register_next_step_handler(msg, process_departure_city)

def send_long_message(chat_id, message):
    max_length = 4096  # Максимальная длина сообщения в Telegram
    # Разбиваем сообщение на части
    for i in range(0, len(message), max_length):
        bot.send_message(chat_id, message[i:i + max_length])

def calculate_distance(trail1, trail2):
    coords_1 = city_trails[trail1[0]][trail1[1]]
    coords_2 = city_trails[trail2[0]][trail2[1]]
    return great_circle(coords_1, coords_2).kilometers

def find_optimal_route(trails):
    if len(trails) == 2:
        return trails, calculate_distance(trails[0], trails[1])

    start_trail = trails[0]
    other_trails = trails[1:]

    min_distance = float('inf')
    optimal_route = []

    for perm in permutations(other_trails):
        current_route = [start_trail] + list(perm)
        distance = sum(calculate_distance(current_route[i], current_route[i + 1]) for i in range(len(current_route) - 1))

        if distance < min_distance:
            min_distance = distance
            optimal_route = current_route

    return optimal_route, min_distance

def generate_yandex_maps_link(trails):
    coordinates_str = "~".join(f"{city_trails[trail[0]][trail[1]][0]},{city_trails[trail[0]][trail[1]][1]}" for trail in trails)
    return f"https://yandex.ru/maps/?rtext={coordinates_str}"

def show_user_route_menu(chat_id):
    if chat_id not in user_routes:
        user_routes[chat_id] = []
    starting_city = user_start_city.get(chat_id)
    # Проверяем наличие города отправления и других городов в маршруте
    if starting_city or user_routes[chat_id]:  # Если есть город отправления или другие города
        trails = []

        if starting_city and starting_city in city_trails:
            trails += [(starting_city, trail) for trail in city_trails[starting_city]]

        for city in user_routes[chat_id]:
            if city != starting_city and city in city_trails:
                trails += [(city, trail) for trail in city_trails[city]]

        optimal_route, total_distance = find_optimal_route(trails)

        route_str = ""
        for i in range(len(optimal_route) - 1):
            trail1 = optimal_route[i]
            trail2 = optimal_route[i + 1]
            distance = calculate_distance(trail1, trail2)
            route_str += f"{trail1[0]} - {trail1[1]} → {trail2[0]} - {trail2[1]}: {distance:.2f} км\n"

        if len(optimal_route) > 0:
            last_trail = optimal_route[-1]
            route_str += f"{last_trail[0]} - {last_trail[1]}"

        yandex_link = generate_yandex_maps_link(optimal_route)
        full_message = (f"Ваш оптимальный маршрут:🤗 \n{route_str}\n"
                        f"Общая дистанция: {total_distance:.2f} км 🌐\n"
                        f"Ссылка на маршрут: {yandex_link}")

        send_long_message(chat_id, full_message)
    else:
        bot.send_message(chat_id, "Ваш маршрут пуст.")

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for city in user_routes[chat_id]:
        markup.add(types.KeyboardButton(f"Удалить {city}"))
    markup.add(types.KeyboardButton("Очистить маршрут ❌"), types.KeyboardButton("Вернуться в главное меню ↩"))
    bot.send_message(chat_id, "Выберите действие:", reply_markup=markup)


def generate_yandex_maps_link(trails):
    coordinates_str = "~".join(f"{city_trails[trail[0]][trail[1]][0]},{city_trails[trail[0]][trail[1]][1]}" for trail in trails)
    return f"https://yandex.ru/maps/?rtext={coordinates_str}"

def clear_user_route(message):
    chat_id = message.chat.id
    print(f"Запрос на очистку маршрута от {chat_id}")
    user_routes[chat_id] = []  # Очищаем маршрут
    bot.send_message(chat_id, "Ваш маршрут очищен.")

@bot.message_handler(func=lambda message: message.chat.id in user_start_city)
def handle_text_messages_with_start_city(message):
    process_city_addition(message)

def process_city_addition(message):
    chat_id = message.chat.id
    selected_city = message.text
    if selected_city in city_coordinates and selected_city not in user_routes[chat_id]:
        user_routes[chat_id].append(selected_city)  # Добавляем выбранный город в маршрут
        bot.send_message(chat_id, f"{selected_city} добавлен в ваш маршрут.")

        # Если у пользователя уже есть города в маршруте, можно сразу показать оптимальный маршрут
        if len(user_routes[chat_id]) > 0:
            optimal_route, total_distance = find_optimal_route([user_start_city[chat_id]] + user_routes[chat_id])
            yandex_link = generate_yandex_maps_link(optimal_route)
            bot.send_message(chat_id, f"Ваш оптимальный маршрут: {optimal_route}\nОбщая дистанция: {total_distance:.2f} км 🌐\nСсылка на маршрут: {yandex_link}")

    else:
        bot.send_message(chat_id, "Этот город уже добавлен или не доступен.")


#Функция удаления города из маршрута
def delete_city_from_route(message):
    chat_id = message.chat.id
    city_to_delete = next((city for city in user_routes[chat_id] if city in message.text), None)

    if city_to_delete:
        user_routes[chat_id].remove(city_to_delete)
        new_route = "\n".join(user_routes[chat_id])
        bot.send_message(chat_id, f"Город {city_to_delete} был удалён из Вашего маршрута.\nНовый маршрут:\n{new_route}" if new_route else "Теперь Ваш маршрут пуст.")

    show_user_route_menu(chat_id)

def show_regions(chat_id):
    markup = types.InlineKeyboardMarkup()
    buttons = [
        types.InlineKeyboardButton("Центральный", callback_data='central'),
        types.InlineKeyboardButton("Северо-западный", callback_data='northwest'),
        types.InlineKeyboardButton("Южный", callback_data='south'),
        types.InlineKeyboardButton("Приволжский", callback_data='volga'),
        types.InlineKeyboardButton("Уральский", callback_data='ural'),
        types.InlineKeyboardButton("Сибирский", callback_data='sibirsk'),
        types.InlineKeyboardButton("Дальневосточный", callback_data='daln'),
        types.InlineKeyboardButton("Северо-кавказский", callback_data='kavkaz')
    ]
    markup.add(*buttons)
    bot.send_message(chat_id, "Какие округа России вы рассматриваете для своего путешествия?", reply_markup=markup)

#Функция отображения регионов России
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    user_id = call.from_user.id
    if call.data in ['central', 'northwest', 'south', 'volga', 'ural', 'sibirsk', 'daln', 'kavkaz']:
        cities, photos = get_region_info(call.data)
        # Сохранение данных в состояние пользователя
        user_states[user_id] = {
            'page': 1,
            'cities': cities,
            'photos': photos,
            'count': len(cities)
        }
        send_city_info(call.message.chat.id, call.message.message_id, user_states[user_id]['page'])

    elif call.data.startswith("view_attractions_"):
        city_name = call.data.split("_")[-1]
        show_attractions(call.message.chat.id, city_name)

    #Добавить в маршрут
    elif call.data.startswith("add_to_route_"):
        city_name = call.data.split("_")[-1]
        add_to_route(user_id, city_name)
        bot.answer_callback_query(call.id, f"Город {city_name} добавлен в ваш маршрут. ☺")

    #Предыдущая и следующая страница
    elif call.data == 'back-page':
        if user_id in user_states and user_states[user_id]['page'] > 1:
            user_states[user_id]['page'] -= 1
            send_city_info(call.message.chat.id, call.message.message_id, user_states[user_id]['page'])
    elif call.data == 'next-page':
        if user_id in user_states and user_states[user_id]['page'] < user_states[user_id]['count']:
            user_states[user_id]['page'] += 1
            send_city_info(call.message.chat.id, call.message.message_id, user_states[user_id]['page'])

#Показать достопримечательности новым сообщением
def show_attractions(chat_id, city_name):
    if city_name in attractions:
        if chat_id not in user_states:
            user_states[chat_id] = {}

        attraction_list = attractions[city_name]
        message = f"Экотропы в городе {city_name}:\n"

        for attraction, details in attraction_list.items():
            message += f"- {attraction}: {details['description']}\n"

        first_photo = list(attraction_list.values())[0]['photo']

        # Отправляем сообщение с достопримечательностями
        bot.send_photo(chat_id, first_photo, caption=message)
    else:
        bot.send_message(chat_id, "Нет экологических троп для этого города. 🤷‍♀️")
#Добавить в маршрут
def add_to_route(user_id, city_name):
    if user_id not in user_routes:
        user_routes[user_id] = []
    if city_name not in user_routes[user_id]:
        user_routes[user_id].append(city_name)



@bot.callback_query_handler(func=lambda call: call.data.startswith("attraction_"))
def handle_attraction_navigation(call):
    chat_id = call.from_user.id
    city_name = call.data.split("_")[2]

    if call.data.startswith("attraction_next"):
        if user_states[chat_id]['attraction_page'] < user_states[chat_id]['attraction_count']:
            user_states[chat_id]['attraction_page'] += 1
    elif call.data.startswith("attraction_back"):
        if user_states[chat_id]['attraction_page'] > 1:
            user_states[chat_id]['attraction_page'] -= 1


#Информация о регионах с фото
def get_region_info(region_code):
    regions = {
        'central': (["Москва", "Тула", "Рязань", "Владимир", "Воронеж",  "Ярославль"], ["https://avatars.dzeninfra.ru/get-zen_doc/9860299/pub_64afd857fce6ed467aaf0046_64afd8a5eaf1e9161ef9a56b/scale_1200",\
            "https://avatars.mds.yandex.net/i?id=4e6a32c409c1df287b83768f1ee452ad_l-4571838-images-thumbs&n=13",\
            "https://avatars.mds.yandex.net/i?id=f4de9998f5304629e13ccc73e7c14e9c_l-5234673-images-thumbs&n=13", \
            "https://avatars.mds.yandex.net/get-ydo/1384592/2a00000181d510092edbcd19d6f645adcf83/diploma",\
            "https://avatars.mds.yandex.net/get-ydo/880658/2a00000167e64b112f2be35d1731b02e9a2c/diploma",\
            "https://cdn.culture.ru/images/274652a7-06e0-5d4f-bee9-6f96c1dec58a",\
            "https://avatars.mds.yandex.net/i?id=cef1e610ef85d0f24465bdeb15c673f9_l-4599018-images-thumbs&n=13",
            "https://cdn.culture.ru/images/9cbea0f8-ef0c-5afe-b108-5ad2d9007737",\
            "https://cdn.culture.ru/images/fd82b080-ff7b-52b4-9298-c4613e02c86b"]),

        'northwest': (["Санкт-Петербург", "Калининград", "Архангельск"], ["https://rus163m5.ru/wp-content/uploads/2023/10/sankt-peterburg.jpg",\
                                                           "https://www.travelleo.ru/wp-content/uploads/2023/03/snyat-kvartiru-v-kaliningrade-posutochno.jpg",\
                                                            "https://avatars.mds.yandex.net/i?id=b88417923d781dce55443e662a8f41d362c879f3542afae6-3593759-images-thumbs&n=13"]),

        'south': (["Астрахань", "Ростов-на-Дону", "Сочи"], ["https://avatars.mds.yandex.net/i?id=4912a5f3e914743715fd0a3645c74ae276a5df1d-9872761-images-thumbs&n=13",\
                                               "https://avatars.mds.yandex.net/i?id=80973c6e6c5182cb14091d0bb75f91ffe7bafc94-4538204-images-thumbs&n=13",\
                                                "https://avatars.mds.yandex.net/i?id=3a6a87859d6a1ca4d23e11fb6f70f11792a29136-9830843-images-thumbs&n=13"]),

        'volga': (["Уфа", "Казань", "Оренбург"], ["https://avatars.mds.yandex.net/i?id=05d8ba91d09106e94f7c78fb74838796_l-5243975-images-thumbs&n=13",\
             "https://avatars.mds.yandex.net/i?id=e5e9db54429bf7dbd8061524bfb34f25a0b6bf16-5233821-images-thumbs&n=13",\
                "https://avatars.mds.yandex.net/i?id=4732a185efd5aca8c0b8418c836cd7afb37a7536fe295ed5-11532301-images-thumbs&n=13"]),

        'ural': (["Челябинск", "Екатеринбург", "Тюмень"], ["https://avatars.mds.yandex.net/i?id=2fb145abe46f77d38b605af7f6b565c279563858-4432686-images-thumbs&n=13",\
             "https://avatars.mds.yandex.net/i?id=d4978742fbdd4097efd8135dc5cdfd04df9447c4-9100075-images-thumbs&n=13", \
                "https://avatars.mds.yandex.net/i?id=5ceb1c3ce85f320994c97339e4b56a549352d42a-9744150-images-thumbs&n=13"]),

        'sibirsk': (["Новосибирск", "Омск", "Норильск"], ["https://avatars.mds.yandex.net/i?id=c3dfdb8a411a2d4b116a84f0c6fbe2bfba5737b4-10930046-images-thumbs&n=13",\
             "https://avatars.mds.yandex.net/i?id=6af222d7aedf939fc4c4610499648d094d7b1873-11449045-images-thumbs&n=13",\
                "https://sdelanounas.ru/i/a/w/1/f_aW1nLmdlbGlvcGhvdG8uY29tL25vcmlsc2svMzBfbm9yaWxzay5qcGc_X19pZD0xNDU4MDU=.jpeg"]),

        'daln': (["Благовещенск", "Хабаровск", "Владивосток"], ["https://avatars.mds.yandex.net/i?id=3ecfbdae04677c9f2e9364f2cc3f03b0c2a6ba49-10132791-images-thumbs&n=13", \
            "https://i.vuzopedia.ru/storage/app/uploads/public/662/3a8/3a4/6623a83a46f28936474700.jpg", \
                "https://avatars.mds.yandex.net/i?id=40e2c816f9ace9c6e522fc28638dc3e7_l-9068341-images-thumbs&n=13"]),

        'kavkaz': (["Грозный", "Махачкала", "Владикавказ"], ["https://cdn.culture.ru/images/bb8ad0c6-5810-52d6-b686-13f1487cb7cb",\
             "https://avatars.mds.yandex.net/i?id=573e21324cdfdd4e9f1f69f770cf3bda84356a87-2955839-images-thumbs&n=13", \
                "https://avatars.mds.yandex.net/i?id=9b64adef9bee4c321b075ea10f48d9feda068114-7757111-images-thumbs&n=13"])
    }
    return regions.get(region_code, ([], []))


def send_city_info(chat_id, mes_id, page):
    user_id = chat_id
    cities = user_states[user_id].get('cities', [])
    photos = user_states[user_id].get('photos', [])
    count = len(cities)

    if count == 0:
        bot.send_message(chat_id, "Нет доступных городов. 🤷‍♀️")
        return

    city_index = page - 1
    if city_index < 0 or city_index >= len(cities):
        bot.send_message(chat_id, "Некорректный индекс города. 🤷‍♂️")
        return

    city_info = f"Город: {cities[city_index]}"

    # Проверка на наличие фотографий
    if city_index < len(photos):
        photo = photos[city_index]
    else:
        bot.send_message(chat_id, "Нет доступных фотографий для данного города. 🤷‍♂️")
        return

    markup = types.InlineKeyboardMarkup()
    view_button = types.InlineKeyboardButton("Рассмотреть варианты экотроп 👀", callback_data=f"view_attractions_{cities[city_index]}")
    markup.add(view_button)
    add_to_route_button = types.InlineKeyboardButton("Добавить в маршрут 🏞", callback_data=f"add_to_route_{cities[city_index]}")
    markup.add(add_to_route_button)
    nav_buttons = [
        types.InlineKeyboardButton(text='<-- Назад', callback_data='back-page'),
        types.InlineKeyboardButton(text=f'{page}/{count}', callback_data=' '),
        types.InlineKeyboardButton(text='Вперёд -->', callback_data='next-page')
    ]
    markup.add(*nav_buttons)

    if page == 1:
        bot.send_photo(chat_id, photo, caption=city_info, reply_markup=markup)
    else:
        bot.edit_message_media(types.InputMediaPhoto(photo), chat_id, mes_id)
        bot.edit_message_caption(city_info, chat_id, mes_id, reply_markup=markup)
# Запуск бота
bot.polling(none_stop=True)