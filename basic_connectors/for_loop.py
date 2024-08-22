def prepare_results(results):
    try:
        counter = 0
        response = {}
        for result in results:
            if "ResponseWebhook" in result:
                result.pop("ResponseWebhook")
            response[f"loop_{counter}"] = result
            counter += 1

        nb_of_items = len(response)
        response["count"] = nb_of_items
        return response
    except Exception as error:
        raise Exception(error)