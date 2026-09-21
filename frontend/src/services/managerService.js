const API_BASE_URL = 'http://127.0.0.1:8000'

export const getManagers = async ({
    page = 1,
    limit = 10,
    name = '',
    teamId = null,
    status = '',
    sort = '',
} = {}) => {
    const params = new URLSearchParams({
        page,
        limit,
    })

    if (name) {
        params.append('name', name)
    }

    if (teamId !== null && teamId !== '') {
        params.append('team_id', teamId)
    }

    if (status) {
        params.append('status', status)
    }

    if (sort) {
        params.append('sort', sort)
    }

    const response = await fetch(
        `${API_BASE_URL}/manager/?${params.toString()}`
    )

    if (!response.ok) {
        throw new Error('Failed to fetch managers')
    }

    return response.json()
}

export const getManager = async (managerId) => {
    const response = await fetch(
        `${API_BASE_URL}/manager/${managerId}`
    )

    if (!response.ok) {
        throw new Error('Failed to fetch manager')
    }

    return response.json()
}

export const createManager = async (managerData) => {
    const response = await fetch(
        `${API_BASE_URL}/manager/`,
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(managerData),
        }
    )

    if (!response.ok) {
        throw new Error('Failed to create manager')
    }

    return response.json()
}

export const updateManager = async (managerId, managerData) => {
    const response = await fetch(
        `${API_BASE_URL}/manager/${managerId}`,
        {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(managerData),
        }
    )

    if (!response.ok) {
        throw new Error('Failed to update manager')
    }

    return response.json()
}

export const deleteManager = async (managerId) => {
    const response = await fetch(
        `${API_BASE_URL}/manager/${managerId}`,
        {
            method: 'DELETE',
        }
    )

    if (!response.ok) {
        throw new Error('Failed to delete manager')
    }

    return response.json()
}

export const uploadManagerImage = async (managerId, file) => {
    const formData = new FormData()

    formData.append('file', file)

    const response = await fetch(
        `${API_BASE_URL}/manager/${managerId}/image`,
        {
            method: 'POST',
            body: formData,
        }
    )

    if (!response.ok) {
        throw new Error('Failed to upload manager image')
    }

    return response.json()
}