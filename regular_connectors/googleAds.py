from google.ads.googleads.client import GoogleAdsClient
from google.api_core import protobuf_helpers
import proto, json, hashlib




def create_client_instance(credential, login_customer_id):
    """
    Create a client instance of GoogleAdsClient using the provided credentials.

    :credentials: A dictionary containing credential parameters.
    
    - :clientID: (str, Required) - client_id acquired from OAuth2 flow
    - :clientSecret: (str, Required) - client_secret acquired from OAuth2 flow
    - :refreshToken: (str, Required) - refresh_token acquired from OAuth2 flow
    - :developerToken: (str, Required) - developer_token acquired according to this `link <https://developers.google.com/google-ads/api/docs/first-call/dev-token>`_.
    
    
    :loginCustomerId: (str, Required) - the customer ID of the authenticated manager account. It should be set without dashes.
    
    :return: A GoogleAdsClient instance.
    :rtype: GoogleAdsClient object

    :raises Exception: If there's an issue with the input data or if an error occurs during connection setup.
    """
    try:
        credentials = json.loads(credential)
        if "clientID" in credentials and "clientSecret" in credentials and "refreshToken" in credentials and "developerToken" in credentials and login_customer_id:
            creds = {
                "client_id": credentials["clientID"],
                "client_secret": credentials["clientSecret"],
                "refresh_token": credentials["refreshToken"],
                "developer_token": credentials["developerToken"],
                "login_customer_id": login_customer_id,
                "use_proto_plus": True,
            }
            client = GoogleAdsClient.load_from_dict(creds)
            return client
        else:
            raise Exception("missing credentials")
    except Exception as e:
        raise Exception(f"Error creating client instance: {e}")


def normalize_and_hash(s, remove_all_whitespace):
    """
    Normalizes and hashes a string with SHA-256.

    :s: (str, Required) - The string to perform this operation on.
    :remove_all_whitespace: (bool, Required) - If true, removes leading, trailing, and intermediate spaces from the string before hashing. If false, only removes leading and trailing spaces from the string before hashing.
    
    :return: A normalized (lowercase, remove whitespace) and SHA-256 hashed string.
    :rtype: String.
    """
    # Normalizes by first converting all characters to lowercase, then trimming
    # spaces.
    if remove_all_whitespace:
        # Removes leading, trailing, and intermediate whitespace.
        s = "".join(s.split())
    else:
        # Removes only leading and trailing spaces.
        s = s.strip().lower()

    # Hashes the normalized string using the hashing algorithm.
    return hashlib.sha256(s.encode()).hexdigest()



###################################### Campaigns ##################################


def Google_Ads_get_campaign_by_id(credentials,params):
    """
    Retrieves the campaign by it's ID

    :credentials: A dictionary containing credential parameters.
    :params: Dictionary containing parameters.
    
    - :manager_id: (str, Required) - the customer ID of the authenticated manager account. It should be set without dashes.
    - :customer_id: (str, Required) - the customer ID of the authenticated customer account. It should be set without dashes.
    - :campaign_id: (int, Required) - the campaign ID of the campaign to be retrieved
    - :resource_fields: (str, Optional) - selected resource fields of the campaign resource where the fields are seperated by a comma and a space
    - :attributed_resource_fields: (str, Optional) - selected attributed resource fields of the campaign resource where the fields are seperated by a comma and a space
    - :metrics: (str, Optional) - selected metrics fields of the campaign resource where the fields are seperated by a comma and a space
    - :segments: (str, Optional) - selected segment fields of the campaign resource where the fields are seperated by a comma and a space
    

    :return: dictionary containing a campaign object
    :rtype: dict
    """
    try:
        if "manager_id" in params and "customer_id" in params and "customer_id" in params and ("resource_fields" in params or "metrics" in params or "segments" in params or "attributed_resource_fields" in params):
            customer_id = params["customer_id"]
            manager_id = params["manager_id"]
            campaign_id = params["campaign_id"]
            resource_fields = params.get("resource_fields", "")
            attributed_resource_fields = params.get("attributed_resource_fields", "")
            metrics = params.get("metrics", "")
            segments = params.get("segments", "")
            client = create_client_instance(credentials, manager_id)
            ga_service = client.get_service("GoogleAdsService")
            
            fields = f"{resource_fields}{attributed_resource_fields}{metrics}{segments}"
            
            query = f"""
                    SELECT
                        {fields[0:-1]}
                    FROM campaign
                    WHERE campaign.id = {campaign_id}"""
            
            stream = ga_service.search_stream(customer_id=customer_id, query=query)

            campaigns_list = []
            for batch in stream:
                for row in batch.results:
                    campaigns_list.append(proto.Message.to_dict(row, use_integers_for_enums=False))

            if campaigns_list:
                return {"message": "Operation Completed Successfully", "Campaign": campaigns_list}
            else:
                return {"message": "Campaign Not Found"}
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def Google_Ads_get_campaign_by_name(credentials,params):
    """
    Retrieves the campaign by it's Name

    :credentials: A dictionary containing credential parameters.
    :params: Dictionary containing parameters.
    
    - :manager_id: (str, Required) - the customer ID of the authenticated manager account. It should be set without dashes.
    - :customer_id: (str, Required) - the customer ID of the authenticated customer account. It should be set without dashes.
    - :campaign_name: (str, Required) - the campaign Name of the campaign to be retrieved
    - :resource_fields: (str, Optional) - selected resource fields of the campaign resource where the fields are seperated by a comma and a space
    - :attributed_resource_fields: (str, Optional) - selected attributed resource fields of the campaign resource where the fields are seperated by a comma and a space
    - :metrics: (str, Optional) - selected metrics fields of the campaign resource where the fields are seperated by a comma and a space
    - :segments: (str, Optional) - selected segment fields of the campaign resource where the fields are seperated by a comma and a space
    

    :return: dictionary containing a campaign object
    :rtype: dict
    """
    try:
        if "manager_id" in params and "customer_id" in params and "campaign_name" in params and ("resource_fields" in params or "metrics" in params or "segments" in params or "attributed_resource_fields" in params):
            customer_id = params["customer_id"]
            manager_id = params["manager_id"]
            campaign_name = params["campaign_name"]
            resource_fields = params.get("resource_fields", "")
            attributed_resource_fields = params.get("attributed_resource_fields", "")
            metrics = params.get("metrics", "")
            segments = params.get("segments", "")
            client = create_client_instance(credentials, manager_id)
            ga_service = client.get_service("GoogleAdsService")
            
            fields = f"{resource_fields}{attributed_resource_fields}{metrics}{segments}"
            
            query = f"""
                    SELECT
                        {fields[0:-1]}
                    FROM campaign
                    WHERE campaign.name = '{campaign_name}'"""
            
            stream = ga_service.search_stream(customer_id=customer_id, query=query)
            
            campaigns_list = []
            for batch in stream:
                for row in batch.results:
                    campaigns_list.append(proto.Message.to_dict(row, use_integers_for_enums=False))
            
            if campaigns_list:
                return {"message": "Operation Completed Successfully", "Campaign": campaigns_list}
            else:
                return {"message": "Campaign Not Found"}
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def Google_Ads_set_campaign_status(credentials,params):
    """
    Sets the status of a Campaign

    :credentials: A dictionary containing credential parameters.
    :params: Dictionary containing parameters.
    
    - :manager_id: (str, Required) - the customer ID of the authenticated manager account. It should be set without dashes.
    - :customer_id: (str, Required) - the customer ID of the authenticated customer account. It should be set without dashes.
    - :campaign_id: (int, Required) - the campaign ID of the campaign to be retrieved
    - :status: (str, Required) - The status of the campaign. Possible Values: (ENABLED, PAUSED)

    :return: dictionary containing a campaign object
    :rtype: dict
    """
    try:
        if "manager_id" in params and "customer_id" in params and "campaign_id" in params and "status" in params:
            customer_id = params["customer_id"]
            manager_id = params["manager_id"]
            campaign_id = params["campaign_id"]
            status = params["status"]
            client = create_client_instance(credentials, manager_id)
            campaign_service = client.get_service("CampaignService")
            # Create campaign operation.
            campaign_operation = client.get_type("CampaignOperation")
            campaign = campaign_operation.update

            campaign.resource_name = campaign_service.campaign_path(
                customer_id, campaign_id
            )

            if status == "ENABLED":
                campaign.status = client.enums.CampaignStatusEnum.ENABLED
            elif status == "PAUSED":
                campaign.status = client.enums.CampaignStatusEnum.PAUSED
            else:
                raise Exception(f"accepted values for status are only: ENABLED or PAUSED. not {status}")

            campaign.network_settings.target_search_network = False
            # Retrieve a FieldMask for the fields configured in the campaign.
            client.copy_from(
                campaign_operation.update_mask,
                protobuf_helpers.field_mask(None, campaign._pb),
            )

            campaign_response = campaign_service.mutate_campaigns(
                customer_id=customer_id, operations=[campaign_operation]
            )

            return {"message": f"Set Campaign status to '{status}' for the Campaign with resource name: '{campaign_response.results[0].resource_name}'.",}
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)



####################################### Customer List ######################################


def Google_Ads_get_user_list(credentials,params):
    """
    Retrieves the User List by it's Name

    :credentials: A dictionary containing credential parameters.
    :params: Dictionary containing parameters.
    
    - :manager_id: (str, Required) - the customer ID of the authenticated manager account. It should be set without dashes.
    - :customer_id: (str, Required) - the customer ID of the authenticated customer account. It should be set without dashes.
    - :user_list_name: (str, Required) - the User List Name of the User List to be retrieved
    

    :return: dictionary containing a User List object
    :rtype: dict
    """
    try:
        if "manager_id" in params and "customer_id" in params and "user_list_name" in params:
            customer_id = params["customer_id"]
            manager_id = params["manager_id"]
            user_list_name = params["user_list_name"]
            client = create_client_instance(credentials, manager_id)
            ga_service = client.get_service("GoogleAdsService")
            
            fields = "user_list.access_reason, user_list.account_user_list_status, user_list.basic_user_list.actions, user_list.closing_reason, user_list.crm_based_user_list.app_id, user_list.crm_based_user_list.data_source_type, user_list.crm_based_user_list.upload_key_type, user_list.description, user_list.eligible_for_display, user_list.eligible_for_search, user_list.id, user_list.integration_code, user_list.logical_user_list.rules, user_list.lookalike_user_list.country_codes, user_list.lookalike_user_list.expansion_level, user_list.lookalike_user_list.seed_user_list_ids, user_list.match_rate_percentage, user_list.membership_life_span, user_list.membership_status, user_list.name, user_list.read_only, user_list.resource_name, user_list.rule_based_user_list.flexible_rule_user_list.exclusive_operands, user_list.rule_based_user_list.flexible_rule_user_list.inclusive_operands, user_list.rule_based_user_list.flexible_rule_user_list.inclusive_rule_operator, user_list.rule_based_user_list.prepopulation_status, user_list.similar_user_list.seed_user_list, user_list.size_for_display, user_list.size_for_search, user_list.size_range_for_display, user_list.size_range_for_search, user_list.type, customer.auto_tagging_enabled, customer.call_reporting_setting.call_conversion_action, customer.call_reporting_setting.call_conversion_reporting_enabled, customer.call_reporting_setting.call_reporting_enabled, customer.conversion_tracking_setting.accepted_customer_data_terms, customer.conversion_tracking_setting.conversion_tracking_id, customer.conversion_tracking_setting.conversion_tracking_status, customer.conversion_tracking_setting.cross_account_conversion_tracking_id, customer.conversion_tracking_setting.enhanced_conversions_for_leads_enabled, customer.conversion_tracking_setting.google_ads_conversion_customer, customer.currency_code, customer.customer_agreement_setting.accepted_lead_form_terms, customer.descriptive_name, customer.final_url_suffix, customer.has_partners_badge, customer.id, customer.image_asset_auto_migration_done, customer.image_asset_auto_migration_done_date_time, customer.local_services_settings.granular_insurance_statuses, customer.local_services_settings.granular_license_statuses, customer.location_asset_auto_migration_done, customer.location_asset_auto_migration_done_date_time, customer.manager, customer.optimization_score, customer.optimization_score_weight, customer.pay_per_conversion_eligibility_failure_reasons, customer.remarketing_setting.google_global_site_tag, customer.resource_name, customer.status, customer.test_account, customer.time_zone, customer.tracking_url_template"
            
            query = f"""
                    SELECT
                        {fields}
                    FROM user_list
                    WHERE user_list.name = '{user_list_name}'"""
            
            stream = ga_service.search_stream(customer_id=customer_id, query=query)
            
            user_lists_list = []
            for batch in stream:
                for row in batch.results:
                    user_lists_list.append(proto.Message.to_dict(row, use_integers_for_enums=False))
            
            if user_lists_list:
                return {"message": "Operation Completed Successfully", "User List": user_lists_list}
            else:
                return {"message": "User List Not Found"}
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)



def Google_Ads_create_user_list(credentials,params):
    """
    Creates a User List and displays it

    :credentials: A dictionary containing credential parameters.
    :params: Dictionary containing parameters.
    
    - :manager_id: (str, Required) - the customer ID of the authenticated manager account. It should be set without dashes.
    - :customer_id: (str, Required) - the customer ID of the authenticated customer account. It should be set without dashes.
    - :user_list_name: (str, Required) - the User List Name of the User List to be Created
    - :user_list_description: (str, Optional) - the User List Description of the User List to be Created
    

    :return: dictionary containing a User List object
    :rtype: dict
    """
    try:
        if "manager_id" in params and "customer_id" in params and "user_list_name" in params:
            customer_id = params["customer_id"]
            manager_id = params["manager_id"]
            user_list_name = params["user_list_name"]
            user_list_description = params.get("user_list_description", "")
            fields = "user_list.access_reason, user_list.account_user_list_status, user_list.basic_user_list.actions, user_list.closing_reason, user_list.crm_based_user_list.app_id, user_list.crm_based_user_list.data_source_type, user_list.crm_based_user_list.upload_key_type, user_list.description, user_list.eligible_for_display, user_list.eligible_for_search, user_list.id, user_list.integration_code, user_list.logical_user_list.rules, user_list.lookalike_user_list.country_codes, user_list.lookalike_user_list.expansion_level, user_list.lookalike_user_list.seed_user_list_ids, user_list.match_rate_percentage, user_list.membership_life_span, user_list.membership_status, user_list.name, user_list.read_only, user_list.resource_name, user_list.rule_based_user_list.flexible_rule_user_list.exclusive_operands, user_list.rule_based_user_list.flexible_rule_user_list.inclusive_operands, user_list.rule_based_user_list.flexible_rule_user_list.inclusive_rule_operator, user_list.rule_based_user_list.prepopulation_status, user_list.similar_user_list.seed_user_list, user_list.size_for_display, user_list.size_for_search, user_list.size_range_for_display, user_list.size_range_for_search, user_list.type, customer.auto_tagging_enabled, customer.call_reporting_setting.call_conversion_action, customer.call_reporting_setting.call_conversion_reporting_enabled, customer.call_reporting_setting.call_reporting_enabled, customer.conversion_tracking_setting.accepted_customer_data_terms, customer.conversion_tracking_setting.conversion_tracking_id, customer.conversion_tracking_setting.conversion_tracking_status, customer.conversion_tracking_setting.cross_account_conversion_tracking_id, customer.conversion_tracking_setting.enhanced_conversions_for_leads_enabled, customer.conversion_tracking_setting.google_ads_conversion_customer, customer.currency_code, customer.customer_agreement_setting.accepted_lead_form_terms, customer.descriptive_name, customer.final_url_suffix, customer.has_partners_badge, customer.id, customer.image_asset_auto_migration_done, customer.image_asset_auto_migration_done_date_time, customer.local_services_settings.granular_insurance_statuses, customer.local_services_settings.granular_license_statuses, customer.location_asset_auto_migration_done, customer.location_asset_auto_migration_done_date_time, customer.manager, customer.optimization_score, customer.optimization_score_weight, customer.pay_per_conversion_eligibility_failure_reasons, customer.remarketing_setting.google_global_site_tag, customer.resource_name, customer.status, customer.test_account, customer.time_zone, customer.tracking_url_template"
            client = create_client_instance(credentials, manager_id)
            user_list_service_client = client.get_service("UserListService")

            # Creates the user list operation.
            user_list_operation = client.get_type("UserListOperation")

            # Creates the new user list.
            user_list = user_list_operation.create
            user_list.name = user_list_name
            user_list.description = user_list_description
            
            user_list.crm_based_user_list.upload_key_type = (
                client.enums.CustomerMatchUploadKeyTypeEnum.CONTACT_INFO
            )
            
            user_list.membership_life_span = 10000

            response = user_list_service_client.mutate_user_lists(
                customer_id=customer_id, operations=[user_list_operation]
            )
            user_list_resource_name = response.results[0].resource_name
            
            
            query = f"""
                    SELECT
                        {fields}
                    FROM user_list
                    WHERE user_list.resource_name = '{user_list_resource_name}'"""
            
            # fetches the newly created user list
            ga_service = client.get_service("GoogleAdsService")
            stream = ga_service.search_stream(customer_id=customer_id, query=query)
            
            user_lists_list = []
            for batch in stream:
                for row in batch.results:
                    user_lists_list.append(proto.Message.to_dict(row, use_integers_for_enums=False))
            
            if user_lists_list:
                return {"message": "Operation Completed Successfully", "Created User List": user_lists_list}
            else:
                return {"message": "An Error occured while fetching the created user list"}
            
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)



def Google_Ads_add_user_to_user_list(credentials,params):
    """
    Adds a User to a User List

    :credentials: A dictionary containing credential parameters.
    :params: Dictionary containing parameters.
    
    - :manager_id: (str, Required) - the customer ID of the authenticated manager account. It should be set without dashes.
    - :customer_id: (str, Required) - the customer ID of the authenticated customer account. It should be set without dashes.
    - :user_list_resource_name: (str, Required) - the Resource Name of the User List where the User will be added
    - :user_identifier_type: (str, Required) - indicates the type of the user identifier to be used. Possible Values: (email, phone, address)
    - :user_email: (str, Optional) - email of the user to add. only required if user_identifier_type = email
    - :user_phone: (str, Optional) - phone number of the user to add. only required if user_identifier_type = phone
    - :user_first_name: (str, Optional) - first name of the user to add. only required if user_identifier_type = address
    - :user_last_name: (str, Optional) - last name of the user to add. only required if user_identifier_type = address
    - :user_country_code: (str, Optional) - country code of the user to add. only required if user_identifier_type = address
    - :user_postal_code: (str, Optional) - postal code of the user to add. only required if user_identifier_type = address
    - :ad_user_data_consent: (str, Optional) - This represents consent for ad user data. Possible Values: (UNSPECIFIED, GRANTED, DENIED)
    - :ad_personalization_consent: (str, Optional) - This represents consent for ad personalization. Possible Values: (UNSPECIFIED, GRANTED, DENIED)
    

    :return: dictionary containing success message
    :rtype: dict
    """
    try:
        if (
            "manager_id" in params and 
            "customer_id" in params and 
            "user_list_resource_name" in params and 
            "user_identifier_type" in params and 
            (
                "user_email" in params or 
                "user_phone" in params or 
                (
                    "user_first_name" in params and 
                    "user_last_name" in params and 
                    "user_country_code" in params and 
                    "user_postal_code" in params
                )
            )
        ):
            customer_id = params["customer_id"]
            manager_id = params["manager_id"]
            user_list_resource_name = params["user_list_resource_name"]
            user_identifier_type = params["user_identifier_type"]
            user_email = params.get("user_email", "")
            user_phone = params.get("user_phone", "")
            user_first_name = params.get("user_first_name", "")
            user_last_name = params.get("user_last_name", "")
            user_country_code = params.get("user_country_code", "")
            user_postal_code = params.get("user_postal_code", "")
            ad_user_data_consent = params.get("ad_user_data_consent", "")
            ad_personalization_consent = params.get("ad_personalization_consent", "")
            
            client = create_client_instance(credentials, manager_id)
            
            user_data_service_client = client.get_service("UserDataService")
            user_data_operation = client.get_type("UserDataOperation")
            user_data = client.get_type("UserData")
            user_identifier = client.get_type("UserIdentifier")
            offline_user_address_info = client.get_type("OfflineUserAddressInfo")
            upload_user_data_request = client.get_type("UploadUserDataRequest")
            customer_match_user_list_metadata = client.get_type("CustomerMatchUserListMetadata")
            
            if user_identifier_type == "email":
                user_identifier.hashed_email = normalize_and_hash(user_email, True)
                
            elif user_identifier_type == "phone":
                user_identifier.hashed_phone_number = normalize_and_hash(user_phone, True)
                
            elif user_identifier_type == "address":
                offline_user_address_info.hashed_first_name = normalize_and_hash(
                    user_first_name, False
                )
                offline_user_address_info.hashed_last_name = normalize_and_hash(
                    user_last_name, False
                )
                offline_user_address_info.country_code = user_country_code
                offline_user_address_info.postal_code = user_postal_code
                
                user_identifier.address_info = offline_user_address_info
                
            else:
                raise Exception(f"Unsupported Value Entered for user_identifier_type with the value being {user_identifier_type}")
            
            user_data.user_identifiers.append(user_identifier)
            user_data_operation.create = user_data
            
            customer_match_user_list_metadata.user_list = user_list_resource_name
            
            if ad_user_data_consent:
                customer_match_user_list_metadata.consent.ad_user_data = client.enums.ConsentStatusEnum[
                    ad_user_data_consent
                ]
            if ad_personalization_consent:
                customer_match_user_list_metadata.consent.ad_personalization = client.enums.ConsentStatusEnum[
                    ad_personalization_consent
                ]
            
            upload_user_data_request.customer_id = customer_id
            upload_user_data_request.operations = [user_data_operation]
            
            upload_user_data_request.customer_match_user_list_metadata = customer_match_user_list_metadata
            
            response = user_data_service_client.upload_user_data(
                upload_user_data_request
            )
            return {
                "message": "Operation is in Proccess",
                "Upload Date Time": response.upload_date_time,
                "Received Operations Count": response.received_operations_count,
            }
            
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)



def Google_Ads_remove_user_from_user_list(credentials,params):
    """
    Remove a User from a User List

    :credentials: A dictionary containing credential parameters.
    :params: Dictionary containing parameters.
    
    - :manager_id: (str, Required) - the customer ID of the authenticated manager account. It should be set without dashes.
    - :customer_id: (str, Required) - the customer ID of the authenticated customer account. It should be set without dashes.
    - :user_list_resource_name: (str, Required) - the Resource Name of the User List where the User will be removed
    - :user_identifier_type: (str, Required) - indicates the type of the user identifier to be used. Possible Values: (email, phone, address)
    - :user_email: (str, Optional) - email of the user to remove. only required if user_identifier_type = email
    - :user_phone: (str, Optional) - phone number of the user to remove. only required if user_identifier_type = phone
    - :user_first_name: (str, Optional) - first name of the user to remove. only required if user_identifier_type = address
    - :user_last_name: (str, Optional) - last name of the user to remove. only required if user_identifier_type = address
    - :user_country_code: (str, Optional) - country code of the user to remove. only required if user_identifier_type = address
    - :user_postal_code: (str, Optional) - postal code of the user to remove. only required if user_identifier_type = address
    - :ad_user_data_consent: (str, Optional) - This represents consent for ad user data. Possible Values: (UNSPECIFIED, GRANTED, DENIED)
    - :ad_personalization_consent: (str, Optional) - This represents consent for ad personalization. Possible Values: (UNSPECIFIED, GRANTED, DENIED)
    

    :return: dictionary containing success message
    :rtype: dict
    """
    try:
        if (
            "manager_id" in params and 
            "customer_id" in params and 
            "user_list_resource_name" in params and 
            "user_identifier_type" in params and 
            (
                "user_email" in params or 
                "user_phone" in params or 
                (
                    "user_first_name" in params and 
                    "user_last_name" in params and 
                    "user_country_code" in params and 
                    "user_postal_code" in params
                )
            )
        ):
            customer_id = params["customer_id"]
            manager_id = params["manager_id"]
            user_list_resource_name = params["user_list_resource_name"]
            user_identifier_type = params["user_identifier_type"]
            user_email = params.get("user_email", "")
            user_phone = params.get("user_phone", "")
            user_first_name = params.get("user_first_name", "")
            user_last_name = params.get("user_last_name", "")
            user_country_code = params.get("user_country_code", "")
            user_postal_code = params.get("user_postal_code", "")
            ad_user_data_consent = params.get("ad_user_data_consent", "")
            ad_personalization_consent = params.get("ad_personalization_consent", "")
            
            client = create_client_instance(credentials, manager_id)
            
            user_data_service_client = client.get_service("UserDataService")
            user_data_operation = client.get_type("UserDataOperation")
            user_data = client.get_type("UserData")
            user_identifier = client.get_type("UserIdentifier")
            offline_user_address_info = client.get_type("OfflineUserAddressInfo")
            upload_user_data_request = client.get_type("UploadUserDataRequest")
            customer_match_user_list_metadata = client.get_type("CustomerMatchUserListMetadata")
            
            if user_identifier_type == "email":
                user_identifier.hashed_email = normalize_and_hash(user_email, True)
                
            elif user_identifier_type == "phone":
                user_identifier.hashed_phone_number = normalize_and_hash(user_phone, True)
                
            elif user_identifier_type == "address":
                offline_user_address_info.hashed_first_name = normalize_and_hash(
                    user_first_name, False
                )
                offline_user_address_info.hashed_last_name = normalize_and_hash(
                    user_last_name, False
                )
                offline_user_address_info.country_code = user_country_code
                offline_user_address_info.postal_code = user_postal_code
                
                user_identifier.address_info = offline_user_address_info
                
            else:
                raise Exception(f"Unsupported Value Entered for user_identifier_type with the value being {user_identifier_type}")
            
            user_data.user_identifiers.append(user_identifier)
            user_data_operation.remove = user_data
            
            customer_match_user_list_metadata.user_list = user_list_resource_name
            
            if ad_user_data_consent:
                customer_match_user_list_metadata.consent.ad_user_data = client.enums.ConsentStatusEnum[
                    ad_user_data_consent
                ]
            if ad_personalization_consent:
                customer_match_user_list_metadata.consent.ad_personalization = client.enums.ConsentStatusEnum[
                    ad_personalization_consent
                ]
            
            upload_user_data_request.customer_id = customer_id
            upload_user_data_request.operations = [user_data_operation]
            
            upload_user_data_request.customer_match_user_list_metadata = customer_match_user_list_metadata
            
            response = user_data_service_client.upload_user_data(
                upload_user_data_request
            )
            
            return {
                "message": "Operation is in Proccess",
                "Upload Date Time": response.upload_date_time,
                "Received Operations Count": response.received_operations_count,
            }
            
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)




############################################ Common ########################################


def Google_Ads_create_report(credentials,params):
    """
    Retrieves the selected Resource data

    :credentials: A dictionary containing credential parameters.
    :params: Dictionary containing parameters.
    
    - :manager_id: (str, Required) - the customer ID of the authenticated manager account. It should be set without dashes.
    - :customer_id: (str, Required) - the customer ID of the authenticated customer account. It should be set without dashes.
    - :resource: (str, Required) - The resource to report on. Possible values: (ad_group, ad_group_ad, campaign, customer)
    - :date: (str, Required) - filters campaigns by start date. Possible values: (BETWEEN 'YYYY-MM-DD' AND 'YYYY-MM-DD', DURING TODAY, DURING YESTERDAY, DURING LAST_7_DAYS, DURING LAST_BUSINESS_WEEK, DURING THIS_MONTH, DURING LAST_MONTH, DURING LAST_14_DAYS, DURING LAST_30_DAYS, DURING THIS_WEEK_SUN_TODAY, DURING THIS_WEEK_MON_TODAY, DURING LAST_WEEK_SUN_SAT, DURING LAST_WEEK_MON_SUN)
    - :resource_fields: (str, Optional) - selected resource fields of the selected resource where the fields are seperated by a comma and a space
    - :attributed_resource_fields: (str, Optional) - selected attributed resource fields of the selected resource where the fields are seperated by a comma and a space
    - :metrics: (str, Optional) - selected metrics fields of the campaign resource where the fields are seperated by a comma and a space
    - :segments: (str, Optional) - selected segment fields of the campaign resource where the fields are seperated by a comma and a space
    - :limit: (int, Optional) - limits the number of results to the specified number. default is 25
    - :order_by: (str, Optional) - order the results according to the selected fields where the fields are seperated by a comma and a space. note that selected fields should already be selected in resource_fields, attributed_resource_fields, metrics or segments

    :return: dictionary containing a list of dictionaries with each one representing a resource object
    :rtype: dict
    """
    try:
        if "manager_id" in params and "customer_id" in params and "resource" in params and "date" in params and ("resource_fields" in params or "metrics" in params or "segments" in params or "attributed_resource_fields" in params):
            customer_id = params["customer_id"]
            manager_id = params["manager_id"]
            resource = params["resource"]
            date = params["date"]
            resource_fields = params.get("resource_fields", "")
            attributed_resource_fields = params.get("attributed_resource_fields", "")
            metrics = params.get("metrics", "")
            segments = params.get("segments", "")
            limit = params.get("limit", 25)
            order_by = params.get("order_by", "")
            
            client = create_client_instance(credentials, manager_id)
            ga_service = client.get_service("GoogleAdsService")
            
            if order_by:
                order_by = f"ORDER BY {order_by}"
            
            fields = f"{resource_fields}{attributed_resource_fields}{metrics}{segments}"
            
            query = f"""
                    SELECT
                        {fields[0:-1]}
                    FROM {resource}
                    WHERE segments.date {date}
                    {order_by}
                    LIMIT {str(limit)}"""
            
            stream = ga_service.search_stream(customer_id=customer_id, query=query)
            
            resource_list = []
            for batch in stream:
                for row in batch.results:
                    resource_list.append(proto.Message.to_dict(row, use_integers_for_enums=False))
            
            if resource_list:
                return {"message": "Operation Completed Successfully", "query": query, resource: resource_list}
            else:
                return {"message": "No Resources Found", "query": query}
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def Google_Ads_custom_query(credentials,params):
    """
    Retrieves the Query results

    :credentials: A dictionary containing credential parameters.
    :params: Dictionary containing parameters.
    
    - :manager_id: (str, Required) - the customer ID of the authenticated manager account. It should be set without dashes.
    - :customer_id: (str, Required) - the customer ID of the authenticated customer account. It should be set without dashes.
    - :query: (str, Required) - the query assigned by the user
    

    :return: dictionary containing a list of dictionaries with each one representing a row object from the query's result
    :rtype: dict
    """
    try:
        if "manager_id" in params and "customer_id" in params and "query" in params:
            customer_id = params["customer_id"]
            manager_id = params["manager_id"]
            query = params["query"]
            
            client = create_client_instance(credentials, manager_id)
            ga_service = client.get_service("GoogleAdsService")
            
            stream = ga_service.search_stream(customer_id=customer_id, query=query)
            
            resource_list = []
            for batch in stream:
                for row in batch.results:
                    resource_list.append(proto.Message.to_dict(row, use_integers_for_enums=False))
            
            if resource_list:
                return {"message": "Operation Completed Successfully", "query": query, "result": resource_list}
            else:
                return {"message": "No Resources Found", "query": query}
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


