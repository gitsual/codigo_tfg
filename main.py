# Import the sympy module
from sympy import *

# List of characteristics
## All characteristics
c_dict = {}

## Wrong characteristics
w_list = []

## Right characteristics
r_list = []

## Relation characteristics
s_dict = []

# Conditions
## Define the conditions
cond_list = []

# Define the variables
x, y, z = symbols('x, y, z')


def load_string(string):
    # Load a string
    return string


def load_list(list_name):
    # Load a list of strings
    return list_name


def load_lists():
    # Load the lists and the conditions
    global w_list, r_list, s_dict, c_dict

    c_dict = retrieve_characteristics_dict('CHARACTERISTICS')
    r_list = retrieve_characteristics_list('RIGHT_SUBCHARACTERISTICS')
    w_list = retrieve_characteristics_list('WRONG_SUBCHARACTERISTICS')
    # TODO
    s_dict = retrieve_characteristics_dict('RELATION_CHARACTERISTICS')


def print_lists():
    # Print the lists
    print('W:', w)
    print('R:', r)
    print('S:', s)
    print('R:', r)


def judge_action(action, alternatives, tab):
    # Judge an action
    # Count the number of characteristics in each list
    w_count = 0
    s_count = 0
    r_count = 0

    for item in action:
        if item in w_list:
            w_count += 1
        if item in r_list:
            r_count += 1
        if item in s_list:
            relationship_type = get_item_from_s_list(item).split('-')[2]
            s_count += 0.5
            if relationship_type == 'positive':
                r_count += 0.5
            else:
                w_count += 0.5
            r_count += 1

    # Print the result
    if w_count == 0 and r_count == 0 and s_count == 0:
        print('\t'*tab + 'The action is neutral.')
        return None
    else: # w_count > 0 or r_count > 0 or s_count > 0
        if w_count > 0 and r_count == 0 and s_count == 0:
            print('\t'*tab + 'The action is inadmissible.')
            return None
        elif r_count > 0 and w_count == 0 and s_count == 0:
            print('\t'*tab + 'The action is necessary.')
            return None
        elif r_count > 0 and w_count > 0 and s_count > 0:
            if alternatives != []:
                for alternative in alternatives:
                    alternative_action = judge_action(alternative, [], tab+1)
                    if alternative_action is not None:
                        if r_count > w_count:
                            print('\t'*tab + 'The action is not morally permissible if the alternative "' + alternative_action + '" action is morally permissible.')
                            return action
                        else:
                            print('\t'*tab + 'The action is morally permissible if the alternative action "' + alternative_action + '" is not morally permissible.')
                            return action
        elif r_count > 0 and w_count > 0 and s_count == 0:
            if r_count > w_count:
                print('\t'*tab + 'The action is permissible.')
                return action
            else:
                print('\t'*tab + 'The action is not permissible.')
                return action
        else:
            print('\t'*tab + 'The action is complex.')
            return None


def judge_actions(actions, alternatives):
    # Judge a list of actions
    if alternatives is not {}:
        for action, alternatives in zip(actions, alternatives):
            judge_action(action, alternatives, 1)
    else:
        for action in actions:
            judge_action(action, [], 1)

def get_file_path():
    file_path = os.path.dirname(os.path.abspath(__file__))
    return file_path


def retrieve_characteristics_dict(section):
    lines = read_conf_properties_file()

    # Create a dictionary of the properties
    properties = {}

    # Ignore bad written syntax cases
    retrieve = False
    for line in lines:
        if line.startswith('#'):
            continue
        elif line.startswith('\n'):
            continue
        elif line.startswith('\r\n'):
            continue
        elif line.startswith('\r'):
            continue
        elif line.startswith(' '):
            retrieve = False
            continue
        elif line.startswith('\t'):
            continue
        elif line.startswith('\f'):
            continue
        elif line.startswith('\v'):
            continue
        else:
            if line.startswith('[' + section + ']'):
                retrieve = True
            else:
                if retrieve:
                    key, value = line.split('=')
                    properties[key] = value.strip()
    return properties


def retrieve_characteristics_list(section):
    lines = read_conf_properties_file()

    # Create a dictionary of the properties
    properties = {}

    # Ignore bad written syntax cases
    for line in lines:
        if line.startswith('#'):
            continue
        if line.startswith('\n'):
            continue
        if line.startswith('\r\n'):
            continue
        if line.startswith('\r'):
            continue
        if line.startswith(' '):
            continue
            retrieve = False
        if line.startswith('\t'):
            continue
        if line.startswith('\f'):
            continue
        if line.startswith('\v'):
            continue
        else:
            if line.startswith('[' + section + ']'):
                retrieve = True
            else:
                if retrieve:
                    key, _ = line.split('=')
                    properties.append(key)
    return properties


def read_conf_properties_file():
    # Read the conf.properties file
    with open(get_file_path() + '\conf.properties', 'r') as f:
        lines = f.readlines()
    return lines


def select_characteristic():
    # Print the index number and the content of the keys of the 'c_dict' dictionary
    for i, key in enumerate(c_dict.keys()):
        print(i, key)
    # Make the user select one by number
    while True:
        try:
            selection = int(input('Select one by number: '))
            if selection in range(len(c_dict.keys())):
                break
            else:
                print('Please select a number between 0 and ' + str(len(c_dict.keys()) - 1))
        except ValueError:
            print('Please select a number between 0 and ' + str(len(c_dict.keys()) - 1))
    # Return the index number and the content of the selected index in the 'c_dict' dictionary
    return selection, c_dict[list(c_dict.keys())[selection]]


def insert_actions_and_alternatives():
    actions = {}
    action_alternatives = {}

    while True:  # Insert a list of actions
        action = []
        alternatives = {}
        while True:  # Insert an action
            action_name = input('Enter the name of the action: ')
            if action_name == '':
                break
            while True:
                print('Select the characteristics of the action "' + action + '": ')
                number_selected, characteristic_selected = select_characteristic()
                if number_selected == 0:
                    break
            action.append(characteristic_selected)
        actions[action_name].append(action)
        while True:  # Insert alternatives for that action
            alternative_name = input('Enter the name of the alternative for the action "' + action + '": ')
            if alternative_name == '':
                break
            while True:
                print('Select the characteristics of the alternative "' + alternative_name + '": ')
                number_selected, characteristic_selected = select_characteristic()
                if number_selected == 0:
                    break
            alternatives[alternative_name] = alternatives
        action_alternatives[action_name].append(alternatives)
        another = input('Do you want to enter another action? (y/N)')
        if another == '' or another == ' ' or another == 'N' or another == 'n':
            break
    return actions, action_alternatives


def read_nlp_data():
    with open(get_file_path() + '\\nlp__text.txt', 'r') as f:
        data = f.readlines()
    return data


def get_capacitist_words():
    return ['cojo',
            'coja',
            'loco',
            'loca',
            'estúpido',
            'estúpida',
            'autista',
            'retrasado',
            'retrasada',
            'idiota',
            'imbécil',
            'trastornado',
            'trastornada',
            'psicópata',
            'esquizo',
            'hervor',
            'chiflado',
            'chiflada']


def get_inclusive_words():
    return ['con capacidades diferentes',
            'neurodivergente',
            'discapacitado',
            'discapacitado cognitivo',
            'discapacitada cognitiva',
            'discapacitada intelectual',
            'disléxico',
            'minusválido',
            'minusválida'
            ]


def detect_nlp_actions_and_alternatives(phrase):
    actions = {}
    action_alternatives = {}

    capacitist_words = get_capacitist_words()
    for capacitist_word in capacitist_words:
        if capacitist_word in phrase:
            actions['capacitismo'].append(capacitist_word)
            w_list.append(capacitist_word)

    """
    racist_words = get_racist_words()
    for racist_word in racist_words:
        if racist_word in phrase:
            actions['racismo'].append(racist_word)
            w_list.append(racist_word)
    """

    inclusive_words = get_inclusive_words()
    for inclusive_word in inclusive_words:
        if inclusive_word in phrase:
            actions['inclusividad'].append(inclusive_word)
            r_list.append(inclusive_word)

    return actions, {}


def main():
    # Load the lists
    load_lists()

    # Print the lists
    print_lists()

    # Prompt the user to get the actions and its alternatives
    # actions, actions_alternatives = insert_actions_and_alternatives()

    # Judge the of actions
    # judge_actions(actions, actions_alternatives)

    # or Retrieve the actions and its alternatives from NLP text
    nlp_data = read_nlp_data()
    for phrase in nlp_data:
        actions, actions_alternatives = detect_nlp_actions_and_alternatives(phrase)

        # Judge the of actions
        judge_actions(actions, actions_alternatives)


"""
def judge_overcoming(actions):
    # Judge a list of overcoming
    # So, if according to the Moral Framework you have a moral obligation to do something, but then something happens that makes you no longer have that obligation, this is called \textbf{Overcoming} an obligation. For example, if you have a moral obligation to help a stranger, but later discover that the stranger is a thief, the new information \textit{outweighs} the obligation.
    for action in actions:
        judge_action(action)


def judge_neutralize(actions):
    # Judge a list of neutralize
    # \textbf{Neutralize} an obligation means that the obligation no longer exists, but is not due to any new information. For example, if you have a moral obligation to help a stranger, but then the stranger helps you, the obligation is \textit{neutralized} because you no longer need to help the stranger.
    for action in actions:
        judge_action(action)


def judge_reversing(actions):
    # Judge a list of reversing
    # \textbf{Reversing} an obligation means that the obligation now exists where it did not exist before. For example, if you have a moral obligation to help a stranger, but then the stranger harms you, the obligation is \textit{reversed} because you now have an obligation to harm the stranger.
    for action in actions:
        judge_action(action)


def judge_weakening(actions):
    # Judge a list of weakening
    # \textbf{Weakening} an obligation means that the obligation is not as strong as it was before. For example, if you have a moral obligation to help a stranger, but then you find out that the stranger is a bit mean, the obligation is \textit{weakened} because now you don't have to help the stranger as much.
    for action in actions:
        judge_action(action)


def judge_dissolving(actions):
    # Judge a list of dissolving
    # \textbf{Dissolving} an obligation means that the obligation no longer exists, and it is because of the same information that the obligation existed in the first place. For example, if you have a moral obligation to help a stranger, but then the stranger says \textit{no thanks}, the obligation \textit{dissolves} because the reason you had the obligation in the first place was because the stranger needed help, and now the stranger doesn't need help.
    for action in actions:
        judge_action(action)


def judge_cancel(actions):
    # Judge a list of cancel
    # \textbf{Cancel} an obligation means that the obligation no longer exists, but is not due to any new information. For example, if you have a moral obligation to help a stranger, but then the stranger releases you from that obligation, the obligation is \textit{canceled} because the obligation no longer exists, but it is not due to any new information.
    for action in actions:
        judge_action(action)


def judge_destroying(actions):
    # Judge a list of destroying
    for action in actions:
        judge_action(action)


def judge_void(actions):
    # Judge a list of void
    # \textbf{Voiding} an obligation means that the obligation no longer exists, and it is because of the same information that the obligation existed in the first place.
    for action in actions:
        judge_action(action)


def judge_invalidating(actions):
    # Judge a list of invalidating
    for action in actions:
        judge_action(action)
"""


if __name__ == '__main__':
    main()