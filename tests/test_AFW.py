from unittest import TestCase
import unittest
from .context import PySimpleAutomata
import copy
import itertools
from PySimpleAutomata import NFA
from PySimpleAutomata import AFW
from PySimpleAutomata import automata_IO


class TestAfwWordAcceptance(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.afw_word_acceptance_test_01 = automata_IO.afw_json_importer(
            './tests/json/afw/afw_word_acceptance_test_01.json')
        self.afw_word_acceptance_test_empty = {
            'alphabet': set(),
            'states': set(),
            'initial_states': set(),
            'accepting_states': set(),
            'transitions': {}
        }

    def test_word_acceptance(self):
        """ Tests a correct word acceptance """
        self.assertTrue(
            AFW.afw_word_acceptance(self.afw_word_acceptance_test_01,
                                    ['a', 'b', 'b', 'a', 'a', 'b', 'a', 'a']))

    def test_word_acceptance_false(self):
        """ Tests a non correct word to be refused, with good alphabet """
        self.assertFalse(
            AFW.afw_word_acceptance(self.afw_word_acceptance_test_01,
                                    ['a', 'b', 'a']))

    def test_word_acceptance_wrong_alphabet(self):
        """ Tests a non correct word, with letters not form the afw alphabet 
        """
        self.assertFalse(
            AFW.afw_word_acceptance(self.afw_word_acceptance_test_01,
                                    ['a', 'b', 'wrong']))

    def test_word_acceptance_empty_word(self):
        """ Tests an empty word"""
        self.afw_word_acceptance_test_01['initial_state'] = 'q1'
        self.assertFalse(
            AFW.afw_word_acceptance(self.afw_word_acceptance_test_01, []))

    @unittest.expectedFailure
    def test_word_acceptance_wrong_input_1(self):
        """ Tests an input different from a dict() object. [EXPECTED 
        FAILURE]"""
        AFW.afw_word_acceptance(1, ['a', 'b', 'b', 'a', 'b'])

    @unittest.expectedFailure
    def test_word_acceptance_wrong_input_2(self):
        """ Tests an input different from a list() object. [EXPECTED 
        FAILURE]"""
        AFW.afw_word_acceptance(self.afw_word_acceptance_test_01, 1)

    @unittest.expectedFailure
    def test_word_acceptance_wrong_dict(self):
        """ Tests a dict() in input different from a well formatted dict() 
        representing a AFW. [EXPECTED FAILURE]"""
        AFW.afw_word_acceptance({'goofy': 'donald'}, ['a', 'b', 'b', 'a', 'b'])

    def test_word_acceptance_check_side_effects(self):
        """ Tests that the function doesn't make any side effect on the 
        input"""
        before = copy.deepcopy(self.afw_word_acceptance_test_01)
        AFW.afw_word_acceptance(self.afw_word_acceptance_test_01,
                                ['a', 'b', 'b', 'a', 'a', 'b', 'a', 'a'])
        self.assertDictEqual(before, self.afw_word_acceptance_test_01)


class TestNfaToAfwConversion(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.nfa_nfa_to_afw_test_01 = automata_IO.nfa_dot_importer(
            './tests/dot/afw/nfa_nfa_to_afw_test_01.dot')
        self.afw_nfa_to_afw_test_01 = automata_IO.afw_json_importer(
            './tests/json/afw/afw_nfa_to_afw_test_01.json')
        self.nfa_nfa_to_afw_test_empty = {
            'alphabet': set(),
            'states': set(),
            'initial_states': set(),
            'accepting_states': set(),
            'transitions': {}
        }
        self.afw_nfa_to_afw_test_empty = {
            'alphabet': set(),
            'states': set(),
            'initial_state': None,
            'accepting_states': set(),
            'transitions': {}
        }

    def test_nfa_to_afw_conversion(self):
        """ Tests a correct nfa to afw conversion """
        afw_01 = AFW.nfa_to_afw_conversion(self.nfa_nfa_to_afw_test_01)
        self.assertSetEqual(afw_01['alphabet'],
                            self.afw_nfa_to_afw_test_01['alphabet'])
        self.assertSetEqual(afw_01['states'],
                            self.afw_nfa_to_afw_test_01['states'])
        self.assertEqual(afw_01['initial_state'],
                         self.afw_nfa_to_afw_test_01['initial_state'])
        self.assertSetEqual(afw_01['accepting_states'],
                            self.afw_nfa_to_afw_test_01['accepting_states'])

        self.assertEqual(len(afw_01['alphabet']),
                         len(self.afw_nfa_to_afw_test_01['alphabet']))
        # self.assertDictEqual(afw_01, self.afw_nfa_to_afw_test_01)
        # due to set-to-string serialization undecidability of items order,
        # it is not possible to match the result
        # of the operation to a predetermined result without enlist all the
        # possible combination of S^2
        # i.e a result may be 's2 or s5' or 's5 or s2' unpredictably

    def test_nfa_to_afw_conversion_empty_states(self):
        """ Tests converting an empty nfa """
        expected_solution = {
            'alphabet': set(),
            'states': {'root'},
            'initial_state': 'root',
            'accepting_states': set(),
            'transitions': {}
        }
        self.assertDictEqual(
            AFW.nfa_to_afw_conversion(self.nfa_nfa_to_afw_test_empty),
            expected_solution)

    def test_nfa_to_afw_conversion_empty_transition(self):
        """ Tests converting an nfa without transition """
        expected_solution = {
            'alphabet': self.nfa_nfa_to_afw_test_01['alphabet'],
            'states': self.nfa_nfa_to_afw_test_01['states'].union({'root'}),
            'initial_state': 'root',
            'accepting_states': self.nfa_nfa_to_afw_test_01[
                'accepting_states'],
            'transitions': {}
        }
        self.nfa_nfa_to_afw_test_01['transitions'] = {}
        self.assertDictEqual(
            AFW.nfa_to_afw_conversion(self.nfa_nfa_to_afw_test_01),
            expected_solution)

    @unittest.expectedFailure
    def test_nfa_to_afw_conversion_wrong_input(self):
        """ Tests the function using an input different from a dict object. 
        [EXPECTED FAILURE] """
        AFW.nfa_to_afw_conversion(0)

    @unittest.expectedFailure
    def test_nfa_to_afw_conversion_wrong_dict(self):
        """ Tests the function using an input different from a well 
        formatted dict representing a afw. [EXPECTED FAILURE] """
        AFW.nfa_to_afw_conversion({'goofy': 'donald'})

    def test_nfa_to_afw_conversion_side_effects(self):
        """ Tests the function doesn't make any side effect on the input """
        before = copy.deepcopy(self.nfa_nfa_to_afw_test_01)
        AFW.nfa_to_afw_conversion(self.nfa_nfa_to_afw_test_01)
        self.assertDictEqual(before, self.nfa_nfa_to_afw_test_01)


class TestAfwToNfaConversion(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.nfa_afw_to_nfa_test_01 = automata_IO.nfa_dot_importer(
            './tests/dot/afw/nfa_afw_to_nfa_test_01.dot')
        self.afw_afw_to_nfa_test_01 = automata_IO.afw_json_importer(
            './tests/json/afw/afw_afw_to_nfa_test_01.json')
        self.afw_nonemptiness_check_test_2 = automata_IO.afw_json_importer(
            './tests/json/afw/afw_nonemptiness_check_test_2.json')
        self.nfa_empty = {
            'alphabet': set(),
            'states': set(),
            'initial_states': set(),
            'accepting_states': set(),
            'transitions': {}
        }
        self.afw_afw_to_nfa_test_empty = {
            'alphabet': set(),
            'states': set(),
            'initial_state': None,
            'accepting_states': set(),
            'transitions': {}
        }

    def test_afw_to_nfa_conversion_language(self):
        """ Test a correct afw conversion to nfa comparing the language read 
        by the two automaton """
        nfa_01 = AFW.afw_to_nfa_conversion(self.afw_afw_to_nfa_test_01)
        # automata_IO.nfa_to_dot(nfa_01, 'afw_to_nfa_01')
        i = 0
        last = 7
        while i <= last:
            base = list(itertools.repeat('a', i))
            base += list(itertools.repeat('b', i))
            # build all permutation of 'a' and 'b' till length i
            word_set = set(itertools.permutations(base, i))
            for word in word_set:
                word = list(word)
                # print(word)
                afw_acceptance = AFW.afw_word_acceptance(
                    self.afw_afw_to_nfa_test_01, word)
                nfa_acceptance = NFA.nfa_word_acceptance(nfa_01, word)
                self.assertEqual(afw_acceptance, nfa_acceptance)
            i += 1

    def test_afw_to_nfa_conversion_language_bis_bis(self):
        """ Test a correct afw conversion to nfa comparing the language read 
        by the two automaton """
        nfa_01 = AFW.afw_to_nfa_conversion(self.afw_nonemptiness_check_test_2)
        # automata_IO.nfa_to_dot(nfa_01, 'afw_to_nfa_strange')
        i = 0
        last = 7
        while i <= last:
            base = list(itertools.repeat('a', i))
            base += list(itertools.repeat('b', i))
            # build all permutation of 'a' and 'b' till length i
            word_set = set(itertools.permutations(base, i))
            for word in word_set:
                word = list(word)
                # print(word)
                afw_acceptance = AFW.afw_word_acceptance(
                    self.afw_nonemptiness_check_test_2, word)
                nfa_acceptance = NFA.nfa_word_acceptance(nfa_01, word)
                self.assertEqual(afw_acceptance, nfa_acceptance)
            i += 1

    def test_afw_to_nfa_conversion_language_bis(self):
        """ Test a correct afw conversion to nfa comparing the language read 
        by the two automaton.
            Here we take a nfa, we covert it to afw and back to nfa,
            then the original and final nfa are compared trough the language 
            read.
        """
        original_nfa_to_afw = AFW.nfa_to_afw_conversion(
            self.nfa_afw_to_nfa_test_01)
        nfa_01 = AFW.afw_to_nfa_conversion(original_nfa_to_afw)
        i = 0
        last = 7
        while i <= last:
            base = list(itertools.repeat('a', i))
            base += list(itertools.repeat('b', i))
            # build all permutation of 'a' and 'b' till length i
            word_set = set(itertools.permutations(base, i))
            for word in word_set:
                word = list(word)
                # print(word)
                original_nfa_acceptance = NFA.nfa_word_acceptance(
                    self.nfa_afw_to_nfa_test_01, word)
                nfa_acceptance = NFA.nfa_word_acceptance(nfa_01, word)
                self.assertEqual(original_nfa_acceptance, nfa_acceptance)
            i += 1

    def test_afw_to_nfa_conversion_empty_states(self):
        """ Tests a AFW to NFA conversion with an empty AFW """
        nfa_01 = AFW.afw_to_nfa_conversion(self.afw_afw_to_nfa_test_empty)
        self.nfa_empty['initial_states'] = {(None,)}
        self.nfa_empty['states'] = self.nfa_empty['initial_states']
        self.assertDictEqual(nfa_01, self.nfa_empty)

    def test_afw_to_nfa_conversion_empty_transitions(self):
        """ Tests a AFW to NFA conversion with a AFW without transitions """
        self.afw_afw_to_nfa_test_01['transitions'] = {}
        nfa_01 = AFW.afw_to_nfa_conversion(self.afw_afw_to_nfa_test_01)
        result = {
            'initial_states': {('s',)},
            'accepting_states': {('s',)},
            'transitions': {},
            'states': {('s',)},
            'alphabet': {'b', 'a'}
        }
        self.assertSetEqual(nfa_01['initial_states'], result['initial_states'])
        self.assertDictEqual(nfa_01['transitions'], result['transitions'])
        self.assertSetEqual(nfa_01['alphabet'], result['alphabet'])
        self.assertEqual(len(nfa_01['accepting_states']),
                         len(result['accepting_states']))
        self.assertEqual(len(nfa_01['states']), len(result['states']))

    @unittest.expectedFailure
    def test_afw_to_nfa_conversion_wrong_input(self):
        """ Tests the function using an input different from a dict object. 
        [EXPECTED FAILURE] """
        AFW.afw_to_nfa_conversion(0)

    @unittest.expectedFailure
    def test_afw_to_nfa_conversion_wrong_dict(self):
        """ Tests the function using an input different from a well 
        formatted dict representing a afw. [EXPECTED FAILURE] """
        AFW.afw_to_nfa_conversion({'goofy': 'donald'})

    def test_afw_to_nfa_conversion_side_effects(self):
        """ Tests the function doesn't make any side effect on the input """
        before = copy.deepcopy(self.afw_afw_to_nfa_test_01)
        AFW.afw_to_nfa_conversion(self.afw_afw_to_nfa_test_01)
        self.assertDictEqual(before, self.afw_afw_to_nfa_test_01)


class TestAfwCompletion(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.afw_completion_test_01 = automata_IO.afw_json_importer(
            './tests/json/afw/afw_completion_test_01.json')
        self.afw_completion_test_empty = {
            'alphabet': set(),
            'states': set(),
            'initial_state': None,
            'accepting_states': set(),
            'transitions': {}
        }

    def test_afw_completion(self):
        """ Tests a correct afw completion comparing the language read, 
        that must be the same"""
        original = copy.deepcopy(self.afw_completion_test_01)
        AFW.afw_completion(self.afw_completion_test_01)

        i = 0
        last = 7
        while i <= last:
            base = list(itertools.repeat('a', i))
            base += list(itertools.repeat('b', i))
            # build all permutation of 'a' and 'b' till length i
            word_set = set(itertools.permutations(base, i))
            for word in word_set:
                word = list(word)
                original_acceptance = AFW.afw_word_acceptance(original, word)
                completed_acceptance = AFW.afw_word_acceptance(
                    self.afw_completion_test_01, word)
                self.assertEqual(original_acceptance, completed_acceptance)
            i += 1

    def test_afw_completion_empty_states(self):
        """ Tests a completion of a afw without states"""
        AFW.afw_completion(self.afw_completion_test_empty)
        result = {
            'alphabet': set(),
            'states': set(),
            'initial_state': None,
            'accepting_states': set(),
            'transitions': {}
        }
        self.assertDictEqual(self.afw_completion_test_empty, result)

    def test_afw_completion_empty_transitions(self):
        """ Tests a completion of a afw without transitions"""
        self.afw_completion_test_01['transitions'] = {}
        result = copy.deepcopy(self.afw_completion_test_01)
        for state in result['states']:
            for action in result['alphabet']:
                result['transitions'][state, action] = 'False'
        AFW.afw_completion(self.afw_completion_test_01)
        self.assertDictEqual(self.afw_completion_test_01, result)

    @unittest.expectedFailure
    def test_afw_completion_wrong_input(self):
        """ Tests an input different from a dict() object. [EXPECTED 
        FAILURE]"""
        AFW.afw_completion(0)

    @unittest.expectedFailure
    def test_afw_completion_wrong_dict(self):
        """ Tests a dict() in input different from a well formatted dict() 
        representing a AFW. [EXPECTED FAILURE]"""
        AFW.afw_completion({'goofy': 'donald'})

    def test_afw_completion_side_effects(self):
        """ Tests the function makes side effect on the input """
        before = copy.deepcopy(self.afw_completion_test_01)
        AFW.afw_completion(self.afw_completion_test_01)
        self.assertNotEqual(before, self.afw_completion_test_01)


class TestAfwComplementation(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.afw_complementation_test_01 = automata_IO.afw_json_importer(
            './tests/json/afw/afw_complementation_test_01.json')
        self.afw_complementation_test_empty = {
            'alphabet': set(),
            'states': set(),
            'initial_state': None,
            'accepting_states': set(),
            'transitions': {}
        }

    def test_afw_complementation(self):
        """ Test a correct afw complementation comparing the language read, 
        that must be discording"""
        afw_complemented = AFW.afw_complementation(
            self.afw_complementation_test_01)

        i = 0
        last = 7
        while i <= last:
            base = list(itertools.repeat('a', i))
            base += list(itertools.repeat('b', i))
            # build all permutation of 'a' and 'b' till length i
            word_set = set(itertools.permutations(base, i))
            for word in word_set:
                word = list(word)
                afw_acceptance = AFW.afw_word_acceptance(
                    self.afw_complementation_test_01, word)
                complement_acceptance = AFW.afw_word_acceptance(
                    afw_complemented, word)
                self.assertNotEqual(afw_acceptance, complement_acceptance)
            i += 1

    def test_afw_complementation_empty_states(self):
        """ Tests a complementation of a afw without states"""
        complemented = AFW.afw_complementation(
            self.afw_complementation_test_empty)
        self.assertEqual(complemented, self.afw_complementation_test_empty)

    def test_afw_complementation_empty_transitions(self):
        """ Tests a complementation of a afw without transitions"""
        self.afw_complementation_test_01['transitions'] = {}
        result = copy.deepcopy(self.afw_complementation_test_01)
        result['accepting_states'] = {'q1', 'q2'}
        for state in result['states']:
            for action in result['alphabet']:
                result['transitions'][state, action] = 'True'

        complemented = AFW.afw_complementation(
            self.afw_complementation_test_01)
        self.assertEqual(complemented, result)

    @unittest.expectedFailure
    def test_afw_complementation_wrong_input(self):
        """ Tests an input different from a dict() object. [EXPECTED 
        FAILURE]"""
        AFW.afw_complementation(0)

    @unittest.expectedFailure
    def test_afw_complementation_wrong_dict(self):
        """ Tests a dict() in input different from a well formatted dict() 
        representing a DFA. [EXPECTED FAILURE]"""
        AFW.afw_complementation({'goofy': 'donald'})

    def test_afw_complementation_side_effects(self):
        """ Tests the function doesn't make any side effect on the input """
        before = copy.deepcopy(self.afw_complementation_test_01)
        AFW.afw_complementation(self.afw_complementation_test_01)
        self.assertDictEqual(before, self.afw_complementation_test_01)


class TestAfwUnion(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.afw_union_1_test_01 = automata_IO.afw_json_importer(
            './tests/json/afw/afw_union_1_test_01.json')
        self.afw_union_2_test_01 = automata_IO.afw_json_importer(
            './tests/json/afw/afw_union_2_test_01.json')
        self.afw_union_3_test_01 = automata_IO.afw_json_importer(
            './tests/json/afw/afw_union_3_test_01.json')
        self.afw_union_test_empty = {
            'alphabet': set(),
            'states': set(),
            'initial_state': None,
            'accepting_states': set(),
            'transitions': {}
        }

    def test_afw_union_disjoint(self):
        """ Tests a correct afw union with completely disjoint afws  """
        AFW.rename_afw_states(self.afw_union_2_test_01, 'a_')
        union = AFW.afw_union(self.afw_union_1_test_01,
                              self.afw_union_2_test_01)

        i = 0
        last = 7
        while i <= last:
            base = list(itertools.repeat('a', i))
            base += list(itertools.repeat('b', i))
            # build all permutation of 'a' and 'b' till length i
            word_set = set(itertools.permutations(base, i))
            for word in word_set:
                word = list(word)
                original_acceptance_1 = AFW.afw_word_acceptance(
                    self.afw_union_1_test_01, word)
                original_acceptance_2 = AFW.afw_word_acceptance(
                    self.afw_union_2_test_01, word)
                union_acceptance = AFW.afw_word_acceptance(union, word)
                self.assertEqual(
                    original_acceptance_1 or original_acceptance_2,
                    union_acceptance)
            i += 1

    def test_afw_union_intersecting(self):
        """ Tests a correct afw union where the afws have some state in 
        common  """
        AFW.rename_afw_states(self.afw_union_3_test_01, 'a_')
        union = AFW.afw_union(self.afw_union_1_test_01,
                              self.afw_union_3_test_01)

        i = 0
        last = 7
        while i <= last:
            base = list(itertools.repeat('a', i))
            base += list(itertools.repeat('b', i))
            # build all permutation of 'a' and 'b' till length i
            word_set = set(itertools.permutations(base, i))
            for word in word_set:
                word = list(word)
                # print(word)
                original_acceptance_1 = AFW.afw_word_acceptance(
                    self.afw_union_1_test_01, word)
                original_acceptance_2 = AFW.afw_word_acceptance(
                    self.afw_union_3_test_01, word)
                union_acceptance = AFW.afw_word_acceptance(union, word)
                self.assertEqual(
                    original_acceptance_1 or original_acceptance_2,
                    union_acceptance)
            i += 1

    def test_afw_union_equals(self):
        """ Tests a correct afw union with the same afw """
        AFW.rename_afw_states(self.afw_union_1_test_01, 'a_')
        union = AFW.afw_union(self.afw_union_1_test_01,
                              self.afw_union_1_test_01)

        i = 0
        last = 7
        while i <= last:
            base = list(itertools.repeat('a', i))
            base += list(itertools.repeat('b', i))
            # build all permutation of 'a' and 'b' till length i
            word_set = set(itertools.permutations(base, i))
            for word in word_set:
                word = list(word)
                original_acceptance_1 = AFW.afw_word_acceptance(
                    self.afw_union_1_test_01, word)
                original_acceptance_2 = AFW.afw_word_acceptance(
                    self.afw_union_1_test_01, word)
                union_acceptance = AFW.afw_word_acceptance(union, word)
                self.assertEqual(
                    original_acceptance_1 or original_acceptance_2,
                    union_acceptance)
            i += 1

    def test_afw_union_empty_states_1(self):
        """ Tests a afw union where the first afw is empty """
        union = AFW.afw_union(self.afw_union_test_empty,
                              self.afw_union_1_test_01)
        i = 0
        last = 7
        while i <= last:
            base = list(itertools.repeat('a', i))
            base += list(itertools.repeat('b', i))
            # build all permutation of 'a' and 'b' till length i
            word_set = set(itertools.permutations(base, i))
            for word in word_set:
                word = list(word)
                original_acceptance_1 = AFW.afw_word_acceptance(
                    self.afw_union_1_test_01, word)
                original_acceptance_2 = AFW.afw_word_acceptance(
                    self.afw_union_test_empty, word)
                union_acceptance = AFW.afw_word_acceptance(union, word)
                self.assertEqual(
                    original_acceptance_1 or original_acceptance_2,
                    union_acceptance)
            i += 1

    def test_afw_union_empty_states_2(self):
        """ Tests a afw union where the second afw is empty """
        union = AFW.afw_union(self.afw_union_1_test_01,
                              self.afw_union_test_empty)
        i = 0
        last = 7
        while i <= last:
            base = list(itertools.repeat('a', i))
            base += list(itertools.repeat('b', i))
            # build all permutation of 'a' and 'b' till length i
            word_set = set(itertools.permutations(base, i))
            for word in word_set:
                word = list(word)
                original_acceptance_1 = AFW.afw_word_acceptance(
                    self.afw_union_1_test_01, word)
                original_acceptance_2 = AFW.afw_word_acceptance(
                    self.afw_union_test_empty, word)
                union_acceptance = AFW.afw_word_acceptance(union, word)
                self.assertEqual(
                    original_acceptance_1 or original_acceptance_2,
                    union_acceptance)
            i += 1

    @unittest.expectedFailure
    def test_afw_union_wrong_input_1(self):
        """ Tests an input different from a dict() object. [EXPECTED 
        FAILURE]"""
        AFW.afw_union(0, self.afw_union_1_test_01)

    @unittest.expectedFailure
    def test_afw_union_wrong_input_2(self):
        """ Tests an input different from a dict() object. [EXPECTED 
        FAILURE]"""
        AFW.afw_union(self.afw_union_1_test_01, 0)

    @unittest.expectedFailure
    def test_afw_union_wrong_dict_1(self):
        """ Tests a dict() in input different from a well formatted dict() 
        representing a AFW. [EXPECTED FAILURE]"""
        AFW.afw_union(self.afw_union_1_test_01, {'goofy': 'donald'})

    @unittest.expectedFailure
    def test_afw_union_wrong_dict_2(self):
        """ Tests a dict() in input different from a well formatted dict() 
        representing a AFW. [EXPECTED FAILURE]"""
        AFW.afw_union({'goofy': 'donald'}, self.afw_union_1_test_01)

    def test_afw_union_side_effects_1(self):
        """ Tests the function makes side effect on the first input """
        before = copy.deepcopy(self.afw_union_1_test_01)
        AFW.afw_union(self.afw_union_1_test_01, self.afw_union_2_test_01)
        self.assertEqual(before, self.afw_union_1_test_01)

    def test_afw_union_side_effects_2(self):
        """ Tests the function makes side effect on the second input """
        before = copy.deepcopy(self.afw_union_2_test_01)
        AFW.afw_union(self.afw_union_1_test_01, self.afw_union_2_test_01)
        self.assertEqual(before, self.afw_union_2_test_01)


class TestAfwIntersection(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.afw_intersection_1_test_01 = automata_IO.afw_json_importer(
            './tests/json/afw/afw_intersection_1_test_01.json')
        self.afw_intersection_2_test_01 = automata_IO.afw_json_importer(
            './tests/json/afw/afw_intersection_2_test_01.json')
        self.afw_intersection_3_test_01 = automata_IO.afw_json_importer(
            './tests/json/afw/afw_intersection_3_test_01.json')
        self.afw_intersection_test_empty = {
            'alphabet': set(),
            'states': set(),
            'initial_state': None,
            'accepting_states': set(),
            'transitions': {}
        }

    def test_afw_intersection_disjoint(self):
        """ Tests a correct afw intersection with completely disjoint afws  """
        AFW.rename_afw_states(self.afw_intersection_2_test_01, 'a_')
        intersection = AFW.afw_intersection(self.afw_intersection_1_test_01,
                                            self.afw_intersection_2_test_01)

        i = 0
        last = 7
        while i <= last:
            base = list(itertools.repeat('a', i))
            base += list(itertools.repeat('b', i))
            # build all permutation of 'a' and 'b' till length i
            word_set = set(itertools.permutations(base, i))
            for word in word_set:
                word = list(word)
                original_acceptance_1 = AFW.afw_word_acceptance(
                    self.afw_intersection_1_test_01, word)
                original_acceptance_2 = AFW.afw_word_acceptance(
                    self.afw_intersection_2_test_01, word)
                intersection_acceptance = AFW.afw_word_acceptance(intersection,
                                                                  word)
                self.assertEqual(
                    original_acceptance_1 and original_acceptance_2,
                    intersection_acceptance)
            i += 1

    def test_afw_intersection_intersecting(self):
        """ Tests a correct afw intersection where the afws have some state 
        in common  """
        AFW.rename_afw_states(self.afw_intersection_3_test_01, 'a_')
        intersection = AFW.afw_intersection(self.afw_intersection_1_test_01,
                                            self.afw_intersection_3_test_01)

        i = 0
        last = 7
        while i <= last:
            base = list(itertools.repeat('a', i))
            base += list(itertools.repeat('b', i))
            # build all permutation of 'a' and 'b' till length i
            word_set = set(itertools.permutations(base, i))
            for word in word_set:
                word = list(word)
                # print(word)
                original_acceptance_1 = AFW.afw_word_acceptance(
                    self.afw_intersection_1_test_01, word)
                original_acceptance_2 = AFW.afw_word_acceptance(
                    self.afw_intersection_3_test_01, word)
                intersection_acceptance = AFW.afw_word_acceptance(intersection,
                                                                  word)
                self.assertEqual(
                    original_acceptance_1 and original_acceptance_2,
                    intersection_acceptance)
            i += 1

    def test_afw_intersection_equals(self):
        """ Tests a correct afw intersection with the same afw """
        AFW.rename_afw_states(self.afw_intersection_1_test_01, 'a_')
        intersection = AFW.afw_intersection(self.afw_intersection_1_test_01,
                                            self.afw_intersection_1_test_01)

        i = 0
        last = 7
        while i <= last:
            base = list(itertools.repeat('a', i))
            base += list(itertools.repeat('b', i))
            # build all permutation of 'a' and 'b' till length i
            word_set = set(itertools.permutations(base, i))
            for word in word_set:
                word = list(word)
                original_acceptance_1 = AFW.afw_word_acceptance(
                    self.afw_intersection_1_test_01, word)
                original_acceptance_2 = AFW.afw_word_acceptance(
                    self.afw_intersection_1_test_01, word)
                intersection_acceptance = AFW.afw_word_acceptance(intersection,
                                                                  word)
                self.assertEqual(
                    original_acceptance_1 and original_acceptance_2,
                    intersection_acceptance)
            i += 1

    def test_afw_intersection_empty_states_1(self):
        """ Tests a afw intersection where the first afw is empty """
        intersection = AFW.afw_intersection(self.afw_intersection_test_empty,
                                            self.afw_intersection_1_test_01)
        i = 0
        last = 7
        while i <= last:
            base = list(itertools.repeat('a', i))
            base += list(itertools.repeat('b', i))
            # build all permutation of 'a' and 'b' till length i
            word_set = set(itertools.permutations(base, i))
            for word in word_set:
                word = list(word)
                original_acceptance_1 = AFW.afw_word_acceptance(
                    self.afw_intersection_1_test_01, word)
                original_acceptance_2 = AFW.afw_word_acceptance(
                    self.afw_intersection_test_empty, word)
                intersection_acceptance = AFW.afw_word_acceptance(intersection,
                                                                  word)
                self.assertEqual(
                    original_acceptance_1 and original_acceptance_2,
                    intersection_acceptance)
            i += 1

    def test_afw_intersection_empty_states_2(self):
        """ Tests a afw intersection where the second afw is empty """
        intersection = AFW.afw_intersection(self.afw_intersection_1_test_01,
                                            self.afw_intersection_test_empty)
        i = 0
        last = 7
        while i <= last:
            base = list(itertools.repeat('a', i))
            base += list(itertools.repeat('b', i))
            # build all permutation of 'a' and 'b' till length i
            word_set = set(itertools.permutations(base, i))
            for word in word_set:
                word = list(word)
                original_acceptance_1 = AFW.afw_word_acceptance(
                    self.afw_intersection_1_test_01, word)
                original_acceptance_2 = AFW.afw_word_acceptance(
                    self.afw_intersection_test_empty, word)
                intersection_acceptance = AFW.afw_word_acceptance(intersection,
                                                                  word)
                self.assertEqual(
                    original_acceptance_1 and original_acceptance_2,
                    intersection_acceptance)
            i += 1

    @unittest.expectedFailure
    def test_afw_intersection_wrong_input_1(self):
        """ Tests an input different from a dict() object. [EXPECTED 
        FAILURE]"""
        AFW.afw_intersection(0, self.afw_intersection_1_test_01)

    @unittest.expectedFailure
    def test_afw_intersection_wrong_input_2(self):
        """ Tests an input different from a dict() object. [EXPECTED 
        FAILURE]"""
        AFW.afw_intersection(self.afw_intersection_1_test_01, 0)

    @unittest.expectedFailure
    def test_afw_intersection_wrong_dict_1(self):
        """ Tests a dict() in input different from a well formatted dict() 
        representing a AFW. [EXPECTED FAILURE]"""
        AFW.afw_intersection(self.afw_intersection_1_test_01,
                             {'goofy': 'donald'})

    @unittest.expectedFailure
    def test_afw_intersection_wrong_dict_2(self):
        """ Tests a dict() in input different from a well formatted dict() 
        representing a AFW. [EXPECTED FAILURE]"""
        AFW.afw_intersection({'goofy': 'donald'},
                             self.afw_intersection_1_test_01)

    def test_afw_intersection_side_effects_1(self):
        """ Tests the function makes side effect on the first input """
        before = copy.deepcopy(self.afw_intersection_1_test_01)
        AFW.afw_intersection(self.afw_intersection_1_test_01,
                             self.afw_intersection_2_test_01)
        self.assertEqual(before, self.afw_intersection_1_test_01)

    def test_afw_intersection_side_effects_2(self):
        """ Tests the function makes side effect on the second input """
        before = copy.deepcopy(self.afw_intersection_2_test_01)
        AFW.afw_intersection(self.afw_intersection_1_test_01,
                             self.afw_intersection_2_test_01)
        self.assertEqual(before, self.afw_intersection_2_test_01)


class TestAfwNonemptinessCheck(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.afw_nonemptiness_check_test_1 = automata_IO.afw_json_importer(
            './tests/json/afw/afw_nonemptiness_check_test_1.json')
        self.afw_nonemptiness_check_test_2 = automata_IO.afw_json_importer(
            './tests/json/afw/afw_nonemptiness_check_test_2.json')
        self.afw_nonemptiness_check_test_empty = {
            'alphabet': set(),
            'states': set(),
            'initial_state': None,
            'accepting_states': set(),
            'transitions': {}
        }

    def test_afw_nonemptiness_check(self):
        """ Tests a correct afw nonemptiness check """
        self.assertTrue(
            AFW.afw_nonemptiness_check(self.afw_nonemptiness_check_test_1))

    def test_afw_nonemptiness_check_false(self):
        """ Tests a correct afw nonemptiness check, where the afw is empty """
        self.assertFalse(
            AFW.afw_nonemptiness_check(self.afw_nonemptiness_check_test_2))

    def test_afw_nonemptiness_check_empty(self):
        """ Tests the nonemptiness of an empty afw"""
        self.assertFalse(
            AFW.afw_nonemptiness_check(self.afw_nonemptiness_check_test_empty))

    @unittest.expectedFailure
    def test_afw_nonemptiness_check_wrong_dict(self):
        """ Tests the nonemptiness of an input dict different from a dict 
        representing a afw. [EXPECTED FAILURE] """
        self.assertFalse(AFW.afw_nonemptiness_check({}))

    @unittest.expectedFailure
    def test_afw_nonemptiness_check_wrong_input(self):
        """ Tests the nonemptines of an input different from a dict object. 
        [EXPECTED FAILURE] """
        self.assertFalse(AFW.afw_nonemptiness_check(0))

    def test_afw_nonemptiness_check_side_effects(self):
        """ Tests that the function doesn't make any side effect on the 
        input"""
        before = copy.deepcopy(self.afw_nonemptiness_check_test_1)
        AFW.afw_nonemptiness_check(self.afw_nonemptiness_check_test_1)
        self.assertDictEqual(before, self.afw_nonemptiness_check_test_1)


class TestAfwNonuniversalityCheck(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.afw_nonuniversality_check_test_1 = automata_IO.afw_json_importer(
            './tests/json/afw/afw_nonuniversality_check_test_1.json')
        self.afw_nonuniversality_check_test_2 = automata_IO.afw_json_importer(
            './tests/json/afw/afw_nonuniversality_check_test_2.json')
        self.afw_nonuniversality_check_test_empty = {
            'alphabet': set(),
            'states': set(),
            'initial_state': None,
            'accepting_states': set(),
            'transitions': {}
        }

    def test_afw_nonuniversality_check(self):
        """ Tests a correct afw nonuniversality check """
        self.assertTrue(AFW.afw_nonuniversality_check(
            self.afw_nonuniversality_check_test_1))

    def test_afw_nonuniversality_check_false(self):
        """ Tests a correct afw nonuniversality check, where the afw is 
        empty """
        self.assertFalse(AFW.afw_nonuniversality_check(
            self.afw_nonuniversality_check_test_2))

    def test_afw_nonuniversality_check_empty(self):
        """ Tests the nonuniversality of an empty afw"""
        self.assertFalse(AFW.afw_nonuniversality_check(
            self.afw_nonuniversality_check_test_empty))

    @unittest.expectedFailure
    def test_afw_nonuniversality_check_wrong_dict(self):
        """ Tests the nonuniversality of an input dict different from a dict 
        representing a afw. [EXPECTED FAILURE] """
        self.assertFalse(AFW.afw_nonuniversality_check({}))

    @unittest.expectedFailure
    def test_afw_nonuniversality_check_wrong_input(self):
        """ Tests the nonuniversality of an input different from a dict 
        object. [EXPECTED FAILURE] """
        self.assertFalse(AFW.afw_nonuniversality_check(0))

    def test_afw_nonuniversality_check_side_effects(self):
        """ Tests that the function doesn't make any side effect on the 
        input"""
        before = copy.deepcopy(self.afw_nonuniversality_check_test_1)
        AFW.afw_nonuniversality_check(self.afw_nonuniversality_check_test_1)
        self.assertDictEqual(before, self.afw_nonuniversality_check_test_1)
