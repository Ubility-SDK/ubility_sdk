import datetime
from dateutil.relativedelta import relativedelta
import pytz
################## STATIC DATA ################

DateTime_Formats = {
    "DD/MM/YY":"%d/%m/%y",
    "DD/MM/YYYY":"%d/%m/%Y",
    "DD-MM-YYYY":"%d-%m-%Y",
    "MM/DD/YY":"%m/%d/%y",
    "MM/DD/YYYY":"%m/%d/%Y",
    "MM-DD-YYYY":"%m-%d-%Y",
    "YYYY-MM-DD":"%Y-%m-%d",
    "YYYY-MM-DD HH:mm:ss Z":"%Y-%m-%d %H:%M:%S %z",
    "YYYY-MM-DDTHH:mm:ssZ":"%Y-%m-%dT%H:%M:%S%z",
    "MMM DD YYYY":"%b %d %Y",
    "MMMM DD YYYY":"%B %d %Y",
    "MMMM DD YYYY HH:mm:ss":"%B %d %Y %H:%M:%S",
    "ddd MMM DD HH:mm:ss Z YYYY":"%a %b %d %H:%M:%S %z %Y",
    "X":"UniX TimeStamp"
}


################################################ FORMAT OPERATION ##############################################

########## TimeZone Offset Functions ##########

def datetime_has_timezone_offset(format,input):
    try:
        character_to_check = "Z"
        timezone_offset_direction = ['+','-']
        if character_to_check in format:
            # check timezone offset direction
            if timezone_offset_direction[0] in input:
                # separate datetime and offset
                split_result = input.split('+') 
                # put the choosed operator before the offset
                offset_part = "+"+split_result[1] 
                return offset_part
            elif timezone_offset_direction[1] in input:
                if "T" not in input: 
                    split_result = input.split(' -')
                    offset_part = "-"+split_result[1]
                    return offset_part
                else: #if the format is YYYY-MM-DDTHH:mm:ssZ
                    split_result = input.rsplit('-',maxsplit=1) #split on the last '-' to get offset
                    offset_part = "-"+split_result[1]
                    return offset_part
            else: 
                raise Exception("Invalid timezone offset")                
        else:
            return "No Offset"       
    except ValueError as ve:
        raise Exception(f"Input date string does not match the specified format: {ve}")
    except Exception as e:
        raise Exception(e)
    

       
def datetime_adjust_date_by_timezone_offset(offset_string,input_date):
    try:
        if ":" in offset_string:
            # Get hours,minutes and sign from the offset string
            sign = offset_string[0]
            hours = int(offset_string[1:3])
            minutes = int(offset_string[4:6])
            offset_value = relativedelta(hours=hours,minutes=minutes)
            if sign == "+":
                final_date = input_date - offset_value
            else:
                final_date = input_date + offset_value
            # Set the timezone of the resulting datetime object to UTC
            final_date = final_date.replace(tzinfo=datetime.timezone.utc)
            return final_date
        else:
            raise Exception("The timeZone offset should be +HH:mm or -HH:mm")
    except Exception as e:
        raise Exception(e)


########## Format Functions ##########

def datetime_format_to_UnixTimeStamp(params):
    try:
        from_timezone = pytz.timezone(params['FromTimeZone'])
        target_timezone = pytz.timezone(params['ToTimeZone'])
        if params['FromFormat'] != "X" and params['ToFormat'] == "X":
            output_date = None
            # parse the input string as date object
            input_date= datetime.datetime.strptime(params['input'],DateTime_Formats[params['FromFormat']])
            offset_response = datetime_has_timezone_offset(params['FromFormat'],params['input'])
            if offset_response !="No Offset": # if yes
                # adjust the date according to the offset provided
                adjusted_date = datetime_adjust_date_by_timezone_offset(offset_response,input_date)
                # Convert the date to the desired timezone
                dateWithDesiredTimeZone = adjusted_date.astimezone(target_timezone)
                output_date = dateWithDesiredTimeZone.timestamp()
            else: # if there is no timezone offset
                # Add timezone information to the input date 
                fromTimeZone = from_timezone.localize(input_date)
                dateWithDesiredTimeZone = fromTimeZone.astimezone(target_timezone)
                unix_timestamp = int(dateWithDesiredTimeZone.timestamp())
                output_date= unix_timestamp
            return output_date
        else:
            return "Maybe From Unix TimeStamp Format"
    except ValueError as ve:
        raise Exception(f"Input date string does not match the specified format: {ve}")
    except Exception as e:
        raise Exception(e)
    
    
    
def datetime_format_from_UnixTimeStamp(params):
    try:
        if params['FromFormat'] == "X" and params['ToFormat'] != "X":
            from_timezone = pytz.timezone(params['FromTimeZone'])
            target_timezone = pytz.timezone(params['ToTimeZone'])
            # parse the input as integer
            integer_unix_timestamp = int(params['input']) 
            # convert the integer to date obj
            input_date = datetime.datetime.fromtimestamp(integer_unix_timestamp)
            fromTimeZone = from_timezone.localize(input_date)
            dateWithDesiredTimeZone = fromTimeZone.astimezone(target_timezone)
            # Format the datetime object into the desired output format  
            output_date = datetime.datetime.strftime(dateWithDesiredTimeZone,DateTime_Formats[params['ToFormat']]) 
            return output_date
        else:
            return "No Unix-TimeStamp Format"
    except ValueError as ve:
        raise Exception(f"Input date string does not match the specified format: {ve}")
    except Exception as e:
        raise Exception(e)
    


def datetime_format_to_any_format(params):
    try:
        if params['FromFormat'] !="X" and params['ToFormat'] != "X":
            output_date = None
            adjusted_date = None
            from_timezone = pytz.timezone(params['FromTimeZone'])
            target_timezone = pytz.timezone(params['ToTimeZone'])
            input_date= datetime.datetime.strptime(params['input'],DateTime_Formats[params['FromFormat']])
            offset_response = datetime_has_timezone_offset(params['FromFormat'],params['input'])
            if offset_response !="No Offset":
                adjusted_date = datetime_adjust_date_by_timezone_offset(offset_response,input_date)
                dateWithDesiredTimeZone = adjusted_date.astimezone(target_timezone)
                output_date = dateWithDesiredTimeZone
            else:
                fromTimeZone = from_timezone.localize(input_date)
                dateWithDesiredTimeZone = fromTimeZone.astimezone(target_timezone)
                output_date = dateWithDesiredTimeZone
            # Format the datetime object into the desired output format 
            output_date = dateWithDesiredTimeZone.strftime(DateTime_Formats[params['ToFormat']])
            return output_date
        else:
            return "No Unix TimeStamp Format"
    except ValueError as ve:
            raise Exception(f"Input date string does not match the specified format: {ve}")
    except Exception as e:
        raise Exception(e)



def datetime_format_check_if_date_is_current_datetime(params):
    try:
        if params['option'] == "now":
            if "ToFormat" in params and "ToTimeZone" in params:
                output_date = None
                toTimeZone = pytz.timezone(params['ToTimeZone'])
                if params['ToFormat'] != 'X':
                    current_datetime = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
                    datetime_with_desired_timezone = current_datetime.astimezone(toTimeZone)
                    formatted_date = datetime.datetime.strftime(datetime_with_desired_timezone,DateTime_Formats[params['ToFormat']])
                    output_date = formatted_date
                else:
                    current_datetime = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
                    datetime_with_desired_timezone = current_datetime.astimezone(toTimeZone)
                    output_date = datetime_with_desired_timezone.timestamp()
                return output_date  
        else:
            raise Exception(f"{params['option']} should be 'now'")      
    except ValueError as ve:
            raise Exception(f"Input date string does not match the specified format: {ve}")
    except Exception as e:
        raise Exception(e)


######################## Main Function ##########################


def datetime_format_operation(params):
    try:
        if params['option'] != "now":
            if "ToFormat"in params and "input" in params and "FromFormat" in params and "ToTimeZone" in params:
                output_date = None
                check_to_unix = datetime_format_to_UnixTimeStamp(params)
                if check_to_unix != 'Maybe From Unix TimeStamp Format':
                    output_date = check_to_unix
                else:
                    check_from_unix = datetime_format_from_UnixTimeStamp(params)
                    if check_from_unix != 'No Unix-TimeStamp Format':
                        output_date = check_from_unix
                    else:
                        output_date = datetime_format_to_any_format(params)
                return output_date
            else:
                raise Exception("Missing Required Parameter(s)")
        else:
            output_date = datetime_format_check_if_date_is_current_datetime(params)
            return output_date
    except ValueError as ve:
        raise Exception(f"Input date string does not match the specified format: {ve}")
    except Exception as e:
        raise Exception(e)
    
    
    
    
############################ DATETIME GET CURRENT DATETIME OPERATION ############################

def datetime_get_current_datetime(params):
    try:
        if params['option'] == "now":
            if "TimeZone" in params and "Format" in params:
                    timeZone = pytz.timezone(params['TimeZone'])
                    output_date=None
                    if params['Format'] !='X':
                        current_datetime = datetime.datetime.now(tz=timeZone).replace(microsecond=0)
                        output_date = datetime.datetime.strftime(current_datetime,DateTime_Formats[params['Format']])
                    else:
                        # Get current time in the specified timezone
                        current_datetime = datetime.datetime.now(tz=timeZone).replace(microsecond=0)
                        output_date = current_datetime.timestamp()       
                    return output_date
            
            else:
                raise ValueError("Missing required parameters: 'input', 'TimeZone', and/or 'Format'.")
        else:
            raise Exception(f"{params['input']} should be 'now'")
    except Exception as e:
        raise Exception(e)
    



################################################ ADJUST OPERATION ##############################################


############  Accumulate Time Function  #############

def datetime_adjust_accumulate_time_changes(Expression):

    try:
        # Initialize counters for different time units
        monthNumber=0
        dayNumber = 0
        hourNumber =0
        minuteNumber =0
        for expr in Expression:
            if "sign" in expr and "number" in expr and "unit" in expr:
                unit = expr['unit']
                # Check the sign and adjust the number based on the sign provided
                if expr['sign'] == "+":
                    # Add the specified number to the corresponding counter
                    if unit == "month":
                        monthNumber += expr['number']
                    elif unit == "day":
                        dayNumber += expr['number']
                    elif unit == "hour":
                        hourNumber += expr['number']
                    elif unit == "minute":
                        minuteNumber += expr['number']
                    else:
                        raise Exception("Invalid unit")
                elif expr['sign'] == "-":
                    # Subtract the specified number from the corresponding counter
                    if unit == "month":
                        monthNumber -= expr['number']
                    elif unit == "day":
                        dayNumber -= expr['number']
                    elif unit == "hour":
                        hourNumber -= expr['number']
                    elif unit == "minute":
                        minuteNumber -= expr['number']
                    else:
                        raise Exception("Invalid unit")
                else:
                    raise Exception("Invalid sign")    
            else:
                raise Exception("Missing input Parameter(s)")
        return monthNumber,dayNumber,hourNumber,minuteNumber
    except Exception as e:
        raise Exception(e)



########## Format Functions ##########

def datetime_adjust_to_UnixTimeStamp(params):
    try:
        monthNumber,dayNumber,hourNumber,minuteNumber = datetime_adjust_accumulate_time_changes(params['Expression'])
        # create a time difference object based on the provided number
        # of months, days, hours, and minutes.
        timeAmount = relativedelta(months=monthNumber,days=dayNumber,hours=hourNumber,minutes=minuteNumber)
        if params['FromFormat'] != "X" and params['ToFormat'] == "X":
            output_date = None
            # parse the input string as date object
            input_date= datetime.datetime.strptime(params['input'],DateTime_Formats[params['FromFormat']])
            offset_response = datetime_has_timezone_offset(params['FromFormat'],params['input'])
            if offset_response !="No Offset": # if yes
                adjusted_date_offset = datetime_adjust_date_by_timezone_offset(offset_response,input_date)
                adjusted_date_time_difference = adjusted_date_offset + timeAmount
                output_date = adjusted_date_time_difference.timestamp()
            else: # if there is no timezone offset
                adjusted_date_time_difference = input_date + timeAmount
                unix_timestamp = int(adjusted_date_time_difference.timestamp())
                output_date= unix_timestamp
            return output_date
        else:
            return "Maybe From Unix TimeStamp Format"
    except ValueError as ve:
        raise Exception(f"Input date string does not match the specified format: {ve}")
    except Exception as e:
        raise Exception(e)
    
    
def datetime_ajdust_from_unix_timestamp(params):
    try:
        monthNumber,dayNumber,hourNumber,minuteNumber = datetime_adjust_accumulate_time_changes(params['Expression'])
        timeAmount = relativedelta(months=monthNumber,days=dayNumber,hours=hourNumber,minutes=minuteNumber)
        if params['FromFormat'] == "X" and params['ToFormat'] != "X":
            integer_unix_timestamp = int(params['input']) 
            input_date = datetime.datetime.fromtimestamp(integer_unix_timestamp)
            adjusted_date_time_difference = input_date + timeAmount
            return adjusted_date_time_difference
        else:
            return "No Unix-TimeStamp Format"
        
    except ValueError as ve:
        raise Exception(f"Input date string does not match the specified format: {ve}")
    except Exception as e:
        raise Exception(e)


def datetime_adjust_to_any_format(params):
    try:
        if params['FromFormat'] !="X" and params['ToFormat'] != "X":
            output_date = None
            adjusted_date = None
            input_date= datetime.datetime.strptime(params['input'],DateTime_Formats[params['FromFormat']])
            offset_response = datetime_has_timezone_offset(params['FromFormat'],params['input'])
            if offset_response !="No Offset":
                adjusted_date = datetime_adjust_date_by_timezone_offset(offset_response,input_date)
                output_date = adjusted_date
            else:
                output_date = input_date
            monthNumber,dayNumber,hourNumber,minuteNumber = datetime_adjust_accumulate_time_changes(params['Expression'])
            timeAmount = relativedelta(months=monthNumber,days=dayNumber,hours=hourNumber,minutes=minuteNumber)
            final_date = output_date + timeAmount
            return final_date
        else:
            return "Unix TimeStamp Format"
    except ValueError as ve:
            raise Exception(f"Input date string does not match the specified format: {ve}")
    except Exception as e:
        raise Exception(e)



def datetime_adjust_check_if_date_is_current_datetime(params):
    try:
        if params['option'] == "now":
            final_date = None
            current_date = datetime_get_current_datetime(params)
            if isinstance(current_date,float): #check if unix
                extracted_date = datetime.datetime.fromtimestamp(current_date)
                current_date =extracted_date
                monthNumber,dayNumber,hourNumber,minuteNumber = datetime_adjust_accumulate_time_changes(params['Expression'])
                timeAmount = relativedelta(months=monthNumber,days=dayNumber,hours=hourNumber,minutes=minuteNumber)
                final_date = current_date + timeAmount
                final_date = final_date.timestamp()
            else: # parse the string date as datetime object
                current_date = datetime.datetime.strptime(current_date,DateTime_Formats[params['Format']])
                monthNumber,dayNumber,hourNumber,minuteNumber = datetime_adjust_accumulate_time_changes(params['Expression'])
                timeAmount = relativedelta(months=monthNumber,days=dayNumber,hours=hourNumber,minutes=minuteNumber)
                final_date = current_date + timeAmount
                final_date = datetime.datetime.strftime(final_date,DateTime_Formats[params['Format']])
            return final_date
    except ValueError as ve:
        raise Exception(f"Input date string does not match the specified format: {ve}")
    except Exception as e:
        raise Exception(e)

######################## Main Function ##########################


def datetime_adjust_operation(params):
    try:
        if params['option'] !="now":
            if 'input' in params and "ToFormat" in params and "Expression" in params and "FromFormat" in params:
                output_date = None
                final_date = None
                check_to_unix = datetime_adjust_to_UnixTimeStamp(params)
                if check_to_unix != 'Maybe From Unix TimeStamp Format':
                    output_date = check_to_unix
                else:
                    check_from_unix = datetime_ajdust_from_unix_timestamp(params)
                    if check_from_unix != 'No Unix-TimeStamp Format':
                        output_date = check_from_unix
                    else:
                        output_date  = datetime_adjust_to_any_format(params)
                if isinstance(output_date, int): # if is in unix format
                    return output_date
                else:
                    final_date = datetime.datetime.strftime(output_date,DateTime_Formats[params['ToFormat']])
                    return final_date
            else:
                raise Exception("Missing Required Parameter(s)")
        else:
            output_date = datetime_adjust_check_if_date_is_current_datetime(params)
            return output_date
    except ValueError as ve:
        raise Exception(f"Input date string does not match the specified format: {ve}")
    except Exception as e:
        raise Exception(e)



################################################ COMPARE OPERATION ################################################



def datetime_compare_check_offset_existence(date_format):
    character_to_check = 'Z'
    if character_to_check in date_format:
        return True
    else:
        return False
    

######## Format Function ######## 

def datetime_compare_format_input_dates(params):
    try:
        adjusted_start_date = None
        adjusted_end_date = None
        start_date = datetime.datetime.strptime(params['startDateValue'],DateTime_Formats[params['startDateFormat']])
        end_date = datetime.datetime.strptime(params['endDateValue'],DateTime_Formats[params['endDateFormat']])
        start_date_result = datetime_compare_check_offset_existence(params['startDateFormat'])
        end_date_result = datetime_compare_check_offset_existence(params['endDateFormat'])
        # if only start_date has timezone offset
        if start_date_result == True and end_date_result == False:
            formatted_end_date = datetime.datetime.strftime(end_date,DateTime_Formats["YYYY-MM-DD HH:mm:ss Z"])
            adjusted_end_date = formatted_end_date + "+00:00"
            # parse the formatted date as datetime obj
            adjusted_end_date = datetime.datetime.strptime(adjusted_end_date,DateTime_Formats["YYYY-MM-DD HH:mm:ss Z"])
            adjusted_start_date = start_date
        # if only end_date has timezone offset
        elif start_date_result == False and end_date_result == True:             
            formatted_start_date = datetime.datetime.strftime(start_date,DateTime_Formats["YYYY-MM-DD HH:mm:ss Z"])
            adjusted_end_date = end_date
            adjusted_start_date = formatted_start_date + "+00:00"
            # parse the formatted date as datetime obj
            adjusted_start_date = datetime.datetime.strptime(adjusted_start_date,DateTime_Formats["YYYY-MM-DD HH:mm:ss Z"])
        else:
            adjusted_start_date = start_date
            adjusted_end_date = end_date
        return adjusted_start_date,adjusted_end_date
    except Exception as e:
        raise Exception(e)


########## Compare Function ##########

def datetime_compare_subtract_and_decompose_result(adjusted_start_date,adjusted_end_date):
    output_date_swapped = False
    days = 0
    hours = 0
    minutes = 0
    seconds = 0
    sub_result = adjusted_end_date - adjusted_start_date
    # if subtraction is negative
    if sub_result < datetime.timedelta(0):
        # Swap the two dates subtraction to get positive values
        output_date_swapped = True
        sub_result = adjusted_start_date - adjusted_end_date
    days = sub_result.days
    hours,remainder = divmod(sub_result.seconds,3600)
    minutes,remainder = divmod(remainder,60)
    seconds = remainder
    output_result = {
        "output_date_swapped":output_date_swapped,
        "days":days,
        "hours":hours,
        "minutes":minutes,
        "seconds":seconds
    }
    return output_result



def datetime_compare_check_if_date_is_current_date(params):
    try:
        if params['option'] == "now":
            adjusted_start_date = None
            adjusted_end_date = None
            current_date = datetime_get_current_datetime(params)
            current_date = datetime.datetime.strptime(current_date,DateTime_Formats[params['Format']])
            end_date = datetime.datetime.strptime(params['endDateValue'],DateTime_Formats[params['endDateFormat']])
            end_date_result = datetime_compare_check_offset_existence(params['endDateFormat'])
            current_date_result = datetime_compare_check_offset_existence(params['Format'])
            if current_date_result == True and end_date_result == False:
                formatted_end_date = datetime.datetime.strftime(end_date,DateTime_Formats["YYYY-MM-DD HH:mm:ss Z"])
                adjusted_end_date = formatted_end_date + "+00:00"
                # parse the formatted date as datetime obj
                adjusted_end_date = datetime.datetime.strptime(adjusted_end_date,DateTime_Formats["YYYY-MM-DD HH:mm:ss Z"])
                adjusted_start_date = current_date
            # if only end_date has timezone offset
            elif current_date_result == False and end_date_result == True:             
                formatted_start_date = datetime.datetime.strftime(current_date,DateTime_Formats["YYYY-MM-DD HH:mm:ss Z"])
                adjusted_end_date = end_date
                adjusted_start_date = formatted_start_date + "+00:00"
                # parse the formatted date as datetime obj
                adjusted_start_date = datetime.datetime.strptime(adjusted_start_date,DateTime_Formats["YYYY-MM-DD HH:mm:ss Z"])
            else:
                adjusted_start_date = current_date
                adjusted_end_date = end_date
            adjusted_start_date = adjusted_start_date.replace(tzinfo=datetime.timezone.utc)
            final_result = datetime_compare_subtract_and_decompose_result(adjusted_start_date,adjusted_end_date)
            return final_result
    except ValueError as ve:
            raise Exception(f"Input date string does not match the specified format: {ve}")
    except Exception as e:
        raise Exception(e)


####################### Main Function ####################### 

def datetime_compare_operation(params):
    try:
        if params['option'] !='now':
            if "startDateValue" in params and "endDateValue" in params and "endDateFormat" in params and "startDateFormat" :
                start_date, end_date = datetime_compare_format_input_dates(params)
                output_result = datetime_compare_subtract_and_decompose_result(start_date,end_date)
                return output_result
            else:
                raise Exception("Missing Required Parameter(s)")  
        else:
            output_result = datetime_compare_check_if_date_is_current_date(params)
            return output_result
    except ValueError as ve:
        raise Exception(f"Input date string does not match the specified format: {ve}")    
    except Exception as e:
        raise Exception(e)
