const API_BASE_URL = 'http://127.0.0.1:8000'

export const getTeams = async ({
    page= 1,
    limit = 100,
} = {})=>{
    const params=new URLSearchParams({
        page,
        limit,
    })

    const response = await fetch(
        `${API_BASE_URL}/team/?${params.toString()}`
    )

    if (!response.ok) {
        throw new Error('Failed to fetch teams')
    }

    return response.json()
}

