const API_BASE_URL = 'http://127.0.0.1:8000'

export const getCoaches = async ({
    page =1,
    limit = 10,
    name = '',
    role = '',
    teamId = null,
    sort = '',
}={}) => {
    const params = new URLSearchParams({
        page,
        limit,
    })

    if (name) {
        params.append('name', name)
    }

    if (role) {
        params.append('role', role)
    }

    if (teamId != null) {
        params.append('team_id', teamId)
    }

    if (sort) {
        params.append('sort', sort)
    }

    const response = await fetch(
        `${API_BASE_URL}/coach/?${params.toString()}`
    )

    if (!response.ok) {
        throw new Error('Failed to fetch coaches')
    }

    return response.json()
}

export const getCoach = async(coachId) => {
    const response = await fetch(
        `${API_BASE_URL}/coach/${coachId}`
    )

    if (!response.ok) {
        throw new Error('Failed to fetch coach')
    }

    return response.json()
}

export const deleteCoach = async (coachId)=> {
    const response = await fetch(
        `${API_BASE_URL}/coach/${coachId}`,
        {
            method: 'DELETE'
        }
    )

    if (!response.ok) {
        throw new Error('Failed to delete coach')
    }

    return response.json()
}

export const updateCoach= async (coachId, coachData)=>{
    const response = await fetch(
        `${API_BASE_URL}/coach/${coachId}`,
        {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(coachData),
        }
    )

    if (!response.ok) {
        throw new Error('Failed to update coach')
    }

    return response.json()
}

export const createCoach = async (coachData) => {
    const response = await fetch(
        `${API_BASE_URL}/coach/`,
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(coachData),
        }
    )

    if (!response.ok) {
        throw new Error('Failed to create coach')
    }

    return response.json()
}

export const uploadCoachImage = async (coachId, file) => {
    const formData = new FormData()
    formData.append('file', file)

    const response = await fetch (
        `${API_BASE_URL}/coach/${coachId}/image`,
        {
            method: 'POST',
            body: formData,
        }
    )

    if (!response.ok) {
        throw new Error('Failed to upload coach image')
    }

    return response.json()
}