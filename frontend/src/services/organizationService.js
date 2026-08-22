const API_BASE_URL = 'http://127.0.0.1:8000'

export const getOrganizations = async ({
    page = 1,
    limit = 100,
    name='',
} = {})=>{
    const params = new URLSearchParams({
        page,
        limit,
        name,
    })
    const response = await fetch(
        `${API_BASE_URL}/organization/?${params.toString()}`
    )
    if (!response.ok) {
        throw new Error('Failed to fetch organizations')
    }

    return response.json()
}

export const createOrganization = async (organizationData) => {
    const response = await fetch(
        `${API_BASE_URL}/organization/`,
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(organizationData),
        }
    )

    if (!response.ok) {
        throw new Error('Failed to create organization')
    }

    return response.json()
}

export const updateOrganization = async (
    organizationId,
    organizationData
) => {
    const response = await fetch(
        `${API_BASE_URL}/organization/${organizationId}`,
        {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(organizationData),
        }
    )

    if (!response.ok) {
        throw new Error('Failed to update organization')
    }

    return response.json()
}

export const deleteOrganization = async (organizationId) => {
    const response = await fetch(
        `${API_BASE_URL}/organization/${organizationId}`,
        {
            method: 'DELETE',
        }
    )

    if (!response.ok) {
        throw new Error('Failed to delete organization')
    }

    return response.json()
}

