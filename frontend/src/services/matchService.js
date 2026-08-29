const API_BASE_URL = 'http://127.0.0.1:8000'

export const getMatches = async ({
    page = 1,
    limit = 10,
    search = '',
}={})=> {
    const params = new URLSearchParams({
        page,
        limit,
        search,
    })

    const response = await fetch (
        `${API_BASE_URL}/match/?${params.toString()}`
    )

    if (!response.ok) {
        throw new Error('Failed to fetch matches')
    }

    return response.json()
}

export const createMatch = async (matchData) => {
    const response = await fetch(
        `${API_BASE_URL}/match/`,
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(matchData),
        }
    )

    if (!response.ok) {
        throw new Error('Failed to create match')
    }

    return response.json()
}


export const updateMatch = async (matchId, matchData) => {
    const response = await fetch(
        `${API_BASE_URL}/match/${matchId}`,
        {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(matchData),
        }
    )

    if (!response.ok) {
        throw new Error('Failed to update match')
    }

    return response.json()
}

export const deleteMatch = async (matchId) => {
    const response = await fetch(
        `${API_BASE_URL}/match/${matchId}`,
        {
            method: 'DELETE',
        }
    )

    if (!response.ok) {
        throw new Error('Failed to delete match')
    }

    return response.json()
}

export const getMatch = async (matchId) => {
    const response = await fetch(
        `${API_BASE_URL}/match/${matchId}`
    )
    if (!response.ok) {
        throw new Error('Failed to fetch match')
    }

    return response.json()
}

export const getMatchSquad = async (matchId) => {
    const response = await fetch(
        `${API_BASE_URL}/match/${matchId}/squad`
    )
    if (!response.ok) {
        throw new Error('Failed to fetch match squad')
    }

    return response.json()
}

export const updateMatchSquad = async (matchId, playerIds) => {
    const response = await fetch(
        `${API_BASE_URL}/match/${matchId}/squad`,
        {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                player_ids: playerIds,
            }),
        }
    )

    if (!response.ok) {
        throw new Error('Failed to update match squad')
    }

    return response.json()
}