import aiohttp

async def get_patient_id(appointment_data):
    """
    Make API call to create a new patient with minimal data
    
    Args:
        appointment_data (dict): Dictionary containing patient details (first_name, last_name, date_of_birth)
        
    Returns:
        dict: API response with status and any error information
    """
    url = "https://ep.soaper.ai/api/v1/agent/patients/create"  # Update with your actual FastAPI server URL
    headers = {
        "Content-Type": "application/json",
        "X-Agent-API-Key": "sk-int-agent-PJNvT3BlbkFJe8ykcJe6kV1KQntXzgMW"  # Replace with actual API key
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=appointment_data, headers=headers) as response:
                response_data = await response.json()
                
                if response_data.get("success", False):
                    return {
                        "status": "success",
                        "message": response_data.get("message"),
                        "patient_id": response_data.get("patient", {}).get("id")
                    }
                else:
                    return {
                        "status": "error",
                        "message": response_data.get("message", "Error creating patient")
                    }
    
    except Exception as e:
        print(f"Error calling patient creation API: {str(e)}")
        return {
            "status": "error",
            "message": f"There was a problem connecting to the patient creation service: {str(e)}"

        }
    
async def book_appointment(appointment_data):
    """
    Make API call to book an appointment. From first name and last name, get physician_id using get_physician_by_name.
    and use the physician_id to get the visit types using get_physician_visit_type.
    
    Args:
        appointment_data (dict): Dictionary containing appointment details including:
            - patient_id: UUID of the patient
            - physician_id: UUID of the physician
            - datetime: ISO format datetime string (YYYY-MM-DDTHH:MM:SS)
            - visit_type: Type of visit
            - duration_minutes: (optional) Length of appointment in minutes, defaults to 30
            - visit_notes: (optional) Notes for the visit
            - location_id: (optional) UUID of the location
    
    Returns:
        dict: API response with status and any error information
    """
    url = "https://ep.soaper.ai/api/v1/agent/appointments/schedule"
    headers = {
        "Content-Type": "application/json",
        "X-Agent-API-Key": "sk-int-agent-PJNvT3BlbkFJe8ykcJe6kV1KQntXzgMW"  # Replace with actual API key
    }

    # Ensure required fields are present
    required_fields = ["patient_id", "physician_id", "datetime", "visit_type"]
    missing_fields = [field for field in required_fields if field not in appointment_data]
    
    if missing_fields:
        return {
            "status": "error",
            "message": f"Missing required fields: {', '.join(missing_fields)}"
        }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=appointment_data, headers=headers) as response:
                response_data = await response.json()
                print(response_data)
                
                if response_data.get("success", False):
                    return {
                        "status": "success",
                        "message": response_data.get("message"),
                        "appointment_id": response_data.get("appointment_id"),
                        "datetime": response_data.get("datetime"),
                        "physician_name": response_data.get("physician_name"),
                        "visit_type": response_data.get("visit_type"),
                        "duration_minutes": response_data.get("duration_minutes")
                    }
                else:
                    return {
                        "status": "error",
                        "message": response_data.get("message", "Error scheduling appointment")
                    }  
    except Exception as e:
        print(f"Error calling appointment scheduling API: {str(e)}")
        return {
            "status": "error",
            "message": f"There was a problem connecting to the appointment scheduling service: {str(e)}"
        }
    
async def get_physician_id_by_name(physician_first_name, physician_last_name):
    """
    Make API call to get a physician by first name and last name
    """
    url = f"https://ep.soaper.ai/api/v1/agent/appointments/physicians"
    headers = {
        "Content-Type": "application/json",
        "X-Agent-API-Key": "sk-int-agent-PJNvT3BlbkFJe8ykcJe6kV1KQntXzgMW"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                response_data = await response.json()
                # for physician in response_data.get("items", []):
                #     if (physician.get("first_name") == physician_first_name and 
                #         physician.get("last_name") == physician_last_name):
                #         return {
                #             "status": "success",
                #             "physician_id": physician.get("id"),
                #             "physician_name": f"{physician.get('first_name')} {physician.get('last_name')}"
                #         }
                print(response_data)
                
                # return {
                #     "status": "error",
                #     "message": "Physician not found"
                # }
    except Exception as e:
        print(f"Error calling physician API: {str(e)}")
        return {
            "status": "error",
            "message": f"There was a problem connecting to the physician service: {str(e)}"
        }

async def get_physician_visit_type(physician_first_name, physician_last_name, patient_id):
    """
    Make API call to get the visit types for a physician
    
    Args:
        physician_id (str): UUID of the physician
        patient_id (str): UUID of the patient
        
    Returns:
        dict: API response with status and visit type information
    """
    all_physicians = []
    physician_url = f"https://ep.soaper.ai/api/v1/agent/appointments/physicians"
    headers = {
        "Content-Type": "application/json",
        "X-Agent-API-Key": "sk-int-agent-PJNvT3BlbkFJe8ykcJe6kV1KQntXzgMW"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(physician_url, headers=headers) as response:
                response_data = await response.json()
                all_physicians = response_data.get("slots", [])
    except Exception as e:
        print(f"Error calling physician API: {str(e)}")
        

    # Get physician_id from physician_first_name and physician_last_name from api call
    url = f"https://ep.soaper.ai/api/v1/agent/appointments/physicians"
    headers = {
        "Content-Type": "application/json",
        "X-Agent-API-Key": "sk-int-agent-PJNvT3BlbkFJe8ykcJe6kV1KQntXzgMW"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                response_data = await response.json()
                print(response_data)
    except Exception as e:
        print(f"Error calling physician API: {str(e)}")
    

    url = f"https://ep.soaper.ai/api/v1/agent/appointments/physicians/{physician_id}/visit-types"
    headers = {
        "Content-Type": "application/json",
        "X-Agent-API-Key": "sk-int-agent-PJNvT3BlbkFJe8ykcJe6kV1KQntXzgMW"
    }    
    # Add patient_id as query parameter
    params = {"patient_id": patient_id}
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=headers) as response:
                response_data = await response.json()
                
                if response_data.get("success", False):
                    return {
                        "status": "success",
                        "total": response_data.get("total", 0),
                        "visit_types": response_data.get("items", [])
                    }
                else:
                    return {
                        "status": "error",
                        "message": response_data.get("detail", "Error retrieving physician visit types")
                    }
    
    except Exception as e:
        print(f"Error calling physician visit types API: {str(e)}")
        return {
            "status": "error",
            "message": f"There was a problem connecting to the physician visit types service: {str(e)}"
        }
    
async def get_doctor_time_slots(appointment_data):
    """
    Make API call to get next available appointment slots for an agent
    """
    url = f"https://ep.soaper.ai/api/v1/agent/appointments/next-available"
    headers = {
        "Content-Type": "application/json",
        "X-Agent-API-Key": "sk-int-agent-PJNvT3BlbkFJe8ykcJe6kV1KQntXzgMW"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=appointment_data, headers=headers) as response:
                response_data = await response.json()
                if response_data.get("success", False):
                    return {
                        "success": True,
                        "slots": response_data.get("slots", []),
                        "message": response_data.get("message", "Doctor time slots retrieved successfully")
                    }
                else:
                    return {
                        "success": False,
                        "slots": [],
                        "message": response_data.get("message", "No available appointments found")
                    }
    except Exception as e:
        print(f"Error calling next available slots API: {str(e)}")
        return {
            "success": False,
            "slots": [],
            "message": f"There was a problem connecting to the next available slots service: {str(e)}"
        }

if __name__ == "__main__":
    import asyncio
    # response = asyncio.run(get_patient_id({"first_name": "John", "last_name": "Doe", "date_of_birth": "1990-01-01"}))
    # print(response)

    # response = asyncio.run(book_appointment({
    #     "patient_id": "0e2a370e-5b01-404c-8a74-3e6e6d3949a2",
    #     "physician_first_name": "Nicholas",
    #     "physician_last_name": "Romero",
    #     "datetime": "2025-03-19T15:00:00",
    #     "visit_type": "New Patient Consultation",
    #     "duration_minutes": 30,
    #     "visit_notes": "Follow-up visit",
    #     "location_id": "123e4567-e89b-12d3-a456-426614174000"
    # }))
    # print(response)

    # response = asyncio.run(get_physician_visit_type("81877c7b-d22a-49f4-a2e1-598a12e2bf7c", "0e2a370e-5b01-404c-8a74-3e6e6d3949a2"))
    # print(response)

    # response = asyncio.run(get_physician_id_by_name("Nicholas", "Romero"))
    # print(response)

    response = asyncio.run(get_doctor_time_slots({
        "patient_id": "0e2a370e-5b01-404c-8a74-3e6e6d3949a2",
        "physician_id": "81877c7b-d22a-49f4-a2e1-598a12e2bf7c",
    }))
    print(response)