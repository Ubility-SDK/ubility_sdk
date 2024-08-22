import random
########################################## TEXT OPERATIONS  ##########################################

def text_capitalize_input(params):
    try:
        if "inputText" in params:
            if "\\n" in params['inputText']: # replace all \\n and \\t from UI to real tab and new line
                params['inputText'] = params['inputText'].replace("\\n","\n")
            if "\\t" in params['inputText']:
                params['inputText'] = params['inputText'].replace("\\t","\t")
            capitalized_text = params['inputText'].capitalize()
            return capitalized_text
        else:
            raise Exception("Missing Required Parameter(s)")
    except Exception as e:
        raise Exception(e)


def text_lowercase_input(params):
    try:
        if "\\n" in params['inputText']: # replace all \\n and \\t from UI to real tab and new line
                params['inputText'] = params['inputText'].replace("\\n","\n")
        if "\\t" in params['inputText']:
                params['inputText'] = params['inputText'].replace("\\t","\t")
        if "inputText" in params:
            lowercase_text = params['inputText'].lower()
            return lowercase_text
        else:
            raise Exception("Missing Required Parameter(s)")
    except Exception as e:
        raise Exception(e)
    
def text_title_input(params):
    try:
        if "\\n" in params['inputText']: # replace all \\n and \\t from UI to real tab and new line
                params['inputText'] = params['inputText'].replace("\\n","\n")
        if "\\t" in params['inputText']:
                params['inputText'] = params['inputText'].replace("\\t","\t")
        if "inputText" in params:
            title_text = params['inputText'].title()
            return title_text
        else:
            raise Exception("Missing Required Parameter(s)")
    except Exception as e:
        raise Exception(e)
    
    
def text_uppercase_input(params):
    try:
        if "inputText" in params:
            if "\\n" in params['inputText']: # replace all \\n and \\t from UI to real tab and new line
                params['inputText'] = params['inputText'].replace("\\n","\n")
            if "\\t" in params['inputText']:
                params['inputText'] = params['inputText'].replace("\\t","\t")
            uppercase_text = params['inputText'].upper()
            return uppercase_text
        else:
            raise Exception("Missing Required Parameter(s)")
    except Exception as e:
        raise Exception(e)
    
def text_get_input_length(params):
    try:
        if "inputText" in params:
            text_length = 0
            if params["IgnoreWhiteSpace"] == "True":
                no_whiteSpace_text = params['inputText'].replace(" ","")
                no_newlines_text = no_whiteSpace_text.replace("\n","")
                text_length = len(no_newlines_text)
            else:
                text_length = len(params['inputText'])
            return text_length
        else:
            raise Exception("Missing Required Parameter(s)")
    except Exception as e:
        raise Exception(e)
    
    
def text_find_value_in_input(params):
    try:
        if "inputText" in params and "valueToFind" in params:
            if "\\n" in params['inputText']: # replace all \\n and \\t from UI to real tab and new line
                params['inputText'] = params['inputText'].replace("\\n","\n")
            if "\\t" in params['inputText']:
                params['inputText'] = params['inputText'].replace("\\t","\t")
            start_index = 0
            if "skipCharacters" in params and "skipCharacters":
                start_index = params['inputText'].find(params['valueToFind'],params['skipCharacters'])
            else:
                start_index = params['inputText'].find(params['valueToFind'])
            if start_index != -1:
                return f"The substring '{params['valueToFind']}' appears at index {start_index} in your input string."
            else:
                return f"The substring '{params['valueToFind']}' does not appear in your input text"
    except Exception as e:
        raise Exception(e)
    
    
def text_split_input_text(params):
    try:
        if "inputText" in params:
            if "\\n" in params['inputText']: # replace all \\n and \\t from UI to real tab and new line
                params['inputText'] = params['inputText'].replace("\\n","\n")
            if "\\t" in params['inputText']:
                params['inputText'] = params['inputText'].replace("\\t","\t")
            split_response= ''
            if "separator" in params and "separator": 
                if params['separator'] == "[:newLine:]":
                    split_text = params['inputText'].split("\n")
                    split_response = split_text
                elif params['separator'] == "[:tab:]":
                    split_text = params['inputText'].split("\t")
                    split_response = split_response
                else:
                    split_text = params['inputText'].split(params['separator'])
                    split_response = split_text  
            else:
                split_text = params['inputText'].split()
                split_response = split_text
                
            if params['segmentIndex'] != "all" and params['segmentIndex'] !="fields":
                    split_response = split_text[params['segmentIndex']]
            elif params['segmentIndex'] == "all": #Returns the response as line-items
                split_response =split_text
            else: #Returns the response as separate_fields
                dictionary_format = {}
                for i,item in enumerate(split_text):
                    print(item)
                    key = f"Output_item_{i+1}"
                    dictionary_format[key] = item
                    print(dictionary_format)
                split_response = dictionary_format            
            return split_response
        else:
            raise Exception("Missing Required Parameter(s)")
        
    except Exception as e:
        raise Exception(e)
    
    
    
def text_replace_a_string_in_input(params):
    try:
        if "inputText" in params and "find" in params:
            replaced_text = ""
            if "\\n" in params['inputText']: # replace all \\n and \\t from UI to real tab and new line
                params['inputText'] = params['inputText'].replace("\\n","\n")
            if "\\t" in params['inputText']:
                params['inputText'] = params['inputText'].replace("\\t","\t")
            if "replace" in params and "replace":
                if params['find'] == "[:space:]":
                    replaced_text = params['inputText'].replace(" ",params['replace'])
                elif params['find'] == "[:tab:]":
                    replaced_text = params['inputText'].replace("\t",params['replace'])
                elif params['find'] == "[:newLine:]":
                    replaced_text = params['inputText'].replace("\n",params['replace'])
                else:
                    replaced_text = params['inputText'].replace(params['find'],params['replace'])
            else:
                if params['find'] == "[:space:]":
                    replaced_text = params['inputText'].replace(" ","")
                elif params['find'] == "[:tab:]":
                    replaced_text = params['inputText'].replace("\t","")
                elif params['find'] == "[:newLine:]":
                    replaced_text = params['inputText'].replace("\n","")
                else:
                    replaced_text = params['inputText'].replace(params['find'],"")
            return replaced_text
        else:
            raise Exception("Missing Required Paramters(s)")
    except Exception as e:
        raise Exception(e)




########################################## NUMBER OPERATIONS  ##########################################
    
def number_generate_random_numbers(params):
    try:
        if "lowerRange" in params and "upperRange" in params:
            random_number =0
            if "decimalPoints" in params and "decimalPoints":
                random_number=round(random.uniform(params['lowerRange'],params['upperRange']),params['decimalPoints'])
            else:
                random_number = random.randrange(params['lowerRange'],params['upperRange'])
            if params['decimalPoints'] == 0: #convert to integer if the decimal point is 0
                random_number = int(random_number)
            return random_number
        else:
            raise Exception("Missing Required Parameter(s)")
    except Exception as e:
        raise Exception(e)    
