const API_BASE_URL= 'http://127.0.0.1:8000'

export const getPlayers = async({
    page = 1,
    limit = 10,
    name = '',
    position = '',
    teamId = null,
    sort = '',

} = {}) => {
    const params = new URLSearchParams({
        page,
        limit,
    })

    if (name) {
        params.append('name', name)
    }

    if (position) {
        params.append('position', position)
    }

    if (teamId != null) {
        params.append('team_id', teamId)
    }

    if (sort) {
        params.append('sort', sort)
    }

    const response = await fetch(
        `${API_BASE_URL}/player/?${params.toString()}`
    )

    if (!response.ok) {
        throw new Error('Failed to fetch players')
    }

    return response.json()
}

export const deletePlayer = async (playerId) => {
    const response = await fetch(
        `${API_BASE_URL}/player/${playerId}`,
        {
            method: 'DELETE',
        }
    )

    if (!response.ok) {
        throw new Error('Failed to delete player')
    }

    return response.json()
}

export const updatePlayer = async (playerId, playerData)=>{
    const response = await fetch(
        `${API_BASE_URL}/player/${playerId}`,
        {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(playerData),
        }
    )

    if (!response.ok) {
        throw new Error('Failed to update player')
    }
    return response.json()
}

export const createPlayer = async (playerData) => {
    const response = await fetch(
        `${API_BASE_URL}/player/`,
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(playerData),
        }
    )
    if (!response.ok) {
        throw new Error('Failed to create player')
    }
    return response.json()
}