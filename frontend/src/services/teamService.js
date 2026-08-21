const API_BASE_URL = 'http://127.0.0.1:8000'

export const getTeams = async ({
    page= 1,
    limit = 100,
    name,
    team_type,
    club_id,
    sort,
} = {})=>{
    const params=new URLSearchParams({
        page,
        limit,
    })
    
if (name) params.append('name',name)
if (team_type) params.append('team_type', team_type)
if (club_id) params.append('club_id', club_id)
if (sort) params.append('sort', sort)

    const response = await fetch(
        `${API_BASE_URL}/team/?${params.toString()}`
    )

    if (!response.ok) {
        throw new Error('Failed to fetch teams')
    }

    return response.json()
}

export const createTeam = async (teamData) => {
    const response = await fetch(`${API_BASE_URL}/team/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(teamData),
    })

    if (!response.ok) {
        throw new Error('Failed to create team')
    }

    return response.json()
}
