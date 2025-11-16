const API_BASE_URL = 'http://localhost:8000';

export const videoService = {
  async createRoom(roomData, authToken) {
    const response = await fetch(`${API_BASE_URL}/api/video/create-room`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authToken || 'test-token'}`,
      },
      body: JSON.stringify(roomData),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Error creando sala');
    }

    return await response.json();
  },

  async joinRoom(roomId, userData, authToken) {
    const response = await fetch(`${API_BASE_URL}/api/video/join-room`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authToken || 'test-token'}`,
      },
      body: JSON.stringify({
        room_id: roomId,
        ...userData,
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Error uniéndose a sala');
    }

    return await response.json();
  },

  async getRoom(roomId, authToken) {
    const response = await fetch(`${API_BASE_URL}/api/video/rooms/${roomId}`, {
      headers: {
        'Authorization': `Bearer ${authToken || 'test-token'}`,
      },
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Error obteniendo sala');
    }

    return await response.json();
  },
};
