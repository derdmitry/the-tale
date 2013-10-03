# coding: utf-8
import mock

from common.utils import testcase

from accounts.logic import register_user
from game.heroes.prototypes import HeroPrototype
from game.logic_storage import LogicStorage


from game.balance import constants as c, formulas as f, enums as e

from game.logic import create_test_map
from game.actions.prototypes import ActionMoveNearPlacePrototype, ActionRestPrototype, ActionResurrectPrototype
from game.actions.prototypes import ActionIdlenessPrototype, ActionBattlePvE1x1Prototype, ActionInPlacePrototype, ActionRegenerateEnergyPrototype
from game.prototypes import TimePrototype

from game.map.relations import TERRAIN
from game.map.storage import map_info_storage


class MoveNearActionTest(testcase.TestCase):

    def setUp(self):
        super(MoveNearActionTest, self).setUp()

        self.p1, self.p2, self.p3 = create_test_map()

        result, account_id, bundle_id = register_user('test_user')

        self.hero = HeroPrototype.get_by_account_id(account_id)
        self.storage = LogicStorage()
        self.storage.add_hero(self.hero)
        self.action_idl = self.hero.actions.current_action

        self.hero.position.set_place(self.p1)

        self.action_move = ActionMoveNearPlacePrototype.create(hero=self.hero, place=self.p1, back=False)
    def tearDown(self):
        pass


    def test_create(self):
        self.assertEqual(self.action_idl.leader, False)
        self.assertEqual(self.action_move.leader, True)
        self.assertEqual(self.action_move.bundle_id, self.action_idl.bundle_id)
        self.storage._test_save()

    def test_get_destination_coordinates(self):

        self.assertTrue(len(self.p1.nearest_cells) > 3) # two coordinates will be in coordinates set, other will not

        x_1, y_1 = self.p1.nearest_cells[0]
        map_info_storage.item.terrain[y_1][x_1] = TERRAIN.WATER_DEEP

        x_2, y_2 = self.p1.nearest_cells[1]
        map_info_storage.item.terrain[y_2][x_2] = TERRAIN.WATER_DEEP

        coordinates = set()

        for i in xrange(100):
            coordinates.add(ActionMoveNearPlacePrototype._get_destination_coordinates(back=False, place=self.p1, terrains=(TERRAIN.WATER_DEEP,)))

        self.assertEqual(coordinates, set([(x_1, y_1), (x_2, y_2)]))


    def test_get_destination_coordinates__no_terrains(self):

        self.assertTrue(len(self.p1.nearest_cells) > 3) # two coordinates will be in coordinates set, other will not

        coordinates = set()

        for i in xrange(100):
            coordinates.add(ActionMoveNearPlacePrototype._get_destination_coordinates(back=False, place=self.p1, terrains=(TERRAIN.WATER_DEEP,)))

        self.assertEqual(coordinates, set(self.p1.nearest_cells))

    def test_get_destination_coordinates__back(self):

        self.assertTrue(len(self.p1.nearest_cells) > 3) # two coordinates will be in coordinates set, other will not

        x_1, y_1 = self.p1.nearest_cells[0]
        map_info_storage.item.terrain[y_1][x_1] = TERRAIN.WATER_DEEP

        x_2, y_2 = self.p1.nearest_cells[1]
        map_info_storage.item.terrain[y_2][x_2] = TERRAIN.WATER_DEEP

        coordinates = set()

        for i in xrange(100):
            coordinates.add(ActionMoveNearPlacePrototype._get_destination_coordinates(back=True, place=self.p1, terrains=(TERRAIN.WATER_DEEP,)))

        self.assertEqual(coordinates, set([(self.p1.x, self.p1.y)]))


    @mock.patch('game.heroes.prototypes.HeroPositionPrototype.is_battle_start_needed', lambda self: False)
    def test_processed(self):

        current_time = TimePrototype.get_current_time()

        self.storage.process_turn(second_step_if_needed=False)

        x, y = self.action_move.get_destination()
        self.hero.position.set_coordinates(x, y, x, y, percents=1)

        current_time.increment_turn()
        self.storage.process_turn(second_step_if_needed=False)

        # can end in field or in start place
        self.assertTrue(self.hero.actions.current_action.TYPE in [ActionIdlenessPrototype.TYPE, ActionInPlacePrototype.TYPE])
        self.assertTrue(self.hero.position.is_walking or self.hero.position.place)

        self.storage._test_save()


    @mock.patch('game.heroes.prototypes.HeroPositionPrototype.is_battle_start_needed', lambda self: False)
    def test_not_ready(self):
        self.storage.process_turn(second_step_if_needed=False)
        self.assertEqual(len(self.hero.actions.actions_list), 2)
        self.assertEqual(self.hero.actions.current_action, self.action_move)
        self.assertTrue(self.hero.position.is_walking or self.hero.position.place) # can end in start place
        self.storage._test_save()

    @mock.patch('game.heroes.prototypes.HeroPositionPrototype.is_battle_start_needed', lambda self: False)
    @mock.patch('game.heroes.prototypes.HeroPositionPrototype.subroad_len', lambda self: 1)
    def test_modify_speed(self):

        with mock.patch('game.heroes.prototypes.HeroPositionPrototype.modify_move_speed',
                        mock.Mock(return_value=self.hero.move_speed)) as speed_modifier_call_counter:
            self.storage.process_turn(second_step_if_needed=False)

        self.assertEqual(speed_modifier_call_counter.call_count, 1)

    def test_full_move_and_back(self):

        current_time = TimePrototype.get_current_time()

        while len(self.hero.actions.actions_list) != 1:
            self.storage.process_turn(second_step_if_needed=False)
            current_time.increment_turn()

        self.assertEqual(self.hero.actions.current_action.TYPE, ActionIdlenessPrototype.TYPE)
        self.assertTrue(self.hero.position.is_walking or self.hero.position.place)  # can end in start place

        ActionMoveNearPlacePrototype.create(hero=self.hero, place=self.p1, back=True)
        while self.hero.position.place is None or self.hero.position.place.id != self.p1.id:
            self.storage.process_turn(second_step_if_needed=False)
            current_time.increment_turn()

        self.assertEqual(self.hero.actions.current_action.TYPE, ActionInPlacePrototype.TYPE)
        self.assertTrue(not self.hero.position.is_walking)
        self.storage._test_save()

    def test_move_change_place_coordinates_and_back(self):

        current_time = TimePrototype.get_current_time()

        while len(self.hero.actions.actions_list) != 1:
            self.storage.process_turn(second_step_if_needed=False)
            current_time.increment_turn()

        self.assertEqual(self.hero.actions.current_action.TYPE, ActionIdlenessPrototype.TYPE)
        self.assertTrue(self.hero.position.is_walking or self.hero.position.place)  # can end in start place

        ActionMoveNearPlacePrototype.create(hero=self.hero, place=self.p1, back=True)
        self.p1._model.x = self.p1.x + 1
        self.p1._model.y = self.p1.y + 1
        self.p1.save()

        while self.hero.position.place is None or self.hero.position.place.id != self.p1.id:
            self.storage.process_turn(second_step_if_needed=False)
            current_time.increment_turn()

        self.assertEqual(self.hero.actions.current_action.TYPE, ActionInPlacePrototype.TYPE)
        self.assertTrue(not self.hero.position.is_walking)
        self.storage._test_save()

    def test_full(self):

        current_time = TimePrototype.get_current_time()

        while len(self.hero.actions.actions_list) != 1:
            self.storage.process_turn(second_step_if_needed=False)
            current_time.increment_turn()

        self.assertTrue(self.action_idl.leader)

        self.storage._test_save()

    @mock.patch('game.heroes.prototypes.HeroPositionPrototype.is_battle_start_needed', lambda self: True)
    def test_battle(self):
        self.storage.process_turn(second_step_if_needed=False)
        self.assertEqual(self.hero.actions.current_action.TYPE, ActionBattlePvE1x1Prototype.TYPE)
        self.storage._test_save()

    def test_regenerate_energy_on_move(self):
        self.hero.preferences.set_energy_regeneration_type(e.ANGEL_ENERGY_REGENERATION_TYPES.PRAY)
        self.hero.last_energy_regeneration_at_turn -= max([f.angel_energy_regeneration_delay(energy_regeneration_type)
                                                           for energy_regeneration_type in c.ANGEL_ENERGY_REGENERATION_STEPS.keys()])
        self.action_move.state = self.action_move.STATE.MOVING

        self.storage.process_turn(second_step_if_needed=False)

        self.assertEqual(self.hero.actions.current_action.TYPE, ActionRegenerateEnergyPrototype.TYPE)

        self.storage._test_save()

    def test_not_regenerate_energy_on_move_for_sacrifice(self):
        self.hero.preferences.set_energy_regeneration_type(e.ANGEL_ENERGY_REGENERATION_TYPES.SACRIFICE)
        self.hero.last_energy_regeneration_at_turn -= max([f.angel_energy_regeneration_delay(energy_regeneration_type)
                                                           for energy_regeneration_type in c.ANGEL_ENERGY_REGENERATION_STEPS.keys()])
        self.action_move.state = self.action_move.STATE.MOVING

        self.storage.process_turn(second_step_if_needed=False)

        self.assertNotEqual(self.hero.actions.current_action.TYPE, ActionRegenerateEnergyPrototype.TYPE)

        self.storage._test_save()


    def test_regenerate_energy_after_battle_for_sacrifice(self):
        self.hero.preferences.set_energy_regeneration_type(e.ANGEL_ENERGY_REGENERATION_TYPES.SACRIFICE)
        self.hero.last_energy_regeneration_at_turn -= max([f.angel_energy_regeneration_delay(energy_regeneration_type)
                                                           for energy_regeneration_type in c.ANGEL_ENERGY_REGENERATION_STEPS.keys()])
        self.action_move.state = self.action_move.STATE.BATTLE

        self.storage.process_turn(second_step_if_needed=False)

        self.assertEqual(self.hero.actions.current_action.TYPE, ActionRegenerateEnergyPrototype.TYPE)

        self.storage._test_save()


    def test_rest(self):
        self.hero.health = 1
        self.action_move.state = self.action_move.STATE.BATTLE
        self.storage.process_turn(second_step_if_needed=False)

        self.assertEqual(self.hero.actions.current_action.TYPE, ActionRestPrototype.TYPE)
        self.storage._test_save()


    def test_resurrect(self):
        self.hero.kill()
        self.action_move.state = self.action_move.STATE.BATTLE
        self.storage.process_turn(second_step_if_needed=False)

        self.assertEqual(self.hero.actions.current_action.TYPE, ActionResurrectPrototype.TYPE)
        self.storage._test_save()


    @mock.patch('game.heroes.prototypes.HeroPositionPrototype.is_battle_start_needed', lambda self: False)
    def test_stop_when_quest_required_replane(self):
        while self.action_move.state != ActionMoveNearPlacePrototype.STATE.MOVING:
            self.storage.process_turn(second_step_if_needed=False)

        with mock.patch('game.quests.container.QuestsContainer.has_quests', True):
            with mock.patch('game.quests.container.QuestsContainer.current_quest', mock.Mock(replane_required=False)):
                self.storage.process_turn(second_step_if_needed=False)

            self.assertEqual(self.action_move.state, ActionMoveNearPlacePrototype.STATE.MOVING)

            with mock.patch('game.quests.container.QuestsContainer.current_quest', mock.Mock(replane_required=True)):
                self.storage.process_turn(second_step_if_needed=False)

        self.assertEqual(self.action_move.state, ActionMoveNearPlacePrototype.STATE.PROCESSED)
