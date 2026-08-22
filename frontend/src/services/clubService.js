

const API_BASE_URL = 'http://127.0.0.1:8000'

export const getClubs = async ({
    page = 1,
    limit = 10,
    name = '',
} = {}) => {
    const params = new URLSearchParams({
        page,
        limit,
        name,
    })

    const response = await fetch(
        `${API_BASE_URL}/club/?${params.toString()}`
    )
    if (!response.ok) {
        throw new Error('Failed to fetch clubs')
}
    return response.json()
}

export const createClub = async (clubData) =>{
    const response = await fetch(
        `${API_BASE_URL}/club/`,
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(clubData),
        }
    )
    if (!response.ok) {
        throw new Error('Failed to create club')
    }

    return response.json()
}

export const updateClub = async (clubId, clubData) => {
    const response = await fetch(
        `${API_BASE_URL}/club/${clubId}`,
        {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(clubData),
        }
    )

    if (!response.ok) {
        throw new Error('Failed to update club')
    }

    return response.json()
}

export const deleteClub = async (clubId) => {
    const response = await fetch(
        `${API_BASE_URL}/club/${clubId}`,
        {
            method: 'DELETE',
        }
    )

    if (!response.ok) {
        throw new Error('Failed to delete club')
    }

    return response.json()
}
