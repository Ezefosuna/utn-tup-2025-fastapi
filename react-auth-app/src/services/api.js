// API base URL - change this if your backend is running on a different port
const API_BASE_URL = 'http://localhost:8000';

// Register a new user
export const registerUser = async (username, email, password) => {
  const response = await fetch(`${API_BASE_URL}/auth/register`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      username,
      email,
      password
    }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Registration failed');
  }

  return await response.json();
};

// Login user
export const loginUser = async (username, password) => {
  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      username,
      password
    }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Login failed');
  }

  return await response.json();
};

// Get current user info
export const getCurrentUser = async (token) => {
  if (token === 'fake_token_for_demo') {
    return {
      id: 999,
      username: 'usuario',
      email: 'usuario@example.com',
      is_active: true,
      created_at: new Date().toISOString()
    };
  }

  const response = await fetch(`${API_BASE_URL}/auth/me`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to get user info');
  }

  return await response.json();
};

// Protected endpoint - Test
export const getProtectedTest = async (token) => {
  if (token === 'fake_token_for_demo') {
    return {
      message: "Hello from a mocked protected endpoint!",
      user: "usuario",
      status: "mocked_success"
    };
  }

  const response = await fetch(`${API_BASE_URL}/protected/test`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to access protected endpoint');
  }

  return await response.json();
};

// Protected endpoint - User Profile
export const getUserProfile = async (token) => {
  if (token === 'fake_token_for_demo') {
    return {
      profile_id: "profile_999",
      bio: "This is a mocked profile for the demo user.",
      preferences: {
        theme: "dark",
        notifications: true
      }
    };
  }

  const response = await fetch(`${API_BASE_URL}/protected/user-profile`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to get user profile');
  }

  return await response.json();
};

// Protected endpoint - Dashboard
export const getDashboard = async (token) => {
  if (token === 'fake_token_for_demo') {
    return {
      stats: {
        visits: 1234,
        sales: 5678,
        active_users: 89
      },
      last_updated: new Date().toISOString()
    };
  }

  const response = await fetch(`${API_BASE_URL}/protected/dashboard`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to get dashboard');
  }

  return await response.json();
};

