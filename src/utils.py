import aiohttp

async def book_appointment(appointment_data):
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
                        "message": "Patient created successfully",
                        "patient": response_data.get("patient")
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
if __name__ == "__main__":
    import asyncio
    response = asyncio.run(book_appointment({"first_name": "John", "last_name": "Doe", "date_of_birth": "1990-01-01"}))
    print(response)
