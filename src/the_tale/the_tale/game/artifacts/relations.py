
from rels import Column
from rels.django import DjangoEnum

from tt_logic.artifacts.relations import WEAPON_TYPE

from the_tale.game.balance import constants as c
from the_tale.game.balance.power import PowerDistribution

from the_tale.linguistics.lexicon.dictionary import noun


class INDEX_ORDER_TYPE(DjangoEnum):
    records = (('BY_LEVEL', 'by_level', 'по уровню'),
               ('BY_NAME', 'by_name', 'по имени'))


class ARTIFACT_TYPE(DjangoEnum):

    records = (('USELESS', 0, 'хлам'),
               ('MAIN_HAND', 1, 'основная рука'),
               ('OFF_HAND', 2, 'вторая рука'),
               ('PLATE', 3, 'доспех'),
               ('AMULET', 4, 'амулет'),
               ('HELMET', 5, 'шлем'),
               ('CLOAK', 6, 'плащ'),
               ('SHOULDERS', 7, 'наплечники'),
               ('GLOVES', 8, 'перчатки'),
               ('PANTS', 9, 'штаны'),
               ('BOOTS', 10, 'обувь'),
               ('RING', 11, 'кольцо'))


class ARTIFACT_POWER_TYPE(DjangoEnum):
    distribution = Column()

    records = (('MOST_MAGICAL', 0, 'магическая', PowerDistribution(0.1, 0.9)),
               ('MAGICAL', 1, 'ближе к магии', PowerDistribution(0.25, 0.75)),
               ('NEUTRAL', 2, 'равновесие', PowerDistribution(0.5, 0.5)),
               ('PHYSICAL', 3, 'ближе к физике', PowerDistribution(0.75, 0.25)),
               ('MOST_PHYSICAL', 4, 'физическая', PowerDistribution(0.9, 0.1)))


class ARTIFACT_RECORD_STATE(DjangoEnum):
    records = (('ENABLED', 0, 'в игре'),
               ('DISABLED', 1, 'вне игры'))


class RARITY(DjangoEnum):
    probability = Column()
    max_integrity = Column()
    preference_rating = Column()
    cost = Column()

    records = (('NORMAL', 0, 'обычный артефакт', c.NORMAL_ARTIFACT_PROBABILITY, c.ARTIFACT_MAX_INTEGRITY, 1.0, 1.0),
               ('RARE', 1, 'редкий артефакт', c.RARE_ARTIFACT_PROBABILITY, int(c.ARTIFACT_MAX_INTEGRITY*c.ARTIFACT_RARE_MAX_INTEGRITY_MULTIPLIER), 1.5, 3.0),
               ('EPIC', 2, 'эпический артефакт', c.EPIC_ARTIFACT_PROBABILITY, int(c.ARTIFACT_MAX_INTEGRITY*c.ARTIFACT_EPIC_MAX_INTEGRITY_MULTIPLIER), 2.0, 9.0))


class ARTIFACT_EFFECT(DjangoEnum):

    records = (('PHYSICAL_DAMAGE', 0, 'мощь'),
               ('MAGICAL_DAMAGE', 1, 'колдовство'),
               ('INITIATIVE', 2, 'хорошая реакция'),
               ('HEALTH', 3, 'здоровье'),
               ('EXPERIENCE', 4, 'повышение интуиции'),
               ('POWER', 5, 'хитрость'),
               ('CONCENTRATION', 6, 'концентрация'),
               ('SPEED', 7, 'скороход'),
               ('BAG', 8, 'карманы'),

               ('NO_EFFECT', 666, 'нет эффекта'),

               ('GREAT_PHYSICAL_DAMAGE', 1000, 'небывалая мощь'),
               ('GREAT_MAGICAL_DAMAGE', 1001, 'могучее колдовство'),
               ('GREAT_INITIATIVE', 1002, 'превосходная реакция'),
               ('GREAT_HEALTH', 1003, 'невероятное здоровье'),
               ('GREAT_EXPERIENCE', 1004, 'сверхинтуиция'),
               ('GREAT_POWER', 1005, 'особая хитрость'),
               # ('GREAT_ENERGY', 1006, 'большой астральный сосуд'),
               ('GREAT_SPEED', 1007, 'неутомимый скороход'),
               ('GREAT_BAG', 1008, 'большие карманы'),
               ('REST_LENGTH', 1009, 'выносливость'),
               ('RESURRECT_LENGTH', 1010, 'живучесть'),
               ('IDLE_LENGTH', 1011, 'деятельность'),
               ('CONVICTION', 1012, 'убеждение'),
               ('CHARM', 1013, 'очарование'),
               # ('SPIRITUAL_CONNECTION', 1014, 'духовная связь'),
               ('PEACE_OF_MIND', 1015, 'душевное равновесие'),
               ('SPECIAL_AURA', 1016, 'особая аура'),
               ('REGENERATION', 1017, 'регенерация'),
               ('LAST_CHANCE', 1018, 'последний шанс'),
               ('ICE', 1019, 'лёд'),
               ('FLAME', 1020, 'пламя'),
               ('POISON', 1021, 'яд'),
               ('VAMPIRE_STRIKE', 1022, 'вампиризм'),
               ('ESPRIT', 1023, 'живость ума'),
               ('TERRIBLE_VIEW', 1024, 'ужасный вид'),
               ('CRITICAL_HIT', 1025, 'точные атаки'),
               ('ASTRAL_BARRIER', 1026, 'астральная преграда'),
               ('CLOUDED_MIND', 1027, 'затуманенный разум'),
               ('LUCK_OF_STRANGER', 1028, 'удача странника'),
               ('LUCK_OF_HERO', 1029, 'удача героя'),
               ('FORTITUDE', 1030, 'крепость духа'),
               ('IDEOLOGICAL', 1031, 'идейность'),
               ('UNBREAKABLE', 1032, 'нерушимость'),
               ('SPEEDUP', 1033, 'ускорение'),
               ('RECKLESSNESS', 1034, 'безрассудность'),
               ('CHILD_GIFT', 100001, 'детский подарок'))


# TODO: use real artifacts instead thar enum
class STANDARD_WEAPON(DjangoEnum):
    weapon_type = Column(unique=False, no_index=True)
    utg_name = Column(no_index=True)

    records = (('WEAPON_0', 0, 'булава', WEAPON_TYPE.TYPE_1, noun(['булава', 'булавы', 'булаве', 'булаву', 'булавой', 'булаве',
                                                                   'булавы', 'булав', 'булавам', 'булавы', 'булавами', 'булавах'], 'но,жр')),
               ('WEAPON_1', 1, 'дубина', WEAPON_TYPE.TYPE_2, noun(['дубина', 'дубины', 'дубине', 'дубины', 'дубинами', 'дубинах',
                                                                   'дубины', 'дубин', 'дубинам', 'дубины', 'дубинами', 'дубинах'], 'но,жр')),
               ('WEAPON_2', 2, 'жало на хвосте', WEAPON_TYPE.TYPE_29, noun(['жало', 'жала', 'жалу', 'жало', 'жалом', 'жале',
                                                                            'жалы', 'жал', 'жалам', 'жалы', 'жалами', 'жалах'], 'но,жр')),
               ('WEAPON_3', 3, 'жвалы', WEAPON_TYPE.TYPE_14, noun(['', '', '', '', '', '',
                                                                   'жвалы', 'жвал', 'жвалам', 'жвалы', 'жвалами', 'жвалах'], 'мн,но,жр')),
               ('WEAPON_4', 4, 'касание энергетическое', WEAPON_TYPE.TYPE_30, noun(['касание', 'касания', 'касанию', 'касание', 'касанием', 'касаниях',
                                                                                    'касания', 'касаний', 'касаниям', 'касания', 'касаниями', 'касаниях'], 'но,жр')),
               ('WEAPON_5', 5, 'катар', WEAPON_TYPE.TYPE_3, noun(['катар', 'катара', 'катару', 'катар', 'катаром', 'катаре',
                                                                  'катары', 'катаров', 'катарам', 'катары', 'катарами', 'катарах'], 'но,мр')),
               ('WEAPON_6', 6, 'кинжал', WEAPON_TYPE.TYPE_4, noun(['кинжал', 'кинжала', 'кинжалу', 'кинжал', 'кинжалом', 'кинжале',
                                                                   'кинжалы', 'кинжалов', 'кинжалам', 'кинжалы', 'кинжалами', 'кинжалах'], 'но,мр')),
               ('WEAPON_7', 7, 'кистень', WEAPON_TYPE.TYPE_5, noun(['кистень', 'кистеня', 'кистеню', 'кистень', 'кистенем', 'кистене',
                                                                    'кистени', 'кистеней', 'кистеням', 'кистени', 'кистенями', 'кистенями'], 'но,мр')),
               ('WEAPON_8', 8, 'клешня', WEAPON_TYPE.TYPE_15, noun(['клешня', 'клешни', 'клешне', 'клешню', 'клешнёй', 'клешне',
                                                                    'клешни', 'клешней', 'клешням', 'клешни', 'клешнями', 'клешнях'], 'но,жр')),
               ('WEAPON_9', 9, 'клыки', WEAPON_TYPE.TYPE_16, noun(['', '', '', '', '', '',
                                                                   'клыки', 'клыков', 'клыкам', 'клаки', 'клыками', 'клыках'], 'мн,но,мр')),
               ('WEAPON_10', 10, 'клюв', WEAPON_TYPE.TYPE_17, noun(['клюв', 'клюва', 'клюву', 'клюв', 'клювом', 'клюве',
                                                                    'клювы', 'клювов', 'клювам', 'клювы', 'клювами', 'клювах'], 'но,мр')),
               ('WEAPON_11', 11, 'когти', WEAPON_TYPE.TYPE_18, noun(['', '', '', '', '', '',
                                                                     'когти', 'когтей', 'когтям', 'когти', 'когнтями', 'когтях'], 'мн,но,мр')),
               ('WEAPON_12', 12, 'копьё', WEAPON_TYPE.TYPE_6, noun(['копьё', 'копья', 'копью', 'копьё', 'копьём', 'копье',
                                                                    'копья', 'копий', 'копьям', 'копья', 'копьями', 'копьях'], 'но,ср')),
               ('WEAPON_13', 13, 'кулак', WEAPON_TYPE.TYPE_19, noun(['кулак', 'кулака', 'кулаку', 'кулак', 'кулаком', 'кулаке',
                                                                     'кулаки', 'кулаков', 'кулакам', 'кулаки', 'кулаками', 'кулаках'], 'но,мр')),
               ('WEAPON_14', 14, 'меч', WEAPON_TYPE.TYPE_7, noun(['меч', 'меча', 'мечу', 'меч', 'мечём', 'мечу',
                                                                  'мечи', 'мечей', 'мечам', 'мечи', 'мечами', 'мечах'], 'но,мр')),
               ('WEAPON_15', 15, 'нож', WEAPON_TYPE.TYPE_8, noun(['нож', 'ножа', 'ножу', 'нож', 'ножом', 'ноже',
                                                                  'ножи', 'ножей', 'ножам', 'ножи', 'ножами', 'ножах'], 'но,мр')),
               ('WEAPON_16', 16, 'палка', WEAPON_TYPE.TYPE_20, noun(['палка', 'палки', 'палке', 'палку', 'палкой', 'палке',
                                                                     'палки', 'палок', 'палкам', 'палки', 'палками', 'палках'], 'но,жр')),
               ('WEAPON_17', 17, 'пика', WEAPON_TYPE.TYPE_6, noun(['пика', 'пики', 'пике', 'пику', 'пикой', 'пике',
                                                                   'пики', 'пик', 'пикам', 'пики', 'пиками', 'пиках'], 'но,жр')),
               ('WEAPON_18', 18, 'плеть', WEAPON_TYPE.TYPE_9, noun(['плеть', 'плети', 'плети', 'плеть', 'плетью', 'плетье',
                                                                    'плети', 'плетей', 'плетям', 'плети', 'плетями', 'плетях'], 'но,жр')),
               ('WEAPON_19', 19, 'посох', WEAPON_TYPE.TYPE_10, noun(['посох', 'посоха', 'посоху', 'посох', 'посохом', 'посохе',
                                                                     'посохи', 'посохов', 'посохам', 'посохи', 'посохами', 'посохах'], 'но,мр')),
               ('WEAPON_20', 20, 'рог', WEAPON_TYPE.TYPE_21, noun(['рог', 'рога', 'рогу', 'рог', 'рогом', 'роге',
                                                                   '', '', '', '', '', ''], 'ед,но,мр')),
               ('WEAPON_21', 21, 'рога', WEAPON_TYPE.TYPE_22, noun(['', '', '', '', '', '',
                                                                   'рога', 'рогов', 'рогам', 'рога', 'рогами', 'рогах'], 'мн,но,мр')),
               ('WEAPON_22', 22, 'сабля', WEAPON_TYPE.TYPE_11, noun(['сабля', 'сабли', 'сабле', 'саблю', 'саблей', 'сабле',
                                                                     'сабли', 'сабель', 'саблям', 'сабли', 'саблями', 'саблях'], 'но,жр')),
               ('WEAPON_23', 23, 'топор', WEAPON_TYPE.TYPE_12, noun(['топор', 'топора', 'топору', 'топор', 'топором', 'топаре',
                                                                     'топоры', 'топоров', 'топорам', 'топоры', 'топорами', 'топорах'], 'но,мр')),
               ('WEAPON_24', 24, 'хопеш', WEAPON_TYPE.TYPE_23, noun(['хопеш', 'хопеша', 'хопешу', 'хопеш', 'хопешем', 'хопеше',
                                                                     'хопеши', 'хопешей', 'хопешам', 'хопеши', 'хопешами', 'хопешах'], 'но,мр')),
               ('WEAPON_25', 25, 'шипы', WEAPON_TYPE.TYPE_24, noun(['', '', '', '', '', '',
                                                                    'шипы', 'шипов', 'шипам', 'шипы', 'шипами', 'шипах'], 'мн,но,мр')),
               ('WEAPON_26', 26, 'хватательная лапа', WEAPON_TYPE.TYPE_31, noun(['лапа', 'лапы', 'лапе', 'лапу', 'лапой', 'лапе',
                                                                                 'лапы', 'лап', 'лапам', 'лапы', 'лапами', 'лапах'], 'но,жр')),
               ('WEAPON_27', 27, 'копыто', WEAPON_TYPE.TYPE_32, noun(['копыто', 'копыта', 'копыту', 'копыто', 'копытом', 'копыте',
                                                                      'копыта', 'копыт', 'копытам', 'копыта', 'копытами', 'копытах'], 'но,ср')),
               ('WEAPON_28', 28, 'нога', WEAPON_TYPE.TYPE_33, noun(['нога', 'ноги', 'ноге', 'ногу', 'ногой', 'ноге',
                                                                    'ноги', 'ног', 'ногам', 'ноги', 'ногами', 'ногах'], 'но,жр')),
               ('WEAPON_29', 29, 'серп', WEAPON_TYPE.TYPE_34, noun(['серп', 'серпа', 'серпу', 'серп', 'серпом', 'серпе',
                                                                    'серпы', 'серпов', 'серпам', 'серпы', 'серпами', 'серпах'], 'но,мр')),
               ('WEAPON_30', 30, 'пила', WEAPON_TYPE.TYPE_26, noun(['пила', 'пилы', 'пиле', 'пилу', 'пилой', 'пиле',
                                                                    'пилы', 'пил', 'пилам', 'пилы', 'пилами', 'пилах'], 'но,жр')),
               ('WEAPON_31', 31, 'праща', WEAPON_TYPE.TYPE_35, noun(['праща', 'пращи', 'праще', 'пращу', 'пращой', 'праще',
                                                                     'пращи', 'пращей', 'пращам', 'пращи', 'пращами', 'пращах'], 'но,жр')),
               ('WEAPON_32', 32, 'лук', WEAPON_TYPE.TYPE_36, noun(['лук', 'лука', 'луку', 'лук', 'луком', 'луке',
                                                                   'луки', 'луков', 'лукам', 'луки', 'луками', 'луках'], 'но,мр')),
               ('WEAPON_33', 33, 'артаблет', WEAPON_TYPE.TYPE_37, noun(['арбалет', 'арбалета', 'арбалету', 'арбалет', 'арбалетом', 'арбалете',
                                                                        'арбалеты', 'арбалетов', 'арбалетам', 'арбалеты', 'арбалетами', 'арбалетах'], 'но,мр')),
               ('WEAPON_34', 34, 'молот', WEAPON_TYPE.TYPE_38, noun(['молот', 'молота', 'молоту', 'молот', 'молотом', 'молоте',
                                                                     'молоты', 'молотов', 'молотам', 'молоты', 'молотами', 'молотах'], 'но,мр')))
