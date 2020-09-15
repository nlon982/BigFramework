import hou

# A framework to quickly make node setups / configure parameters
# Made by Nathan Longhurst

def parameter_processor(the_node, params): # I wrote the_node in order to not confuse with 'a_node', which means housing node.
    while "!" in params:
        #print(params)
        param_name = params[1:params.find(":")] # we know the first digit is going to be !
        end = params[1:].find("!") + 1 # index is in terms of 'params' because of +1. Very cool.
        if end == 0:
            end = len(params)
        param_content = params[params.find(":") + 1: end]
        set_parms(the_node, param_name, param_content)
        params = params[end:]


def set_parms(the_node, param_name, param_content):
    if param_content[0:3] == "int": # this if/else provides a way to manage types in params. "str" is default, so no need to declare.
        param_content = int(param_content[3:])
    elif param_content[0:3] == "str":
        param_content = param_content[3:] 
    the_node.setParms({param_name: param_content})
    #print("do the following on this node: {} . param_name : {} . param_content : {}".format(node.path(), param_name, param_content))

def get_name_and_type(entry):
    if "-" in entry: # has name
        seperator_location = entry.find("-")
        entry_type = entry[:seperator_location]
        entry_name = entry[seperator_location + 1:]            
    else:
        entry_type = entry
        entry_name = None
    return entry_type, entry_name

def parameter_temp_processor(entry):
    if "!" in entry:
        entry_without_param = entry[:entry.find("!")]
        params = entry[entry.find("!"):]
        return entry_without_param, params
    return entry, None


def setup(a_node, entry_1, entry_2, entry_3, entry_4):
    entry_1, params_entry_1 = parameter_temp_processor(entry_1)
    entry_3, params_entry_3 = parameter_temp_processor(entry_3) # seperates parameters from entry
    #from here on, entry_1 and entry_3, contains only their type and name. I chose to write this comment instead of doing it in variable names

    if entry_1[0] == "c": # create
        entry_1_type, entry_1_name = get_name_and_type(entry_1[1:])
        output_node = a_node.createNode(entry_1_type, entry_1_name)
    elif entry_1[0] == "e": # existing
        output_node = hou.node("{}/{}".format(a_node.path(), entry_1[1:]))
    else:
        raise Exception("BAD INPUT entry_1: {}, no 'c' or 'e' at start.".format(entry_1))

    if entry_2[0] == "i":
        output_connector_int = int(entry_2[1:])
    elif entry_2[0] == "n":
        output_connector_int = output_node.outputIndex(entry_2[1:])
    else:
        raise Exception("BAD INPUT entry_2: {}, no 'i' or 'n' at start.".format(entry_2))

    if entry_3[0] == "c": # create
        entry_3_type, entry_3_name = get_name_and_type(entry_3[1:])
        input_node = a_node.createNode(entry_3_type, entry_3_name)
    elif entry_3[0] == "e": # existing
        input_node = hou.node("{}/{}".format(a_node.path(), entry_3[1:]))
    else:
        raise Exception("BAD INPUT entry_3: {}, no 'c' or 'e' at start.".format(entry_3))

    if entry_4[0] == "i":
        input_connector_int = int(entry_4[1:])
    elif entry_4[0] == "n":
        input_connector_int = input_node.inputIndex(entry_4[1:])
    else:
        raise Exception("BAD INPUT entry_4: {}, no 'i' or 'n' at start.".format(entry_4))

    if params_entry_1 is not None:
        parameter_processor(output_node, params_entry_1)
    if params_entry_3 is not None:
        parameter_processor(input_node, params_entry_3)

    input_node.setInput(input_connector_int, output_node, output_connector_int)


def string_processor(a_node, a_string):
    a_list = a_string.split(" ")
    
    # clean any might've accidental spaces etc.
    while "" in a_list:
        a_list.remove("")
    while " " in a_list:
        a_list.remove(" ")
    
    if len(a_list) % 4 != 0: # error prevention
        print("Not divisible by 4")
        return

    while len(a_list) != 0:
        entry_1 = a_list[0]
        entry_2 = a_list[1]
        entry_3 = a_list[2]
        entry_4 = a_list[3]
        setup(a_node, entry_1, entry_2, entry_3, entry_4) 
        # ^ how about, a return type, that may or may not be used, which if used again, allows for the interpretting to not be done so much.
        a_list = a_list[4:]

    a_node.layoutChildren() # assuming that if used at 'setp_object' line, or at the end (here), has no difference. It is worth trying though.


