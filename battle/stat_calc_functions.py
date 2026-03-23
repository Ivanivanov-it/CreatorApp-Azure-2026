

ATK_ROLES = ["ATTACK","BUFF"]
ATK_TYPES = ["HERO","DEMON","GOD","VILLAIN"]
DEFENSE_ROLES = ["DEFEND","SUPPORT"]
DEFENSE_TYPES = ["ALIEN","ANGEL"]
HP_ROLES = ["HEAL","SEARCH"]
HP_TYPES = ["TIME TRAVELER"]

def calc_buff_atk(obj) -> int:
    result = 0

    roles = getattr(obj, "roles", None)

    if roles is not None:
        for role in roles.all():
            if role.role in ATK_ROLES:
                result += 5

    if obj.type in ATK_TYPES:
        result += 5

    return result


def calc_buff_def(obj) -> int:
    result = 0

    roles = getattr(obj, "roles", None)

    if roles is not None:
        for role in roles.all():
            if role.role in DEFENSE_ROLES:
                result += 3

    if obj.type in DEFENSE_TYPES:
        result += 5

    return result


def calc_buff_hp(obj) -> int:
    result = 0

    roles = getattr(obj, "roles" , None)

    if roles is not None:
        for role in roles.all():
            if role.role in HP_ROLES:
                result += 50

    if obj.type in HP_TYPES:
        result += 50

    return result

def calc_debuff_hp(enemy_obj,hero_obj) -> int:
    enemy_weaknesses = [e.role for e in enemy_obj.weakness.all()]
    hero_roles = [h.role for h in hero_obj.roles.all()]

    result = 0

    for weakness in enemy_weaknesses:
        if weakness in HP_ROLES and weakness in hero_roles:
            result += 50

    return result


def calc_debuff_atk(enemy_obj, hero_obj) -> int:
    enemy_weaknesses = [e.role for e in enemy_obj.weakness.all()]
    hero_roles = [h.role for h in hero_obj.roles.all()]

    result = 0

    for weakness in enemy_weaknesses:
        if weakness in ATK_ROLES and weakness in hero_roles:
            result += 35

    return result

def calc_debuff_def(enemy_obj, hero_obj) -> int:
    enemy_weaknesses = [e.role for e in enemy_obj.weakness.all()]
    hero_roles = [h.role for h in hero_obj.roles.all()]

    result = 0

    for weakness in enemy_weaknesses:
        if weakness in DEFENSE_ROLES and weakness in hero_roles:
            result += 25

    return result